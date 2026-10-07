import re
from urllib.parse import urljoin


def clean_text(value):
    if value is None:
        return ""
    text = str(value).replace("\xa0", " ").replace("\u202f", " ").replace("\u2007", " ")
    return re.sub(r"\s+", " ", text).strip()


def strip_quotes(value):
    if value is None:
        return ""
    mapping = str.maketrans({
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "„": '"',
        "‚": "'",
        "«": '"',
        "»": '"',
    })
    return clean_text(str(value).translate(mapping))


def clean_price(value):
    if value is None:
        return None

    text = strip_quotes(clean_text(value)).replace("£", "").replace("$", "").replace("€", "")
    if not text:
        return None

    text = text.replace(",", "").strip()
    if not text or text in {"-", "--", "--0"}:
        return None

    try:
        return float(text)
    except ValueError:
        return None


def clean_rating(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        number = int(value)
        if 1 <= number <= 5:
            return number
        return None

    text = clean_text(strip_quotes(value)).lower()
    if not text:
        return None

    numeric = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
    words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }

    if text in numeric:
        return numeric[text]
    if text in words:
        return words[text]

    match = re.search(r"(\d)", text)
    if match:
        number = int(match.group(1))
        if 1 <= number <= 5:
            return number
    return None


def clean_tags(value):
    if value is None:
        return ""

    if isinstance(value, str):
        raw_items = [part.strip() for part in value.split(";")]
    elif isinstance(value, (list, tuple, set)):
        raw_items = list(value)
    else:
        raw_items = [str(value)]

    tags = []
    for item in raw_items:
        text = clean_text(strip_quotes(item))
        if not text:
            continue
        for tag in text.split(";"):
            clean_tag = clean_text(strip_quotes(tag)).lower()
            if clean_tag:
                tags.append(clean_tag)

    return ";".join(sorted(set(tags)))


def normalize_url(value):
    if value is None:
        return ""

    text = clean_text(strip_quotes(value)).strip()
    if not text:
        return ""

    if text.startswith("//"):
        text = "https:" + text
    if "://" not in text:
        return "https://" + text.lstrip("/")
    return text
