from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base_scraper import build_session, fetch_html

QUOTES_URL = "https://quotes.toscrape.com/"


def collect_quotes(base_url: str = QUOTES_URL, session=None):
    active_session = session or build_session()
    records = []
    next_page = base_url

    while next_page:
        response = fetch_html(next_page, session=active_session, delay=0.5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        quote_blocks = soup.select("div.quote")

        for block in quote_blocks:
            text_tag = block.select_one("span.text")
            author_tag = block.select_one("small.author")
            tags = [tag.get_text(" ", strip=True) for tag in block.select("a.tag")]

            record = {
                "source": "quotes",
                "source_url": next_page,
                "name_or_title": text_tag.get_text(" ", strip=True) if text_tag else "",
                "category": "",
                "price": "",
                "rating": "",
                "author": author_tag.get_text(" ", strip=True) if author_tag else "",
                "tags": ";".join(sorted(tag.lower() for tag in tags)),
                "description": "",
                "scraped_at": "",
            }
            records.append(record)

        next_link = soup.select_one("li.next > a")
        if next_link is None:
            break
        next_page = urljoin(next_page, next_link["href"])

    return records
