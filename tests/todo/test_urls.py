from django.test import SimpleTestCase
from django.urls import resolve

from ..decorators import tc


class TodoUrlsTests(SimpleTestCase):
    @tc("TC001")
    def test_root_url_uses_tasks_list_view(self):
        resolver = resolve("/")
        self.assertEqual(resolver.view_name, "list")

    @tc("TC010")
    def test_admin_url_resolves(self):
        resolver = resolve("/admin/")
        self.assertIsNotNone(resolver.func)
