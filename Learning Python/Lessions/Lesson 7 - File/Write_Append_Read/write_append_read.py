
#Write, use "w" for normal write
with open("Learning Python/Lesson 7 - File/Write/note.txt", "w", encoding = "utf-8") as f:
    f.write("Hello\n")
    f.write("Second line\n")

#Append, use "a" for add one or more line at the bottom
with open("Learning Python/Lesson 7 - File/Write/note.txt", "a", encoding = "utf-8") as f:
    f.write("This is added at the bottom\n")

#Read, use "r" for read the content of the file
#Read a file
with open("Learning Python/Lesson 7 - File/Write/note.txt", "r", encoding = "utf-8") as f:
    content = f.read()
print(content)

#Read line per line
with open("Learning Python/Lesson 7 - File/Write/note.txt", "r", encoding = "utf-8") as f:
    for line in f:
        print(line.strip())