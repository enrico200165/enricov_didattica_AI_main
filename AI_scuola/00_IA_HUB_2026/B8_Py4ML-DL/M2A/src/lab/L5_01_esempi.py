# L5 - Esempi: liste e ciclo for

temperature = [18.5, 21.0, 23.4, 19.8, 25.1]

# Indici e lunghezza
print(temperature[0], temperature[4], temperature[-1], len(temperature))

# Slicing: dall'indice iniziale (incluso) a quello finale (escluso)
print(temperature[1:3])
print(temperature[:2], temperature[3:])

# Modifica e aggiunta
temperature[0] = 18.0
temperature.append(22.7)
print(temperature)

# Ciclo for su una lista
for t in temperature:
    print("temperatura:", t)

# range
for i in range(3):
    print("i =", i)
print(list(range(2, 10, 3)))

# enumerate: indice e valore insieme
for i, t in enumerate(temperature):
    print(i, t)

# zip: due liste in parallelo
giorni = ["lun", "mar", "mer", "gio", "ven", "sab"]
for g, t in zip(giorni, temperature):
    print(g, t)

# Accumulatore: somma e media
somma = 0
for t in temperature:
    somma = somma + t
media = somma / len(temperature)
print(f"somma {somma:.1f}, media {media:.2f}")

# Massimo
massimo = temperature[0]
for t in temperature:
    if t > massimo:
        massimo = t
print("massimo:", massimo)

# Le stesse operazioni con le funzioni predefinite
print(sum(temperature), max(temperature), min(temperature))
