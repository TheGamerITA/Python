import numpy as np
import matplotlib.pyplot as plt

# Funzione
def f(x):
    return x**3 - 3*x

# Derivata approssimata
def derivata(x):
    h = 0.0001
    return (f(x + h) - f(x)) / h

# ========================
# INPUT UTENTE
# ========================

print("=== ANALISI FUNZIONE f(x) = x^3 - 3x ===")

x_input = float(input("Inserisci un valore di x: "))

inizio = float(input("Da dove vuoi iniziare l'intervallo? "))
fine = float(input("Fino a dove vuoi arrivare? "))

# ========================
# CALCOLO SINGOLO PUNTO
# ========================

val_f = f(x_input)
val_d = derivata(x_input)

print("\n--- RISULTATI NEL PUNTO ---")
print("f(x) =", round(val_f, 2))
print("f'(x) =", round(val_d, 2))

if val_d > 0:
    print("La funzione è crescente 📈")
elif val_d < 0:
    print("La funzione è decrescente 📉")
else:
    print("Possibile massimo o minimo!")

# ========================
# RICERCA MAX/MIN
# ========================

print("\n--- RICERCA MASSIMI E MINIMI ---")

xs = np.linspace(inizio, fine, 1000)

for i in range(1, len(xs) - 1):
    d1 = derivata(xs[i - 1])
    d2 = derivata(xs[i + 1])

    if d1 > 0 and d2 < 0:
        print("Massimo vicino a x =", round(xs[i], 2))

    if d1 < 0 and d2 > 0:
        print("Minimo vicino a x =", round(xs[i], 2))

# ========================
# GRAFICO
# ========================

plt.plot(xs, f(xs))
plt.axhline(0)
plt.grid(True)
plt.title("f(x) = x^3 - 3x")

# Evidenzio il punto inserito
plt.scatter(x_input, f(x_input))

plt.show()