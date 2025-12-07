from django.test import TestCase
from django.urls import reverse

from tasks.forms import TaskForm
from tasks.models import Task


class TaskModelTests(TestCase):
    def test_str_returns_title(self):
        task = Task.objects.create(title="My title", complete=False)
        self.assertEqual(str(task), "My title")


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


class TaskViewsTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Existing task",
            complete=False,
        )

    def test_home_page_list_form(self):
        """GET / should return 200 OK, get list & form."""
        response = self.client.get(reverse("list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/list.html")
        self.assertIn("tasks", response.context)
        self.assertIn("form", response.context)
        self.assertIn(self.task, response.context["tasks"])

    def test_home_page_post_creates_task_and_redirects(self):
        """POST / should return 302 & redirect."""
        response = self.client.post(reverse("list"), data={"title": "Created from POST", "complete": False})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")

        self.assertTrue(
            Task.objects.filter(title="Created from POST").exists()
        )

    def test_update_task_get(self):
        """GET /update_task/<id>/ should return 200 OK."""
        url = reverse("update_task", args=[self.task.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/update_task.html")
        self.assertIn("form", response.context)
        self.assertEqual(response.context["form"].instance, self.task)

    def test_update_task_post_updates_and_redirects(self):
        """POST /update_task/<id>/ should redirect."""
        url = reverse("update_task", args=[self.task.id])
        response = self.client.post(
            url,
            data={"title": "Updated title", "complete": True},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated title")
        self.assertTrue(self.task.complete)

    def test_delete_task_flow(self):
        """GET /delete_task/<id>/ should delete & redirect."""
        url = reverse("delete_task", args=[self.task.id])

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, "tasks/delete.html")

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(post_response["Location"], "/")

        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_home_page_post_invalid_shows_form_errors(self):
        """POST / with invalid data must stay on page and show errors."""
        response = self.client.post(
            reverse("list"),
            data={"title": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/list.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertFalse(Task.objects.filter(title="").exists())

    def test_update_task_post_invalid_shows_form_errors(self):
        """POST /update_task/<id>/ with invalid data must show form again."""
        url = reverse("update_task", args=[self.task.id])
        response = self.client.post(
            url,
            data={"title": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/update_task.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Existing task")
