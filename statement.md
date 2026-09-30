# Project Statement: Student Management System

## 1. Problem Statement

Institutions keep student records in scattered files and spreadsheets. Checking marks,
finding weak students and preparing reports by hand is slow and error prone. This project
provides a command line tool that loads student records, validates them, calculates
statistics and generates reports.

## 2. Input Specification

Each student record has:

| Field | Type | Rule |
|-------|------|------|
| Student Name | string | not empty |
| Registration No | string | not empty, unique |
| CGPA | float | 0.0 to 10.0 |
| Branch | string | not empty (e.g. CSE, ECE, MECH) |
| Proctor Name | string | not empty |

Sources: CSV file, JSON file, or manual entry through the CLI.

## 3. Output Specification

- Console tables of students, top performers, low CGPA students and search results.
- Summary statistics: total, average, highest, lowest, top and low counts.
- Group reports by branch and by proctor (count and average CGPA).
- Saved files: `reports/report.csv` (with a status column TOP / OK / LOW) and
  `reports/report.json` (summary plus student list).
- Progress and error messages printed as `[INFO]`, `[WARNING]` and `[ERROR]`.

## 4. Functional Modules

**Module 1 - Data Input and Ingestion (`ingestion.py`):** Reads CSV and JSON files or manual
input, validates every field, rejects bad and duplicate rows and builds the list of valid
students, processing rows in batches.

**Module 2 - Processing Engine (`processor.py`):** Calculates average, highest and lowest
CGPA, filters top performers and low CGPA students, groups students by branch or proctor
and searches by registration number.

**Module 3 - Output and Report Generator (`reporter.py`):** Prints formatted text tables and
summaries to the terminal and saves reports to CSV and JSON files.

## 5. Logical Workflow

```
Input / Read  ->  Validation  ->  Calculation / Filtering  ->  Report Printing and Saving
```

1. The user picks a menu option in `main.py`.
2. Raw records are read from CSV, JSON or typed in.
3. Each record is validated; bad rows are skipped with a warning.
4. Valid students are stored in a list and processed (statistics, filters, groups).
5. Results are printed as tables and optionally saved to report files.
6. The time taken for each action is printed.
