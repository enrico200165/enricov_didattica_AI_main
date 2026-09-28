# L5 - Somma pesata e neurone con un numero qualsiasi di ingressi

# Media ponderata dei voti: ogni voto conta secondo il proprio peso
voti = [7, 6, 9]
pesi = [0.5, 0.3, 0.2]      # scritto 50%, orale 30%, laboratorio 20%

somma_pesata = 0
for v, p in zip(voti, pesi):
    somma_pesata = somma_pesata + v * p
print("Media ponderata:", somma_pesata)

# Neurone a soglia con tre ingressi: la stessa operazione, poi il confronto
ingressi = [1, 0, 1]
pesi = [0.6, 0.6, 0.6]
soglia = 1.0

s = 0
for x, w in zip(ingressi, pesi):
    s = s + x * w
if s >= soglia:
    y = 1
else:
    y = 0
print("somma pesata:", s, "uscita:", y)

# Tabella di verità completa per due ingressi con due cicli for annidati
pesi = [1, 1]
soglia = 1.5
for x1 in [0, 1]:
    for x2 in [0, 1]:
        s = x1 * pesi[0] + x2 * pesi[1]
        y = 1 if s >= soglia else 0
        print(x1, x2, "->", y)
