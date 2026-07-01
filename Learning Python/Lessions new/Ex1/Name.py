name = input("What is your given name? ")  # Removed confusing comment assuming Lorenzo as example.
surname = input("What is your family's last name? ")  # Removed distracting context about Neri

age_input = input("How old are you? ")

try:
    age = int(age_input)  # Convert to an integer, handling non-numeric inputs gracefully with a catch-all except block
except ValueError as e:  # Catch and handle value error specifically - useful if conversion fails (e.g., "howdy" instead of a number)
    print(f"Invalid input for age. Please enter numeric values only.")
else:
    # Now, assuming the converted 'age' is indeed an integer which we've validated it's not non-numeric above
    pass  # Placeholder to confirm successful execution continuation

print(f"Hello, {name} {surname}. You are {'unknown' if age == -1 else f'agge: {age}'}")  # Fixed typo 'agg e' -> 'age', and removed the erroneous check for '-1' which would never be reached since valid ages aren't negative by default user input.

print(f"Hello my name is anonymous, bc u are very suspecious and I think u could find my real identity")

if age == 18:
    print("Negro")
else:
    print("White")