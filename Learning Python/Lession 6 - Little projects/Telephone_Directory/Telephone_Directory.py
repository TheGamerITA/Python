Telephone_directory = {}

while True:
    print("\n1: Create a new contact")
    print("2: Search contact")
    print("3: Show all contacts")
    print("4: Delete contact")
    print("5: Close")

    Choose = input("Choose between 1 and 4: ").strip()

    if Choose == "1":
        name = input("Enter the name: ").strip()
        Phone_Number = input("Enter phone number: ")
        Telephone_directory[name] = Phone_Number
        print("Contact saved")

    elif Choose == "2":
        name = input("Enter the name: ").strip()
        Phone_Number = Telephone_directory.get(name)
        if Phone_Number is None: 
            print(" Contact not found")
        else:
            print("Phone Number: ", Phone_Number)

    elif Choose == "3":
        if len(Telephone_directory) == 0:
            print("Telephone directory is empty")
        else:
            for name, Phone_Number in Telephone_directory.items():
                print(name, "->", Phone_Number)
    
    elif Choose == "4":
        name = input("Enter the name to delete: ").strip()
        if name in Telephone_directory:
            del Telephone_directory[name]
            print("Contact deleted")
        else:
            print("Contact not found")

    elif Choose == "5":
        break

    else:
        print("This choose is not valid")