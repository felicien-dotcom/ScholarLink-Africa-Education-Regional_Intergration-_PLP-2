
from datetime import date, datetime

from models import DATE_FORMAT, TABLE_HEADER


def ask_text(prompt):
    
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This cannot be empty. Please try again.")


def ask_number(prompt, low, high, error=None):
    
    while True:
        raw = input(prompt).strip()
        try:
            number = int(raw)
        except ValueError:                       # user typed letters, e.g. "abc"
            number = None
        if number is not None and low <= number <= high:
            return number
        print(error or f"Invalid choice. Please enter a number from {low} to {high}.")


def ask_date(prompt):
    
    while True:
        raw = input(prompt).strip()
        try:
            chosen = datetime.strptime(raw, DATE_FORMAT).date()
        except ValueError:
            print("Invalid date. Use DD/MM/YYYY, for example 30/11/2026.")
            continue
        if chosen < date.today():
            print("The deadline cannot be in the past. Please try again.")
            continue
        return chosen


def show_table(scholarships):
    
    print(TABLE_HEADER)
    for s in scholarships:
        print(s.table_row())


def ask_text_max(prompt, max_length):
    
    while True:
        value = ask_text(prompt)
        if len(value) <= max_length:
            return value
        print(f"Too long. Please use at most {max_length} characters.")


def ask_yes_no(prompt):
    
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")
