from django.test import SimpleTestCase


class AsgiWsgiTests(SimpleTestCase):
    def test_asgi_application_importable(self):
        from todo.asgi import application  # noqa: F401

    def test_wsgi_application_importable(self):
        from todo.wsgi import application  # noqa: F401
