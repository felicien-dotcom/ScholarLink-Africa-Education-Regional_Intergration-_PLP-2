import os
import sqlite3
import ssl
from datetime import date, timedelta
from urllib.parse import urlparse, unquote

from models import Scholarship, Notification, format_date

SCHOLARSHIP_COLUMNS = ("id, name, provider, country, level, field, "
                       "eligibility, deadline, link, date_checked")

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))


def load_env_file():
    path = os.path.join(APP_FOLDER, ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def connect_mysql(url):
    import pymysql                                   
    parts = urlparse(url)
    ca_file = os.environ.get("DB_CA_CERT", "")
    if ca_file:
        if not os.path.isabs(ca_file):
            ca_file = os.path.join(APP_FOLDER, ca_file)
        ssl_options = {"ca": ca_file, "check_hostname": False}   
    else:
        ssl_options = {"check_hostname": False}                  
    return pymysql.connect(
        host=parts.hostname, port=parts.port or 3306,
        user=unquote(parts.username or ""), password=unquote(parts.password or ""),
        database=(parts.path or "/").lstrip("/") or "defaultdb",
        ssl=ssl_options, charset="utf8mb4", connect_timeout=15)


class Database:
    def __init__(self, path="scholarlink.db"):
        load_env_file()
        url = os.environ.get("DATABASE_URL", "").strip()
        self.kind = "sqlite"
        self.notice = ""
        self.conn = None
        if url and path != ":memory:":               
            try:
                self.conn = connect_mysql(url)
                self.kind = "mysql"
            except Exception as error:               
                self.notice = (f"Could not reach the cloud database ({type(error).__name__}). "
                               "Using the local SQLite file instead.")
        if self.conn is None:
            self.conn = sqlite3.connect(path)

    def close(self):
        self.conn.close()

    def describe(self):
        return "Aiven MySQL (cloud)" if self.kind == "mysql" else "SQLite (local file)"

    def _execute(self, sql, params=()):
        if self.kind == "mysql":
            sql = sql.replace("?", "%s")
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(params))
        return cursor

    def _is_duplicate_error(self, error):
        if self.kind == "sqlite":
            return isinstance(error, sqlite3.IntegrityError)
        import pymysql
        return isinstance(error, pymysql.err.IntegrityError)   

    def create_tables(self):
        pk = "INT AUTO_INCREMENT PRIMARY KEY" if self.kind == "mysql" else "INTEGER PRIMARY KEY AUTOINCREMENT"
        statements = [
            f"""CREATE TABLE IF NOT EXISTS scholarships (
                id           {pk},
                name         VARCHAR(255) NOT NULL,
                provider     VARCHAR(255) NOT NULL,
                country      VARCHAR(100) NOT NULL,
                level        VARCHAR(30)  NOT NULL,
                field        VARCHAR(100) NOT NULL,
                eligibility  TEXT NOT NULL,
                deadline     VARCHAR(10)  NOT NULL,
                link         VARCHAR(500) NOT NULL,
                date_checked VARCHAR(10)  NOT NULL,
                UNIQUE (name, provider)
            )""",
            f"""CREATE TABLE IF NOT EXISTS notifications (
                id           {pk},
                message      TEXT NOT NULL,
                kind         VARCHAR(10) NOT NULL CHECK (kind IN ('update', 'reminder')),
                date_created VARCHAR(10) NOT NULL,
                is_read      INTEGER NOT NULL DEFAULT 0
            )""",
            f"""CREATE TABLE IF NOT EXISTS student_profiles (
                id           {pk},
                home_country VARCHAR(100) NOT NULL,
                level        VARCHAR(30)  NOT NULL,
                field        VARCHAR(100) NOT NULL,
                date_saved   VARCHAR(10)  NOT NULL
            )""",
        ]
        for statement in statements:
            self._execute(statement)
        self.conn.commit()

    def count_scholarships(self):
        return self._execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]

    def add_scholarship(self, s):
        sql = ("INSERT INTO scholarships (name, provider, country, level, field, "
               "eligibility, deadline, link, date_checked) VALUES (?,?,?,?,?,?,?,?,?)")
        params = (s.name, s.provider, s.country, s.level, s.field, s.eligibility,
                  s.deadline.isoformat(), s.link, s.date_checked.isoformat())
        try:
            cursor = self._execute(sql, params)
            new_id = cursor.lastrowid
        except Exception as error:
            if self._is_duplicate_error(error):
                self.conn.rollback()                
                raise ValueError("That scholarship (same name and provider) is already saved.")
            raise
        self.conn.commit()
        s.id = new_id
        return new_id

    def search_by_country(self, country):
        rows = self._execute(
            f"SELECT {SCHOLARSHIP_COLUMNS} FROM scholarships "
            "WHERE LOWER(country) IN (?, 'all africa') ORDER BY deadline",
            (country.strip().lower(),)).fetchall()
        return [Scholarship.from_row(r) for r in rows]

    def get_all(self):
        rows = self._execute(
            f"SELECT {SCHOLARSHIP_COLUMNS} FROM scholarships ORDER BY deadline").fetchall()
        return [Scholarship.from_row(r) for r in rows]

    def get_by_id(self, scholarship_id):
        row = self._execute(
            f"SELECT {SCHOLARSHIP_COLUMNS} FROM scholarships WHERE id = ?",
            (scholarship_id,)).fetchone()
        return Scholarship.from_row(row) if row else None

    def closing_within(self, days):
        today = date.today()
        rows = self._execute(
            f"SELECT {SCHOLARSHIP_COLUMNS} FROM scholarships "
            "WHERE deadline BETWEEN ? AND ? ORDER BY deadline",
            (today.isoformat(), (today + timedelta(days=days)).isoformat())).fetchall()
        return [Scholarship.from_row(r) for r in rows]

    def delete_scholarship(self, scholarship_id):
        cursor = self._execute("DELETE FROM scholarships WHERE id = ?", (scholarship_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_all_scholarships(self):
        self._execute("DELETE FROM scholarships")
        self.conn.commit()

    def add_notification(self, message, kind):
        exists = self._execute(
            "SELECT 1 FROM notifications WHERE message = ? AND kind = ?",
            (message, kind)).fetchone()
        if exists:
            return False
        self._execute(
            "INSERT INTO notifications (message, kind, date_created, is_read) VALUES (?,?,?,0)",
            (message, kind, date.today().isoformat()))
        self.conn.commit()
        return True

    def create_deadline_reminders(self, days=7):
        created = 0
        for s in self.closing_within(days):
            left = s.days_left()
            when = "today" if left == 0 else f"in {left} day(s)"
            msg = f"Deadline reminder: '{s.name}' closes {when} ({format_date(s.deadline)})."
            if self.add_notification(msg, "reminder"):
                created += 1
        return created

    def get_notifications(self):
        rows = self._execute(
            "SELECT id, message, kind, date_created, is_read FROM notifications "
            "ORDER BY id DESC").fetchall()
        return [Notification(m, k, date.fromisoformat(d), bool(r), i) for i, m, k, d, r in rows]

    def count_unread(self):
        return self._execute(
            "SELECT COUNT(*) FROM notifications WHERE is_read = 0").fetchone()[0]

    def mark_all_read(self):
        self._execute("UPDATE notifications SET is_read = 1")
        self.conn.commit()

    def save_profile(self, profile):
        self._execute(
            "INSERT INTO student_profiles (home_country, level, field, date_saved) VALUES (?,?,?,?)",
            (profile.home_country, profile.level, profile.field, date.today().isoformat()))
        self.conn.commit()
