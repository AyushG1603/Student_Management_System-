import time
import ingestion
import processor
import reporter

students = []
TOP_LIMIT = 8.5
LOW_LIMIT = 6.0


def show_menu():
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1.  Load students from CSV")
    print("2.  Load students from JSON")
    print("3.  Add student manually")
    print("4.  View all students")
    print("5.  Summary statistics")
    print("6.  Top performers")
    print("7.  Low CGPA students")
    print("8.  Group by Branch")
    print("9.  Group by Proctor")
    print("10. Search by Registration No")
    print("11. Save report as CSV")
    print("12. Save report as JSON")
    print("0.  Exit")


def ask_path(default):
    path = input("File path [" + default + "]: ").strip()
    if path == "":
        path = default
    return path


def has_data():
    if len(students) == 0:
        print("[WARNING] No students loaded yet")
        return False
    return True


def main():
    print("[INFO] Student Management System started")
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()
        start = time.time()

        if choice == "0":
            print("[INFO] Exiting. Goodbye!")
            break
        elif choice == "1":
            ingestion.read_csv(ask_path("data/students.csv"), students)
        elif choice == "2":
            ingestion.read_json(ask_path("data/students.json"), students)
        elif choice == "3":
            ingestion.add_manual(students)
        elif choice == "4":
            if has_data():
                reporter.print_table(students, "All Students")
        elif choice == "5":
            if has_data():
                reporter.print_summary(students, TOP_LIMIT, LOW_LIMIT)
        elif choice == "6":
            if has_data():
                top = processor.top_performers(students, TOP_LIMIT)
                reporter.print_table(top, "Top Performers (CGPA >= " + str(TOP_LIMIT) + ")")
        elif choice == "7":
            if has_data():
                low = processor.low_cgpa(students, LOW_LIMIT)
                reporter.print_table(low, "Low CGPA Students (CGPA < " + str(LOW_LIMIT) + ")")
        elif choice == "8":
            if has_data():
                reporter.print_groups(processor.group_by(students, "branch"), "Branch")
        elif choice == "9":
            if has_data():
                reporter.print_groups(processor.group_by(students, "proctor"), "Proctor")
        elif choice == "10":
            if has_data():
                reg_no = input("Enter Registration No: ").strip()
                found = processor.find_by_reg_no(students, reg_no)
                if found is None:
                    print("[WARNING] No student with Registration No " + reg_no)
                else:
                    reporter.print_table([found], "Search Result")
        elif choice == "11":
            if has_data():
                reporter.save_csv(students, "reports/report.csv", TOP_LIMIT, LOW_LIMIT)
        elif choice == "12":
            if has_data():
                reporter.save_json(students, "reports/report.json", TOP_LIMIT, LOW_LIMIT)
        else:
            print("[WARNING] Invalid choice, try again")
            continue

        elapsed = time.time() - start
        print("[INFO] Action finished in " + str(round(elapsed, 4)) + " seconds")


main()
