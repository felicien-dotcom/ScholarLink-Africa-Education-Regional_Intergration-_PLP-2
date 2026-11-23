import os

import features_admin
import features_search
import helpers
from database import Database
from sample_data import sample_scholarships

DB_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "scholarlink.db")


def authenticate_user(db, admin_password):
    """Handle Student registration/login and Admin login without auto-redirecting on failure."""
    while True:
        print("\n" + "=" * 50)
        print("WELCOME TO SCHOLARLINK AFRICA")
        print("=" * 50)
        print("1. Student Login")
        print("2. Create Student Account")
        print("3. Admin Login")
        print("0. Exit")

        choice = helpers.ask_number(
            "Select an option (0-3): ", 0, 3,
            "Invalid choice. Please enter 0, 1, 2, or 3."
        )

        if choice == 0:
            return None

        elif choice == 1:
            username = helpers.ask_text("Enter username: ")
            password = helpers.ask_text("Enter password: ")
            if db.verify_student(username, password):
                print(f"\nWelcome back, {username}!")
                return False  # False = Student mode
            else:
                print("Invalid username or password. Please try again.")

        elif choice == 2:
            username = helpers.ask_text_max("Choose a username: ", 100)
            password = helpers.ask_text_max(
                "Create a password (min 4 characters): ", 255)
            if len(password) < 4:
                print("Password must be at least 4 characters. Account not created.")
                continue
            try:
                db.register_student(username, password)
                print("Account created successfully! Please select option 1 to log in.")
            except ValueError as error:
                print(f"Could not create account: {error}")

        elif choice == 3:
            password = helpers.ask_text("Enter admin password: ")
            if password == admin_password:
                print("\nAdmin access granted.")
                return True  # True = Admin mode
            else:
                print("Incorrect admin password. Returning to login screen.")


def show_menu(unread, is_admin=False):
    """Print the Main Menu based on user role."""
    print("\n" + "=" * 50)
    print("SCHOLARLINK AFRICA - MAIN MENU")
    print("=" * 50)
    print("What would you like to do today?")
    print("1. Search scholarships by country")
    print("2. Check my eligibility")
    print("3. View scholarship details & deadline")
    print(f"4. Notifications ({unread} unread)")
    print("5. Scholarships closing in the next 30 days")
    if is_admin:
        print("6. Add a scholarship (admin)")
        print("7. Delete a scholarship (admin)")
    print("0. Exit program")


def main():
    db = Database(DB_FILE)
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")

    if db.notice:
        print(db.notice)
    print(f"Database: {db.describe()}")
    db.create_tables()

    if db.count_scholarships() == 0:
        for s in sample_scholarships():
            db.add_scholarship(s)
        print(
            "(First run: loaded SAMPLE scholarships. Use import_data.py to load real ones.)")

    new_reminders = db.create_deadline_reminders(days=7)
    if new_reminders:
        print(
            f"You have {new_reminders} new deadline reminder(s). See option 4.")

    try:
        is_admin = authenticate_user(db, admin_password)
        if is_admin is None:
            return

        actions = {
            1: features_search.search_by_country,
            2: features_search.check_eligibility,
            3: features_search.view_details,
            4: features_admin.view_notifications,
            5: features_admin.closing_soon,
        }

        if is_admin:
            actions.update({
                6: features_admin.add_scholarship,
                7: features_admin.delete_scholarship,
            })

        max_choice = 7 if is_admin else 5

        while True:
            show_menu(db.count_unread(), is_admin)
            choice = helpers.ask_number(
                f"Type a number (0-{max_choice}) and press Enter: ",
                0,
                max_choice,
                f"Invalid choice. Please enter a number from 0 to {max_choice}."
            )
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
