import hashlib
import re

from processing.cleaning import clean_text, strip_quotes


def compact_text(value):
    text = clean_text(strip_quotes(value)).lower()
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def fingerprint_record(record):
    source = clean_text(record.get("source", "")).lower()
    title = compact_text(record.get("name_or_title", ""))

    if source == "books":
        value = f"{source}:{title}"
    elif source == "quotes":
        author = compact_text(record.get("author", ""))
        quote_prefix = title[:50]
        value = f"{source}:{author}:{quote_prefix}"
    else:
        value = source + ":" + title

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def deduplicate_records(records):
    unique_records = []
    seen = set()
    duplicates_removed = 0

    for record in records:
        fingerprint = fingerprint_record(record)
        if fingerprint in seen:
            duplicates_removed += 1
            continue
        seen.add(fingerprint)
        unique_records.append(record)

    return unique_records, duplicates_removed
