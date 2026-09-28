# Student Record Management System

## About the Project

The **Student Record Management System** is a simple Python project made to manage student information easily. It allows the user to add students, update their marks, view their results, search for students, delete records, and check class performance.

The project uses a simple **GUI (Graphical User Interface)** made with Python's Tkinter library, so the user can perform different operations by clicking buttons instead of entering everything through the terminal.

## Features

The system provides the following features:

- Add a new student
- Search for a student
- Add or update student marks
- View a student's result card
- Delete a student record
- View class analytics
- Save student records
- Search students by name

## How It Works

When the program starts, the existing student records are loaded. The main window displays the available student records in a table.

The user can select a student and perform different operations such as adding marks, viewing the result, or deleting the record. New student details and updated marks are saved so that the information can be used again when the program is opened.

## Technologies Used

- **Python 3**
- **Tkinter** for the graphical user interface
- Python data structures and functions for managing student records

## Main Parts of the Project

The project is divided into different parts to keep the code organized.

### `srms_gui.py`

This file is responsible for creating the graphical interface. It contains the buttons, student table, search box, dialogs, and other GUI elements.

### `srms_core.py`

This file handles the main student record operations, such as adding, searching, updating marks, generating results, saving records, and deleting students.

Keeping the GUI and main logic separate makes the project easier to understand and maintain.

## How to Run

Make sure Python 3 is installed on your computer.

Then run:

```bash
python srms_gui.py
```

Tkinter is normally included with Python on Windows and macOS. On Linux, Tkinter may need to be installed separately.

## Conclusion

This project is a basic example of how Python can be used to create a small management system with a graphical interface. It is useful for learning concepts such as functions, classes, data handling, file storage, and Tkinter GUI programming.
