import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Define students data (ID, Name, Coursework Marks, Exam Mark)
students = [
    (1345, "John Curry", [8, 15, 7], 45),
    (2345, "Sam Sturtivant", [14, 15, 14], 77),
    (9876, "Lee Scott", [17, 11, 16], 99),
    (3724, "Matt Thompson", [19, 11, 15], 81),
    (1212, "Ron Herrema", [14, 17, 18], 66),
    (8439, "Jake Hobbs", [10, 11, 10], 43),
    (2344, "Jo Hyde", [6, 15, 10], 55),
    (9384, "Gareth Southgate", [5, 6, 8], 33),
    (8327, "Alan Shearer", [20, 20, 20], 100),
    (2983, "Les Ferdinand", [15, 17, 18], 92),
]

def calculate_metrics(student):
    """Calculate total marks, percentage, and grade for a student."""
    coursework_total = sum(student[2])  # Sum of coursework marks
    total_marks = coursework_total + student[3]  # Adding exam mark
    percentage = (total_marks / 160) * 100  # Calculate percentage

    # Determine grade based on percentage
    if percentage >= 70:
        grade = 'A'
    elif percentage >= 60:
        grade = 'B'
    elif percentage >= 50:
        grade = 'C'
    elif percentage >= 40:
        grade = 'D'
    else:
        grade = 'F'
    
    return coursework_total, total_marks, percentage, grade

def generate_report(student):
    """Generate a formatted string report for a single student."""
    coursework_total, total_marks, percentage, grade = calculate_metrics(student)
    return f"""
    Name: {student[1]}
    Student ID: {student[0]}
    Coursework Total: {coursework_total}
    Exam Mark: {student[3]}
    Overall Percentage: {percentage:.2f}%
    Grade: {grade}
    """

def display_all_students():
    """Display the information of all students."""
    report = ""
    total_percentage = 0
    for student in students:
        report += generate_report(student) + "\n\n"
        total_percentage += calculate_metrics(student)[2]

    average_percentage = total_percentage / len(students)
    report += f"\nSummary:\nTotal Students: {len(students)}\nAverage Percentage: {average_percentage:.2f}%"

    text_output.delete('1.0', tk.END)
    text_output.insert(tk.END, report)

def display_student_info():
    """Display information of a selected student."""
    selected_name = student_combo.get()
    for student in students:
        if student[1] == selected_name:
            report = generate_report(student)
            text_output.delete('1.0', tk.END)
            text_output.insert(tk.END, report)
            return
    messagebox.showerror("Error", "Student not found.")

def display_top_student():
    """Display the student with the highest marks."""
    top_student = max(students, key=lambda s: calculate_metrics(s)[1])
    report = generate_report(top_student)
    text_output.delete('1.0', tk.END)
    text_output.insert(tk.END, report)

def display_lowest_student():
    """Display the student with the lowest marks."""
    lowest_student = min(students, key=lambda s: calculate_metrics(s)[1])
    report = generate_report(lowest_student)
    text_output.delete('1.0', tk.END)
    text_output.insert(tk.END, report)

def sort_students(order="ascending"):
    """Sort and display students based on their total marks."""
    sorted_students = sorted(students, key=lambda s: calculate_metrics(s)[1], reverse=(order == "descending"))
    report = ""
    for student in sorted_students:
        report += generate_report(student) + "\n\n"
    
    text_output.delete('1.0', tk.END)
    text_output.insert(tk.END, report)

def add_student():
    """Open a window to add a new student."""
    def save_student():
        """Save the new student data."""
        try:
            student_id = int(entry_id.get())
            name = entry_name.get()
            coursework = [int(entry_coursework_1.get()), int(entry_coursework_2.get()), int(entry_coursework_3.get())]
            exam = int(entry_exam.get())
            if not name or any(mark < 0 or mark > 20 for mark in coursework) or not (0 <= exam <= 100):
                raise ValueError("Invalid data entered.")
            students.append((student_id, name, coursework, exam))
            student_combo['values'] = [s[1] for s in students]
            messagebox.showinfo("Success", "Student added successfully!")
            add_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    # Add student window setup
    add_window = tk.Toplevel(root)
    add_window.title("Add Student")
    add_window.geometry("400x300")

    tk.Label(add_window, text="Student ID:", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="w")
    entry_id = tk.Entry(add_window, font=("Arial", 12))
    entry_id.grid(row=0, column=1, pady=5)

    tk.Label(add_window, text="Name:", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
    entry_name = tk.Entry(add_window, font=("Arial", 12))
    entry_name.grid(row=1, column=1, pady=5)

    tk.Label(add_window, text="Coursework Marks (out of 20 each):", font=("Arial", 12)).grid(row=2, column=0, columnspan=2)
    entry_coursework_1 = tk.Entry(add_window, font=("Arial", 12), width=5)
    entry_coursework_2 = tk.Entry(add_window, font=("Arial", 12), width=5)
    entry_coursework_3 = tk.Entry(add_window, font=("Arial", 12), width=5)
    entry_coursework_1.grid(row=3, column=0, pady=5)
    entry_coursework_2.grid(row=3, column=1, pady=5)
    entry_coursework_3.grid(row=3, column=2, pady=5)

    tk.Label(add_window, text="Exam Mark (out of 100):", font=("Arial", 12)).grid(row=4, column=0, pady=5, sticky="w")
    entry_exam = tk.Entry(add_window, font=("Arial", 12))
    entry_exam.grid(row=4, column=1, pady=5)

    tk.Button(add_window, text="Save", command=save_student, font=("Arial", 12)).grid(row=5, column=0, columnspan=3, pady=10)

def delete_student():
    """Delete a student from the records."""
    selected_name = student_combo.get()
    global students
    students = [s for s in students if s[1] != selected_name]
    student_combo['values'] = [s[1] for s in students]
    messagebox.showinfo("Success", f"Student '{selected_name}' deleted successfully!")

def update_student():
    """Open a window to update a student's record."""
    def save_update():
        """Save the updated student data."""
        try:
            coursework = [int(entry_coursework_1.get()), int(entry_coursework_2.get()), int(entry_coursework_3.get())]
            exam = int(entry_exam.get())
            if any(mark < 0 or mark > 20 for mark in coursework) or not (0 <= exam <= 100):
                raise ValueError("Invalid data entered.")
            
            # Update the global students list
            for i, student in enumerate(students):
                if student[1] == selected_name:
                    students[i] = (student[0], student[1], coursework, exam)
                    break

            messagebox.showinfo("Success", "Student record updated successfully!")
            update_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    selected_name = student_combo.get()
    for student in students:
        if student[1] == selected_name:
            update_window = tk.Toplevel(root)
            update_window.title("Update Student")
            update_window.geometry("400x300")

            tk.Label(update_window, text=f"Updating: {student[1]}", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)

            # Display current coursework and exam marks
            tk.Label(update_window, text="Coursework Marks (out of 20 each):", font=("Arial", 12)).grid(row=1, column=0, columnspan=2)
            entry_coursework_1 = tk.Entry(update_window, font=("Arial", 12), width=5)
            entry_coursework_1.insert(0, student[2][0])
            entry_coursework_1.grid(row=2, column=0, pady=5)

            entry_coursework_2 = tk.Entry(update_window, font=("Arial", 12), width=5)
            entry_coursework_2.insert(0, student[2][1])
            entry_coursework_2.grid(row=2, column=1, pady=5)

            entry_coursework_3 = tk.Entry(update_window, font=("Arial", 12), width=5)
            entry_coursework_3.insert(0, student[2][2])
            entry_coursework_3.grid(row=2, column=2, pady=5)

            tk.Label(update_window, text="Exam Mark (out of 100):", font=("Arial", 12)).grid(row=3, column=0, pady=5, sticky="w")
            entry_exam = tk.Entry(update_window, font=("Arial", 12))
            entry_exam.insert(0, student[3])
            entry_exam.grid(row=3, column=1, pady=5)

            tk.Button(update_window, text="Save", command=save_update, font=("Arial", 12)).grid(row=4, column=0, columnspan=3, pady=10)
            return

    messagebox.showerror("Error", "Student not found.")


# Create the main application window
root = tk.Tk()
root.title("Student Management System")
root.geometry("800x600")
root.config(bg="#f4f4f4")

# Title Label
title_label = tk.Label(root, text="Student Management System", font=("Arial", 18, "bold"), bg="#4DCCBD", fg="#ffffff", pady=10)
title_label.pack(fill="x")

# Frame for buttons and combo box
control_frame = tk.Frame(root, bg="#ffffff")
control_frame.pack(pady=10, padx=20)

# Buttons for the menu
btn_show_all = tk.Button(control_frame, text="Show All Students", command=display_all_students, font=("Arial", 12), bg="#4DCCBD", fg="white", relief="raised", width=18)
btn_show_all.grid(row=0, column=0, padx=10, pady=5)

btn_top_student = tk.Button(control_frame, text="Top Student", command=display_top_student, font=("Arial", 12), bg="#4DCCBD", fg="white", relief="raised", width=18)
btn_top_student.grid(row=0, column=1, padx=10, pady=5)

btn_lowest_student = tk.Button(control_frame, text="Lowest Student", command=display_lowest_student, font=("Arial", 12), bg="#4DCCBD", fg="white", relief="raised", width=18)
btn_lowest_student.grid(row=0, column=2, padx=10, pady=5)

btn_sort_asc = tk.Button(control_frame, text="Sort Ascending", command=lambda: sort_students(order="ascending"), font=("Arial", 12), bg="#4DCCBD", fg="white", relief="raised", width=18)
btn_sort_asc.grid(row=1, column=0, padx=10, pady=5)

btn_sort_desc = tk.Button(control_frame, text="Sort Descending", command=lambda: sort_students(order="descending"), font=("Arial", 12), bg="#4DCCBD", fg="white", relief="raised", width=18)
btn_sort_desc.grid(row=1, column=1, padx=10, pady=5)

btn_add_student = tk.Button(control_frame, text="Add Student", command=add_student, font=("Arial", 12), bg="#4DCCBD", fg="white", relief="raised", width=18)
btn_add_student.grid(row=1, column=2, padx=10, pady=5)

btn_delete_student = tk.Button(control_frame, text="Delete Student", command=delete_student, font=("Arial", 12), bg="#4DCCBD", fg="white", relief="raised", width=18)
btn_delete_student.grid(row=2, column=0, padx=10, pady=5)

btn_update_student = tk.Button(control_frame, text="Update Student", command=update_student, font=("Arial", 12), bg="#4DCCBD", fg="white", relief="raised", width=18)
btn_update_student.grid(row=2, column=1, padx=10, pady=5)

student_combo = ttk.Combobox(control_frame, values=[s[1] for s in students], font=("Arial", 12))
student_combo.grid(row=2, column=2, padx=10, pady=5)
student_combo.set("Select Student")

btn_show_individual = tk.Button(control_frame, text="Show Individual Student", command=display_student_info, font=("Arial", 12), bg="#4DCCBD", fg="white", relief="raised", width=54)
btn_show_individual.grid(row=3, column=0, columnspan=3, pady=10)

# Text output area for displaying student information
text_output = tk.Text(root, wrap=tk.WORD, height=20, width=80, font=("Arial", 12), bg="#f4f4f4")
text_output.pack(pady=10, padx=20)

root.mainloop()


