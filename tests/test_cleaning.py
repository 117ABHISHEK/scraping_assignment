from processing.cleaning import (
    clean_price,
    clean_rating,
    clean_tags,
    clean_text,
    normalize_url,
    strip_quotes,
)


def test_clean_text_handles_nbsp():
    assert clean_text("Hello\xa0world") == "Hello world"


def test_strip_quotes_removes_curly_quotes():
    assert strip_quotes("“Hello”") == '"Hello"'


def test_clean_price_parses_pounds_and_commas():
    assert clean_price("£51.77") == 51.77
    assert clean_price("£1,234.56") == 1234.56
    assert clean_price("not a price") is None


def test_clean_rating_converts_words_and_numbers():
    assert clean_rating("Three") == 3
    assert clean_rating("4") == 4
    assert clean_rating("eight") is None


def test_clean_tags_lowercases_and_sorts():
    assert clean_tags(["Life", "love", "life", "wisdom"]) == "life;love;wisdom"


def test_normalize_url_handles_whitespace_and_missing_scheme():
    assert normalize_url("  https://example.com/path  ") == "https://example.com/path"
    assert normalize_url("example.com") == "https://example.com"
