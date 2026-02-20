a = int(input("inserisci il voto: "))
if a < 0 or a > 10:
    print("Voto non valido")
elif a >= 6:
    print("Promosso")
else:
    print("Bocciato")