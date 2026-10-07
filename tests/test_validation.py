from processing.validation import validate_record


def test_valid_record_passes():
    record = {
        "source": "books",
        "source_url": "https://books.toscrape.com/catalogue/example.html",
        "name_or_title": "Example Book",
        "price": "£12.50",
        "rating": "4",
    }
    assert validate_record(record) == []


def test_invalid_source_is_rejected():
    record = {
        "source": "news",
        "source_url": "https://books.toscrape.com/catalogue/example.html",
        "name_or_title": "Example Book",
    }
    assert "unknown_source" in validate_record(record)


def test_missing_name_is_rejected():
    record = {
        "source": "quotes",
        "source_url": "https://quotes.toscrape.com/page/1/",
        "name_or_title": "",
    }
    assert "missing_name" in validate_record(record)


def test_invalid_url_is_rejected():
    record = {
        "source": "books",
        "source_url": "not a url",
        "name_or_title": "Example Book",
    }
    assert "invalid_url" in validate_record(record)


def test_invalid_price_is_rejected():
    record = {
        "source": "books",
        "source_url": "https://books.toscrape.com/catalogue/example.html",
        "name_or_title": "Example Book",
        "price": "not a price",
    }
    assert "invalid_price" in validate_record(record)


def test_invalid_rating_is_rejected():
    record = {
        "source": "books",
        "source_url": "https://books.toscrape.com/catalogue/example.html",
        "name_or_title": "Example Book",
        "rating": "nine",
    }
    assert "invalid_rating" in validate_record(record)
