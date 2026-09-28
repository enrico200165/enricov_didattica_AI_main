# L4 - Esempi: confronti, condizioni, ciclo while

# Operatori di confronto: il risultato è True o False
x = 7
print(x > 5, x == 7, x != 7, x <= 6)

# Operatori logici
print(x > 5 and x < 10)   # True: entrambe vere
print(x < 5 or x > 10)    # False: nessuna vera
print(not x > 5)          # False: negazione di True

# if / elif / else
voto = 6.5
if voto >= 8:
    giudizio = "ottimo"
elif voto >= 6:
    giudizio = "sufficiente"
else:
    giudizio = "insufficiente"
print("Voto", voto, "->", giudizio)

# Ciclo while: conto alla rovescia
n = 5
while n > 0:
    print(n)
    n = n - 1
print("Partenza")
