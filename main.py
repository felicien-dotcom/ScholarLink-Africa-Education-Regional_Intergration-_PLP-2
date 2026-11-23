"""ScholarLink Africa - a free, terminal-based scholarship finder.

OWNER: Felicien (Team Lead). Starts the app, shows the menu and runs the menu loop.

Run:  python main.py        (Windows: python main.py or py main.py)
Menu loop (while), if/else, exceptions, classes, SQL database (Aiven MySQL or local SQLite).
"""
import os

import features_admin
import features_search
import helpers
from database import Database
from sample_data import sample_scholarships

# The local SQLite file is used when no cloud database is set up (or when the cloud is unreachable).
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scholarlink.db")


def show_menu(unread):
    """Print the Main Menu. 'unread' is the number of unread notifications."""
    print("\n" + "=" * 50)
    print("WELCOME TO SCHOLARLINK AFRICA")
    print("=" * 50)
    print("What would you like to do today?")
    print("1. Search scholarships by country")
    print("2. Check my eligibility")
    print("3. View scholarship details & deadline")
    print("4. Add a scholarship (admin)")
    print(f"5. Notifications ({unread} unread)")
    print("6. Scholarships closing in the next 30 days")
    print("0. Exit program")


def main():
    # 1. Open the database (cloud MySQL or local SQLite) and make sure the tables exist
    db = Database(DB_FILE)
    if db.notice:
        print(db.notice)                             # e.g. "Could not reach the cloud database..."
    print(f"Database: {db.describe()}")
    db.create_tables()

    # 2. First run only: load SAMPLE scholarships so the demo is not empty
    if db.count_scholarships() == 0:
        for s in sample_scholarships():
            db.add_scholarship(s)
        print("(First run: loaded SAMPLE scholarships. Use import_data.py to load real ones.)")

    # 3. Create reminders for scholarships closing within 7 days
    new_reminders = db.create_deadline_reminders(days=7)
    if new_reminders:
        print(f"You have {new_reminders} new deadline reminder(s). See option 5.")

    # 4. A dictionary links each menu number to the feature function that runs it
    actions = {
        1: features_search.search_by_country,
        2: features_search.check_eligibility,
        3: features_search.view_details,
        4: features_admin.add_scholarship,
        5: features_admin.view_notifications,
        6: features_admin.closing_soon,
    }

    # 5. The menu loop: show the menu, read a number, run the feature, repeat until 0
    try:
        while True:
            show_menu(db.count_unread())
            choice = helpers.ask_number("Type a number (0-6) and press Enter: ", 0, 6,
                                        "Invalid choice. Please enter a number from 0 to 6.")
            if choice == 0:
                break
            actions[choice](db)
    except (EOFError, KeyboardInterrupt):            # Ctrl+C / Ctrl+D: leave cleanly
        print()
    finally:
        db.close()                                   # always close the database
    print("Thank you for using ScholarLink Africa. Goodbye!")


if __name__ == "__main__":
    main()
