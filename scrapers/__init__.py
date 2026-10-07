from .base_scraper import DEFAULT_DELAY_SECONDS, DEFAULT_TIMEOUT, build_session, fetch_html, polite_delay
from .books_scraper import BOOKS_URL, collect_books
from .quotes_scraper import QUOTES_URL, collect_quotes

__all__ = [
    "DEFAULT_DELAY_SECONDS",
    "DEFAULT_TIMEOUT",
    "BOOKS_URL",
    "QUOTES_URL",
    "build_session",
    "collect_books",
    "collect_quotes",
    "fetch_html",
    "polite_delay",
]
