import csv
import json
import os
import processor


def print_table(students, title="Students"):
    print("\n" + title)
    line = "-" * 78
    print(line)
    print("{:<5}{:<22}{:<14}{:<8}{:<9}{:<20}".format(
        "No", "Name", "Reg No", "CGPA", "Branch", "Proctor"))
    print(line)
    if len(students) == 0:
        print("(no students to show)")
    count = 1
    for s in students:
        print("{:<5}{:<22}{:<14}{:<8.2f}{:<9}{:<20}".format(
            count, s["name"][:20], s["reg_no"][:12], s["cgpa"],
            s["branch"][:7], s["proctor"][:18]))
        count += 1
    print(line)
    print("Total: " + str(len(students)))


def print_summary(students, top_limit, low_limit):
    best = processor.highest_cgpa(students)
    worst = processor.lowest_cgpa(students)
    top = processor.top_performers(students, top_limit)
    low = processor.low_cgpa(students, low_limit)
    print("\n===== SUMMARY =====")
    print("Total students   : " + str(len(students)))
    print("Average CGPA     : " + str(round(processor.average_cgpa(students), 2)))
    print("Highest CGPA     : " + str(best["cgpa"]) + " (" + best["name"] + ")")
    print("Lowest CGPA      : " + str(worst["cgpa"]) + " (" + worst["name"] + ")")
    print("Top performers   : " + str(len(top)) + " (CGPA >= " + str(top_limit) + ")")
    print("Low CGPA flagged : " + str(len(low)) + " (CGPA < " + str(low_limit) + ")")


def print_groups(groups, label):
    print("\n===== STUDENTS BY " + label.upper() + " =====")
    print("{:<22}{:<10}{:<10}".format(label, "Count", "Avg CGPA"))
    print("-" * 42)
    for key in sorted(groups):
        members = groups[key]
        avg = processor.average_cgpa(members)
        print("{:<22}{:<10}{:<10.2f}".format(key[:20], len(members), avg))
    print("-" * 42)


def make_folder(path):
    folder = os.path.dirname(path)
    if folder != "":
        os.makedirs(folder, exist_ok=True)


def save_csv(students, path, top_limit, low_limit):
    print("[INFO] Saving CSV report to " + path)
    try:
        make_folder(path)
        f = open(path, "w", newline="")
        writer = csv.writer(f)
        writer.writerow(["name", "reg_no", "cgpa", "branch", "proctor", "status"])
        for s in students:
            status = processor.get_status(s["cgpa"], top_limit, low_limit)
            writer.writerow([s["name"], s["reg_no"], s["cgpa"], s["branch"], s["proctor"], status])
        f.close()
        print("[INFO] CSV report saved")
    except Exception as e:
        print("[ERROR] Could not save CSV: " + str(e))


def save_json(students, path, top_limit, low_limit):
    print("[INFO] Saving JSON report to " + path)
    rows = []
    for s in students:
        row = dict(s)
        row["status"] = processor.get_status(s["cgpa"], top_limit, low_limit)
        rows.append(row)

    groups = processor.group_by(students, "branch")
    branch_avg = {}
    for key in groups:
        branch_avg[key] = round(processor.average_cgpa(groups[key]), 2)

    report = {
        "summary": {
            "total_students": len(students),
            "average_cgpa": round(processor.average_cgpa(students), 2),
            "top_performers": len(processor.top_performers(students, top_limit)),
            "low_cgpa_students": len(processor.low_cgpa(students, low_limit)),
            "average_cgpa_by_branch": branch_avg,
        },
        "students": rows,
    }
    try:
        make_folder(path)
        f = open(path, "w")
        json.dump(report, f, indent=4)
        f.close()
        print("[INFO] JSON report saved")
    except Exception as e:
        print("[ERROR] Could not save JSON: " + str(e))
