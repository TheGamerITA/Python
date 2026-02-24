#Save
def save_phonebook(phonebook, filename="phonebook.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for name, phone_number in phonebook.items():
            file.write(f"{name};{phone_number}\n")

#Load
def load_phonebook(filename="phonebook.txt"):
    phonebook = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue

                name, phone_number = line.split(";", 1)
                phonebook[name] = phone_number

    except FileNotFoundError:
        # If file does not exist, start with empty phonebook
        pass

    return phonebook

# Main program logic
# Loads existing data and presents a menu-driven interface to the user.
def main():
    phonebook = load_phonebook()

    while True:
        print("\n--- PHONE DIRECTORY ---")
        print("1. Add contact")
        print("2. Search contact")
        print("3. Show all contacts")
        print("4. Delete contact")
        print("5. Exit")

        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            # Add a new contact
            name = input("Enter name: ").strip()
            phone_number = input("Enter phone number: ").strip()

            phonebook[name] = phone_number
            save_phonebook(phonebook)  # persist changes to disk

            print("Contact saved successfully.")

        elif choice == "2":
            # Search for a contact by name
            name = input("Enter name to search: ").strip()
            phone_number = phonebook.get(name)

            if phone_number:
                print(f"{name} -> {phone_number}")
            else:
                print("Contact not found.")

        elif choice == "3":
            # Display all entries in the phonebook
            if not phonebook:
                print("Phone directory is empty.")
            else:
                for name, phone_number in phonebook.items():
                    print(f"{name} -> {phone_number}")

        elif choice == "4":
            # Remove a contact if it exists
            name = input("Enter name to delete: ").strip()

            if name in phonebook:
                del phonebook[name]
                save_phonebook(phonebook)  # update file after deletion
                print("Contact deleted.")
            else:
                print("Contact not found.")

        elif choice == "5":
            # Exit the application loop
            print("Goodbye!")
            break

        else:
            # Handle any unexpected menu selection
            print("Invalid choice.")


if __name__ == "__main__":
    main()