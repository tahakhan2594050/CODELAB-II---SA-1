import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
import random

# Game state variables
difficulty = 1
score = 0
current_question = 0
total_questions = 10


def generate_number():
    """Generate a number based on difficulty level."""
    if difficulty == 1:
        return random.randint(1, 9)
    elif difficulty == 2:
        return random.randint(10, 99)
    return random.randint(1000, 9999)


def choose_operation():
    """Randomly select an operation: addition or subtraction."""
    return random.choice(["+", "-"])


def main_menu():
    """Display the main menu for selecting difficulty."""
    def select_difficulty(level):
        global difficulty
        difficulty = level
        menu.destroy()
        start_quiz()

    menu = tk.Tk()
    menu.title("Math Quiz")
    menu.geometry("500x500")
    menu.configure(bg="#6600CC")

    tk.Label(menu, text="🎯 Maths Quiz 🎯", font=("Segoe UI", 18, "bold"), fg="#FF00CC", bg="#6600CC").pack(pady=20)
    tk.Label(menu, text="Choose a Difficulty", font=("Segoe UI", 16), fg="#CC66CC", bg="#6600CC").pack(pady=10)

    difficulty_levels = ["Easy", "Moderate", "Advanced"]
    for i, level in enumerate(difficulty_levels, start=1):
        tk.Button(
            menu,
            text=f"{i}. {level}",
            font=("Segoe UI", 14),
            bg="#990099",
            fg="#FFFFFF",
            command=lambda lvl=i: select_difficulty(lvl),
            relief="flat",
            width=20,
        ).pack(pady=15)

    menu.mainloop()


def start_quiz():
    """Reset game state and begin quiz."""
    global score, current_question
    score = 0
    current_question = 1
    next_problem()


def next_problem():
    """Display a new math problem."""
    global current_question

    num1 = generate_number()
    num2 = generate_number()
    operation = choose_operation()

    if operation == "-" and num1 < num2:
        num1, num2 = num2, num1

    correct_answer = eval(f"{num1} {operation} {num2}")

    problem_window = tk.Tk()
    problem_window.title(f"Question {current_question}/{total_questions}")
    problem_window.geometry("500x400")
    problem_window.configure(bg="#FF99CC")

    progress_value = (current_question - 1) * (100 / total_questions)
    Progressbar(problem_window, orient=tk.HORIZONTAL, length=400, mode='determinate', value=progress_value).pack(pady=20)

    tk.Label(problem_window, text=f"Question {current_question}/{total_questions}", font=("Segoe UI", 16, "bold"), fg="#FF00FF", bg="#FF99CC").pack(pady=10)
    tk.Label(problem_window, text=f"{num1} {operation} {num2} = ?", font=("Segoe UI", 24, "bold"), fg="#FF00FF", bg="#FF99CC").pack(pady=20)

    answer_entry = tk.Entry(problem_window, font=("Segoe UI", 18), justify="center")
    answer_entry.pack(pady=10)

    attempts = 0

    def check_answer():
        """Evaluate the user's response and handle results."""
        nonlocal attempts
        attempts += 1
        try:
            user_answer = int(answer_entry.get())
            if user_answer == correct_answer:
                points = 10 if attempts == 1 else 5
                messagebox.showinfo("Correct!", f"You earned {points} points!")
                global score
                score += points
                problem_window.destroy()
                load_next_question()
            else:
                if attempts == 1:
                    messagebox.showwarning("Try Again", "Incorrect! Give it another shot.")
                    answer_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Wrong Answer", f"The correct answer was {correct_answer}.")
                    problem_window.destroy()
                    load_next_question()
        except ValueError:
            messagebox.showwarning("Error", "Enter a valid number.")

    tk.Button(problem_window, text="Submit", font=("Segoe UI", 14), bg="#FFCCFF", fg="#CC0099", command=check_answer, relief="flat").pack(pady=20)

    problem_window.mainloop()


def load_next_question():
    """Advance to the next question or finish the quiz."""
    global current_question
    if current_question < total_questions:
        current_question += 1
        next_problem()
    else:
        show_results()


def show_results():
    """Display the final score and ranking."""
    rank = "A+" if score > 90 else "A" if score > 75 else "B" if score > 50 else "C"

    results = tk.Tk()
    results.title("Results")
    results.geometry("500x400")
    results.configure(bg="#FFCCCC")

    tk.Label(results, text="🎉 Quiz Complete 🎉", font=("Segoe UI", 20, "bold"), fg="#FF3399", bg="#FFCCCC").pack(pady=20)
    tk.Label(results, text=f"Score: {score}/100", font=("Segoe UI", 16), fg="#FF3399", bg="#FFCCCC").pack(pady=10)
    tk.Label(results, text=f"Rank: {rank}", font=("Segoe UI", 16), fg="#FF3399", bg="#FFCCCC").pack(pady=10)

    button_width = 15  # Ensures both buttons have the same width

    tk.Button(
        results,
        text="Play Again",
        font=("Segoe UI", 14),
        bg="#FF3399",
        fg="white",
        width=button_width,
        command=lambda: [results.destroy(), main_menu()],
        relief="flat"
    ).pack(pady=10)

    tk.Button(
        results,
        text="Exit",
        font=("Segoe UI", 14),
        bg="#FF3399",
        fg="white",
        width=button_width,
        command=results.destroy,
        relief="flat"
    ).pack(pady=10)

    results.mainloop()


if __name__ == "__main__":
    main_menu()
