"""
Testes para utilitarios do Sienge.
"""

import pytest
from sienge.utils import format_currency, parse_sienge_date, paginate
from sienge.rate_limiter import RateLimiter


class TestFormatCurrency:
    def test_basic(self):
        assert format_currency(1500.50) == "R$ 1.500,50"

    def test_zero(self):
        assert format_currency(0) == "R$ 0,00"

    def test_none(self):
        assert format_currency(None) == "R$ 0,00"

    def test_large(self):
        assert format_currency(1234567.89) == "R$ 1.234.567,89"

    def test_custom_symbol(self):
        assert format_currency(100, symbol="US$") == "US$ 100,00"


class TestParseSiengeDate:
    def test_full_datetime(self):
        assert parse_sienge_date("2026-03-14T10:30:00") == "2026-03-14"

    def test_date_only(self):
        assert parse_sienge_date("2026-03-14") == "2026-03-14"

    def test_none(self):
        assert parse_sienge_date(None) is None

    def test_empty(self):
        assert parse_sienge_date("") is None


class TestPaginate:
    def test_single_page(self):
        def fetch(offset, limit):
            return {
                "resultSetMetadata": {"count": 3, "offset": offset, "limit": limit},
                "results": [{"id": 1}, {"id": 2}, {"id": 3}],
            }

        items = list(paginate(fetch))
        assert len(items) == 3

    def test_multiple_pages(self):
        all_items = [{"id": i} for i in range(5)]

        def fetch(offset, limit):
            page = all_items[offset:offset + limit]
            return {
                "resultSetMetadata": {"count": 5, "offset": offset, "limit": limit},
                "results": page,
            }

        items = list(paginate(fetch, limit_per_page=2))
        assert len(items) == 5
        assert items[0]["id"] == 0
        assert items[4]["id"] == 4

    def test_max_results(self):
        def fetch(offset, limit):
            return {
                "resultSetMetadata": {"count": 100, "offset": offset, "limit": limit},
                "results": [{"id": i} for i in range(offset, offset + limit)],
            }

        items = list(paginate(fetch, limit_per_page=10, max_results=25))
        assert len(items) == 25

    def test_empty_results(self):
        def fetch(offset, limit):
            return {"resultSetMetadata": {"count": 0}, "results": []}

        items = list(paginate(fetch))
        assert len(items) == 0


class TestRateLimiter:
    def test_remaining(self):
        limiter = RateLimiter(max_requests=5, window_seconds=60.0)
        assert limiter.remaining == 5
        limiter.acquire()
        assert limiter.remaining == 4

    def test_acquire_within_limit(self):
        limiter = RateLimiter(max_requests=3, window_seconds=60.0)
        for _ in range(3):
            wait = limiter.acquire()
            assert wait == 0.0
