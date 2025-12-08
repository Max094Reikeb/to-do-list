from django.contrib.admin.sites import site
from django.test import SimpleTestCase

from tasks.models import Task


class AdminTests(SimpleTestCase):
    def test_task_is_registered_in_admin(self):
        from tasks import admin  # noqa: F401
        self.assertIn(Task, site._registry)
