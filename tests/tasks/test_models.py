from django.test import TestCase

from tasks.models import Task

from ..decorators import tc


class TaskModelTests(TestCase):
    @tc("TC008")
    def test_str_returns_title(self):
        task = Task.objects.create(title="My title", complete=False)
        self.assertEqual(str(task), "My title")
