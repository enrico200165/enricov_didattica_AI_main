# L8 - La classe Neurone
import math


def gradino(z):
    return 1 if z >= 0 else 0


def sigmoide(z):
    return 1 / (1 + math.exp(-z))


class Neurone:
    """Neurone artificiale con pesi, bias e funzione di attivazione."""

    def __init__(self, pesi, bias, attivazione):
        self.pesi = pesi
        self.bias = bias
        self.attivazione = attivazione

    def somma_pesata(self, ingressi):
        z = self.bias
        for x, w in zip(ingressi, self.pesi):
            z = z + x * w
        return z

    def calcola(self, ingressi):
        return self.attivazione(self.somma_pesata(ingressi))


n_and = Neurone([1, 1], -1.5, gradino)
n_or = Neurone([1, 1], -0.5, gradino)

print("x1 x2 | AND OR")
for x1 in [0, 1]:
    for x2 in [0, 1]:
        print(f" {x1}  {x2} |  {n_and.calcola([x1, x2])}   {n_or.calcola([x1, x2])}")

# Un neurone con attivazione sigmoide produce valori graduati tra 0 e 1
n_morbido = Neurone([4, 4], -6, sigmoide)
for x1 in [0, 1]:
    for x2 in [0, 1]:
        print(x1, x2, "->", round(n_morbido.calcola([x1, x2]), 3))

# I parametri sono attributi: si possono modificare dopo la creazione
n_and.bias = -0.5          # ora il neurone si comporta come OR
print("AND modificato:", [n_and.calcola([a, b]) for a in [0, 1] for b in [0, 1]])
