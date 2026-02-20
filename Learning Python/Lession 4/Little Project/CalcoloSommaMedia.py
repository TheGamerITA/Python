numeri = []
for i in range(5):
    numeri.append(int(input("Inserisci un numero: ")))

somma = 0
for i in range(len(numeri)):
    print(numeri[i])
    somma = somma + numeri[i]

print("La somma dei numeri è: ", somma)
print("La media dei numeri è: ", somma/len(numeri))
