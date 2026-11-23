# ScholarLink Africa

A free, terminal-based scholarship finder for African students (African Leadership University, BSE Year 1, PLP2).
Students use a numbered menu to search scholarships by country, check their eligibility, view deadlines and official
links, and get update and reminder notifications. Data is stored in an SQL database: Aiven MySQL (cloud), or a local SQLite file when no cloud is set up.

## Requirements
- Python 3.8 or newer (tested on Python 3.12).
- Local SQLite mode: standard library only, nothing to install.
- Aiven cloud mode: `pip install -r requirements.txt` (installs PyMySQL, a pure-Python driver).

## Run it
```
python main.py          # Windows: py main.py
```
The first run creates `scholarlink.db` and loads SAMPLE scholarships (not real). Replace them with verified data:
```
python import_data.py scholarships.csv --replace
```
Use `scholarships_template.csv` as the format (deadline is DD/MM/YYYY).

## Use the Aiven cloud database (optional)
1. Create a free MySQL service on Aiven and copy its Service URI.
2. Copy `.env.example` to `.env` and paste the URI as `DATABASE_URL`. **Never upload `.env` or `ca.pem` to GitHub.**
3. Run `python main.py`. The first line shows which database is used. If the cloud is unreachable the app falls back to the local SQLite file.
4. Only one person loads the real data: `python import_data.py scholarships.csv --replace`.

## Menu
| Option | What it does |
|---|---|
| 1 | Search scholarships by country (also shows "All Africa" ones) |
| 2 | Check eligibility: level, home country and field are compared with each scholarship |
| 3 | View full details, deadline and official link by scholarship ID |
| 4 | Add a scholarship (admin); also creates an "update" notification |
| 5 | Notifications: updates and deadline reminders (a reminder is created at start-up when a deadline is within 7 days) |
| 6 | Bonus: scholarships closing in the next 30 days |
| 0 | Exit |

## Files
| File | Purpose |
|---|---|
| `main.py` | Menu loop and start-up |
| `helpers.py` | Input checks and table display (Axel) |
| `features_search.py` | Features 1, 2, 3: search, eligibility, details (Fidelis) |
| `features_admin.py` | Features 4, 5, 6: add scholarship, notifications, closing soon (Jess) |
| `models.py` | Classes: Scholarship, StudentProfile, Notification |
| `database.py` | All SQL: Aiven MySQL or local SQLite. 3 tables (scholarships, notifications, student_profiles) |
| `check_database.py` | Tests the connection and shows how many rows each table has |
| `schema.sql` | The 3 tables as plain MySQL (the app creates them automatically) |
| `.env.example` | Template for your private `.env` (database URI) |
| `requirements.txt` | PyMySQL (only needed for the cloud database) |
| `sample_data.py` | SAMPLE scholarships for the first run |
| `import_data.py` | Load real scholarships from a CSV file |
| `tests/test_app.py` | Unit tests: `python -m unittest discover -s tests` |

## What "country" means
The `country` of a scholarship is the country whose students it is open to. Use `All Africa` when it is open to every African country.

## Known limits
- One user at a time, offline, English only. No accounts, payments or online applications.
- Scholarship data is entered by hand, so every entry stores the date it was checked. Always confirm on the official page.
- Favourite scholarships (a bonus idea) are not built yet.

## Team Git workflow
1. Felicien creates the repository and adds all members as collaborators.
2. Each member works on their own branch, e.g. `git checkout -b feature/axel-validation`, and commits from their own account.
3. Open a Pull Request, another member reviews it, then merge into `main`.
4. Never commit `scholarlink.db` or `__pycache__` (see `.gitignore`).
