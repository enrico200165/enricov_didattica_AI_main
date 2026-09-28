# L8 - Esercizi: soluzioni
# Completare le classi sostituendo "pass" con il codice richiesto.
# Eseguire il file (F5): i controlli in fondo verificano ogni esercizio.
import math


def gradino(z):
    return 1 if z >= 0 else 0


# Esercizio 1 (base)
# Classe Cerchio: attributo raggio; metodi area() e circonferenza().
class Cerchio:
    def __init__(self, raggio):
        self.raggio = raggio

    def area(self):
        return math.pi * self.raggio ** 2

    def circonferenza(self):
        return 2 * math.pi * self.raggio


# Esercizio 2 (standard)
# Classe Studente: attributi nome e voti (lista, inizialmente vuota).
# Metodo aggiungi_voto(voto): aggiunge il voto alla lista.
# Metodo media(): restituisce la media dei voti, oppure 0 se non ci sono voti.
class Studente:
    def __init__(self, nome):
        self.nome = nome
        self.voti = []

    def aggiungi_voto(self, voto):
        self.voti.append(voto)

    def media(self):
        if len(self.voti) == 0:
            return 0
        return sum(self.voti) / len(self.voti)


# Esercizio 3 (standard)
# Completare il metodo calcola della classe Neurone:
# restituire attivazione(somma pesata degli ingressi + bias).
class Neurone:
    def __init__(self, pesi, bias, attivazione):
        self.pesi = pesi
        self.bias = bias
        self.attivazione = attivazione

    def calcola(self, ingressi):
        z = self.bias
        for x, w in zip(ingressi, self.pesi):
            z = z + x * w
        return self.attivazione(z)


# Esercizio 4 (standard)
# Creare due istanze di Neurone con attivazione gradino:
# n_nand, che calcola NAND (uscita 0 solo se entrambi gli ingressi valgono 1)
# n_maggioranza, con tre ingressi, che restituisce 1 se almeno due ingressi valgono 1
n_nand = Neurone([-1, -1], 1.5, gradino)
n_maggioranza = Neurone([1, 1, 1], -2, gradino)


# Esercizio 5 (approfondimento)
# Classe Strato: contiene una lista di neuroni.
# Il metodo calcola(ingressi) restituisce la lista delle uscite di tutti i neuroni.
class Strato:
    def __init__(self, neuroni):
        self.neuroni = neuroni

    def calcola(self, ingressi):
        return [n.calcola(ingressi) for n in self.neuroni]


# Esercizio 6 (approfondimento)
# XOR non si ottiene con un solo neurone, ma si ottiene con due livelli:
# XOR(x1, x2) = AND(OR(x1, x2), NAND(x1, x2)).
# Creare lo strato "nascosto" con i neuroni OR e NAND e il neurone di uscita AND,
# poi completare la funzione xor.
nascosto = Strato([Neurone([1, 1], -0.5, gradino), n_nand])
uscita = Neurone([1, 1], -1.5, gradino)


def xor(x1, x2):
    h = nascosto.calcola([x1, x2])
    return uscita.calcola(h)


# ---------------- Controlli: non modificare ----------------
def controlla(numero, prova):
    try:
        esito = prova()
    except Exception as e:
        esito = False
        print(f"Esercizio {numero}: errore {type(e).__name__}: {e}")
        return
    print(f"Esercizio {numero}: " + ("corretto" if esito else "da rivedere"))


def tabella(f, n):
    risultati = []
    for k in range(2 ** n):
        bit = [(k >> (n - 1 - i)) & 1 for i in range(n)]
        risultati.append(f(bit))
    return risultati


controlla(1, lambda: math.isclose(Cerchio(2).area(), 4 * math.pi)
          and math.isclose(Cerchio(2).circonferenza(), 4 * math.pi))
s = Studente("Ada")
controlla(2, lambda: s.media() == 0 and (s.aggiungi_voto(6), s.aggiungi_voto(8)) and s.media() == 7 and s.nome == "Ada")
controlla(3, lambda: tabella(Neurone([1, 1], -1.5, gradino).calcola, 2) == [0, 0, 0, 1])
controlla(4, lambda: tabella(n_nand.calcola, 2) == [1, 1, 1, 0]
          and tabella(n_maggioranza.calcola, 3) == [0, 0, 0, 1, 0, 1, 1, 1])
controlla(5, lambda: Strato([Neurone([1, 1], -1.5, gradino), Neurone([1, 1], -0.5, gradino)]).calcola([0, 1]) == [0, 1])
controlla(6, lambda: [xor(a, b) for a in [0, 1] for b in [0, 1]] == [0, 1, 1, 0])
