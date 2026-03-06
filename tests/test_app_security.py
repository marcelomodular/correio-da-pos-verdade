import socket
import unittest

from security_utils import is_public_http_url, parse_published_date


class SecurityHelpersTestCase(unittest.TestCase):
    def test_parse_published_date_handles_invalid_values(self):
        self.assertIsNone(parse_published_date(''))
        self.assertIsNone(parse_published_date('not-a-date'))

    def test_parse_published_date_handles_rfc2822(self):
        parsed = parse_published_date('Tue, 02 Jan 2024 20:10:00 GMT')
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.year, 2024)

    def test_parse_published_date_handles_iso8601(self):
        parsed = parse_published_date('2024-01-02T20:10:00Z')
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.month, 1)

    def test_is_public_http_url_rejects_private_ips(self):
        def private_resolver(_host, _port, proto=None):
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', 80))]

        self.assertFalse(is_public_http_url('http://example.com', resolver=private_resolver))

    def test_is_public_http_url_accepts_public_ips(self):
        def public_resolver(_host, _port, proto=None):
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('8.8.8.8', 80))]

        self.assertTrue(is_public_http_url('https://example.com/news', resolver=public_resolver))

    def test_is_public_http_url_rejects_non_http_scheme(self):
        self.assertFalse(is_public_http_url('file:///etc/passwd'))


if __name__ == '__main__':
    unittest.main()
