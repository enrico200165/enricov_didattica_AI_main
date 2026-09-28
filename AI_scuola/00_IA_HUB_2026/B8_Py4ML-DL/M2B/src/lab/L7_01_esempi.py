# L7 - Esempi: tuple, dizionari, comprehension, moduli, eccezioni

# Tuple: sequenze non modificabili
punto = (3, 4)
x, y = punto                   # spacchettamento
print("x =", x, "y =", y)

# Una funzione può restituire più valori sotto forma di tupla
def minimo_massimo(valori):
    return min(valori), max(valori)

mn, mx = minimo_massimo([7, 2, 9, 4])
print("minimo", mn, "massimo", mx)

# Dizionari: coppie chiave-valore
neurone_and = {"pesi": [1, 1], "bias": -1.5, "attivazione": "gradino"}
print(neurone_and["bias"])
neurone_and["bias"] = -1.2        # modifica
neurone_and["nome"] = "AND"       # aggiunta
print(neurone_and)
print("pesi" in neurone_and, "soglia" in neurone_and)

for chiave, valore in neurone_and.items():
    print(chiave, "->", valore)

print(neurone_and.get("soglia", "non presente"))

# List comprehension
quadrati = [n ** 2 for n in range(6)]
pari = [n for n in range(10) if n % 2 == 0]
print(quadrati, pari)

# Moduli: tre forme di import
import math
from math import sqrt
import random as rnd
print(math.pi, sqrt(2), rnd.randint(1, 6))

# Eccezioni: try / except
for testo in ["12", "3.5", "dodici"]:
    try:
        valore = float(testo)
        print(testo, "->", valore)
    except ValueError:
        print(testo, "-> non è un numero")
