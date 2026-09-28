# L7 - Esercizi
# Completare le funzioni sostituendo "pass" con il codice richiesto.
# Eseguire il file (F5): i controlli in fondo verificano ogni funzione.


# Esercizio 1 (base)
# Restituire una lista con i quadrati dei numeri da 1 a n, usando una list comprehension.
# Esempio: quadrati(4) restituisce [1, 4, 9, 16].
def quadrati(n):
    pass


# Esercizio 2 (base)
# Restituire una lista con i soli valori positivi (maggiori di 0), con una list comprehension.
def positivi(valori):
    pass


# Esercizio 3 (standard)
# Restituire un dizionario che associa a ogni parola del testo il numero di volte
# in cui compare. Le parole sono separate da spazi: testo.split() restituisce
# la lista delle parole. Ignorare maiuscole e minuscole: testo.lower()
# restituisce il testo tutto in minuscolo.
def conta_parole(testo):
    pass


# Esercizio 4 (standard)
# Convertire il testo in float e restituire il numero.
# Se il testo non rappresenta un numero, restituire None invece di bloccare il programma.
def leggi_numero(testo):
    pass


# Esercizio 5 (standard)
# Restituire una tupla (minimo, massimo, media) dei valori, senza usare min, max, sum.
def statistiche(valori):
    pass


# Esercizio 6 (approfondimento)
# parametri è un dizionario con le chiavi "pesi" e "bias".
# Restituire 1 se la somma pesata degli ingressi più il bias è >= 0, altrimenti 0.
def neurone_da_dizionario(ingressi, parametri):
    pass


# ---------------- Controlli: non modificare ----------------
def controlla(numero, condizione):
    print(f"Esercizio {numero}: " + ("corretto" if condizione else "da rivedere"))


controlla(1, quadrati(4) == [1, 4, 9, 16])
controlla(2, positivi([3, -1, 0, 2.5, -7]) == [3, 2.5])
controlla(3, conta_parole("il gatto e il cane e il topo") == {"il": 3, "gatto": 1, "e": 2, "cane": 1, "topo": 1}
          and conta_parole("Rosa rosa ROSA") == {"rosa": 3})
controlla(4, leggi_numero("3.5") == 3.5 and leggi_numero("tre") is None)
controlla(5, statistiche([4, 8, 6, 2]) == (2, 8, 5.0))
and_neurone = {"pesi": [1, 1], "bias": -1.5}
controlla(6, [neurone_da_dizionario([a, b], and_neurone) for a in [0, 1] for b in [0, 1]] == [0, 0, 0, 1])
