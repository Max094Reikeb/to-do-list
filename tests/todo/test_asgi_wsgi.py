from django.test import SimpleTestCase

from ..decorators import tc

class AsgiWsgiTests(SimpleTestCase):
    @tc("TC010")
    def test_asgi_application_importable(self):
        from todo.asgi import application  # noqa: F401

    @tc("TC010")
    def test_wsgi_application_importable(self):
        from todo.wsgi import application  # noqa: F401
