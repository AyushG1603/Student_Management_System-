def average_cgpa(students):
    if len(students) == 0:
        return 0.0
    total = 0.0
    for s in students:
        total += s["cgpa"]
    return total / len(students)


def highest_cgpa(students):
    best = students[0]
    for s in students:
        if s["cgpa"] > best["cgpa"]:
            best = s
    return best


def lowest_cgpa(students):
    worst = students[0]
    for s in students:
        if s["cgpa"] < worst["cgpa"]:
            worst = s
    return worst


def get_cgpa(student):
    return student["cgpa"]


def top_performers(students, limit):
    result = []
    for s in students:
        if s["cgpa"] >= limit:
            result.append(s)
    return sorted(result, key=get_cgpa, reverse=True)


def low_cgpa(students, limit):
    result = []
    for s in students:
        if s["cgpa"] < limit:
            result.append(s)
    return sorted(result, key=get_cgpa)


def group_by(students, key):
    groups = {}
    for s in students:
        name = s[key]
        if name not in groups:
            groups[name] = []
        groups[name].append(s)
    return groups


def find_by_reg_no(students, reg_no):
    for s in students:
        if s["reg_no"] == reg_no:
            return s
    return None


def get_status(cgpa, top_limit, low_limit):
    if cgpa >= top_limit:
        return "TOP"
    elif cgpa < low_limit:
        return "LOW"
    else:
        return "OK"
