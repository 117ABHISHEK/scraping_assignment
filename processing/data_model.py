from dataclasses import dataclass, field
from typing import Optional

SCRAPED_COLUMNS = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


@dataclass
class ScrapedRecord:
    source: str
    source_url: str
    name_or_title: str
    category: str = ""
    price: Optional[float] = None
    rating: Optional[int] = None
    author: str = ""
    tags: str = ""
    description: str = ""
    scraped_at: str = ""

    def as_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "source_url": self.source_url,
            "name_or_title": self.name_or_title,
            "category": self.category,
            "price": self.price,
            "rating": self.rating,
            "author": self.author,
            "tags": self.tags,
            "description": self.description,
            "scraped_at": self.scraped_at,
        }
