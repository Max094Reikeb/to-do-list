from django.test import TestCase

from tasks.forms import TaskForm


class TaskFormTests(TestCase):
    def test_form_placeholder_is_set(self):
        form = TaskForm()
        self.assertIn("title", form.fields)
        widget = form.fields["title"].widget
        self.assertEqual(
            widget.attrs.get("placeholder"),
            "Add new task",
        )

    def test_form_is_valid_with_title(self):
        form = TaskForm(data={"title": "New task", "complete": False})
        self.assertTrue(form.is_valid())
