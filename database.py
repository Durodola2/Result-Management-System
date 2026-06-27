# database.py
import sqlite3

DB_NAME = "result_management.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Users table (for signup/login)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            matric TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            dept TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            code TEXT PRIMARY KEY,
            title TEXT NOT NULL
        )
    ''')
    
    # Create Results table - Fixed to include total questions and exam type
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matric TEXT,
            subject TEXT,
            score INTEGER,
            total_questions INTEGER,
            exam_type TEXT,
            FOREIGN KEY(matric) REFERENCES users(matric)
        )
    ''')
    
    conn.commit()
    conn.close()