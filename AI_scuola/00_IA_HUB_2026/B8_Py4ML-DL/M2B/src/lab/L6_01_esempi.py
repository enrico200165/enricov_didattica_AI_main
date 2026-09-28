# L6 - Esempi: definizione e uso di funzioni
import math


def area_rettangolo(base, altezza):
    """Restituisce l'area di un rettangolo."""
    return base * altezza


a = area_rettangolo(8, 5)
print("Area:", a)
print("Area di un altro rettangolo:", area_rettangolo(2.5, 4))


# return e print sono diversi
def doppio_con_return(x):
    return 2 * x


def doppio_con_print(x):
    print(2 * x)


r1 = doppio_con_return(7)    # r1 vale 14
r2 = doppio_con_print(7)     # stampa 14, ma r2 vale None
print("r1 =", r1, " r2 =", r2)


# Parametri con valore predefinito e argomenti con nome
def saluta(nome, saluto="Ciao"):
    return f"{saluto}, {nome}!"


print(saluta("Ada"))
print(saluta("Alan", "Buongiorno"))
print(saluta(saluto="Salve", nome="Grace"))


# Variabili locali
def calcola_media(valori):
    somma = 0              # somma è locale: esiste solo durante la chiamata
    for v in valori:
        somma = somma + v
    return somma / len(valori)


print("Media:", calcola_media([6, 7, 8]))

# Funzioni della libreria standard e funzioni proprie si usano allo stesso modo
print(math.sqrt(area_rettangolo(4, 9)))
