"""Load and save student data as JSON."""
import json
import os

from student import Student

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students():
    """Load students from the JSON file. Returns {} if file is missing or broken."""
    try:
        with open(DATA_FILE, "r") as f:
            raw = json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Warning: data file is corrupted. Starting with an empty record.")
        return {}
    else:
        return {item["student_id"]: Student.from_dict(item) for item in raw}


def save_students(students):
    """Save all students (dict of id -> Student) to the JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(DATA_FILE, "w") as f:
            json.dump([s.to_dict() for s in students.values()], f, indent=4)
    except OSError as e:
        print(f"Error saving data: {e}")
        return False
    return True
