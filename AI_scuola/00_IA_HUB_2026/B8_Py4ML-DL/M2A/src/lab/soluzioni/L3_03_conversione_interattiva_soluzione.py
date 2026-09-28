# L3 - Esercizio 5: soluzione
testo = input("Temperatura in gradi Celsius: ")
celsius = float(testo)
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius:.1f} °C corrispondono a {fahrenheit:.1f} °F")
# Con un testo non numerico float() genera ValueError:
# could not convert string to float: 'ventuno'
