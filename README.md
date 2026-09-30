# Student Management System (CLI)

A simple command line program to load, validate, analyse and report student records.
Built with basic Python and only the standard library.

## Setup

1. Install Python 3.8 or newer.
2. Open a terminal inside the project folder.
3. Create and activate a virtual environment (optional, no packages are needed):

```
python -m venv venv
venv\Scripts\activate          (Windows)
source venv/bin/activate       (Linux / Mac)
```

4. Install requirements (nothing to install, kept for completeness):

```
pip install -r requirements.txt
```

## Running

```
python main.py
```

## Example Session

```
Enter choice: 1
File path [data/students.csv]:
[INFO] Loading CSV file: data/students.csv
[WARNING] Skipping bad row: CGPA is not a number -> {...}
[WARNING] Skipping bad row: empty field -> {...}
[WARNING] Skipping duplicate Reg No: 2021002
[INFO] Processed 10/10 rows
[INFO] Added 7 students, skipped 3
[INFO] Action finished in 0.0021 seconds
```

## Usage Guide

| Option | Action |
|--------|--------|
| 1 | Load students from a CSV file (columns: name, reg_no, cgpa, branch, proctor) |
| 2 | Load students from a JSON file (list of objects with the same keys) |
| 3 | Add one student by typing the details |
| 4 | Show all students in a table |
| 5 | Show summary: total, average, highest, lowest, top and low counts |
| 6 | Show top performers (CGPA >= 8.5) |
| 7 | Show low CGPA students (CGPA < 6.0) |
| 8 | Group by branch with count and average CGPA |
| 9 | Group by proctor with count and average CGPA |
| 10 | Search a student by registration number |
| 11 | Save report to `reports/report.csv` |
| 12 | Save report to `reports/report.json` |
| 0 | Exit |

Thresholds can be changed with `TOP_LIMIT` and `LOW_LIMIT` at the top of `main.py`.

## Validation Rules

- Name, registration number, branch and proctor cannot be empty.
- CGPA must be a number from 0 to 10.
- Registration numbers must be unique.
- Invalid rows are skipped with a warning and the program continues.

## Non-Technical Requirements

**Usability:** An interactive numbered menu with simple text prompts, default file paths
(press Enter to accept) and neatly formatted tables.

**Logging / Monitoring:** No `logging` module is used. Plain `print()` messages with tags
`[INFO]`, `[WARNING]` and `[ERROR]` show what the program is doing in real time, such as
file loading, skipped rows and saved reports.

**Scalability:** Rows are processed in batches of 100 (`BATCH_SIZE`) with progress messages,
and one bad row never stops the whole load.

**Performance:** Duplicate checking uses a dictionary lookup. Other operations use simple
loops. Every menu action is timed with `time.time()` and the duration is printed.

## Project Structure

```
main.py        menu and program flow
ingestion.py   Module 1: reading and validating data
processor.py   Module 2: calculations and filtering
reporter.py    Module 3: tables and report files
data/          sample input files
reports/       generated reports
```
