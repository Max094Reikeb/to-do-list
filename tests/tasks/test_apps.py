from django.test import SimpleTestCase

from tasks.apps import TasksConfig


class TasksConfigTests(SimpleTestCase):
    def test_app_config_name(self):
        self.assertEqual(TasksConfig.name, "tasks")
