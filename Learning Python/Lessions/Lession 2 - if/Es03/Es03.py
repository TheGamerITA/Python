a = int(input("Enter your vote: "))
if a < 0 or a > 10:
    print("Invalid vote")
elif a >= 6:
    print("Promoted")
else:
    print("Failed")