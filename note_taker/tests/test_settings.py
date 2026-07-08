from django.test import SimpleTestCase

from turbo_base.settings import DEFAULT_ALLOWED_HOSTS, build_allowed_hosts


class AllowedHostsSettingsTests(SimpleTestCase):
    def test_includes_vercel_deployment_url(self):
        hosts = build_allowed_hosts(
            allowed_hosts_value='localhost,127.0.0.1',
            vercel_url='turbo-api-nine.vercel.app',
            vercel_project_production_url=None,
        )

        self.assertIn('turbo-api-nine.vercel.app', hosts)

    def test_default_allowed_hosts_include_production_vercel_domain(self):
        hosts = build_allowed_hosts(
            allowed_hosts_value=DEFAULT_ALLOWED_HOSTS,
            vercel_url=None,
            vercel_project_production_url=None,
        )

        self.assertIn('turbo-api-nine.vercel.app', hosts)

    def test_includes_production_vercel_domain_when_env_is_empty(self):
        hosts = build_allowed_hosts(
            allowed_hosts_value='',
            vercel_url=None,
            vercel_project_production_url=None,
        )

        self.assertIn('turbo-api-nine.vercel.app', hosts)
