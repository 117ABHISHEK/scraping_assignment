# Multi-source web scraping

## Environment setup

Use Python 3.10, 3.11, or 3.12.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Stage 1: site inspection notes

The live pages match the assignment selectors.

- Books: the index page has repeated `article.product_pod` entries. Each product card exposes the book title via `h3 > a`, and the pagination chain continues with `li.next > a` until the last page.
- Quotes: the index page contains repeated `div.quote` entries, each quote text in `span.text`, author in `small.author`, tags in `a.tag`, and next-page navigation in `li.next > a`.
- The books site page 1 returns 20 book cards and a next link; the quotes page 1 returns 10 quotes and a next link. This confirms the scraper can follow the site’s natural pagination rather than hard-coding page numbers.
