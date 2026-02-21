def average_list(lista):
    sum(lista)
    len(lista)
    return sum(lista)/len(lista)

lista = []
for i in range(5):
    lista.append(int(input("Enter a number: ")))
print("The average of the list is: ",average_list(lista))