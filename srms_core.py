import json
import os

FILE_NAME = "students_data.json"


class Student:
    def __init__(self, roll_no, name, course, marks=None):
        self.roll_no = roll_no
        self.name = name
        self.course = course
        if marks == None:
            self.marks = {}
        else:
            self.marks = marks

    def average(self):
        if len(self.marks) == 0:
            return 0
        total = 0
        for m in self.marks.values():
            total = total + m
        return round(total / len(self.marks), 2)

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 40:
            return "D"
        else:
            return "F"

    def result_status(self):
        if len(self.marks) == 0:
            return "No marks"
        for subject in self.marks:
            if self.marks[subject] < 40:
                return "Fail"
        return "Pass"


def load_students():
    students = []
    if os.path.exists(FILE_NAME) == False:
        return students

    file = open(FILE_NAME, "r")
    try:
        data = json.load(file)
    except:
        file.close()
        return students
    file.close()

    for item in data:
        s = Student(item["roll_no"], item["name"], item["course"], item.get("marks", {}))
        students.append(s)

    return students


def save_students(students):
    data = []
    for s in students:
        data.append({
            "roll_no": s.roll_no,
            "name": s.name,
            "course": s.course,
            "marks": s.marks
        })

    file = open(FILE_NAME, "w")
    json.dump(data, file, indent=2)
    file.close()


def add_student(students, roll_no, name, course):
    roll_no = roll_no.strip()
    name = name.strip()
    course = course.strip()

    if roll_no == "" or name == "" or course == "":
        raise ValueError("Please fill in all fields.")

    existing = search_by_roll_no(students, roll_no)
    if existing != None:
        raise ValueError("Roll number already exists.")

    new_student = Student(roll_no, name, course)
    students.append(new_student)


def search_by_roll_no(students, roll_no):
    roll_no = roll_no.strip()
    for s in students:
        if s.roll_no == roll_no:
            return s
    return None


def search_by_name(students, text):
    text = text.strip().lower()
    if text == "":
        return students

    result = []
    for s in students:
        if text in s.name.lower():
            result.append(s)
    return result


def update_marks(students, roll_no, subject, marks):
    subject = subject.strip()
    if subject == "":
        raise ValueError("Subject can't be empty.")

    if marks < 0 or marks > 100:
        raise ValueError("Marks should be between 0 and 100.")

    student = search_by_roll_no(students, roll_no)
    if student == None:
        raise ValueError("Student not found.")

    student.marks[subject] = marks


def delete_student(students, roll_no):
    student = search_by_roll_no(students, roll_no)
    if student == None:
        return False
    students.remove(student)
    return True


def generate_result(student):
    text = "Roll No: " + student.roll_no + "\n"
    text += "Name: " + student.name + "\n"
    text += "Course: " + student.course + "\n\n"
    text += "Marks:\n"

    if len(student.marks) == 0:
        text += "  No marks yet\n"
    else:
        for subject in student.marks:
            text += "  " + subject + ": " + str(student.marks[subject]) + "\n"

    text += "\nAverage: " + str(student.average()) + "\n"
    text += "Grade: " + student.grade() + "\n"
    text += "Status: " + student.result_status()

    return text


def class_analytics(students):
    if len(students) == 0:
        return "No students yet."

    graded = []
    for s in students:
        if len(s.marks) > 0:
            graded.append(s)

    text = "Total students: " + str(len(students)) + "\n"

    if len(graded) == 0:
        text += "No marks recorded yet."
        return text

    total_avg = 0
    passed = 0
    failed = 0
    top_student = graded[0]

    for s in graded:
        total_avg += s.average()
        if s.result_status() == "Pass":
            passed += 1
        else:
            failed += 1
        if s.average() > top_student.average():
            top_student = s

    class_avg = round(total_avg / len(graded), 2)

    text += "Class average: " + str(class_avg) + "\n"
    text += "Passed: " + str(passed) + "\n"
    text += "Failed: " + str(failed) + "\n"
    text += "Top student: " + top_student.name + " (" + str(top_student.average()) + ")"

    return text
