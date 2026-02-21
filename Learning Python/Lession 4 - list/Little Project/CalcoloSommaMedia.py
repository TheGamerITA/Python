numbers = []
for i in range(5):
    numbers.append(int(input("Enter a number: ")))

somma = 0
for i in range(len(numbers)):
    print(numbers[i])
    somma = somma + numbers[i]

print("The sum of the numbers is: ", somma)
print("the average of the numbers is: ", somma/len(numbers))
