"""sample_data.py - SAMPLE scholarships so the demo works on a fresh install.

OWNER: Joseph (Data Lead)

These are NOT real scholarships. Replace them with verified data using import_data.py.
Deadlines are set relative to today so the reminder feature can be demonstrated.
"""
from datetime import date, timedelta

from models import Scholarship


def sample_scholarships():
    today = date.today()
    note = "SAMPLE DATA - replace with verified scholarship."
    rows = [
        ("Sample Scholarship A", "Sample Provider 1", "Rwanda", "Undergraduate", "Engineering", 5),
        ("Sample Scholarship B", "Sample Provider 2", "Rwanda", "Masters", "Any", 20),
        ("Sample Scholarship C", "Sample Provider 3", "Kenya", "Undergraduate", "Medicine", 45),
        ("Sample Scholarship D", "Sample Provider 4", "Nigeria", "PhD", "Agriculture", 60),
        ("Sample Scholarship E", "Sample Provider 5", "All Africa", "Any", "Computer Science", 25),
        ("Sample Scholarship F", "Sample Provider 6", "Ghana", "Masters", "Education", 90),
    ]
    return [
        Scholarship(name, provider, country, level, field, f"{level} students from {country}. {note}",
                    today + timedelta(days=days), "https://example.org/sample", today)
        for name, provider, country, level, field, days in rows
    ]