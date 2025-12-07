from django.test import TestCase
from django.urls import reverse

from tasks.models import Task


class TaskViewsTests(TestCase):
    def setUp(self):
        # Create a task to use in update/delete tests
        self.task = Task.objects.create(
            title="Test task",
            complete=False,
        )

    def test_home_page_status_code(self):
        """GET / should return 200 OK."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_update_task_status_code(self):
        """GET /update_task/<id>/ should return 200 OK."""
        url = reverse("update_task", args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_task_deletes_and_redirects(self):
        """GET /delete_task/<id>/ should delete and redirect."""
        url = reverse("delete_task", args=[self.task.id])

        # GET should show confirmation
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

        # POST should delete and redirect
        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 302)

        # Task should be gone
        self.assertFalse(
            Task.objects.filter(id=self.task.id).exists()
        )
