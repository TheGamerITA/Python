"""
This program is a simple command-line calculator.
Current features:
- Supported operations: Square root (sqrt), addition (+), subtraction (-), multiplication (*), division (/).
- Input validation: Checks to ensure valid integer numbers are entered for two-number operations.
"""

print("Choose the operation you want to perform: ")
print("sqrt")
print("+")
print("-")
print("*")
print("/")

operation = input("Enter the operation you want to perform: ")

if operation == "sqrt":
    # Function to request a valid integer
    def get_int_input(prompt):
        while True:
            try:
                # Try to convert input to integer
                value = int(input(prompt))
                return value
            except ValueError:
                # If it fails, print an error and ask again
                print("Error: Please enter a valid integer.")
    a = get_int_input("Number: ")
    root = a ** (1/2)
    print(root)
       
else:
    # Function to request a valid integer
    def get_int_input(prompt):
        while True:
            try:
                # Try to convert input to integer
                value = int(input(prompt))
                return value
            except ValueError:
                # If it fails, print an error and ask again
                print("Error: Please enter a valid integer.")

    # Use the function to get a and b
    a = get_int_input("Number 1: ")
    b = get_int_input("Number 2: ")
    if operation == "+":
        result = a + b
        print(result)
    elif operation == "-":
        result = a - b
        print(result)
    elif operation == "*":
        result = a * b
        print(result)
    elif operation == "/":
        if b != 0:
            result = a / b
            print(result)
        else:
            print("Error")

print("Success!")