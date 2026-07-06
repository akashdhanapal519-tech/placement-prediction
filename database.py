import sqlite3
import os
from config import Config
from werkzeug.security import generate_password_hash

def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'student',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Students table
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT,
        reg_number TEXT,
        department TEXT,
        mobile TEXT,
        email TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    # Academic table
    c.execute('''CREATE TABLE IF NOT EXISTS academic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        tenth_pct REAL DEFAULT 0,
        twelfth_pct REAL DEFAULT 0,
        cgpa REAL DEFAULT 0,
        aptitude_score REAL DEFAULT 0,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )''')

    # Skills table
    c.execute('''CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        programming_score REAL DEFAULT 0,
        technical_score REAL DEFAULT 0,
        soft_skills_score REAL DEFAULT 0,
        communication_score REAL DEFAULT 0,
        coding_score REAL DEFAULT 0,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )''')

    # Internships table
    c.execute('''CREATE TABLE IF NOT EXISTS internships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        company TEXT,
        duration TEXT,
        internship_type TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )''')

    # Certifications table
    c.execute('''CREATE TABLE IF NOT EXISTS certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        cert_name TEXT,
        provider TEXT,
        year INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )''')

    # Predictions table
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        probability REAL DEFAULT 0,
        result TEXT,
        tier TEXT,
        recommendations TEXT,
        algorithm_scores TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )''')

    conn.commit()

    # Create default admin
    try:
        admin_hash = generate_password_hash('admin123')
        c.execute("INSERT OR IGNORE INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                  ('admin', 'admin@placement.com', admin_hash, 'admin'))
        conn.commit()
    except Exception:
        pass

    conn.close()

def get_student_by_user_id(user_id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE user_id=?', (user_id,)).fetchone()
    conn.close()
    return student

def get_academic_by_student_id(student_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM academic WHERE student_id=?', (student_id,)).fetchone()
    conn.close()
    return row

def get_skills_by_student_id(student_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM skills WHERE student_id=?', (student_id,)).fetchone()
    conn.close()
    return row

def get_internships_by_student_id(student_id):
    conn = get_db()
    rows = conn.execute('SELECT * FROM internships WHERE student_id=?', (student_id,)).fetchall()
    conn.close()
    return rows

def get_certifications_by_student_id(student_id):
    conn = get_db()
    rows = conn.execute('SELECT * FROM certifications WHERE student_id=?', (student_id,)).fetchall()
    conn.close()
    return rows

def get_latest_prediction(student_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM predictions WHERE student_id=? ORDER BY created_at DESC LIMIT 1', (student_id,)).fetchone()
    conn.close()
    return row

def get_all_students_with_details():
    conn = get_db()
    rows = conn.execute('''
        SELECT u.id, u.username, u.email, u.created_at,
               s.name, s.reg_number, s.department,
               a.cgpa, a.aptitude_score,
               sk.programming_score, sk.communication_score,
               p.probability, p.result, p.tier
        FROM users u
        LEFT JOIN students s ON s.user_id = u.id
        LEFT JOIN academic a ON a.student_id = s.id
        LEFT JOIN skills sk ON sk.student_id = s.id
        LEFT JOIN predictions p ON p.student_id = s.id
        WHERE u.role = 'student'
        ORDER BY u.created_at DESC
    ''').fetchall()
    conn.close()
    return rows

def get_all_predictions():
    conn = get_db()
    rows = conn.execute('''
        SELECT p.*, s.department, s.name, a.cgpa
        FROM predictions p
        JOIN students s ON s.id = p.student_id
        LEFT JOIN academic a ON a.student_id = s.id
        ORDER BY p.created_at DESC
    ''').fetchall()
    conn.close()
    return rows
