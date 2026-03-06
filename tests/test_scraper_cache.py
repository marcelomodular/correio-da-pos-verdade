import sys
import types
import unittest

if 'feedparser' not in sys.modules:
    fake_feedparser = types.ModuleType('feedparser')

    def fake_parse(_content):
        return types.SimpleNamespace(entries=[])

    fake_feedparser.parse = fake_parse
    sys.modules['feedparser'] = fake_feedparser

if 'requests' not in sys.modules:
    fake_requests = types.ModuleType('requests')

    class _FakeResponse:
        def raise_for_status(self):
            return None

        @property
        def content(self):
            return b''

    def fake_get(*args, **kwargs):
        return _FakeResponse()

    fake_requests.get = fake_get
    sys.modules['requests'] = fake_requests

import scraper


class ScraperCacheTestCase(unittest.TestCase):
    def setUp(self):
        self.original_fetch_all_sources = scraper._fetch_all_sources
        self.original_cache = dict(scraper._cache_state)

    def tearDown(self):
        scraper._fetch_all_sources = self.original_fetch_all_sources
        scraper._cache_state.update(self.original_cache)

    def test_cache_reuses_recent_result(self):
        calls = {'count': 0}

        def fake_fetch(limit_per_source, sources):
            calls['count'] += 1
            return [
                {
                    'titulo': 'Teste',
                    'link': f'https://example.com/{calls["count"]}',
                    'resumo': 'Resumo',
                    'fonte': 'Fonte',
                    'data': '',
                }
            ]

        scraper._fetch_all_sources = fake_fetch
        scraper._cache_state.update({'expires_at': 0.0, 'limit_per_source': None, 'news': []})

        first = scraper.get_all_news(limit_per_source=3)
        second = scraper.get_all_news(limit_per_source=3)

        self.assertEqual(calls['count'], 1)
        self.assertEqual(first, second)

    def test_cache_invalidates_when_limit_changes(self):
        calls = {'count': 0}

        def fake_fetch(limit_per_source, sources):
            calls['count'] += 1
            return [
                {
                    'titulo': f'Teste {limit_per_source}',
                    'link': f'https://example.com/{limit_per_source}',
                    'resumo': 'Resumo',
                    'fonte': 'Fonte',
                    'data': '',
                }
            ]

        scraper._fetch_all_sources = fake_fetch
        scraper._cache_state.update({'expires_at': 0.0, 'limit_per_source': None, 'news': []})

        scraper.get_all_news(limit_per_source=2)
        scraper.get_all_news(limit_per_source=5)

        self.assertEqual(calls['count'], 2)


if __name__ == '__main__':
    unittest.main()
