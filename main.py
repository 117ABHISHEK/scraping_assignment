import logging
from datetime import datetime, timezone
from pathlib import Path

from processing.cleaning import clean_price, clean_rating, clean_tags, clean_text, normalize_url
from processing.consolidation import write_dataset, write_summary_report
from processing.deduplication import deduplicate_records
from processing.validation import validate_record
from scrapers.books_scraper import collect_books
from scrapers.quotes_scraper import collect_quotes

OUTPUT_DIR = Path("output")
LOG_DIR = Path("logs")
REASONS = ["unknown_source", "missing_name", "invalid_url", "invalid_price", "invalid_rating"]


def configure_logger():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("scraper")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(LOG_DIR / "scraper.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def clean_record(raw_record, source_name):
    source_url = normalize_url(raw_record.get("source_url", ""))
    name_or_title = clean_text(raw_record.get("name_or_title", ""))
    category = clean_text(raw_record.get("category", ""))
    price_value = clean_price(raw_record.get("price", ""))
    rating_value = clean_rating(raw_record.get("rating", ""))
    author = clean_text(raw_record.get("author", ""))
    tags = clean_tags(raw_record.get("tags", ""))
    description = clean_text(raw_record.get("description", ""))

    if source_name == "quotes":
        category = ""
        description = ""
        price_value = ""
        rating_value = ""

    record = {
        "source": clean_text(source_name),
        "source_url": source_url,
        "name_or_title": name_or_title,
        "category": category,
        "price": price_value if price_value is not None else "",
        "rating": rating_value if rating_value is not None else "",
        "author": author,
        "tags": tags,
        "description": description,
        "scraped_at": "",
    }
    return record


def collect_source(source_name, collector):
    records = []
    try:
        records = collector()
    except Exception:
        logging.getLogger("scraper").exception("Failed to scrape %s source", source_name)
    return records


def collect_valid_records(source_name, raw_records, logger):
    source_rejections = {reason: 0 for reason in REASONS}
    valid_records = []
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    for raw_record in raw_records:
        cleaned_record = clean_record(raw_record, source_name)
        cleaned_record["scraped_at"] = timestamp
        reasons = validate_record(cleaned_record)

        if reasons:
            for reason in reasons:
                source_rejections[reason] += 1
            logger.warning("Rejected record from %s: %s", source_name, reasons)
            continue

        valid_records.append(cleaned_record)

    return valid_records, source_rejections


def build_summary(raw_counts, cleaned_counts, rejected_counts, duplicates_removed, final_count, start_time, end_time):
    duration_seconds = (end_time - start_time).total_seconds()
    summary = {
        "raw_collected": raw_counts,
        "cleaned": cleaned_counts,
        "rejected_counts": rejected_counts,
        "duplicates_removed": duplicates_removed,
        "final_count": final_count,
        "start_time": start_time.isoformat(timespec="seconds"),
        "end_time": end_time.isoformat(timespec="seconds"),
        "duration_seconds": round(duration_seconds, 3),
    }
    return summary


def main():
    logger = configure_logger()
    start_time = datetime.now(timezone.utc)
    logger.info("Scraping started")

    raw_data = {
        "books": collect_source("books", collect_books),
        "quotes": collect_source("quotes", collect_quotes),
    }

    cleaned_by_source = {}
    rejected_by_reason = {reason: 0 for reason in REASONS}
    all_valid_records = []

    for source_name in ["books", "quotes"]:
        valid_records, source_rejections = collect_valid_records(source_name, raw_data.get(source_name, []), logger)
        cleaned_by_source[source_name] = len(valid_records)
        for reason, count in source_rejections.items():
            rejected_by_reason[reason] += count
        all_valid_records.extend(valid_records)

    unique_records, duplicates_removed = deduplicate_records(all_valid_records)
    write_dataset(unique_records, OUTPUT_DIR / "final_dataset.csv")

    raw_total = sum(len(raw_data.get(source_name, [])) for source_name in ["books", "quotes"])
    rejected_total = sum(rejected_by_reason.values())
    final_total = len(unique_records)

    if raw_total - rejected_total - duplicates_removed != final_total:
        raise ValueError("Summary totals do not reconcile")

    summary = build_summary(
        raw_counts={source_name: len(raw_data.get(source_name, [])) for source_name in ["books", "quotes"]},
        cleaned_counts=cleaned_by_source,
        rejected_counts=rejected_by_reason,
        duplicates_removed=duplicates_removed,
        final_count=final_total,
        start_time=start_time,
        end_time=datetime.now(timezone.utc),
    )
    write_summary_report(summary, OUTPUT_DIR / "summary_report.json")

    logger.info("Final dataset written to %s", OUTPUT_DIR / "final_dataset.csv")
    logger.info("Summary written to %s", OUTPUT_DIR / "summary_report.json")
    logger.info("Scraping completed with %s records", final_total)


if __name__ == "__main__":
    main()
