import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

def f(x):
    valore = x**2 + 2 / x
    if valore < 0:
        return np.nan
    return np.sqrt(valore)

def derivata(x):
    h = 0.0001
    return (f(x + h) - f(x)) /h


x0 = float(input("Inserisci il punto per calcolare la derivata (diverso da 0): "))
if x0 != 0:
    try:
        print("Calcolo derivata f'(x) nel punto: ", x0)
        print("f'(x) = ", round(derivata(x0), 4))
    except:
        print("Errore nel calcolo della derivata in questo punto")
else:
    print("Errore: x non può essere 0")
print()

# Creare il grafico escludendo x=0
valori_x_neg = np.linspace(-10, -0.01, 1000)
valori_x_pos = np.linspace(0.01, 10, 1000)

valori_y_neg = []
valori_y_pos = []

# Calcolare i valori, gestendo gli errori
for x in valori_x_neg:
    try:
        valori_y_neg.append(f(x))
    except:
        valori_y_neg.append(np.nan)

for x in valori_x_pos:
    try:
        valori_y_pos.append(f(x))
    except:
        valori_y_pos.append(np.nan)

# Trovare massimi e minimi nelle regioni valide
massimo_trovato = False
minimo_trovato = False

# Cerca nei valori negativi
for i in range(1, len(valori_y_neg)-1):
    if not (np.isnan(valori_y_neg[i]) or np.isnan(valori_y_neg[i-1]) or np.isnan(valori_y_neg[i+1])):
        try:
            derivata_prima = derivata(valori_x_neg[i - 1])
            derivata_seconda = derivata(valori_x_neg[i + 1])
            
            if derivata_prima > 0 and derivata_seconda < 0 and not massimo_trovato:
                print("Massimale trovato:")
                print("x = ", round(valori_x_neg[i], 2))
                print("f(x) = ", round(valori_y_neg[i], 2))
                massimo_trovato = True
            
            if derivata_prima < 0 and derivata_seconda > 0 and not minimo_trovato:
                print("Minimo trovato:")
                print("x = ", round(valori_x_neg[i], 2))
                print("f(x) = ", round(valori_y_neg[i], 2))
                minimo_trovato = True
        except:
            pass

# Cerca nei valori positivi
for i in range(1, len(valori_y_pos)-1):
    if not (np.isnan(valori_y_pos[i]) or np.isnan(valori_y_pos[i-1]) or np.isnan(valori_y_pos[i+1])):
        try:
            derivata_prima = derivata(valori_x_pos[i - 1])
            derivata_seconda = derivata(valori_x_pos[i + 1])
            
            if derivata_prima > 0 and derivata_seconda < 0 and not massimo_trovato:
                print("Massimale trovato:")
                print("x = ", round(valori_x_pos[i], 2))
                print("f(x) = ", round(valori_y_pos[i], 2))
                massimo_trovato = True
            
            if derivata_prima < 0 and derivata_seconda > 0 and not minimo_trovato:
                print("Minimo trovato:")
                print("x = ", round(valori_x_pos[i], 2))
                print("f(x) = ", round(valori_y_pos[i], 2))
                minimo_trovato = True
        except:
            pass

fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot per il dominio negativo
ax.plot(valori_x_neg, np.zeros_like(valori_x_neg), valori_y_neg, 'b-', linewidth=2, label='f(x) nel dominio negativo')

# Plot per il dominio positivo
ax.plot(valori_x_pos, np.zeros_like(valori_x_pos), valori_y_pos, 'b-', linewidth=2, label='f(x) nel dominio positivo')

# Disegna l'asintoto verticale a x=0
z_asintoto = np.linspace(0, 20, 100)
x_zero = np.zeros_like(z_asintoto)
y_zero = np.zeros_like(z_asintoto)
ax.plot(x_zero, y_zero, z_asintoto, 'r--', alpha=0.5, linewidth=2, label='Asintoto (x=0)')

# Configurazione del grafico
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.set_zlabel('f(x)', fontsize=12)
ax.set_title('Grafico 3D: f(x) = √(x² + 2/x)', fontsize=14, fontweight='bold')
ax.legend()
ax.set_zlim([0, 20])
ax.view_init(elev=25, azim=45)

plt.show()
