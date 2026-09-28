# L4 - Esercizi: soluzioni
# Completare gli esercizi nell'ordine ed eseguire il file (F5).
# Le righe con assert controllano i risultati.

# Esercizio 1 (base)
# Assegnare a "tipo" la stringa "pari" se n è pari, "dispari" altrimenti.
# Suggerimento: un numero è pari se il resto della divisione per 2 è 0.
n = 17
if n % 2 == 0:
    tipo = "pari"
else:
    tipo = "dispari"
print("Esercizio 1:", n, "è", tipo)
assert tipo is not None, "Esercizio 1: completare il codice"
assert tipo == "dispari", "Esercizio 1: risultato non corretto"

# Esercizio 2 (base)
# Assegnare a "fascia" la stringa "bambino" se eta < 14,
# "ragazzo" se eta è tra 14 e 17 compresi, "adulto" se eta >= 18.
eta = 16
if eta < 14:
    fascia = "bambino"
elif eta <= 17:
    fascia = "ragazzo"
else:
    fascia = "adulto"
print("Esercizio 2:", eta, "anni ->", fascia)
assert fascia is not None, "Esercizio 2: completare il codice"
assert fascia == "ragazzo", "Esercizio 2: risultato non corretto"

# Esercizio 3 (standard)
# Con un ciclo while calcolare la somma dei numeri interi da 1 a 100.
somma = 0
i = 1
while i <= 100:
    somma = somma + i
    i = i + 1
print("Esercizio 3: somma =", somma)
assert somma == 5050, "Esercizio 3: risultato non corretto"

# Esercizio 4 (standard)
# Modificare i pesi e la soglia in L4_02_neurone_soglia.py in modo che il
# neurone realizzi la funzione OR (uscita 1 se almeno un ingresso vale 1).
# Riportare qui i valori trovati.
w1_or = 1
w2_or = 1
soglia_or = 0.5
assert soglia_or is not None, "Esercizio 4: completare il codice"
assert (w1_or * 0 + w2_or * 0 < soglia_or and w1_or * 1 + w2_or * 0 >= soglia_or
        and w1_or * 0 + w2_or * 1 >= soglia_or and w1_or * 1 + w2_or * 1 >= soglia_or), \
    "Esercizio 4: i valori non realizzano OR"
print("Esercizio 4: OR con pesi", w1_or, w2_or, "e soglia", soglia_or)

# Esercizio 5 (approfondimento)
# Trovare pesi e soglia per NAND: uscita 0 solo se entrambi gli ingressi valgono 1.
# Suggerimento: i pesi possono essere negativi.
w1_nand = -1
w2_nand = -1
soglia_nand = -1.5
assert soglia_nand is not None, "Esercizio 5: completare il codice"
assert (w1_nand * 0 + w2_nand * 0 >= soglia_nand and w1_nand * 1 + w2_nand * 0 >= soglia_nand
        and w1_nand * 0 + w2_nand * 1 >= soglia_nand and w1_nand * 1 + w2_nand * 1 < soglia_nand), \
    "Esercizio 5: i valori non realizzano NAND"
print("Esercizio 5: NAND con pesi", w1_nand, w2_nand, "e soglia", soglia_nand)

print("Tutti gli esercizi sono corretti.")
