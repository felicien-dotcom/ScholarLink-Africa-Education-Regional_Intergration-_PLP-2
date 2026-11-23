from database import Database
from main import DB_FILE


def main():
    db = Database(DB_FILE)
    if db.notice:
        print(db.notice)
    print(f"Connected to: {db.describe()}")
    db.create_tables()                      
    for table, count in db.table_counts().items():
        print(f"  table {table}: {count} row(s)")
    db.close()


if __name__ == "__main__":
    main()
