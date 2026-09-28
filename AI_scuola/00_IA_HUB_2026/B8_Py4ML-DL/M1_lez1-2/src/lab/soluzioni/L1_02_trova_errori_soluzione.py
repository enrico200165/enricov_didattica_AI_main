# L1 - Soluzione dell'esercizio "trova errori"

citta = "Roma"
abitanti = 2750000

print("Città:", citta)
# Errore 1 - SyntaxError: mancava la virgola tra i due argomenti di print
print("Abitanti:", abitanti)
# Errore 2 - TypeError: non si può concatenare una stringa con un numero;
# si passano i due valori come argomenti separati di print
print("Abitanti in milioni:", abitanti / 1000000)
# Errore 3 - NameError: Python distingue maiuscole e minuscole, Citta non esiste
print("Fine del programma", citta)
