# Define a function to get integer input with validation
def get_number(prompt):
    while True:
        try:
            number = float(input(prompt))
            return number
        except ValueError:
            print("Errore: Inserisci un numero valido.")

# Define a function to perform operations
def calculate():
    history = []
    while True:
        # Show the menu
        print("\n========================\n     PYTHON CALCULATOR\n========================\nOperazioni disponibili:")
        print("+  addizione")
        print("-  sottrazione")
        print("*  moltiplicazione")
        print("/  divisione")
        print("sqrt  radice quadrata")
        print("^  potenza")
        print("%  modulo/resto")
        print("abs  valore assoluto")
        print("square  quadrato")
        print("%  percentuale")
        print("log  logaritmo")
        print("sin  seno")
        print("cos  coseno")
        print("tan  tangente")
        print("history  cronologia")
        print("help  guida")
        print("exit  esci")
        print("clear  svuota la cronologia")
        
        operation = input("Scegli l'operazione: ")
        
        if operation == "exit" or operation == "q":
            break
        elif operation == "help":
            print("\nOperazioni disponibili:")
            print("+  addizione")
            print("-  sottrazione")
            print("*  moltiplicazione")
            print("/  divisione")
            print("sqrt  radice quadrata")
            print("^  potenza")
            print("%  modulo/resto")
            print("abs  valore assoluto")
            print("square  quadrato")
            print("%  percentuale")
            print("log  logaritmo")
            print("sin  seno")
            print("cos  coseno")
            print("tan  tangente")
            continue
        elif operation == "clear":
            history = []
            print("Cronologia svuotata.")
            continue
        elif operation == "history":
            if not history:
                print("Nessun calcolo effettuato.")
            else:
                for i, calc in enumerate(history):
                    print(f"{i+1}. {calc}")
            continue
        
        a = get_number("Inserisci il primo numero: ")
        if operation == "sqrt":
            if a < 0:
                print("Non puoi calcolare la radice quadrata di un numero negativo.")
                continue
        b = None
        if operation not in ["sin", "cos", "tan"]:
            b = get_number("Inserisci il secondo numero (opzionale): ")
        
        try:
            if operation == "+":
                result = a + b
            elif operation == "-":
                result = a - b
            elif operation == "*":
                result = a * b
            elif operation == "/":
                if b == 0:
                    print("Errore: divisione per zero non consentita.")
                    continue
                result = a / b
            elif operation == "^":
                result = a ** b
            elif operation == "%":
                result = a % b
            elif operation == "abs":
                result = abs(a)
            elif operation == "square":
                result = a * a
            elif operation == "log":
                if a <= 0:
                    print("Errore: il logaritmo non è definito per numeri non positivi.")
                    continue
                result = math.log(a)
            elif operation == "sin":
                result = math.sin(math.radians(a))
            elif operation == "cos":
                result = math.cos(math.radians(a))
            elif operation == "tan":
                if a % 180 == 90:
                    print("Errore: la tangente non è definita per questi angoli.")
                    continue
                result = math.tan(math.radians(a))
            else:
                print("Operazione non valida.")
                continue
            
            history.append(f"{a} {operation} {b if b is not None else ''} = {result}")
            print(f"Risultato: {result}")
        except Exception as e:
            print(f"Errore durante il calcolo: {e}")
        
        continue_calc = input("Vuoi fare un'altra operazione? (s/n): ")
        if continue_calc.lower() != "s":
            break

if __name__ == "__main__":
    calculate()