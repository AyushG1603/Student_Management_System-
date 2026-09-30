import csv
import json

BATCH_SIZE = 100


def validate_student(name, reg_no, cgpa, branch, proctor):
    name = str(name or "").strip()
    reg_no = str(reg_no or "").strip()
    branch = str(branch or "").strip().upper()
    proctor = str(proctor or "").strip()

    if name == "" or reg_no == "" or branch == "" or proctor == "":
        return None, "empty field"
    try:
        cgpa = float(cgpa)
    except (ValueError, TypeError):
        return None, "CGPA is not a number"
    if cgpa < 0.0 or cgpa > 10.0:
        return None, "CGPA must be between 0 and 10"

    student = {
        "name": name,
        "reg_no": reg_no,
        "cgpa": cgpa,
        "branch": branch,
        "proctor": proctor,
    }
    return student, ""


def process_rows(rows, students):
    known = {}
    for s in students:
        known[s["reg_no"]] = True

    added = 0
    skipped = 0
    total = len(rows)

    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        for row in batch:
            if not isinstance(row, dict):
                print("[WARNING] Skipping bad row: not a record -> " + str(row))
                skipped += 1
                continue
            student, error = validate_student(
                row.get("name"), row.get("reg_no"), row.get("cgpa"),
                row.get("branch"), row.get("proctor"))
            if student is None:
                print("[WARNING] Skipping bad row: " + error + " -> " + str(row))
                skipped += 1
            elif student["reg_no"] in known:
                print("[WARNING] Skipping duplicate Reg No: " + student["reg_no"])
                skipped += 1
            else:
                students.append(student)
                known[student["reg_no"]] = True
                added += 1
        done = min(i + BATCH_SIZE, total)
        print("[INFO] Processed " + str(done) + "/" + str(total) + " rows")

    print("[INFO] Added " + str(added) + " students, skipped " + str(skipped))
    return added, skipped


def read_csv(path, students):
    print("[INFO] Loading CSV file: " + path)
    rows = []
    try:
        f = open(path, "r", newline="")
        reader = csv.DictReader(f)
        for r in reader:
            clean = {}
            for key in r:
                if key is not None:
                    clean[key.strip().lower()] = r[key]
            rows.append(clean)
        f.close()
    except FileNotFoundError:
        print("[ERROR] File not found: " + path)
        return
    except Exception as e:
        print("[ERROR] Could not read CSV: " + str(e))
        return
    process_rows(rows, students)


def read_json(path, students):
    print("[INFO] Loading JSON file: " + path)
    try:
        f = open(path, "r")
        data = json.load(f)
        f.close()
    except FileNotFoundError:
        print("[ERROR] File not found: " + path)
        return
    except json.JSONDecodeError:
        print("[ERROR] File is not valid JSON")
        return
    except Exception as e:
        print("[ERROR] Could not read JSON: " + str(e))
        return

    if not isinstance(data, list):
        print("[ERROR] JSON must contain a list of students")
        return
    process_rows(data, students)


def add_manual(students):
    name = input("Student Name: ")
    reg_no = input("Registration No: ")
    cgpa = input("CGPA (0-10): ")
    branch = input("Branch: ")
    proctor = input("Proctor Name: ")

    student, error = validate_student(name, reg_no, cgpa, branch, proctor)
    if student is None:
        print("[WARNING] Student not added: " + error)
        return False

    for s in students:
        if s["reg_no"] == student["reg_no"]:
            print("[WARNING] Registration No already exists")
            return False

    students.append(student)
    print("[INFO] Student added successfully")
    return True
