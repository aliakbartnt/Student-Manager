# 🎓 Student Grade Management System

A command-line interface (CLI) student grade management system with bilingual support (English/Persian), auto-save, search, sorting, backup functionality, and complete data management.

================================================================================

## 📋 Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Add Student | Manual or auto-generated ID (S1, S2, ...) |
| 2 | Add Course | Manual or auto-generated ID (C1, C2, ...) |
| 3 | Set Grade | Record a grade for a student in a specific course |
| 4 | Edit Student | Change student name |
| 5 | Edit Course | Change course name |
| 6 | Delete Student | With confirmation prompt |
| 7 | Delete Course | Remove course and all associated grades |
| 8 | Show Student | Display full student information with grades |
| 9 | Show All Students | Display all students with their grades |
| 10 | Search | Case-insensitive student search by name |
| 11 | Sort | Sort students by grade average (ascending/descending) |
| 12 | Delete All Data | Double confirmation to prevent accidental deletion |
| 13 | Summary Report | Display statistics, student grades, and averages |
| 14 | Bilingual | Full English/Persian support with RTL |
| 15 | Auto-Save | Automatic JSON file storage with restore capability |
| 16 | Backup | Automatic timestamped backups on exit |
| 17 | Version Check | Validate file version compatibility with the app |
| 18 | Personalization | Show developer name, version, and timestamp |

================================================================================

## 🛠️ Technologies

- Python 3.8+
- colorama - Colored terminal output
- PyYAML - Message file management
- JSON - Data storage
- Standard Libraries - os, sys, json, yaml, re, shutil, time, datetime

================================================================================

## 📂 Project Structure

```txt
project/
│
├── main.py                     # Main application file
├── setup.py                    # Auto-install dependencies & run
├── requirements.txt            # Dependencies list
├── .gitignore                  # Git ignored files
├── README.md                   # This file
│
├── messages/                   # Message files folder
│   ├── message_en.yml          # English messages
│   └── message_fa.yml          # Persian messages
│
└── Storage/                    # Data storage folder
    ├── data.json               # Main data file
    └── backups/                # Backup folder
        ├── backup_20250705_143022.json
        ├── backup_20250705_151845.json
        └── ...
```
================================================================================

## 🚀 Installation & Run

Method 1: Using setup.py (Recommended)
    python setup.py

This will automatically:
    1. Install required dependencies
    2. Run main.py

Method 2: Direct Run
    pip install -r requirements.txt
    python main.py

================================================================================

## 🎮 How to Use

1. Select Language
   After starting, you'll be prompted to choose your language:
   Select language / انتخاب زبان (en/fa):

2. Select Mode
   Two main modes are available:
   - Manage (m) - Perform operations on data
   - Summary (s) - Display statistics and overview
   Do you want to manage data or just view summary? (m for manage, s for summary):

3. Select ID Mode
   - Manual (m) - User enters custom ID
   - Auto (a) - Program generates sequential IDs (S1, S2, ...)
   Do you want to enter IDs manually or auto-generate? (m/a):

### 4. Main Menu
After selecting the mode, the main menu appears:

```
===== MENU =====
1. Add Student
2. Add Course
3. Set Grade
4. Edit Student
5. Edit Course
6. Delete Student
7. Delete Course
8. Show Student
9. Show All Students
10. Search Student by Name
11. Sort Students by Average
12. Delete All Data
0. Exit
================
```

5. Exit
   When selecting option 0, you'll be asked if you want to create a backup before exiting.

6. exit Command
   At any input prompt, type exit to return to the main menu.

================================================================================

## 💾 Sample Workflow

### Adding a Student (Auto Mode)
```
===== MENU =====
1. Add Student
...
Enter your choice (number): 1
Enter student name (or 'exit' to cancel): Ali Ahmadi
Generated student ID: S1
✅ Student with ID 'S1' and name 'Ali Ahmadi' added.
```

### Adding a Course
```
Enter your choice (number): 2
Enter course name (or 'exit' to cancel): Mathematics
Generated course ID: C1
✅ Course with ID 'C1' and name 'Mathematics' added.
```

### Setting a Grade
```
Enter your choice (number): 3
--- List of Students ---
  S1: Ali Ahmadi
-------------------------
Enter student ID from the list above (or 'exit' to cancel): S1
✅ Selected student: Ali Ahmadi
--- List of Courses ---
  C1: Mathematics
------------------------
Enter course ID from the list above (or 'exit' to cancel): C1
✅ Selected course: Mathematics
Enter grade (number) (or 'exit' to cancel): 18.5
✅ Grade 18.5 for student 'Ali Ahmadi' in course 'Mathematics' recorded.
```

### Searching for a Student
```
Enter your choice (number): 10
Enter student name to search (or 'exit' to cancel): Ali
=== Search Results (1 found) ===
ID: S1, Name: Ali Ahmadi, Average: 18.50
```

### Sorting Students by Average
```
Enter your choice (number): 11
Sort ascending or descending? (a for ascending, d for descending) (or 'exit' to cancel): d
=== Students Sorted by Average (Descending (highest first)) ===
ID: S1, Name: Ali Ahmadi, Average: 18.50
ID: S2, Name: Ali Mohammadi, Average: 17.50
ID: S3, Name: Reza Karimi, Average: 0.00
```

================================================================================

## 📊 Sample Summary Report Output

```
========== SUMMARY REPORT ==========
Total Students: 3
Total Courses: 2

Student: Ali Ahmadi (ID: S1)
  - Mathematics: 18.5
  - Physics: 17.0
  Average: 17.75

Student: Ali Mohammadi (ID: S2)
  - Mathematics: 19.0
  Average: 19.00

Student: Reza Karimi (ID: S3)
  (No grades recorded)

Course: Mathematics (ID: C1) - Students with grades: 2
Course: Physics (ID: C2) - Students with grades: 1
=====================================
```

================================================================================

## 🗃️ Storage Format

### Sample `data.json` File

```json
{
  "students": {
    "s1": {
      "id": "S1",
      "name": "Ali Ahmadi",
      "grades": {
        "c1": 18.5,
        "c2": 17.0
      }
    },
    "s2": {
      "id": "S2",
      "name": "Ali Mohammadi",
      "grades": {
        "c1": 19.0
      }
    },
    "s3": {
      "id": "S3",
      "name": "Reza Karimi",
      "grades": {}
    }
  },
  "courses": {
    "c1": {
      "id": "C1",
      "name": "Mathematics"
    },
    "c2": {
      "id": "C2",
      "name": "Physics"
    }
  },
  "student_counter": 4,
  "course_counter": 3,
  "version": "2.0",
  "last_saved": 1783270878.0677762
}
```

### Sample Backup File

Backups are saved in `Storage/backups/` with timestamp format:

```txt
Storage/backups/
├── backup_20260115_143022.json
├── backup_20260115_151845.json
└── backup_20260120_091532.json
```

================================================================================

## 📝 Commands Summary

| Command | Description |
|---------|-------------|
| 1 | Add a new student |
| 2 | Add a new course |
| 3 | Record a grade for a student |
| 4 | Edit a student's name |
| 5 | Edit a course's name |
| 6 | Delete a student |
| 7 | Delete a course |
| 8 | View detailed information about a student |
| 9 | View all students with their grades |
| 10 | Search for students by name |
| 11 | Sort students by their grade average |
| 12 | Delete all data (double confirmation required) |
| 0 | Exit the program |
| exit | Return to main menu (at any input prompt) |

================================================================================

## 🔧 Error Handling

| Error | Solution |
|-------|----------|
| messages.yml missing | Program exits with error message |
| Corrupted data.json | Starts with empty data |
| Duplicate ID | Displays error and asks for new input |
| Invalid grade input | Displays error message |
| Version mismatch | Shows warning and asks for user confirmation |

================================================================================

## 👨‍💻 Developer
```txt
Name: aliakbartnt 
Version: 2.0
Discord: aliakbartnt#9612
Year: 2026
```
================================================================================

## 📜 License
```txt
This project is licensed under the MIT License.

MIT License

Copyright (c) 2026 aliakbartnt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```
================================================================================

## 📝 Important Notes

- Data is automatically saved in the Storage/ folder.
- Always backup your data before updating to a new version.
- In Auto mode, counters continue from the last existing ID.
- IDs are case-insensitive (S1 and s1 are treated the same).
- RTL control characters are used for proper Persian text display.
- Use the exit command at any prompt to return to the main menu.

================================================================================

## 🐛 Bug Reports

If you find a bug, please create an Issue on GitHub or contact the developer via email.

================================================================================

## ⭐ Support

If you like this project, please give it a ⭐ on GitHub!

================================================================================

Made with ❤️ by aliakbartnt
