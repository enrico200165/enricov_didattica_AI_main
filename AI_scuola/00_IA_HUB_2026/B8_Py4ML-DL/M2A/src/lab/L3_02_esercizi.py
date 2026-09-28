# L3 - Esercizi
# Completare gli esercizi nell'ordine, sostituendo ogni None con il calcolo richiesto.
# Eseguire il file (F5): le righe con assert controllano il risultato.
# Se un risultato non è corretto, il programma si ferma con AssertionError
# e il messaggio indica quale esercizio controllare.
import math

# Esercizio 1 (base)
# Convertire secondi_totali in ore, minuti e secondi rimanenti.
# Suggerimento: usare // e %. Un'ora ha 3600 secondi, un minuto 60.
secondi_totali = 3725
ore = None
minuti = None
secondi = None
print("Esercizio 1:", ore, "h", minuti, "min", secondi, "s")
assert ore is not None, "Esercizio 1: completare il codice"
assert (ore, minuti, secondi) == (1, 2, 5), "Esercizio 1: risultato non corretto"

# Esercizio 2 (base)
# Convertire una temperatura da gradi Celsius a gradi Fahrenheit: F = C * 9 / 5 + 32
celsius = 36.6
fahrenheit = None
print(f"Esercizio 2: {celsius} °C = {fahrenheit} °F")
assert fahrenheit is not None, "Esercizio 2: completare il codice"
assert math.isclose(fahrenheit, 97.88), "Esercizio 2: risultato non corretto"

# Esercizio 3 (standard)
# Calcolare la media dei tre voti e stamparla con due cifre decimali usando una f-string.
voto1 = 6.5
voto2 = 7
voto3 = 8.25
media = None
print("Esercizio 3: sostituire questa riga con la stampa richiesta")
assert media is not None, "Esercizio 3: completare il codice"
assert math.isclose(media, 7.25), "Esercizio 3: risultato non corretto"

# Esercizio 4 (approfondimento)
# La funzione sigmoide, usata nelle reti neurali, vale 1 / (1 + e^(-x)).
# Calcolarla per x = 0, x = 4 e x = -4 usando math.exp.
sig_0 = None
sig_4 = None
sig_meno4 = None
print(f"Esercizio 4: {sig_0}, {sig_4}, {sig_meno4}")
assert None not in (sig_0, sig_4, sig_meno4), "Esercizio 4: completare il codice"
assert math.isclose(sig_0, 0.5), "Esercizio 4: sigmoide in 0 non corretta"
assert math.isclose(sig_4 + sig_meno4, 1.0), "Esercizio 4: sigmoide in 4 o in -4 non corretta"

print("Tutti gli esercizi sono corretti.")
