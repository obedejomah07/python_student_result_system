# Student Result Management System

A menu-driven Python application for managing student records and results.

## Features
- Add, view, search, update and delete students (ID validated with regex)
- Record scores for 5 subjects; total, average and grade (A–F) calculated automatically
- Report cards, sorted result lists (by average or name), class statistics
- Export a text report to `reports/`
- Data saved to `data/students.json` and loaded on start (works if file is missing)

## Run
Requires Python 3.8+ (no external packages).

```
python main.py
```

## Structure
| File | Purpose |
|------|---------|
| `main.py` | Menu and user input |
| `student.py` | `Student` class, ID/date validation |
| `results.py` | Totals, averages, grading, class stats |
| `storage.py` | JSON load/save |
| `reports.py` | Report card, tables, text export |

## Grading
A ≥ 70 · B ≥ 60 · C ≥ 50 · D ≥ 40 · F < 40
