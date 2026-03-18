# Derivata: f'(x) = ( f(x+h) - f(x) ) / h

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**3 - 3*x

def derivata(x):
    h = 0.0001
    return (f(x + h) - f(x)) / h

xs = np.linspace(-3, 3, 1000)

# Cerca massimi e minimi: dove f' cambia segno
for i in range(1, len(xs) - 1):
    if derivata(xs[i-1]) > 0 and derivata(xs[i+1]) < 0:
        print(f"MASSIMO: x={xs[i]:.2f}  f(x)={f(xs[i]):.2f}")
    if derivata(xs[i-1]) < 0 and derivata(xs[i+1]) > 0:
        print(f"MINIMO:  x={xs[i]:.2f}  f(x)={f(xs[i]):.2f}")

# Grafico
plt.plot(xs, f(xs))
plt.axhline(0, color='gray')
plt.grid(True)
plt.title("f(x) = x³ - 3x")
plt.savefig("derivata_min.png", dpi=150)
plt.show()