from django.test import TestCase

from dashboard.models import BlockedDomain


class DomainBlockingTest(TestCase):
    def create_blocking(self, domain_regex):
        BlockedDomain.objects.create(domain_regex=domain_regex)

    def is_blocked(self, url):
        return self.assertEqual(BlockedDomain.objects.is_blocked(url), True)

    def is_not_blocked(self, url):
        return self.assertEqual(BlockedDomain.objects.is_blocked(url), False)

    def test_subdomain_shortcut(self):
        self.create_blocking("||example.com#")

        for scheme in ["http://", "https://"]:
            for subdomain in ["", "www.", "www.fff."]:
                for path in ["", "/", "/test", "/test?p=122"]:
                    self.is_blocked(f"{scheme}{subdomain}example.com{path}")

        self.is_not_blocked("https://clck.com/")
        self.is_not_blocked("https://click.ru/")

    def test_scheme_shortcut(self):
        self.create_blocking("|test.ru#")

        for scheme in ["http://", "https://"]:
            for subdomain in ["www.", "www.fff."]:
                for path in ["", "/", "/test", "/test?p=122"]:
                    self.is_not_blocked(f"{scheme}{subdomain}test.ru{path}")

        self.is_blocked("https://test.ru/")
        self.is_blocked("https://test.ru/test?p=122")

    def test_toplevel_domain_shortcut(self):
        self.create_blocking("||python^")

        for toplevel_domain in [".ru", ".com", ".рф", ".org", ".servers.com"]:
            self.is_blocked(f"https://python{toplevel_domain}")
            self.is_blocked(f"https://www.python{toplevel_domain}")
            self.is_blocked(f"https://www.code.python{toplevel_domain}")

        self.is_not_blocked("https://www.pythonanywhere.com/")

    def test_any_letters_shortcut(self):
        self.create_blocking("#test#")

        self.is_blocked("https://test.com/")
        self.is_blocked("ftp://portal.testserver.com")
        self.is_blocked("https://test-this.com/")

    def test_other_case(self):
        self.create_blocking("||booking^^")
        self.is_blocked("https://booking.bad_server.com/")
        self.is_blocked("https://booking.id2234223.ru/")
        self.is_blocked("https://www.booking.id2234223.com/")
        self.is_not_blocked("https://booking.com/")

        self.create_blocking("|||replit^")
        self.is_blocked("https://subdomainXYZ.replit.app")
        self.is_blocked("https://open-facebook.replit.app")
        self.is_blocked("https://google-official.replit.app")

        # by link_shorteners python lib
        self.is_blocked("https://replit.com")


__all__ = []
