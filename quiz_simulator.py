# quiz_simulator.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import json
from result import save_result

class QuizSimulator:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Quiz Simulator")
        self.root.geometry("650x450")
        self.root.configure(bg="#f0f0f0")
        
        self.username = username
        self.subject = ""
        self.questions = []
        self.q_index = 0
        self.score = 0
        self.answers_review = []
        self.time_per_question = 20
        self.timer_id = None
        self.all_subjects = self.load_subjects()
        
        self.setup_start_screen()
    
    def load_subjects(self):
        try:
            with open("questions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception as e:
            messagebox.showwarning("Warning", f"Using default questions. Error: {e}")
        
        # Default questions if file not found/empty
        return {
            "Mathematics": [
                {"question": "What is 2 + 2?", "options": ["A. 3", "B. 4", "C. 5", "D. 6"], "answer": "B"},
                {"question": "What is 5 * 3?", "options": ["A. 15", "B. 20", "C. 25", "D. 10"], "answer": "A"}
            ],
            "English": [
                {"question": "Choose the correct spelling:", "options": ["A. Recieve", "B. Receive", "C. Recive", "D. Receeve"], "answer": "B"},
                {"question": "What is the synonym of 'Happy'?", "options": ["A. Angry", "B. Sad", "C. Joyful", "D. Weak"], "answer": "C"}
            ]
        }
    
    def setup_start_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text=f"Welcome, {self.username}!", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Select Subject", font=("Arial", 14)).pack(pady=10)
        
        self.subject_var = tk.StringVar()
        subjects = list(self.all_subjects.keys())
        
        if subjects:
            self.subject_var.set(subjects[0])
            self.subject_menu = tk.OptionMenu(self.root, self.subject_var, *subjects)
            self.subject_menu.config(width=20, font=("Arial", 12))
            self.subject_menu.pack(pady=5)
        else:
            tk.Label(self.root, text="No subjects available!", fg="red", font=("Arial", 12)).pack(pady=5)
        
        tk.Button(self.root, text="Start Quiz", font=("Arial", 12), command=self.start_quiz).pack(pady=20)
    
    def start_quiz(self):
        subject = self.subject_var.get().strip()
        if not subject:
            messagebox.showwarning("Missing Info", "Please select a subject.")
            return
        
        self.subject = subject
        self.questions = self.all_subjects[subject]
        self.q_index = 0
        self.score = 0
        self.answers_review = []
        
        self.load_question_screen()
    
    def load_question_screen(self):
        self.clear_screen()
        
        self.selected_option = tk.StringVar()
        self.selected_option.set(" ")
        
        self.timer_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red")
        self.timer_label.pack(pady=5)
        
        question_data = self.questions[self.q_index]
        
        tk.Label(
            self.root,
            text=f"Q{self.q_index + 1}: {question_data['question']}",
            font=("Arial", 14),
            wraplength=600
        ).pack(pady=10)
        
        self.radio_buttons = []
        for option in question_data['options']:
            rb = tk.Radiobutton(
                self.root,
                text=option,
                variable=self.selected_option,
                value=option[0],  # "A"/"B"/"C"/"D"
                font=("Arial", 12),
                anchor='w'
            )
            rb.pack(anchor='w', padx=20, pady=2)
            self.radio_buttons.append(rb)
        
        tk.Button(self.root, text="Next", font=("Arial", 12), command=self.next_question).pack(pady=20)
        
        self.remaining_time = self.time_per_question
        self.update_timer()
    
    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.remaining_time}s")
        
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.next_question(auto=True)
    
    def next_question(self, auto=False):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        selected = self.selected_option.get()
        question = self.questions[self.q_index]
        correct = question['answer']
        
        self.answers_review.append({
            'question': question['question'],
            'selected': selected if selected.strip() else "None",
            'correct': correct
        })
        
        if selected == correct:
            self.score += 1
        
        self.q_index += 1
        
        if self.q_index < len(self.questions):
            self.load_question_screen()
        else:
            self.show_result_screen()
    
    def show_result_screen(self):
        self.clear_screen()
        
        # Save result to database
        try:
            save_result(self.username, self.subject, self.score, len(self.questions), "Quiz")
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save result: {e}")
        
        tk.Label(self.root, text=f"Quiz Complete, {self.username}!", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Subject: {self.subject}", font=("Arial", 12)).pack()
        
        percentage = round((self.score / len(self.questions)) * 100, 2)
        tk.Label(self.root, text=f"Score: {self.score}/{len(self.questions)} ({percentage}%)", font=("Arial", 12)).pack(pady=10)
        
        tk.Label(self.root, text="Answer Review", font=("Arial", 13, "underline")).pack(pady=(10, 5))
        
        # Create a frame for the scrollable text area
        review_frame = tk.Frame(self.root)
        review_frame.pack(pady=5, padx=20, fill='both', expand=True)
        
        # Use ScrolledText widget for automatic scrollbars
        review = scrolledtext.ScrolledText(
            review_frame, 
            width=75, 
            height=15, 
            font=("Arial", 10),
            wrap=tk.WORD,  # Word wrapping
            state='normal'  # Allow editing temporarily
        )
        review.pack(fill='both', expand=True)
        
        # Add content to the text area
        for i, entry in enumerate(self.answers_review, 1):
            # Color code correct/incorrect answers
            if entry['selected'] == entry['correct']:
                status = "✓ CORRECT"
                color = "green"
            else:
                status = "✗ INCORRECT"
                color = "red"
            
            # Insert question and answer info
            review.insert(tk.END, f"Question {i}: {entry['question']}\n")
            review.insert(tk.END, f"Your Answer: {entry['selected']} | Correct Answer: {entry['correct']}\n")
            
            # Insert status with color
            start_pos = review.index(tk.INSERT)
            review.insert(tk.END, f"Status: {status}\n")
            end_pos = review.index(tk.INSERT)
            
            # Apply color to status line
            review.tag_add(f"status_{i}", f"{start_pos} linestart", f"{end_pos} lineend")
            review.tag_config(f"status_{i}", foreground=color, font=("Arial", 10, "bold"))
            
            review.insert(tk.END, "\n" + "-"*60 + "\n\n")
        
        # Make text area read-only after adding content
        review.config(state='disabled')
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            review.yview_scroll(int(-1*(event.delta/120)), "units")
        
        review.bind("<MouseWheel>", on_mousewheel)  # Windows
        review.bind("<Button-4>", lambda e: review.yview_scroll(-1, "units"))  # Linux
        review.bind("<Button-5>", lambda e: review.yview_scroll(1, "units"))   # Linux
        
        # Add restart button
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Restart Quiz", command=self.setup_start_screen, 
                 font=("Arial", 12), bg="green", fg="white").pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Close", command=self.root.destroy, 
                 font=("Arial", 12), bg="red", fg="white").pack(side='left', padx=5)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizSimulator(root, username="Guest")
    root.mainloop()