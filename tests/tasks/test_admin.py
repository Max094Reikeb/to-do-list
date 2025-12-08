from django.contrib.admin.sites import site
from django.test import SimpleTestCase

from tasks.models import Task
from ..decorators import tc


class AdminTests(SimpleTestCase):
    @tc("TC008")
    def test_task_is_registered_in_admin(self):
        from tasks import admin  # noqa: F401
        self.assertIn(Task, site._registry)
