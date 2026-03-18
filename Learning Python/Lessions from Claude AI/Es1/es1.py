def calcolatrice(a, b, operazione):
    if operazione == "addizione":
        return a + b
    elif operazione == "sottrazione":
        return a - b
    elif operazione == "moltiplicazione":
        return a * b
    elif operazione == "divisione":
        if b!= 0:
            return a / b
        else:
            return "Error: Dividere per zero non è consentito."
    else:
        return "Errore: Operazione non valida"