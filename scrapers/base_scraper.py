import time
from typing import Optional

import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_TIMEOUT = 15
DEFAULT_DELAY_SECONDS = 0.5
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def polite_delay(seconds: float = DEFAULT_DELAY_SECONDS) -> None:
    if seconds > 0:
        time.sleep(seconds)


def build_session() -> Session:
    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})

    retry = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=None,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_html(url: str, session: Optional[Session] = None, timeout: int = DEFAULT_TIMEOUT, delay: float = 0.0) -> Response:
    if delay > 0:
        polite_delay(delay)

    active_session = session or build_session()
    response = active_session.get(url, timeout=timeout)
    response.encoding = "utf-8"
    return response
