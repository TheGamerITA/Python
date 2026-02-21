students = []

while True:

    name = input("Enter student name (or 'stop' to exit): ").strip()

    if name == "stop":
        break

    grade = int(input("Enter student grade: ").strip())
    student = {
        "name": name,
        "grade": grade
    }

    students.append(student)

print("\nStudient list:")

total = 0
for student in students:
    print(student["name"], "-->", student["grade"])
    total += student["grade"]

if len(students) > 0:
    print("Avarage:", total / len(students))
else:
    print("No student entered")
