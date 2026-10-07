from processing.deduplication import deduplicate_records


def test_books_are_deduplicated_case_and_whitespace_insensitive():
    records = [
        {"source": "books", "name_or_title": "Example Book Title"},
        {"source": "books", "name_or_title": " Example Book Title "},
        {"source": "books", "name_or_title": "EXAMPLE BOOK TITLE"},
    ]

    unique, duplicates = deduplicate_records(records)
    assert len(unique) == 1
    assert duplicates == 2


def test_quotes_are_deduplicated_using_author_and_quote_prefix():
    records = [
        {"source": "quotes", "author": "Albert Einstein", "name_or_title": "The world as we have created it is a process of our thinking."},
        {"source": "quotes", "author": "Albert Einstein", "name_or_title": " The world as we have created it is a process of our thinking. "},
        {"source": "quotes", "author": "Charles Dickens", "name_or_title": "The world as we have created it is a process of our thinking."},
    ]

    unique, duplicates = deduplicate_records(records)
    assert len(unique) == 2
    assert duplicates == 1
