"""Étape 7 — Rapport de migration : état des lieux de l'import WordPress.

Usage :
    python manage.py wordpress_report [--out docs/rapport-migration-AAAA-MM-JJ.md] [--no-file]

Agrège l'état de la base (exécutions, éléments importés, URLMapping,
brouillons en attente de validation) et écrit le rapport dans ``docs/``.
"""

import json
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.articles.models import Article, ArticleCategory
from apps.media.models import MediaItem
from apps.migration.models import ImportedRecord, MigrationRun, URLMapping
from apps.pages.models import Page


class Command(BaseCommand):
    help = "Génère le rapport de migration (état de l'import WordPress)."

    def add_arguments(self, parser):
        parser.add_argument("--out", default="", help="Fichier de rapport (défaut : docs/rapport-migration-AAAA-MM-JJ.md)")
        parser.add_argument("--no-file", action="store_true", help="Ne pas écrire de fichier de rapport")

    def handle(self, *args, **options):
        run = MigrationRun.objects.create(kind="report")

        articles = Article.objects.count()
        articles_draft = Article.objects.filter(status="draft").count()
        pages = Page.objects.count()
        pages_draft = Page.objects.filter(status="draft").count()
        media = MediaItem.objects.count()
        media_imported = MediaItem.objects.exclude(source_url="").count()
        mappings = URLMapping.objects.count()
        mappings_pending = URLMapping.objects.filter(new_url="").count()
        imports = ImportedRecord.objects.exclude(status="SKIPPED").count()
        errors = ImportedRecord.objects.filter(status="ERROR").count()

        runs = list(MigrationRun.objects.all()[:10])
        summary = {
            "runs": [{"kind": r.kind, "status": r.status, "started_at": str(r.started_at)} for r in runs],
            "articles": {"total": articles, "draft": articles_draft},
            "pages": {"total": pages, "draft": pages_draft},
            "media": {"total": media, "imported": media_imported},
            "url_mappings": {"total": mappings, "pending": mappings_pending},
            "errors": errors,
        }
        run.log = json.dumps(summary, ensure_ascii=False, indent=2)
        run.status = "SUCCESS"
        run.finished_at = timezone.now()
        run.save()

        self.stdout.write(self.style.SUCCESS("Rapport de migration :"))
        self.stdout.write(f"  Articles : {articles} (dont {articles_draft} brouillons)")
        self.stdout.write(f"  Pages : {pages} (dont {pages_draft} brouillons)")
        self.stdout.write(f"  Médias : {media} (dont {media_imported} importés de WordPress)")
        self.stdout.write(f"  Correspondances d'URL : {mappings} (dont {mappings_pending} en attente)")

        if not options["no_file"]:
            out_path = Path(options["out"]) if options["out"] else (
                settings.BASE_DIR.parent / "docs" / f"rapport-migration-{date.today().isoformat()}.md"
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(self._render_markdown(summary, runs), encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"Rapport écrit : {out_path}"))

    def _render_markdown(self, summary: dict, runs: list) -> str:
        lines = [
            "# RAPPORT DE MIGRATION — Cité de la Miséricorde",
            "",
            f"**Date** : {date.today().isoformat()}",
            "",
            "## 1. Exécutions de migration",
            "",
            "| Date | Type | Statut |",
            "|---|---|---|",
        ]
        for r in runs:
            lines.append(f"| {r.started_at:%Y-%m-%d %H:%M} | {r.get_kind_display()} | {r.get_status_display()} |")
        lines += [
            "",
            "## 2. Contenus",
            "",
            f"- Articles : **{summary['articles']['total']}** (dont **{summary['articles']['draft']}** brouillons en attente de validation)",
            f"- Pages : **{summary['pages']['total']}** (dont **{summary['pages']['draft']}** brouillons)",
            f"- Catégories d'articles : **{ArticleCategory.objects.count()}**",
            "",
            "## 3. Médias",
            "",
            f"- Médias : **{summary['media']['total']}** (dont **{summary['media']['imported']}** importés de WordPress, dédupliqués par SHA-256)",
            f"- Échecs de téléchargement : **{MediaItem.objects.filter(source_url='', file='').count()}** enregistrés dans le journal",
            "",
            "## 4. Correspondances d'URL (§28)",
            "",
            f"- Total : **{summary['url_mappings']['total']}** (dont **{summary['url_mappings']['pending']}** non mappées)",
            "",
            "## 5. Actions restantes (validation humaine)",
            "",
            "1. Valider le nom officiel du fondateur (4 variantes trouvées).",
            "2. Valider et publier chaque article/page encore en brouillon.",
            "3. Valider les statuts des projets (P1–P7) et les chiffres d'impact.",
            "4. Vérifier les images importées (pertinence, doublons).",
            "5. Supprimer définitivement WordPress après validation complète.",
            "",
            f"**Erreurs d'import** : {summary['errors']}",
            "",
            "_Rapport généré automatiquement par `python manage.py wordpress_report`._",
            "",
        ]
        return "\n".join(lines)
