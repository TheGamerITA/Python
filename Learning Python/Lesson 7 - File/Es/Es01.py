with open("Learning Python/Lesson 7 - File/Es/note.txt", "a", encoding="utf-8") as f:
    text = input("Write here: ")  # prompt the user to enter some text
    if text.strip() == "": #Verify if the text is empty or not
        print("Text is empty")
    else:
        f.write(text + "\n")  # write the text to the file and add a newline at the end
