"""Student class and validation helpers."""
import re
from datetime import datetime

import results

ID_PATTERN = re.compile(r"^\d{2}/[A-Z]{2,5}\d{2}/\d{3}$")  


def is_valid_id(student_id):
    """Check Student ID format using a regular expression."""
    return bool(ID_PATTERN.match(student_id))


def is_valid_dob(dob):
    """Check that a date of birth is in YYYY-MM-DD format and not in the future."""
    try:
        date = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        return False
    return date <= datetime.now()


class Student:
    def __init__(self, student_id, name, form, gender, dob, scores=None, date_entered=None):
        self.student_id = student_id
        self.name = name
        self.form = form
        self.gender = gender
        self.dob = dob
        self.scores = scores if scores is not None else {}
        self.date_entered = date_entered  

    def set_scores(self, scores):
        """Store scores and record the date/time they were entered."""
        self.scores = scores
        self.date_entered = datetime.now().strftime("%Y-%m-%d %H:%M")

    def total(self):
        return results.calculate_total(self.scores)

    def average(self):
        return results.calculate_average(self.scores)

    def grade(self):
        return results.assign_grade(self.average())

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "form": self.form,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "date_entered": self.date_entered,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"], data["name"], data["form"], data["gender"],
            data["dob"], data.get("scores", {}), data.get("date_entered"),
        )

    def __str__(self):
        return f"{self.student_id:<10} {self.name:<25} {self.form:<8} {self.gender:<7} {self.dob}"
