import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from tasks.models import Task


class Command(BaseCommand):
    help = "Import tasks from a JSON dataset file (dataset.json par défaut)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="dataset.json",
            help="Chemin vers le fichier JSON (par défaut: dataset.json à la racine du projet).",
        )
        parser.add_argument(
            "--truncate",
            action="store_true",
            help="Supprime toutes les tâches existantes avant import.",
        )

    def handle(self, *args, **options):
        path = Path(options["path"])

        if not path.exists():
            raise CommandError(f"Dataset file not found: {path}")

        self.stdout.write(f"Loading dataset from {path} ...")

        with path.open(encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise CommandError("Dataset JSON must be a list of objects.")

        if options["truncate"]:
            deleted, _ = Task.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} existing task(s).")

        created = 0
        for entry in data:
            title = entry.get("title")
            complete = entry.get("complete", False)

            if not title:
                self.stderr.write(
                    self.style.WARNING(f"Skipping entry without title: {entry!r}")
                )
                continue

            Task.objects.create(title=title, complete=complete)
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Imported {created} task(s) from {path}"
        ))
