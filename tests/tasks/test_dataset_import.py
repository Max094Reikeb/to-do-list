import json
import tempfile
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from tasks.models import Task

from ..decorators import tc


class ImportDatasetTests(TestCase):
    def _write_temp_json(self, obj) -> Path:
        """
        Helper to write a Python object in a temporary JSON file
        and return the matching Path.
        """
        tmp = tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False)
        path = Path(tmp.name)
        json.dump(obj, tmp)
        tmp.flush()
        tmp.close()
        return path

    @tc("TC016")
    def test_import_dataset_creates_tasks_from_file_with_truncate(self):
        data = [
            {"title": "Task A", "complete": False},
            {"title": "Task B", "complete": True},
        ]
        path = self._write_temp_json(data)

        Task.objects.create(title="OLD", complete=False)

        call_command("import_dataset", path=str(path), truncate=True)

        self.assertEqual(Task.objects.count(), 2)
        titles = list(Task.objects.values_list("title", flat=True))
        self.assertIn("Task A", titles)
        self.assertIn("Task B", titles)
        self.assertFalse(Task.objects.filter(title="OLD").exists())

    @tc("TC017")
    def test_import_dataset_appends_tasks_without_truncate(self):
        existing = Task.objects.create(title="Existing", complete=False)

        data = [
            {"title": "New Task", "complete": False},
        ]
        path = self._write_temp_json(data)

        call_command("import_dataset", path=str(path))

        self.assertEqual(Task.objects.count(), 2)
        titles = list(Task.objects.values_list("title", flat=True))
        self.assertIn("Existing", titles)
        self.assertIn("New Task", titles)
        self.assertTrue(Task.objects.filter(id=existing.id).exists())

    @tc("TC018")
    def test_import_dataset_missing_file_raises_error(self):
        """Nonexisting file → CommandError."""
        with self.assertRaises(CommandError):
            call_command("import_dataset", path="does_not_exist.json")

    @tc("TC018")
    def test_import_dataset_with_non_list_data_raises_error(self):
        """If the JSON is not a list, we must throw CommandError."""
        obj = {"title": "Not a list"}
        path = self._write_temp_json(obj)

        with self.assertRaises(CommandError):
            call_command("import_dataset", path=str(path))

    @tc("TC019")
    def test_import_dataset_skips_entries_without_title(self):
        """We ignore entries without 'title'"""
        data = [
            {"title": "Valid task", "complete": False},
            {"complete": True},
        ]
        path = self._write_temp_json(data)

        call_command("import_dataset", path=str(path), truncate=True)

        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.get()
        self.assertEqual(task.title, "Valid task")
        self.assertFalse(Task.objects.filter(title="").exists())
