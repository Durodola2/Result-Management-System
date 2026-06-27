# result_viewer.py
import tkinter as tk
from tkinter import messagebox
from result import get_results

class ResultViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Viewer")
        self.root.geometry("500x400")
        
        tk.Label(self.root, text="Student Result Viewer", font=("Arial", 16, "bold")).pack(pady=15)
        
        tk.Label(self.root, text="Enter Matric Number:", font=("Arial", 12)).pack(pady=5)
        self.matric_entry = tk.Entry(self.root, font=("Arial", 12))
        self.matric_entry.pack(pady=5)
        
        tk.Button(self.root, text="Fetch Results", font=("Arial", 12, "bold"),
                 command=self.show_results).pack(pady=10)
        
        self.result_box = tk.Text(self.root, height=15, width=55, font=("Arial", 11))
        self.result_box.pack(pady=10)
    
    def show_results(self):
        matric = self.matric_entry.get().strip()
        if not matric:
            messagebox.showwarning("Input Error", "Please enter a matric number.")
            return
        
        results = get_results(matric)
        self.result_box.delete(1.0, tk.END)
        
        if results:
            self.result_box.insert(tk.END, f"Results for {matric}:\n\n")
            for res in results:
                self.result_box.insert(tk.END, res + "\n")
        else:
            self.result_box.insert(tk.END, f"No results found for {matric}.")