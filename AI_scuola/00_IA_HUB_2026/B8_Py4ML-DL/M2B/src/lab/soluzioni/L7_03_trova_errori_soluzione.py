# L7 - Soluzione: errori corretti
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
    # Errore 2 (logico): return era dentro il ciclo, la funzione terminava al primo elemento
    return somma / len(valori)


voti = [6, 7, 8]
print("media dei voti:", media(voti))
# Errore 3 - IndexError: l'ultimo indice valido è len(voti) - 1
print("ultimo voto:", voti[len(voti) - 1])

registro = {"Anna": 8, "Luca": 6, "Sara": 7}
# Errore 4 - KeyError: le chiavi distinguono maiuscole e minuscole
print("voto di Luca:", registro["Luca"])

# Errore 1 - SyntaxError: la funzione si chiama con le parentesi tonde
print("media di una lista vuota:", media([]))
