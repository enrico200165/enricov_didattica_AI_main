# L6 - Esercizi: soluzioni
# Completare le funzioni sostituendo "pass" con il codice richiesto.
# Eseguire il file (F5): i controlli assert in fondo verificano ogni funzione.
import math


# Esercizio 1 (base)
# Restituire il perimetro di un rettangolo di lati base e altezza.
def perimetro_rettangolo(base, altezza):
    return 2 * (base + altezza)


# Esercizio 2 (base)
# Restituire il valore della funzione sigmoide: 1 / (1 + e^(-z)).
def sigmoide(z):
    return 1 / (1 + math.exp(-z))


# Esercizio 3 (base)
# Restituire z se z è positivo, altrimenti 0 (funzione ReLU).
def relu(z):
    if z > 0:
        return z
    return 0


# Esercizio 4 (standard)
# Restituire la somma pesata degli ingressi più il bias.
def somma_pesata(ingressi, pesi, bias):
    z = bias
    for x, w in zip(ingressi, pesi):
        z = z + x * w
    return z


# Esercizio 5 (standard)
# Restituire l'uscita del neurone: attivazione applicata alla somma pesata.
# Usare la funzione somma_pesata dell'esercizio 4.
def neurone(ingressi, pesi, bias, attivazione):
    return attivazione(somma_pesata(ingressi, pesi, bias))


# Esercizio 6 (approfondimento)
# Restituire una nuova lista con la funzione f applicata a ogni elemento di valori.
# Esempio: applica(relu, [-1, 2]) restituisce [0, 2].
def applica(f, valori):
    risultato = []
    for v in valori:
        risultato.append(f(v))
    return risultato


# Esercizio 7 (approfondimento)
# La derivata della sigmoide vale sigmoide(z) * (1 - sigmoide(z)).
# Restituire questo valore. Verrà usata nella lezione sulla discesa del gradiente.
def derivata_sigmoide(z):
    s = sigmoide(z)
    return s * (1 - s)


# ---------------- Controlli: non modificare ----------------
def controlla(numero, condizione):
    if condizione:
        print(f"Esercizio {numero}: corretto")
    else:
        print(f"Esercizio {numero}: da rivedere")


controlla(1, perimetro_rettangolo(8, 5) == 26)
controlla(2, sigmoide(0) is not None and math.isclose(sigmoide(0), 0.5)
          and math.isclose(sigmoide(2), 0.8807970779778823))
controlla(3, relu(-2) == 0 and relu(3.5) == 3.5 and relu(0) == 0)
controlla(4, somma_pesata([1, 2], [0.5, -1], 0.2) is not None
          and math.isclose(somma_pesata([1, 2], [0.5, -1], 0.2), -1.3))
controlla(5, neurone([1, 1], [1, 1], -1.5, relu) is not None
          and math.isclose(neurone([1, 1], [1, 1], -1.5, relu), 0.5)
          and neurone([0, 1], [1, 1], -1.5, relu) == 0)
controlla(6, applica(relu, [-1, 2, -3, 4]) == [0, 2, 0, 4])
controlla(7, derivata_sigmoide(0) is not None and math.isclose(derivata_sigmoide(0), 0.25))
