"""Étape 7 — Import des contenus WordPress vers Django.

Usage :
    python manage.py wordpress_import [--posts] [--pages] [--ids 256,209]
                                      [--publish] [--no-media] [--force] [--dry-run]

Comportement par défaut : tout est importé **en brouillon** (validation
humaine requise, §7/§30), images téléchargées et dédupliquées (SHA-256),
anciennes URLs mappées vers les nouvelles (URLMapping, §28).
Aucune donnée n'est inventée ; le post 256 (texte collé dans le titre)
est restructuré et signalé dans le journal.
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.migration import importers, wp_api
from apps.migration.models import MigrationRun


class Command(BaseCommand):
    help = "Importe les contenus WordPress (pages, articles, catégories, tags) vers Django."

    def add_arguments(self, parser):
        parser.add_argument("--posts", action="store_true", help="Importer uniquement les articles")
        parser.add_argument("--pages", action="store_true", help="Importer uniquement les pages")
        parser.add_argument("--ids", default="", help="Limiter aux IDs sources (ex. 256,209)")
        parser.add_argument("--publish", action="store_true", help="Publier directement (défaut : brouillon)")
        parser.add_argument("--no-media", action="store_true", help="Ne pas télécharger les images")
        parser.add_argument("--force", action="store_true", help="Ré-importer même si déjà présent")
        parser.add_argument("--dry-run", action="store_true", help="Afficher le plan d'import sans rien écrire")

    def handle(self, *args, **options):
        run = MigrationRun.objects.create(kind="import")
        ids = {i.strip() for i in options["ids"].split(",") if i.strip()}
        counts = {"IMPORTED": 0, "SKIPPED": 0, "ERROR": 0}

        def _keep(item):
            return not ids or str(item.get("ID")) in ids

        try:
            if options["dry_run"]:
                self._dry_run(run, options)
                return

            author = importers._resolve_author()
            if not options["pages"]:
                self.stdout.write("Catégories et étiquettes…")
                for raw in wp_api.fetch_collection("categories"):
                    importers.import_category(raw)
                for raw in wp_api.fetch_collection("tags"):
                    importers.import_tag(raw)

            if not options["posts"]:
                for raw in wp_api.fetch_pages():
                    if not _keep(raw):
                        continue
                    result = importers.import_page(
                        run, raw,
                        publish=options["publish"],
                        download_media=not options["no_media"],
                        force=options["force"],
                    )
                    self.stdout.write("  " + result)
                    counts[self._status(result)] += 1

            if not options["pages"]:
                for raw in wp_api.fetch_collection("posts"):
                    if not _keep(raw):
                        continue
                    result = importers.import_post(
                        run, raw, author=author,
                        publish=options["publish"],
                        download_media=not options["no_media"],
                        force=options["force"],
                    )
                    self.stdout.write("  " + result)
                    counts[self._status(result)] += 1

            run.status = "SUCCESS"
            run.log = f"Importé : {counts['IMPORTED']} | Ignoré : {counts['SKIPPED']} | Erreur : {counts['ERROR']}"
            self.stdout.write(self.style.SUCCESS(
                f"Terminé — importés : {counts['IMPORTED']}, ignorés : {counts['SKIPPED']}, erreurs : {counts['ERROR']}"
            ))
        except wp_api.WordPressAPIError as exc:
            run.status = "FAILED"
            run.log = str(exc)
            self.stderr.write(self.style.ERROR(str(exc)))
            raise CommandError(str(exc)) from exc
        except Exception as exc:  # pragma: no cover — filet de sécurité
            run.status = "FAILED"
            run.log = f"{type(exc).__name__}: {exc}"
            self.stderr.write(self.style.ERROR(f"Import interrompu : {exc}"))
            raise CommandError(str(exc)) from exc
        finally:
            run.finished_at = timezone.now()
            run.save()

    @staticmethod
    def _status(result: str) -> str:
        return result.split("]", 1)[0].lstrip("[").upper() if result.startswith("[") else "ERROR"

    @staticmethod
    def _dry_run(run, options):
        ids = {i.strip() for i in options["ids"].split(",") if i.strip()}
        for collection, kind in ((wp_api.fetch_pages(), "page"), (wp_api.fetch_collection("posts"), "post")):
            for raw in collection:
                if ids and str(raw.get("ID")) not in ids:
                    continue
                slug = (raw.get("slug") or "").strip() or ""
                target = "pages:page_detail" if kind == "page" else "articles:detail"
                run.log += f"[{kind} {raw.get('ID')}] {raw.get('title')} -> {target} (slug: {slug})\n"
                print(f"  {kind} {raw.get('ID')}: {raw.get('title')} -> {target} (slug: {slug})")
        run.status = "SUCCESS"
        run.log = (run.log or "") + "dry-run — aucun objet créé"
