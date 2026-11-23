"""check_database.py - shows which database the app uses and what is inside it.

OWNER: Shekinah (Database Lead)
Run:  python check_database.py        (Windows: py check_database.py)
Use it to test your .env file and to take the database screenshot for the report.
"""
from database import Database
from main import DB_FILE


def main():
    db = Database(DB_FILE)
    if db.notice:
        print(db.notice)
    print(f"Connected to: {db.describe()}")
    db.create_tables()                       # safe to repeat: tables are only created if missing
    for table, count in db.table_counts().items():
        print(f"  table {table}: {count} row(s)")
    db.close()


if __name__ == "__main__":
    main()
