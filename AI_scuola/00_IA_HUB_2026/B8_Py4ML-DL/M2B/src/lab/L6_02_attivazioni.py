# L6 - Funzioni di attivazione e neurone come funzione
import math


def gradino(z):
    """1 se z >= 0, altrimenti 0."""
    if z >= 0:
        return 1
    return 0


def sigmoide(z):
    """Valore compreso tra 0 e 1."""
    return 1 / (1 + math.exp(-z))


def relu(z):
    """z se positivo, altrimenti 0 (Rectified Linear Unit)."""
    if z > 0:
        return z
    return 0


def tangente_iperbolica(z):
    """Valore compreso tra -1 e 1."""
    return math.tanh(z)


def somma_pesata(ingressi, pesi, bias):
    """Somma dei prodotti ingresso per peso, più il bias."""
    z = bias
    for x, w in zip(ingressi, pesi):
        z = z + x * w
    return z


def neurone(ingressi, pesi, bias, attivazione):
    """Calcola l'uscita di un neurone: attivazione(somma pesata + bias)."""
    z = somma_pesata(ingressi, pesi, bias)
    return attivazione(z)


# Tabella dei valori delle funzioni di attivazione
print("   z  | gradino | sigmoide | ReLU | tanh")
for z in [-3, -1, -0.5, 0, 0.5, 1, 3]:
    print(f"{z:5} | {gradino(z):7} | {sigmoide(z):8.3f} | {relu(z):4} | {tangente_iperbolica(z):6.3f}")

# Lo stesso neurone con attivazioni diverse
ingressi = [1, 0]
pesi = [0.8, -0.4]
bias = -0.3
for f in [gradino, sigmoide, relu, tangente_iperbolica]:
    print(f.__name__, "->", neurone(ingressi, pesi, bias, f))

# Neurone AND con attivazione a gradino: bias = -soglia
print("AND:")
for x1 in [0, 1]:
    for x2 in [0, 1]:
        print(x1, x2, "->", neurone([x1, x2], [1, 1], -1.5, gradino))
