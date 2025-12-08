from django.test import SimpleTestCase
from django.urls import resolve, reverse

from ..decorators import tc


class TasksUrlsTests(SimpleTestCase):
    @tc("TC001")
    def test_list_url_resolves_to_view_name(self):
        url = reverse("list")
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "list")

    @tc("TC005")
    def test_update_and_delete_urls_exist(self):
        self.assertEqual(resolve(reverse("update_task", args=[1])).view_name, "update_task")
        self.assertEqual(resolve(reverse("delete_task", args=[1])).view_name, "delete_task")
