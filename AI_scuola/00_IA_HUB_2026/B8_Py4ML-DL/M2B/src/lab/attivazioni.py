"""Modulo attivazioni: funzioni di attivazione e neurone.

Questo file non si esegue direttamente: si importa da altri programmi
con "import attivazioni" (i due file devono stare nella stessa cartella).
"""
import math


def gradino(z):
    """1 se z >= 0, altrimenti 0."""
    return 1 if z >= 0 else 0


def sigmoide(z):
    """Valore compreso tra 0 e 1."""
    return 1 / (1 + math.exp(-z))


def relu(z):
    """z se positivo, altrimenti 0."""
    return z if z > 0 else 0


def somma_pesata(ingressi, pesi, bias):
    """Somma dei prodotti ingresso per peso, più il bias."""
    z = bias
    for x, w in zip(ingressi, pesi):
        z = z + x * w
    return z


def neurone(ingressi, pesi, bias, attivazione):
    """Uscita di un neurone: attivazione(somma pesata + bias)."""
    return attivazione(somma_pesata(ingressi, pesi, bias))
