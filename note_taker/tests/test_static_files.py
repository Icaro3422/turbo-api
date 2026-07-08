from django.test import Client, override_settings, SimpleTestCase


@override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
class StaticFilesTests(SimpleTestCase):
    def test_serves_drf_browsable_api_css(self):
        response = Client().get('/static/rest_framework/css/bootstrap.min.css')

        self.assertEqual(response.status_code, 200)
        self.assertIn('text/css', response['Content-Type'])
