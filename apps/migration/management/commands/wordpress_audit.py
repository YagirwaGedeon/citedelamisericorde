"""Étape 7 — Audit WordPress : relève les contenus via l'API publique.

Usage :
    python manage.py wordpress_audit [--out docs/audit-wordpress-AAAA-MM-JJ.md] [--no-file]

Écrit le rapport d'audit Markdown dans ``docs/`` et trace l'exécution
dans ``MigrationRun`` (kind="audit").
"""

import json
import re
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.migration import importers, wp_api
from apps.migration.models import MigrationRun

_FOUNDER_RE = re.compile(r"Kamola|Kamole|ZIRHUMANA|Manasse|Manass[eé]", re.IGNORECASE)


class Command(BaseCommand):
    help = "Audit du site WordPress via l'API publique (rapport Markdown dans docs/)."

    def add_arguments(self, parser):
        parser.add_argument("--out", default="", help="Fichier de rapport (défaut : docs/audit-wordpress-AAAA-MM-JJ.md)")
        parser.add_argument("--no-file", action="store_true", help="Ne pas écrire de fichier de rapport")

    def handle(self, *args, **options):
        run = MigrationRun.objects.create(kind="audit")
        try:
            info = wp_api.wp_get("")
            posts = wp_api.fetch_collection("posts")
            pages = wp_api.fetch_pages()
            categories = wp_api.fetch_collection("categories")
            tags = wp_api.fetch_collection("tags")

            images = sorted(
                {
                    url
                    for element in posts + pages
                    for url in importers.image_urls_from_html(element.get("content") or "")
                }
            )
            founder_hits = [
                element.get("URL", "?")
                for element in posts + pages
                if _FOUNDER_RE.search(f"{element.get('title') or ''} {element.get('content') or ''}")
            ]
            word_counts = {p.get("ID"): len((p.get("content") or "").split()) for p in posts}

            summary = {
                "site": info.get("name", ""),
                "found": {"posts": len(posts), "pages": len(pages), "categories": len(categories), "tags": len(tags)},
                "images": len(images),
                "founder_hits": founder_hits,
            }
            run.log = json.dumps(summary, ensure_ascii=False, indent=2)
            run.status = "SUCCESS"

            self.stdout.write(self.style.SUCCESS(f"Site : {info.get('name', '?')}"))
            self.stdout.write(f"  Articles : {len(posts)} | Pages : {len(pages)}")
            self.stdout.write(f"  Catégories : {len(categories)} | Étiquettes : {len(tags)}")
            self.stdout.write(f"  Images dans les contenus : {len(images)}")

            if not options["no_file"]:
                out_path = Path(options["out"]) if options["out"] else (
                    settings.BASE_DIR.parent / "docs" / f"audit-wordpress-{date.today().isoformat()}.md"
                )
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(
                    self._render_markdown(info, posts, pages, categories, tags, images, word_counts, founder_hits),
                    encoding="utf-8",
                )
                self.stdout.write(self.style.SUCCESS(f"Rapport écrit : {out_path}"))
        except wp_api.WordPressAPIError as exc:
            run.status = "FAILED"
            run.log = str(exc)
            self.stderr.write(self.style.ERROR(str(exc)))
            raise CommandError(str(exc)) from exc
        finally:
            from django.utils import timezone

            run.finished_at = timezone.now()
            run.save()

    @staticmethod
    def _render_markdown(info, posts, pages, categories, tags, images, word_counts, founder_hits) -> str:
        lines = [
            "# RAPPORT D'AUDIT — ANCIEN SITE WORDPRESS.COM",
            "",
            f"**Site analysé** : {info.get('URL', '')}",
            f"**Site ID WordPress.com** : {info.get('ID', '')}",
            f"**Date de l'audit** : {date.today().isoformat()}",
            f"**Méthode** : API REST publique WordPress.com (`{wp_api.API_BASE}`)",
            "",
            "> L'API REST WordPress native (`/wp-json/`) répond 404 sur ce site WordPress.com.",
            "> L'API publique fonctionne sans authentification pour les données publiques.",
            "",
            "## 1. Informations institutionnelles",
            "",
            "| Élément | Valeur trouvée |",
            "|---|---|",
            f"| Nom du site | {info.get('name', '—')} |",
            f"| Description | {info.get('description', '—')} |",
            f"| URL | {info.get('URL', '—')} |",
            "",
            "## 2. Pages",
            "",
            "| ID | Slug | Titre | Mots | Images |",
            "|---|---|---|---|---|",
        ]
        for page in sorted(pages, key=lambda p: p.get("ID") or 0):
            content = page.get("content") or ""
            lines.append(
                f"| {page.get('ID')} | {page.get('slug')} | {page.get('title')} | "
                f"{len(content.split())} | {len(importers.image_urls_from_html(content))} |"
            )
        lines += ["", "## 3. Articles (posts publiés)", "", "| ID | Date | Titre | Mots | Images |", "|---|---|---|---|---|"]
        for post in sorted(posts, key=lambda p: p.get("ID") or 0):
            content = post.get("content") or ""
            lines.append(
                f"| {post.get('ID')} | {post.get('date', '')[:10]} | {post.get('title')} | "
                f"{len(content.split())} | {len(importers.image_urls_from_html(content))} |"
            )
        lines += [
            "",
            "## 4. Catégories et étiquettes",
            "",
            "| Type | Nom | Slug |",
            "|---|---|---|",
        ]
        for item in categories:
            lines.append(f"| Catégorie | {item.get('name')} | {item.get('slug')} |")
        for item in tags:
            lines.append(f"| Étiquette | {item.get('name')} | {item.get('slug')} |")
        lines += [
            "",
            "## 5. Images à conserver",
            "",
            f"- **{len(images)} images** intégrées dans les contenus (posts + pages).",
            "- À dédupliquer (SHA-256) et à télécharger localement lors de l'import.",
        ]
        if images:
            lines.append("")
            lines.append("```text")
            lines.extend(f"- {url}" for url in images[:100])
            if len(images) > 100:
                lines.append(f"- … et {len(images) - 100} autres")
            lines.append("```")
        lines += [
            "",
            "## 6. Anomalies détectées (à valider humainement)",
            "",
            f"- Mentions du nom du fondateur dans {len(founder_hits)} élément(s) : 4 variantes "
            "connues (Kamola / Kamole / ZIRHUMANA KAMOLE Marie-Manassé / Marie Manasse Zirhumana Kamole) "
            "— à confirmer avant publication.",
            "- Vérifier chaque article avant publication (import en brouillon par défaut).",
            "",
            "_Rapport généré automatiquement — aucune donnée inventée, aucune publication automatique._",
            "",
        ]
        return "\n".join(lines)
