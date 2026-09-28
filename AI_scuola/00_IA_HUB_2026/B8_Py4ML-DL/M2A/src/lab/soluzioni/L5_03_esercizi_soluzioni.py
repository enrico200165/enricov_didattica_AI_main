# L5 - Esercizi: soluzioni
# Completare gli esercizi nell'ordine ed eseguire il file (F5).
# Negli esercizi 1-3 usare un ciclo for, non le funzioni sum, max, min.
import math

misure = [12.4, 15.1, 9.8, 17.6, 14.0, 11.3, 16.2]

# Esercizio 1 (base)
# Calcolare la somma e la media delle misure.
somma = 0
for m in misure:
    somma = somma + m
media = somma / len(misure)
print("Esercizio 1:", somma, media)
assert media is not None, "Esercizio 1: completare il codice"
assert math.isclose(media, 13.771428571428572), "Esercizio 1: risultato non corretto"

# Esercizio 2 (base)
# Trovare la misura minima.
minimo = misure[0]
for m in misure:
    if m < minimo:
        minimo = m
print("Esercizio 2:", minimo)
assert minimo is not None, "Esercizio 2: completare il codice"
assert minimo == 9.8, "Esercizio 2: risultato non corretto"

# Esercizio 3 (standard)
# Contare quante misure superano la media calcolata nell'esercizio 1.
conteggio = 0
for m in misure:
    if m > media:
        conteggio = conteggio + 1
print("Esercizio 3:", conteggio)
assert conteggio == 4, "Esercizio 3: risultato non corretto"

# Esercizio 4 (standard)
# Calcolare la somma pesata di ingressi e pesi (prodotto scalare).
ingressi = [0.5, -1.0, 2.0, 0.0]
pesi = [0.8, 0.3, -0.5, 1.2]
s = 0
for x, w in zip(ingressi, pesi):
    s = s + x * w
print("Esercizio 4:", s)
assert math.isclose(s, -0.9), "Esercizio 4: risultato non corretto"

# Esercizio 5 (standard)
# Neurone di maggioranza: tre ingressi 0/1, uscita 1 se almeno due ingressi valgono 1.
# Scegliere i pesi e la soglia; il controllo prova tutte le 8 combinazioni.
pesi_magg = [1, 1, 1]
soglia_magg = 2
errori = 0
assert soglia_magg is not None, "Esercizio 5: completare il codice"
for x1 in [0, 1]:
    for x2 in [0, 1]:
        for x3 in [0, 1]:
            s = x1 * pesi_magg[0] + x2 * pesi_magg[1] + x3 * pesi_magg[2]
            y = 1 if s >= soglia_magg else 0
            atteso = 1 if x1 + x2 + x3 >= 2 else 0
            if y != atteso:
                errori = errori + 1
print("Esercizio 5: combinazioni errate:", errori)
assert errori == 0, "Esercizio 5: il neurone non realizza la maggioranza"

# Esercizio 6 (approfondimento)
# Normalizzare le misure nell'intervallo [0, 1]:
# valore_normalizzato = (valore - minimo) / (massimo - minimo)
# Costruire la lista "normalizzate" con append.
massimo = misure[0]
for m in misure:
    if m > massimo:
        massimo = m
normalizzate = []
for m in misure:
    normalizzate.append((m - minimo) / (massimo - minimo))
print("Esercizio 6:", normalizzate)
assert len(normalizzate) == len(misure) and min(normalizzate) == 0 and max(normalizzate) == 1, \
    "Esercizio 6: risultato non corretto"

print("Tutti gli esercizi sono corretti.")
