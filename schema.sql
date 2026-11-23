CREATE TABLE IF NOT EXISTS scholarships (
    id           INT AUTO_INCREMENT PRIMARY KEY,   
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
);

CREATE TABLE IF NOT EXISTS notifications (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    message      TEXT NOT NULL,
    kind         VARCHAR(10) NOT NULL CHECK (kind IN ('update', 'reminder')),
    date_created VARCHAR(10) NOT NULL,
    is_read      INT NOT NULL DEFAULT 0            
);

CREATE TABLE IF NOT EXISTS student_profiles (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    home_country VARCHAR(100) NOT NULL,
    level        VARCHAR(30)  NOT NULL,
    field        VARCHAR(100) NOT NULL,
    date_saved   VARCHAR(10)  NOT NULL
);