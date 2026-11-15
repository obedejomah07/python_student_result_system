"""Report generation: report cards, class lists and text export."""
import os
from datetime import datetime

import results
from results import SUBJECTS

REPORT_DIR = "reports"


def report_card(student):
    """Return a formatted report card string for one student."""
    lines = [
        "=" * 44,
        "              STUDENT REPORT CARD",
        "=" * 44,
        f"ID     : {student.student_id}",
        f"Name   : {student.name}",
        f"Class  : {student.form}",
        f"Gender : {student.gender}",
        f"DOB    : {student.dob}",
        "-" * 44,
    ]
    if not student.scores:
        lines.append("No scores recorded yet.")
    else:
        for subject, score in student.scores.items():
            lines.append(f"{subject:<20} {score:>6.1f}")
        lines += [
            "-" * 44,
            f"Total   : {student.total():.1f}",
            f"Average : {student.average():.2f}",
            f"Grade   : {student.grade()}",
            f"Entered : {student.date_entered}",
        ]
    lines.append("=" * 44)
    return "\n".join(lines)


def sort_students(students, by="average"):
    """Sort a list of students by average (high to low) or by name (A-Z)."""
    if by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    return sorted(students, key=lambda s: s.average(), reverse=True)


def results_table(students):
    """Return a table of all students with total, average and grade."""
    lines = [f"{'Pos':<4}{'ID':<10}{'Name':<25}{'Total':>8}{'Average':>9}{'Grade':>7}", "-" * 63]
    for pos, s in enumerate(students, start=1):
        lines.append(f"{pos:<4}{s.student_id:<10}{s.name:<25}{s.total():>8.1f}{s.average():>9.2f}{s.grade():>7}")
    return "\n".join(lines)


def statistics_text(students):
    """Return class statistics as text."""
    stats = results.class_statistics(students)
    if stats is None:
        return "No scores available for statistics."
    highest, lowest, avg = stats
    return (f"Highest average : {highest:.2f}\n"
            f"Lowest average  : {lowest:.2f}\n"
            f"Class average   : {avg:.2f}")


def save_report(students):
    """Write a full class report to a text file and return its path."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(REPORT_DIR, f"class_report_{stamp}.txt")
    ranked = sort_students(students, "average")
    with open(path, "w") as f:
        f.write("CLASS RESULT REPORT\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M}\n\n")
        f.write(results_table(ranked) + "\n\n")
        f.write(statistics_text(students) + "\n")
    return path
