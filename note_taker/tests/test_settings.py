from django.test import SimpleTestCase

from turbo_base.settings import build_allowed_hosts


class AllowedHostsSettingsTests(SimpleTestCase):
    def test_includes_vercel_deployment_url(self):
        hosts = build_allowed_hosts(
            allowed_hosts_value='localhost,127.0.0.1',
            vercel_url='turbo-api-nine.vercel.app',
            vercel_project_production_url=None,
        )

        self.assertIn('turbo-api-nine.vercel.app', hosts)
