# L4 - Esercizio 6 (standard): indovina il numero
# Il programma sceglie un numero intero casuale tra 1 e 100.
# L'utente prova a indovinarlo; dopo ogni tentativo il programma
# risponde "troppo alto", "troppo basso" oppure "indovinato".
import random

segreto = random.randint(1, 100)   # intero casuale tra 1 e 100, estremi inclusi
tentativi = 0
indovinato = False

while not indovinato:
    risposta = int(input("Numero: "))
    tentativi = tentativi + 1
    if risposta > segreto:
        print("troppo alto")
    elif risposta < segreto:
        print("troppo basso")
    else:
        print("indovinato")
        indovinato = True

print("Tentativi:", tentativi)
