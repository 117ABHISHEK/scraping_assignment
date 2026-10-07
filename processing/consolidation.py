import csv
import json
from pathlib import Path

from processing.data_model import SCRAPED_COLUMNS


def write_dataset(records, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=SCRAPED_COLUMNS)
        writer.writeheader()
        for record in records:
            writer.writerow({key: record.get(key, "") for key in SCRAPED_COLUMNS})


def write_summary_report(summary, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as json_file:
        json.dump(summary, json_file, indent=2, ensure_ascii=False)
        json_file.write("\n")
