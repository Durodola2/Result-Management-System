# test_jamb.py - Test window for JAMB exam
import tkinter as tk
from tkinter import messagebox
import json

# Sample test questions (in case JSON file isn't available)
TEST_QUESTIONS = {
    "Mathematics": [
        {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "B"},
        {"question": "What is 5 × 3?", "options": ["15", "20", "25", "10"], "answer": "A"},
        {"question": "What is 10 ÷ 2?", "options": ["3", "4", "5", "6"], "answer": "C"}
    ],
    "English": [
        {"question": "What is the plural of 'child'?", "options": ["Childs", "Children", "Childes", "Childer"], "answer": "B"},
        {"question": "Choose correct spelling:", "options": ["Recieve", "Receive", "Recive", "Receeve"], "answer": "B"},
        {"question": "What is a verb?", "options": ["Run", "Red", "House", "Happy"], "answer": "A"}
    ],
    "Biology": [
        {"question": "What pumps blood?", "options": ["Lungs", "Heart", "Liver", "Kidney"], "answer": "B"},
        {"question": "Smallest unit of life?", "options": ["Atom", "Cell", "Molecule", "Organ"], "answer": "B"},
        {"question": "Photosynthesis occurs in?", "options": ["Root", "Stem", "Leaf", "Flower"], "answer": "C"}
    ],
    "Chemistry": [
        {"question": "Chemical symbol for water?", "options": ["H2O", "O2", "HCl", "Na"], "answer": "A"},
        {"question": "Which gas for respiration?", "options": ["Nitrogen", "Oxygen", "CO2", "Hydrogen"], "answer": "B"},
        {"question": "Atomic number of oxygen?", "options": ["6", "8", "10", "12"], "answer": "B"}
    ]
}

class JAMBTestWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("JAMB Exam Test - Radio Button Selection")
        self.root.geometry("700x600")
        
        # Initialize with test data
        self.username = "Test User"
        self.selected_subjects = ["Mathematics", "English", "Biology"]
        self.questions_by_subject = {subj: TEST_QUESTIONS[subj] for subj in self.selected_subjects}
        self.current_subject = self.selected_subjects[0]
        self.current_index = 0
        self.answers = {}
        
        self.create_widgets()
        self.update_question()
    
    def create_widgets(self):
        # Title
        tk.Label(self.root, text="JAMB Exam - Testing Radio Button Selection", 
                font=("Arial", 14, "bold"), fg="blue").pack(pady=10)
        
        # Instructions
        instruction_text = "Test Instructions:\n• Navigate between questions\n• Select options - only one should be selectable\n• Previously answered questions should show your selection"
        tk.Label(self.root, text=instruction_text, font=("Arial", 10), 
                justify="left", bg="#ffffcc").pack(pady=5, padx=10, fill="x")
        
        # Subject buttons
        self.subject_bar = tk.Frame(self.root)
        self.subject_bar.pack(pady=5)
        
        for sub in self.selected_subjects:
            btn = tk.Button(self.subject_bar, text=sub, 
                          command=lambda s=sub: self.switch_subject(s),
                          font=("Arial", 10), padx=10, bg="#e0e0e0")
            btn.pack(side="left", padx=3)
        
        # Subject and question labels
        self.subject_label = tk.Label(self.root, text="", font=("Arial", 13, "bold"), fg="darkgreen")
        self.subject_label.pack(pady=5)
        
        self.question_label = tk.Label(self.root, text="", font=("Arial", 12), 
                                      wraplength=650, justify="left", height=2)
        self.question_label.pack(pady=10)
        
        # Radio buttons - THE KEY PART TO TEST
        tk.Label(self.root, text="Options (Select one):", font=("Arial", 11, "bold")).pack(anchor="w", padx=40)
        
        self.selected_option = tk.StringVar()
        self.selected_option.set("")  # NO PRE-SELECTION
        
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
                anchor="w",
                bg="#f9f9f9"
            )
            btn.pack(anchor='w', padx=50, pady=3, fill="x")
            self.option_buttons.append(btn)
        
        # Status label
        self.status_label = tk.Label(self.root, text="", font=("Arial", 10), fg="blue")
        self.status_label.pack(pady=5)
        
        # Question navigation
        self.question_nav_frame = tk.Frame(self.root)
        self.question_nav_frame.pack(pady=10)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(pady=10)
        
        tk.Button(nav_frame, text="◀ Previous", command=self.prev_question,
                 font=("Arial", 10), width=12).grid(row=0, column=0, padx=5)
        tk.Button(nav_frame, text="Next ▶", command=self.next_question,
                 font=("Arial", 10), width=12).grid(row=0, column=1, padx=5)
        
        # Clear answer button (for testing)
        tk.Button(self.root, text="Clear My Answer", command=self.clear_answer,
                 font=("Arial", 9), bg="orange", fg="white").pack(pady=5)
        
        # Show answers button
        tk.Button(self.root, text="Show All My Answers", command=self.show_answers,
                 font=("Arial", 10), bg="purple", fg="white").pack(pady=5)
        
        self.update_question_buttons()
    
    def update_question_buttons(self):
        for widget in self.question_nav_frame.winfo_children():
            widget.destroy()
        
        current_questions = self.questions_by_subject[self.current_subject]
        for i in range(len(current_questions)):
            key = (self.current_subject, i)
            answered = "✓" if key in self.answers else ""
            btn = tk.Button(
                self.question_nav_frame, 
                text=f"Q{i+1}{answered}", 
                width=5,
                command=lambda idx=i: self.go_to_question(idx),
                font=("Arial", 9),
                bg="lightgreen" if key in self.answers else "white"
            )
            btn.grid(row=0, column=i, padx=1)
    
    def update_question(self):
        questions_list = self.questions_by_subject[self.current_subject]
        question_data = questions_list[self.current_index]
        
        # Update labels
        self.subject_label.config(text=f"{self.current_subject} - Question {self.current_index + 1} of {len(questions_list)}")
        self.question_label.config(text=question_data["question"])
        
        # Update options
        options = question_data["options"]
        for i, option_btn in enumerate(self.option_buttons):
            if i < len(options):
                option_btn.config(text=f"{chr(65 + i)}. {options[i]}")
                option_btn.pack()
            else:
                option_btn.pack_forget()
        
        # CRITICAL: Clear selection first, then restore if saved
        key = (self.current_subject, self.current_index)
        saved_answer = self.answers.get(key, "")
        
        # Always clear first
        self.selected_option.set("")
        
        # Then restore if exists
        if saved_answer:
            self.selected_option.set(saved_answer)
            self.status_label.config(text=f"Your saved answer: {saved_answer}", fg="green")
        else:
            self.status_label.config(text="No answer selected yet", fg="red")
        
        # Force refresh
        self.root.update_idletasks()
        
        self.update_question_buttons()
    
    def save_answer(self):
        key = (self.current_subject, self.current_index)
        selected = self.selected_option.get()
        if selected:
            self.answers[key] = selected
            self.status_label.config(text=f"Saved answer: {selected}", fg="green")
            self.update_question_buttons()
    
    def clear_answer(self):
        key = (self.current_subject, self.current_index)
        if key in self.answers:
            del self.answers[key]
        self.selected_option.set("")
        self.status_label.config(text="Answer cleared", fg="orange")
        self.update_question_buttons()
    
    def prev_question(self):
        self.save_answer()
        if self.current_index > 0:
            self.current_index -= 1
            self.update_question()
    
    def next_question(self):
        self.save_answer()
        questions_list = self.questions_by_subject[self.current_subject]
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
    
    def show_answers(self):
        if not self.answers:
            messagebox.showinfo("Answers", "No answers saved yet!")
            return
        
        result = "Your Saved Answers:\n\n"
        for (subject, q_idx), answer in sorted(self.answers.items()):
            result += f"{subject} Q{q_idx+1}: {answer}\n"
        
        messagebox.showinfo("All Answers", result)

# Run the test window
if __name__ == "__main__":
    root = tk.Tk()
    app = JAMBTestWindow(root)
    root.mainloop()