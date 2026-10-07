from processing.cleaning import clean_price, clean_rating, clean_text, normalize_url

VALID_SOURCES = {"books", "quotes"}


def validate_record(record):
    reasons = []

    source = clean_text(record.get("source", "")).lower()
    if source not in VALID_SOURCES:
        reasons.append("unknown_source")

    if not clean_text(record.get("name_or_title", "")):
        reasons.append("missing_name")

    source_url = normalize_url(record.get("source_url", ""))
    if not source_url:
        reasons.append("invalid_url")

    price = record.get("price")
    if price not in (None, "", " ") and clean_price(price) is None:
        reasons.append("invalid_price")

    rating = record.get("rating")
    if rating not in (None, "", " ") and clean_rating(rating) is None:
        reasons.append("invalid_rating")

    return reasons
