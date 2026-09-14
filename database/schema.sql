-- Database Schema for Intelligent Student Admission Recommendation System

DROP TABLE IF EXISTS officer_decisions;
DROP TABLE IF EXISTS ai_recommendations;
DROP TABLE IF EXISTS eligibility_results;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS academic_info;
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'admin')),
    phone TEXT,
    dob TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    application_number TEXT UNIQUE NOT NULL,
    course TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'DRAFT',
    submitted_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE academic_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER UNIQUE NOT NULL,
    class10_percentage REAL NOT NULL,
    class12_percentage REAL NOT NULL,
    mathematics REAL NOT NULL,
    physics REAL NOT NULL,
    chemistry REAL NOT NULL,
    entrance_exam TEXT NOT NULL,
    entrance_score REAL NOT NULL,
    passing_year INTEGER NOT NULL,
    school_board TEXT NOT NULL,
    achievements TEXT,
    certifications TEXT,
    extracurricular TEXT,
    work_experience TEXT,
    sop TEXT,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
);

CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    document_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    ocr_text TEXT,
    verification_status TEXT DEFAULT 'PENDING',
    verification_message TEXT,
    is_digilocker INTEGER DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
);

CREATE TABLE eligibility_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER UNIQUE NOT NULL,
    is_eligible INTEGER NOT NULL,
    summary_json TEXT NOT NULL,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
);

CREATE TABLE ai_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER UNIQUE NOT NULL,
    suitability_score REAL NOT NULL,
    recommendation TEXT NOT NULL,
    feature_importance_json TEXT NOT NULL,
    explanation_json TEXT NOT NULL,
    model_version TEXT DEFAULT 'v1.0-RandomForest',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
);

CREATE TABLE officer_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER UNIQUE NOT NULL,
    officer_id INTEGER NOT NULL,
    decision TEXT NOT NULL CHECK (decision IN ('ACCEPTED', 'REJECTED', 'ON_HOLD')),
    comments TEXT,
    is_override INTEGER DEFAULT 0,
    decision_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES users(id)
);
