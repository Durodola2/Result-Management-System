# jamb_exam_window.py
import tkinter as tk
from tkinter import messagebox
import json
import random
from result import save_result

class JAMBExam:
    def __init__(self, root, username, selected_subjects):
        self.root = root
        self.root.title("JAMB Exam Mode")
        self.root.geometry("700x600")
        
        self.username = username
        self.selected_subjects = selected_subjects
        self.questions_by_subject = self.load_questions()
        
        if not self.questions_by_subject or not selected_subjects:
            messagebox.showerror("Error", "Failed to load questions or no subjects selected")
            self.root.destroy()
            return
            
        self.current_subject = selected_subjects[0]
        self.current_index = 0
        self.answers = {}
        self.timer_seconds = 40 * 60  # 40 minutes
        
        try:
            self.create_widgets()
            self.update_question()
            self.update_timer()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create exam interface: {e}")
            self.root.destroy()
    
    def load_questions(self):
        try:
            with open("jamb_questions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                questions = {}
                for subject in self.selected_subjects:
                    if subject in data:
                        subject_questions = data[subject][:10]
                        random.shuffle(subject_questions)
                        questions[subject] = subject_questions
                    else:
                        messagebox.showwarning("Warning", f"No questions found for {subject}")
                return questions
        except FileNotFoundError:
            messagebox.showerror("Error", "jamb_questions.json file not found!")
            return {}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {e}")
            return {}
    
    def create_widgets(self):
        # Welcome label
        welcome_label = tk.Label(self.root, text=f"Welcome, {self.username}!", font=("Arial", 14, "bold"))
        welcome_label.pack(pady=10)
        
        # Timer label
        self.timer_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red")
        self.timer_label.pack(pady=5)
        
        # Subject buttons
        self.subject_bar = tk.Frame(self.root)
        self.subject_bar.pack(pady=5)
        
        for sub in self.selected_subjects:
            btn = tk.Button(
                self.subject_bar, 
                text=sub, 
                command=lambda s=sub: self.switch_subject(s),
                font=("Arial", 10),
                padx=5
            )
            btn.pack(side="left", padx=2)
        
        # Subject and question labels
        self.subject_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"))
        self.subject_label.pack(pady=5)
        
        self.question_label = tk.Label(
            self.root, 
            text="", 
            font=("Arial", 12), 
            wraplength=650, 
            justify="left",
            height=3
        )
        self.question_label.pack(pady=10)
        
        # Radio buttons for options - NO PRESELECTION
        self.selected_option = tk.StringVar()
        self.selected_option.set("None")  # ✅ no option is selected initially

        
        self.option_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(
                self.root, 
                text="", 
                variable=self.selected_option,
                value=chr(65 + i),  # A, B, C, D
                font=("Arial", 11), 
                wraplength=600,
                command=self.save_answer,
                anchor="w"
            )
            btn.pack(anchor='w', padx=40, pady=2)
            self.option_buttons.append(btn)
        
        # Question navigation buttons
        self.question_nav_frame = tk.Frame(self.root)
        self.question_nav_frame.pack(pady=10)
        
        self.question_buttons = []
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(pady=10)
        
        self.prev_btn = tk.Button(
            nav_frame, 
            text="Previous", 
            command=self.prev_question,
            font=("Arial", 10)
        )
        self.prev_btn.grid(row=0, column=0, padx=10)
        
        self.next_btn = tk.Button(
            nav_frame, 
            text="Next", 
            command=self.next_question,
            font=("Arial", 10)
        )
        self.next_btn.grid(row=0, column=1, padx=10)
        
        # Submit button
        self.submit_btn = tk.Button(
            self.root, 
            text="Submit Exam", 
            command=self.submit_exam,
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white"
        )
        self.submit_btn.pack(pady=15)
        
        # Initialize question navigation
        self.update_question_buttons()
    
    def update_question_buttons(self):
        # Clear existing buttons
        for widget in self.question_nav_frame.winfo_children():
            widget.destroy()
        self.question_buttons.clear()
        
        # Create new buttons for current subject
        current_questions = self.questions_by_subject.get(self.current_subject, [])
        for i in range(len(current_questions)):
            btn = tk.Button(
                self.question_nav_frame, 
                text=f"Q{i+1}", 
                width=4,
                command=lambda idx=i: self.go_to_question(idx),
                font=("Arial", 9)
            )
            btn.grid(row=0, column=i, padx=1)
            self.question_buttons.append(btn)
    
    def update_question(self):
        questions_list = self.questions_by_subject.get(self.current_subject, [])
        
        if not questions_list or self.current_index >= len(questions_list):
            return
            
        question_data = questions_list[self.current_index]
        
        # Update subject and question labels
        self.subject_label.config(text=f"{self.current_subject} - Question {self.current_index + 1}")
        self.question_label.config(text=question_data["question"])
        
        # Update option buttons
        options = question_data.get("options", [])
        for i, option_btn in enumerate(self.option_buttons):
            if i < len(options):
                option_btn.config(text=f"{chr(65 + i)}. {options[i]}")
                option_btn.pack()
            else:
                option_btn.config(text="")
                option_btn.pack_forget()
        
        # CRITICAL FIX: Clear selection first, then restore saved answer
        key = (self.current_subject, self.current_index)
        saved_answer = self.answers.get(key, "")
        
        # Always clear first
        self.selected_option.set("")
        
        # Only set if there's a saved answer
        if saved_answer:
            self.selected_option.set(saved_answer)
        
        # Force UI refresh
        self.root.update_idletasks()
        
        # Update navigation buttons
        self.prev_btn.config(state="normal" if self.current_index > 0 else "disabled")
        self.next_btn.config(
            state="normal" if self.current_index < len(questions_list) - 1 else "disabled"
        )
    
    def save_answer(self):
        key = (self.current_subject, self.current_index)
        selected = self.selected_option.get()
        if selected:
            self.answers[key] = selected
    
    def prev_question(self):
        self.save_answer()
        if self.current_index > 0:
            self.current_index -= 1
            self.update_question()
    
    def next_question(self):
        self.save_answer()
        questions_list = self.questions_by_subject.get(self.current_subject, [])
        if self.current_index < len(questions_list) - 1:
            self.current_index += 1
            self.update_question()
    
    def go_to_question(self, index):
        self.save_answer()
        self.current_index = index
        self.update_question()
    
    def switch_subject(self, subject):
        self.save_answer()
        self.current_subject = subject
        self.current_index = 0
        self.update_question_buttons()
        self.update_question()
    
    def update_timer(self):
        if self.timer_seconds <= 0:
            self.submit_exam()
            return
            
        mins, secs = divmod(self.timer_seconds, 60)
        self.timer_label.config(text=f"Time Remaining: {mins:02d}:{secs:02d}")
        
        self.timer_seconds -= 1
        self.root.after(1000, self.update_timer)
    
    def submit_exam(self):
        self.save_answer()
        
        # Calculate scores
        total_score = 0
        subject_scores = {}
        
        for subject in self.selected_subjects:
            correct = 0
            total = 0
            questions = self.questions_by_subject.get(subject, [])
            
            for i, question in enumerate(questions):
                key = (subject, i)
                user_answer = self.answers.get(key, "")
                correct_answer = question.get("answer", "")
                
                total += 1
                if user_answer == correct_answer:
                    correct += 1
                    total_score += 1
            
            subject_scores[subject] = (correct, total)
        
        # Save results to database
        for subject, (correct, total) in subject_scores.items():
            if total > 0:
                save_result(self.username, subject, correct, total, "JAMB")
        
        # Show results
        total_questions = sum(scores[1] for scores in subject_scores.values())
        
        result_text = f"Exam Completed for {self.username}\n\n"
        result_text += f"Overall Score: {total_score} / {total_questions}\n"
        result_text += f"Percentage: {round((total_score/total_questions)*100, 1)}%\n\n"
        
        for subject, (correct, total) in subject_scores.items():
            if total > 0:
                percentage = round((correct / total) * 100, 1)
                result_text += f"{subject}: {correct}/{total} ({percentage}%)\n"
        
        messagebox.showinfo("Exam Results", result_text)
        self.root.destroy()