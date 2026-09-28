import tkinter as tk
from tkinter import ttk, messagebox

from srms_core import (
    load_students,
    save_students,
    add_student,
    search_by_roll_no,
    search_by_name,
    update_marks,
    generate_result,
    class_analytics,
    delete_student,
)


class StudentApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Student Record Management System")
        self.geometry("950x560")
        self.minsize(800, 480)

        self.students = load_students()

        self.make_toolbar()
        self.make_table()
        self.make_status_bar()

        self.refresh_table()

        self.protocol("WM_DELETE_WINDOW", self.close_program)

    def make_toolbar(self):
        toolbar = ttk.Frame(self, padding=8)
        toolbar.pack(fill="x")

        ttk.Button(toolbar, text="Add Student", command=self.add_student_window).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Update / Add Marks", command=self.marks_window).pack(side="left", padx=4)
        ttk.Button(toolbar, text="View Result Card", command=self.result_window).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Delete Student", command=self.delete_student).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Class Analytics", command=self.show_analytics).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Save", command=self.save_records).pack(side="left", padx=4)

        ttk.Label(toolbar, text="Search:").pack(side="left", padx=(24, 4))

        self.search_text = tk.StringVar()
        search_box = ttk.Entry(toolbar, textvariable=self.search_text, width=25)
        search_box.pack(side="left")
        search_box.bind("<KeyRelease>", lambda event: self.refresh_table())

        ttk.Button(toolbar, text="Clear", command=self.clear_search).pack(side="left", padx=4)

    def make_table(self):
        columns = ("roll", "name", "course", "average", "grade", "status")
        headings = {
            "roll": "Roll No",
            "name": "Name",
            "course": "Course",
            "average": "Avg",
            "grade": "Grade",
            "status": "Status",
        }

        frame = ttk.Frame(self, padding=(8, 0, 8, 8))
        frame.pack(fill="both", expand=True)

        self.table = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")

        for col in columns:
            self.table.heading(col, text=headings[col])
            if col == "name" or col == "course":
                w = 200
            else:
                w = 100
            self.table.column(col, width=w, anchor="w")

        self.table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def make_status_bar(self):
        self.status_text = tk.StringVar()
        status_bar = ttk.Label(self, textvariable=self.status_text, relief="sunken", anchor="w", padding=4)
        status_bar.pack(side="bottom", fill="x")
        self.set_status("Loaded " + str(len(self.students)) + " student record(s).")

    def set_status(self, message):
        self.status_text.set(message)

    def clear_search(self):
        self.search_text.set("")
        self.refresh_table()

    def refresh_table(self):
        self.table.delete(*self.table.get_children())

        search = self.search_text.get().strip()
        if search:
            students_to_show = search_by_name(self.students, search)
        else:
            students_to_show = self.students

        for student in students_to_show:
            self.table.insert(
                "",
                "end",
                iid=student.roll_no,
                values=(
                    student.roll_no,
                    student.name,
                    student.course,
                    student.average(),
                    student.grade(),
                    student.result_status(),
                ),
            )

    def get_selected_roll(self):
        selected = self.table.selection()
        if selected:
            return selected[0]
        return None

    def save_records(self):
        save_students(self.students)
        self.set_status("Saved " + str(len(self.students)) + " student record(s).")

    def close_program(self):
        self.save_records()
        self.destroy()

    def add_student_window(self):
        window = tk.Toplevel(self)
        window.title("Add Student")
        window.resizable(False, False)
        window.grab_set()

        fields = {}
        row = 0
        for name in ("Roll No", "Name", "Course"):
            ttk.Label(window, text=name + ":").grid(row=row, column=0, padx=8, pady=6, sticky="e")
            value = tk.StringVar()
            ttk.Entry(window, textvariable=value, width=30).grid(row=row, column=1, padx=8, pady=6)
            fields[name] = value
            row += 1

        def add():
            try:
                add_student(self.students, fields["Roll No"].get(), fields["Name"].get(), fields["Course"].get())
                self.save_records()
                self.refresh_table()
                self.set_status("Student added successfully.")
                window.destroy()
            except ValueError as error:
                messagebox.showerror("Error", str(error), parent=window)

        buttons = ttk.Frame(window)
        buttons.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(buttons, text="Add", command=add).pack(side="left", padx=6)
        ttk.Button(buttons, text="Cancel", command=window.destroy).pack(side="left", padx=6)

    def marks_window(self):
        window = tk.Toplevel(self)
        window.title("Update / Add Marks")
        window.resizable(False, False)
        window.grab_set()

        roll = tk.StringVar(value=self.get_selected_roll() or "")
        subject = tk.StringVar()
        score = tk.StringVar()

        fields = (("Roll No", roll), ("Subject", subject), ("Score (0-100)", score))
        row = 0
        for name, value in fields:
            ttk.Label(window, text=name + ":").grid(row=row, column=0, padx=8, pady=6, sticky="e")
            ttk.Entry(window, textvariable=value, width=30).grid(row=row, column=1, padx=8, pady=6)
            row += 1

        def update():
            try:
                marks = float(score.get())
                update_marks(self.students, roll.get(), subject.get(), marks)
                self.save_records()
                self.refresh_table()
                self.set_status("Marks updated successfully.")
                window.destroy()
            except ValueError as error:
                messagebox.showerror("Error", str(error), parent=window)

        buttons = ttk.Frame(window)
        buttons.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(buttons, text="Update", command=update).pack(side="left", padx=6)
        ttk.Button(buttons, text="Cancel", command=window.destroy).pack(side="left", padx=6)

    def result_window(self):
        roll = self.get_selected_roll()

        if not roll:
            messagebox.showinfo("Select a student", "Select a student row first, or enter a roll number.")
            roll = self.ask_roll_number()
            if not roll:
                return

        student = search_by_roll_no(self.students, roll)
        if not student:
            messagebox.showerror("Not found", "No student found with roll number '" + roll + "'.")
            return

        self.show_text_window("Result Card", generate_result(student))

    def ask_roll_number(self):
        window = tk.Toplevel(self)
        window.title("Enter Roll No")
        window.resizable(False, False)
        window.grab_set()

        roll = tk.StringVar()
        ttk.Label(window, text="Roll No:").grid(row=0, column=0, padx=8, pady=8)
        entry = ttk.Entry(window, textvariable=roll, width=25)
        entry.grid(row=0, column=1, padx=8, pady=8)
        entry.focus_set()

        answer = {"roll": None}

        def submit():
            answer["roll"] = roll.get().strip()
            window.destroy()

        ttk.Button(window, text="OK", command=submit).grid(row=1, column=0, columnspan=2, pady=8)
        window.bind("<Return>", lambda event: submit())

        self.wait_window(window)
        return answer["roll"]

    def delete_student(self):
        roll = self.get_selected_roll()
        if not roll:
            messagebox.showinfo("Select a student", "Select a student row first.")
            return

        confirm = messagebox.askyesno("Confirm delete", "Delete student '" + roll + "'?")
        if not confirm:
            return

        if delete_student(self.students, roll):
            self.save_records()
            self.refresh_table()
            self.set_status("Student deleted.")
        else:
            messagebox.showerror("Not found", "No student found with roll number '" + roll + "'.")

    def show_analytics(self):
        self.show_text_window("Class Analytics", class_analytics(self.students))

    def show_text_window(self, title, content):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("420x300")

        text_box = tk.Text(window, wrap="word", font=("Courier New", 10))
        text_box.insert("1.0", content)
        text_box.configure(state="disabled")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(window, text="Close", command=window.destroy).pack(pady=(0, 10))


def main():
    app = StudentApp()
    app.mainloop()


if __name__ == "__main__":
    main()
