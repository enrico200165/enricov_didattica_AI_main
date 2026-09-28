# L7 - Laboratorio: trovare e correggere gli errori
# Il programma contiene quattro errori. Alcuni producono un messaggio di errore,
# uno produce un risultato sbagliato senza alcun messaggio.
# Usare il traceback e il debugger (Ctrl+F5, F7) per trovarli.
# Risultati attesi:
#   media dei voti: 7.0
#   ultimo voto: 8
#   voto di Luca: 6
#   media di una lista vuota: 0


def media(valori):
    if len(valori) == 0:
        return 0
    somma = 0
    for v in valori:
        somma = somma + v
        return somma / len(valori)


voti = [6, 7, 8]
print("media dei voti:", media(voti))
print("ultimo voto:", voti[len(voti)])

registro = {"Anna": 8, "Luca": 6, "Sara": 7}
print("voto di Luca:", registro["luca"])

print("media di una lista vuota:", media[])
