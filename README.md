# Multi-source web scraping assignment

## Python version and setup

Target Python versions: 3.10 to 3.12.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the project:

```powershell
python main.py
```

## Site inspection notes

The live pages match the assignment selectors.

- Books: the index page contains repeated `article.product_pod` entries. Each book card exposes the title via `h3 > a` and the next page link through `li.next > a`.
- Quotes: the index page contains repeated `div.quote` entries, with quote text in `span.text`, author in `small.author`, tags in `a.tag`, and pagination in `li.next > a`.
- The book site exposes 20 cards per page and the quote site exposes 10 quotes per page, confirming the scraper should follow `urljoin` links rather than hard-coded page numbers.

## Data model and columns

The unified schema is fixed in this order:

`source, source_url, name_or_title, category, price, rating, author, tags, description, scraped_at`

Books are stored with their detail-page URL as `source_url`, while quotes use the page URL where the quote appeared. Fields that do not apply remain empty strings rather than fabricated values.

## Scraping approach

Pagination uses the next link found through `li.next > a` and `urljoin` until no link is present. The books scraper fetches each detail page to collect category and description, and inserts a 0.5s delay between requests to be polite. The quote scraper stays on the main quote pages and records the page URL as the source URL.

## Cleaning, validation, and deduplication

The cleaning layer is pure and network-free. It normalizes whitespace, strips curly quotes, cleans numeric fields, lowercases and sorts tag strings, and normalizes URLs.

Validation returns a list of reason strings using the required values:

- `unknown_source`
- `missing_name`
- `invalid_url`
- `invalid_price`
- `invalid_rating`

The deduplication layer uses SHA-256 fingerprints on lower-cased, punctuation-stripped, whitespace-collapsed text. Books deduplicate on `source + title`, and quotes deduplicate on `source + author + first 50 characters of the quote`. Duplicate rows are removed silently and counted in the summary output.

## Error handling and logging

Each source runs inside its own `try/except` in `main.py` so one failing source cannot stop the other. Individual bad records are logged as warnings and skipped. Logging occurs to both the console and `logs/scraper.log` at INFO, WARNING, and ERROR levels.

## Outputs

The project writes the following files:

- `output/final_dataset.csv`
- `output/summary_report.json`
- `logs/scraper.log`

The CSV uses `csv.DictWriter` with the fixed column order and UTF-8 encoding. The summary JSON includes the requested metrics: per-source raw counts, per-source cleaned counts, rejected reason totals, duplicates removed, final count, timestamps, and duration in seconds.

## Assumptions and known limitations

- This project assumes the public demo sites remain available and follow the same HTML structure used during validation.
- The scraped websites are intentionally demo content, so prices and ratings are treated as the scraped values rather than real-world business data.
- The site is scraped with a polite delay and retries; it is designed for a public academic take-home assignment, not for production-level scraping at scale.

## AI usage summary

This project was developed in a staged workflow: initial workspace setup, live selector confirmation, shared data model, HTTP session setup, scraper implementation, cleaning and validation, deduplication, consolidation, logging, and final verification run.

## Notes for the reviewer

The final run should produce roughly 1100 rows in the combined dataset when both sources are included, with the summary totals reconciling to `raw - rejected - duplicates = final`.
