"""
Questo programma è una semplice calcolatrice da riga di comando.
Funzionalità attuali:
- Operazioni supportate: Radice quadrata (radice), Addizione (+), Sottrazione (-), Moltiplicazione (*), Divisione (/).
- Validazione dell'input: Include controlli per assicurare che vengano inseriti numeri interi validi nelle operazioni a due numeri.
"""

print("Scegli l'operazione che desideri eseguire: ")
print("radice")
print("+")
print("-")
print("*")
print("/")

operazione = input("Inserisci qui l'operazione che desideri eseguire: ")

if operazione == "radice":
 # Funzione per richiedere un numero intero valido
    def get_int_input(prompt):
        while True:
            try:
                # Prova a convertire l'input in intero
                value = int(input(prompt))
                return value
            except ValueError:
                # Se fallisce, stampa un errore e richiedi l'input
                print("Errore: Per favore inserisci un numero intero valido.")
    a = get_int_input("Numero: ")
    radice = a ** 1/2
    print(radice)
       
else:
    # Funzione per richiedere un numero intero valido
    def get_int_input(prompt):
        while True:
            try:
                # Prova a convertire l'input in intero
                value = int(input(prompt))
                return value
            except ValueError:
                # Se fallisce, stampa un errore e richiedi l'input
                print("Errore: Per favore inserisci un numero intero valido.")

    # Utilizziamo la funzione per ottenere a e b
    a = get_int_input("Numero 1: ")
    b = get_int_input("Numero 2: ")
    if operazione == "+":
        risultato = a + b
        print(risultato)
    elif operazione == "-":
        risultato = a - b
        print(risultato)
    elif operazione == "*":
        risultato = a * b
        print(risultato)
    elif operazione == "/":
        if b != 0:
            risultato = a / b
            print(risultato)
        else:
            print("Error")

print("Success!")