"""import_data.py - load real scholarships from a CSV file into the database.

OWNER: Joseph (Data Lead)

Usage:
    python import_data.py scholarships.csv            (adds the rows)
    python import_data.py scholarships.csv --replace  (deletes the old rows first, e.g. the SAMPLE ones)

CSV columns (see scholarships_template.csv):
    name, provider, country, level, field, eligibility, deadline (DD/MM/YYYY), link
Files (class topic): this script reads a CSV file with the csv module.
"""
import csv
import sys
from datetime import datetime

from database import Database
from main import DB_FILE
from models import Scholarship, LEVELS, ANY, DATE_FORMAT

REQUIRED = ["name", "provider", "country", "level", "field", "eligibility", "deadline", "link"]


def read_rows(path):
    """Return (scholarships, problems) from a CSV file."""
    good, problems = [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("CSV is missing column(s): " + ", ".join(missing))
        for line_number, row in enumerate(reader, start=2):
            row = {k: (v or "").strip() for k, v in row.items()}
            if not all(row[c] for c in REQUIRED):
                problems.append(f"line {line_number}: a required value is empty")
                continue
            level = next((l for l in LEVELS + [ANY] if l.lower() == row["level"].lower()), None)
            if level is None:
                problems.append(f"line {line_number}: level must be Undergraduate, Masters, PhD or Any")
                continue
            try:
                deadline = datetime.strptime(row["deadline"], DATE_FORMAT).date()
            except ValueError:
                problems.append(f"line {line_number}: deadline must be DD/MM/YYYY")
                continue
            good.append(Scholarship(row["name"], row["provider"], row["country"], level,
                                    row["field"], row["eligibility"], deadline, row["link"]))
    return good, problems


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    try:
        scholarships, problems = read_rows(sys.argv[1])
    except (OSError, ValueError) as error:
        print(f"Could not read the file: {error}")
        return
    db = Database(DB_FILE)
    db.create_tables()
    if "--replace" in sys.argv:
        db.delete_all_scholarships()
    saved = 0
    for s in scholarships:
        try:
            db.add_scholarship(s)
            saved += 1
        except ValueError as error:
            problems.append(f"'{s.name}': {error}")
    print(f"Total scholarships in the database: {db.count_scholarships()}")
    db.close()
    print(f"Imported {saved} scholarship(s).")
    for p in problems:
        print("  Skipped ->", p)


if __name__ == "__main__":
    main()