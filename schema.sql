-- ScholarLink Africa: the database tables written as plain MySQL.
-- The app creates these tables by itself (database.py, create_tables). This file is for
-- understanding the design and for creating the tables by hand in a MySQL viewer if you want to.

CREATE TABLE IF NOT EXISTS scholarships (
    id           INT AUTO_INCREMENT PRIMARY KEY,   -- unique number given automatically
    name         VARCHAR(255) NOT NULL,
    provider     VARCHAR(255) NOT NULL,
    country      VARCHAR(100) NOT NULL,            -- country it is open to, or 'All Africa'
    level        VARCHAR(30)  NOT NULL,            -- Undergraduate / Masters / PhD / Any
    field        VARCHAR(100) NOT NULL,            -- e.g. Engineering, or 'Any'
    eligibility  TEXT NOT NULL,
    deadline     VARCHAR(10)  NOT NULL,            -- stored as YYYY-MM-DD
    link         VARCHAR(500) NOT NULL,            -- official application page
    date_checked VARCHAR(10)  NOT NULL,            -- YYYY-MM-DD
    UNIQUE (name, provider)                        -- the same scholarship cannot be saved twice
);

CREATE TABLE IF NOT EXISTS notifications (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    message      TEXT NOT NULL,
    kind         VARCHAR(10) NOT NULL CHECK (kind IN ('update', 'reminder')),
    date_created VARCHAR(10) NOT NULL,
    is_read      INT NOT NULL DEFAULT 0            -- 0 = unread, 1 = read
);

CREATE TABLE IF NOT EXISTS student_profiles (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    home_country VARCHAR(100) NOT NULL,
    level        VARCHAR(30)  NOT NULL,
    field        VARCHAR(100) NOT NULL,
    date_saved   VARCHAR(10)  NOT NULL
);

-- ---------------------------------------------------------------------------
-- Useful questions to ask the database (run them one by one in a MySQL viewer)
-- ---------------------------------------------------------------------------
-- SHOW TABLES;
-- DESCRIBE scholarships;
-- SELECT COUNT(*) FROM scholarships;
-- SELECT id, name, country, deadline FROM scholarships ORDER BY deadline;
-- SELECT * FROM scholarships WHERE LOWER(country) IN ('rwanda', 'all africa');
-- SELECT * FROM notifications ORDER BY id DESC;
--
-- Careful: the next commands DELETE data. Only use them to reset the demo.
-- DELETE FROM scholarships;
-- DROP TABLE student_profiles, notifications, scholarships;
