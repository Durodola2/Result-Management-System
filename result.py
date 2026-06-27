# result.py
import sqlite3
from database import DB_NAME

def save_result(matric, subject, score, total_questions, exam_type="Quiz"):
    """Save a student's result for a subject"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO results (matric, subject, score, total_questions, exam_type) VALUES (?, ?, ?, ?, ?)",
            (matric, subject, score, total_questions, exam_type)
        )
        conn.commit()
        print(f"Result saved: {matric} - {subject}: {score}/{total_questions}")
    except Exception as e:
        print(f"Error saving result: {e}")
    finally:
        conn.close()

def get_results(matric):
    """Fetch all results for a student"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT subject, score, total_questions, exam_type FROM results WHERE matric=?", (matric,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return []
    
    # Convert results into a clean list
    results = []
    for subject, score, total, exam_type in rows:
        percentage = round((score / total) * 100, 2) if total > 0 else 0
        results.append(f"{exam_type} - {subject}: {score}/{total} ({percentage}%)")
    
    return results