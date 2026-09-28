# L3 - Esempi: valori, tipi, variabili, espressioni
import math

# Tipi di dato
print(type(42), type(3.14), type("ciao"), type(True))

# Operatori aritmetici
a = 17
b = 5
print("a + b  =", a + b)
print("a - b  =", a - b)
print("a * b  =", a * b)
print("a / b  =", a / b)     # divisione: risultato float
print("a // b =", a // b)    # divisione intera
print("a % b  =", a % b)     # resto della divisione intera
print("a ** 2 =", a ** 2)    # potenza

# Numeri in virgola mobile: approssimazione
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(round(0.1 + 0.2, 2))
print(math.isclose(0.1 + 0.2, 0.3))

# Stringhe e f-string
nome = "Ada"
voto = 8.456
print(f"{nome} ha ottenuto {voto:.1f}")

# Conversioni
testo = "25"
numero = int(testo)
print(numero * 2, testo * 2)

# Funzione esponenziale
print(math.exp(-2), math.exp(0), math.exp(2))
