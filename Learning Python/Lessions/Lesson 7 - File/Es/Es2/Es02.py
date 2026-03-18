with open("Learning Python/Lesson 7 - File/Es/Es2/note.txt", "r", encoding="utf-8") as file:
    for index, line in enumerate(file, start=1):
        # print line number and content
        print(f"{index}: {line.rstrip()}")