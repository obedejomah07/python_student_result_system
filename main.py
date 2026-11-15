"""Student Result Management System - entry point and menu."""
import reports
import storage
from results import SUBJECTS
from student import Student, is_valid_dob, is_valid_id


def ask(prompt):
    return input(prompt).strip()


def find_student(students):
    """Ask for an ID and return the matching student (or None)."""
    sid = ask("Enter Student ID: ").upper()
    student = students.get(sid)
    if student is None:
        print("Student not found.")
    return student


def read_scores():
    """Prompt for a score in each subject, repeating until valid (0-100)."""
    scores = {}
    for subject in SUBJECTS:
        while True:
            try:
                score = float(ask(f"  {subject} score (0-100): "))
            except ValueError:
                print("  Please enter a number.")
                continue
            if 0 <= score <= 100:
                scores[subject] = score
                break
            print("  Score must be between 0 and 100.")
    return scores


# Student management 
def add_student(students):
    sid = ask("Student ID (e.g. 24/SCI01/001): ").upper()
    if not is_valid_id(sid):
        print("Invalid ID format. Use the form 24/SCI01/001.")
        return
    if sid in students:
        print("A student with that ID already exists.")
        return
    name = ask("Full name: ")
    form = ask("Class/Form: ")
    gender = ask("Gender (M/F): ").upper()
    dob = ask("Date of birth (YYYY-MM-DD): ")
    if not name or gender not in ("M", "F") or not is_valid_dob(dob):
        print("Invalid input. Student not added.")
        return
    students[sid] = Student(sid, name, form, gender, dob)
    print("Student added.")


def view_students(students):
    if not students:
        print("No students registered.")
        return
    print(f"{'ID':<10} {'Name':<25} {'Class':<8} {'Gender':<7} DOB")
    for s in students.values():
        print(s)


def search_students(students):
    term = ask("Search by ID or name: ").lower()
    found = [s for s in students.values() if term in s.student_id.lower() or term in s.name.lower()]
    if not found:
        print("No match found.")
    for s in found:
        print(s)


def update_student(students):
    s = find_student(students)
    if not s:
        return
    print("Press Enter to keep the current value.")
    s.name = ask(f"Name [{s.name}]: ") or s.name
    s.form = ask(f"Class [{s.form}]: ") or s.form
    gender = ask(f"Gender [{s.gender}]: ").upper()
    if gender in ("M", "F"):
        s.gender = gender
    dob = ask(f"DOB [{s.dob}]: ")
    if dob and is_valid_dob(dob):
        s.dob = dob
    elif dob:
        print("Invalid date ignored.")
    print("Student updated.")


def delete_student(students):
    s = find_student(students)
    if s and ask(f"Delete {s.name}? (y/n): ").lower() == "y":
        del students[s.student_id]
        print("Student deleted.")


# Scores 
def record_scores(students):
    s = find_student(students)
    if not s:
        return
    if s.scores:
        print("This student already has scores; they will be replaced.")
    s.set_scores(read_scores())
    print(f"Saved. Average {s.average():.2f}, Grade {s.grade()}")


def show_report_card(students):
    s = find_student(students)
    if s:
        print(reports.report_card(s))


# Reports 
def list_results(students):
    if not students:
        print("No students registered.")
        return
    choice = ask("Sort by (1) average or (2) name: ")
    ordered = reports.sort_students(list(students.values()), "name" if choice == "2" else "average")
    print(reports.results_table(ordered))


def show_statistics(students):
    print(reports.statistics_text(list(students.values())))


def export_report(students):
    path = reports.save_report(list(students.values()))
    print(f"Report saved to {path}")


MENU = """
===== STUDENT RESULT MANAGEMENT SYSTEM =====
 1. Add student            7. Update scores
 2. View all students      8. Show report card
 3. Search student         9. List results (sorted)
 4. Update student        10. Class statistics
 5. Delete student        11. Save text report
 6. Record scores          0. Save & exit
"""

ACTIONS = {
    "1": add_student, "2": view_students, "3": search_students,
    "4": update_student, "5": delete_student, "6": record_scores,
    "7": record_scores, "8": show_report_card, "9": list_results,
    "10": show_statistics, "11": export_report,
}


def main():
    students = storage.load_students()
    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        if choice == "0":
            if storage.save_students(students):
                print("Data saved. Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option.")
            continue
        try:
            action(students)
            storage.save_students(students)
        except (EOFError, KeyboardInterrupt):
            print("\nInterrupted. Saving and exiting.")
            storage.save_students(students)
            break
        except Exception as e: 
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
