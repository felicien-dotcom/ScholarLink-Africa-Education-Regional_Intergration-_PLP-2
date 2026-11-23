import os

import features_admin
import features_search
import helpers
from database import Database
from sample_data import sample_scholarships

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
    db = Database(DB_FILE)
    if db.notice:
        print(db.notice)                            
    print(f"Database: {db.describe()}")
    db.create_tables()

    if db.count_scholarships() == 0:
        for s in sample_scholarships():
            db.add_scholarship(s)
        print("(First run: loaded SAMPLE scholarships. Use import_data.py to load real ones.)")

    new_reminders = db.create_deadline_reminders(days=7)
    if new_reminders:
        print(f"You have {new_reminders} new deadline reminder(s). See option 5.")

    actions = {
        1: features_search.search_by_country,
        2: features_search.check_eligibility,
        3: features_search.view_details,
        4: features_admin.add_scholarship,
        5: features_admin.view_notifications,
        6: features_admin.closing_soon,
    }

    try:
        while True:
            show_menu(db.count_unread())
            choice = helpers.ask_number("Type a number (0-6) and press Enter: ", 0, 6,
                                        "Invalid choice. Please enter a number from 0 to 6.")
            if choice == 0:
                break
            actions[choice](db)
    except (EOFError, KeyboardInterrupt):            
        print()
    finally:
        db.close()                                  
    print("Thank you for using ScholarLink Africa. Goodbye!")


if __name__ == "__main__":
    main()
