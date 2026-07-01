a = int(input("Type the first number: "))
b = int(input("Type the second number: "))

print("summ")
print("subtraction")
print("division")
print("multiplication")
choose = input("Decide the operation: ")

if choose == "summ":
    print(a + b)
elif choose == "subtraction":
    print(a - b)
elif choose == "division":
    print(a / b)
elif choose == "multiplication":
    print(a * b)
else:
    print("Error")