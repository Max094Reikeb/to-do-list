from django.test import SimpleTestCase

from tasks.apps import TasksConfig
from ..decorators import tc


class TasksConfigTests(SimpleTestCase):
    @tc("TC010")
    def test_app_config_name(self):
        self.assertEqual(TasksConfig.name, "tasks")
