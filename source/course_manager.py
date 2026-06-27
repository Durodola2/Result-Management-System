# course_manager.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import DB_NAME

class CourseManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Courses")
        self.root.geometry("500x400")
        
        tk.Label(root, text="Course Code:", font=("Arial", 12)).pack(pady=5)
        self.entry_code = tk.Entry(root, font=("Arial", 12))
        self.entry_code.pack(pady=5)
        
        tk.Label(root, text="Course Title:", font=("Arial", 12)).pack(pady=5)
        self.entry_title = tk.Entry(root, font=("Arial", 12))
        self.entry_title.pack(pady=5)
        
        tk.Button(root, text="➕ Add Course", bg="green", fg="white",
                 command=self.add_course).pack(pady=10)
        
        tk.Label(root, text="Available Courses:", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Listbox to display courses
        self.course_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 11))
        self.course_listbox.pack(pady=10)
        
        tk.Button(root, text="❌ Delete Selected", bg="red", fg="white",
                 command=self.delete_course).pack(pady=5)
        
        # Load courses initially
        self.load_courses()
    
    def connect_db(self):
        return sqlite3.connect(DB_NAME)
    
    def add_course(self):
        code = self.entry_code.get().strip().upper()
        title = self.entry_title.get().strip()
        
        if not code or not title:
            messagebox.showwarning("Input Error", "Both fields are required.")
            return
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                code TEXT PRIMARY KEY,
                title TEXT NOT NULL
            )
        """)
        
        try:
            cursor.execute("INSERT INTO courses (code, title) VALUES (?, ?)", (code, title))
            conn.commit()
            messagebox.showinfo("Success", f"Course {code} added.")
            self.entry_code.delete(0, tk.END)
            self.entry_title.delete(0, tk.END)
            self.load_courses()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"Course {code} already exists.")
        finally:
            conn.close()
    
    def load_courses(self):
        self.course_listbox.delete(0, tk.END)
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS courses (code TEXT PRIMARY KEY, title TEXT NOT NULL)")
        cursor.execute("SELECT code, title FROM courses ORDER BY code")
        
        for row in cursor.fetchall():
            self.course_listbox.insert(tk.END, f"{row[0]} - {row[1]}")
        
        conn.close()
    
    def delete_course(self):
        selection = self.course_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a course to delete.")
            return
        
        course_text = self.course_listbox.get(selection[0])
        course_code = course_text.split(" - ")[0]
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM courses WHERE code = ?", (course_code,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Deleted", f"Course {course_code} deleted.")
        self.load_courses()