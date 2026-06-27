# dashboard.py
import tkinter as tk
from tkinter import messagebox
from jamb_exam_window import JAMBExam
from quiz_simulator import QuizSimulator
from result_viewer import ResultViewer
from course_manager import CourseManager

def open_dashboard(user):
    matric, name, dept = user
    
    dashboard = tk.Toplevel()
    dashboard.title("Dashboard")
    dashboard.geometry("400x400")
    
    tk.Label(dashboard, text=f"Welcome, {name}!", font=("Arial", 14)).pack(pady=20)
    
    # Quiz Simulator
    def open_quiz():
        quiz_window = tk.Toplevel(dashboard)
        QuizSimulator(quiz_window, matric)
    
    tk.Button(
        dashboard,
        text="Start Quiz",
        width=20,
        bg="purple",
        fg="white",
        command=open_quiz
    ).pack(pady=10)
    
    # JAMB Simulation
    def open_jamb_with_selection():
        subject_win = tk.Toplevel(dashboard)
        subject_win.title("Select JAMB Subjects")
        subject_win.geometry("350x400")
        
        tk.Label(subject_win, text=f"{name}, select 4 subjects:", font=("Arial", 12)).pack(pady=10)
        
        available_subjects = ["English", "Mathematics", "Biology", "Chemistry", "Physics",
                             "Government", "Literature", "Economics", "CRK", "Geography"]
        
        subject_vars = []
        for sub in available_subjects:
            var = tk.IntVar()
            cb = tk.Checkbutton(subject_win, text=sub, variable=var, font=("Arial", 11))
            cb.pack(anchor="w", padx=30)
            subject_vars.append((sub, var))
        
        def confirm_subjects():
            selected = [sub for sub, var in subject_vars if var.get() == 1]
            if len(selected) != 4:
                messagebox.showwarning("Invalid Selection", "Please select exactly 4 subjects.")
                return
            
            subject_win.destroy()
            JAMBExam(tk.Toplevel(dashboard), matric, selected)
        
        tk.Button(subject_win, text="Start Exam", command=confirm_subjects).pack(pady=15)
    
    tk.Button(
        dashboard,
        text="JAMB Simulation",
        width=20,
        bg="orange",
        fg="white",
        command=open_jamb_with_selection
    ).pack(pady=10)
    
    # Result Viewer
    tk.Button(
        dashboard,
        text="View Results",
        width=20,
        bg="blue",
        fg="white",
        command=lambda: ResultViewer(tk.Toplevel(dashboard))
    ).pack(pady=10)
    
    # Course Manager
    tk.Button(
        dashboard,
        text="Manage Courses",
        width=20,
        bg="teal",
        fg="white",
        command=lambda: CourseManager(tk.Toplevel(dashboard))
    ).pack(pady=10)
    
    # Logout
    tk.Button(
        dashboard,
        text="Logout",
        width=20,
        bg="red",
        fg="white",
        command=dashboard.destroy
    ).pack(pady=20)