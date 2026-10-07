from __future__ import annotations

import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base_scraper import build_session, fetch_html

logger = logging.getLogger("scraper")

BOOKS_URL = "https://books.toscrape.com/"


def collect_books(base_url: str = BOOKS_URL, session=None):
    active_session = session or build_session()
    records = []
    next_page = base_url

    while next_page:
        try:
            response = fetch_html(next_page, session=active_session, delay=0.5)
            response.raise_for_status()
        except Exception:
            logger.exception("Failed request for books page %s", next_page)
            break

        logger.info("Fetched books page %s", next_page)
        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.select("article.product_pod")

        for card in cards:
            title_link = card.select_one("h3 > a")
            if title_link is None:
                continue

            title = title_link.get("title") or title_link.get_text(" ", strip=True)
            source_url = urljoin(next_page, title_link["href"])
            record = {
                "source": "books",
                "source_url": source_url,
                "name_or_title": title,
                "category": "",
                "price": "",
                "rating": "",
                "author": "",
                "tags": "",
                "description": "",
                "scraped_at": "",
            }

            detail_response = fetch_html(source_url, session=active_session, delay=0.5)
            detail_response.raise_for_status()
            detail_soup = BeautifulSoup(detail_response.text, "lxml")
            article = detail_soup.select_one("article.product_page")

            if article:
                category_link = article.select_one("ul.breadcrumb li:nth-of-type(3) a")
                if category_link is not None:
                    record["category"] = category_link.get_text(" ", strip=True)

                description_block = article.select_one("#product_description")
                if description_block is not None:
                    description = description_block.find_next("p")
                    if description is not None:
                        record["description"] = description.get_text(" ", strip=True)

                price_tag = article.select_one("p.price_color")
                if price_tag is not None:
                    record["price"] = price_tag.get_text(" ", strip=True)

                rating_tag = article.select_one("p.star-rating")
                if rating_tag is not None:
                    rating_classes = rating_tag.get("class", [])
                    for item in rating_classes:
                        if item.lower() in {"one", "two", "three", "four", "five"}:
                            record["rating"] = item.lower()
                            break

            records.append(record)

        next_link = soup.select_one("li.next > a")
        if next_link is None:
            break
        next_page = urljoin(next_page, next_link["href"])

    return records
