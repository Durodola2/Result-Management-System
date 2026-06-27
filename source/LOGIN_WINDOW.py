# login_window.py
import tkinter as tk
from tkinter import messagebox
from auth import signup, login
from database import initialize_db
from dashboard import open_dashboard
import sys

# Initialize database at start
initialize_db()

def open_login_window():
    def handle_login():
        matric = entry_matric.get().strip()
        password = entry_password.get().strip()
        
        if not matric or not password:
            messagebox.showwarning("Input Error", "Please enter matric number and password.")
            return
        
        user = login(matric, password)
        if user:
            matric, name, dept = user
            messagebox.showinfo("Login Success", f"Welcome {name} ({matric})!")
            login_win.destroy()
            open_dashboard(user)
        else:
            messagebox.showerror("Login Failed", "Invalid matric number or password.")
    
    login_win = tk.Toplevel(root)
    login_win.title("Login")
    login_win.geometry("300x200")
    
    tk.Label(login_win, text="Matric Number:").pack(pady=5)
    entry_matric = tk.Entry(login_win)
    entry_matric.pack(pady=5)
    
    tk.Label(login_win, text="Password:").pack(pady=5)
    entry_password = tk.Entry(login_win, show="*")
    entry_password.pack(pady=5)
    
    tk.Button(login_win, text="Login", command=handle_login, bg="green", fg="white").pack(pady=10)

def open_signup_window():
    def handle_signup():
        matric = entry_matric.get().strip()
        name = entry_name.get().strip()
        dept = entry_dept.get().strip()
        password = entry_password.get().strip()
        
        if not matric or not name or not dept or not password:
            messagebox.showwarning("Input Error", "All fields are required for signup.")
            return
        
        try:
            signup(matric, name, dept, password)
            messagebox.showinfo("Signup Success", f"User {name} registered successfully!")
            signup_win.destroy()
        except Exception as e:
            messagebox.showerror("Signup Error", f"Error: {e}")
    
    signup_win = tk.Toplevel(root)
    signup_win.title("Signup")
    signup_win.geometry("350x300")
    
    tk.Label(signup_win, text="Matric Number:").pack(pady=5)
    entry_matric = tk.Entry(signup_win)
    entry_matric.pack(pady=5)
    
    tk.Label(signup_win, text="Name:").pack(pady=5)
    entry_name = tk.Entry(signup_win)
    entry_name.pack(pady=5)
    
    tk.Label(signup_win, text="Department:").pack(pady=5)
    entry_dept = tk.Entry(signup_win)
    entry_dept.pack(pady=5)
    
    tk.Label(signup_win, text="Password:").pack(pady=5)
    entry_password = tk.Entry(signup_win, show="*")
    entry_password.pack(pady=5)
    
    tk.Button(signup_win, text="Signup", command=handle_signup, bg="blue", fg="white").pack(pady=10)

# Main window
root = tk.Tk()
root.title("Result Management System")
root.geometry("300x200")

tk.Label(root, text="Welcome to Result Management System", font=("Arial", 12, "bold")).pack(pady=20)
tk.Label(root, text="Select an option:", font=("Arial", 11)).pack(pady=10)

tk.Button(root, text="Login", command=open_login_window, width=15, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Signup", command=open_signup_window, width=15, bg="blue", fg="white").pack(pady=5)

if __name__ == "__main__":
    root.mainloop()