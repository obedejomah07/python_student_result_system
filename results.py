"""Score calculation and grading logic."""

SUBJECTS = ["English", "Mathematics", "Physics", "Chemistry", "Biology"]


def calculate_total(scores):
    """Return the sum of all scores in a dict."""
    return sum(scores.values())


def calculate_average(scores):
    """Return the average score (0 if there are no scores)."""
    if not scores:
        return 0.0
    return calculate_total(scores) / len(scores)


def assign_grade(average):
    """Return a letter grade for an average score."""
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 40:
        return "D"
    else:
        return "F"


def class_statistics(students):
    """Return (highest, lowest, class_average) based on student averages.

    Returns None if no student has scores.
    """
    averages = [s.average() for s in students if s.scores]
    if not averages:
        return None
    return max(averages), min(averages), sum(averages) / len(averages)
