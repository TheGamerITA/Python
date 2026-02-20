def media_lista(lista):
    sum(lista)
    len(lista)
    return sum(lista)/len(lista)

lista = []
for i in range(5):
    lista.append(int(input("Inserisci un numero: ")))
print("La media della lista e': ",media_lista(lista))