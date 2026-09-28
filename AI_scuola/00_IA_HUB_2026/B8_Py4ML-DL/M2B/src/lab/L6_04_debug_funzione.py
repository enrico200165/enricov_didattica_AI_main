# L6 - Seguire una chiamata di funzione con il debugger
# Avviare con Ctrl+F5 e procedere con F7 (passo dentro):
# alla chiamata di neurone si apre una finestra con le variabili locali della funzione.
import math


def sigmoide(z):
    return 1 / (1 + math.exp(-z))


def neurone(ingressi, pesi, bias, attivazione):
    z = bias
    for x, w in zip(ingressi, pesi):
        z = z + x * w
    return attivazione(z)


y = neurone([1, 0], [0.8, -0.4], -0.3, sigmoide)
print("uscita:", y)
