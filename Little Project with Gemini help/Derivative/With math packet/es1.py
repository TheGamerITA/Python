import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**3 - 3*x

def derivata(x):
    h = 0.0001
    return (f(x + h) - f(x)) /h

x0 = int(input("Inserisci il punto per calcolare la derivata: "))
print("Calcolo derivata f'(x) nel punto: ", x0)
print("f'(x) = ", round(derivata(x0), 4))
print()

valori_x = np.linspace(-3, 3, 1000)
massimo_trovato = False
minimo_trovato = False

for i in range(1, len(valori_x)-1):
    x_prima = valori_x[i - 1]
    x_dopo = valori_x[i + 1]
    x_corrente = valori_x[i]
    
    derivata_prima = derivata(x_prima)
    derivata_seconda = derivata(x_dopo)
    
    if derivata_prima > 0 and derivata_seconda < 0 and not massimo_trovato:
        print("Massimale trovato:")
        print("x = ", round(x_corrente, 2))
        print("f(x) = ", round(f(x_corrente), 2))
        massimo_trovato = True
    
    if derivata_prima < 0 and derivata_seconda > 0 and not minimo_trovato:
        print("Minimo trovato:")
        print("x = ", round(x_corrente, 2))
        print("f(x) = ", round(f(x_corrente), 2))
        minimo_trovato = True

plt.plot(valori_x, f(valori_x))
plt.grid(True)
plt.title("Grafico di: f(x) = x^3 - 3x")
plt.show()
