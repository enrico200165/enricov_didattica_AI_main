# B.8 - Verifica del Modulo 2: soluzioni
# Tempo: 40 minuti. Lavoro individuale.
# Completare le funzioni e la classe sostituendo "pass" con il codice richiesto.
# Eseguire il file (F5): i controlli in fondo indicano gli esercizi corretti.
# Oltre al superamento dei controlli viene valutata la leggibilità del codice.


# Esercizio 1
# Restituire quanti valori della lista sono maggiori o uguali alla soglia.
def conta_sopra_soglia(valori, soglia):
    conteggio = 0
    for v in valori:
        if v >= soglia:
            conteggio = conteggio + 1
    return conteggio


# Esercizio 2
# Restituire una nuova lista con i valori trasformati nell'intervallo [0, 1]:
# (valore - minimo) / (massimo - minimo). Si può usare min e max.
def normalizza(valori):
    mn = min(valori)
    mx = max(valori)
    return [(v - mn) / (mx - mn) for v in valori]


# Esercizio 3
# registro è una lista di tuple (nome, voto), per esempio [("Ada", 8), ("Alan", 6), ("Ada", 6)].
# Restituire un dizionario che associa a ogni nome la media dei suoi voti:
# per l'esempio {"Ada": 7.0, "Alan": 6.0}.
def medie_per_studente(registro):
    voti = {}
    for nome, voto in registro:
        if nome not in voti:
            voti[nome] = []
        voti[nome].append(voto)
    medie = {}
    for nome, v in voti.items():
        medie[nome] = sum(v) / len(v)
    return medie


# Esercizio 4
# Classe NeuroneSoglia con due ingressi.
# Attributi: pesi (lista di due numeri) e soglia.
# Metodo calcola(x1, x2): 1 se w1*x1 + w2*x2 >= soglia, altrimenti 0.
# Metodo tabella(): lista delle uscite per (0,0), (0,1), (1,0), (1,1), in quest'ordine.
class NeuroneSoglia:
    def __init__(self, pesi, soglia):
        self.pesi = pesi
        self.soglia = soglia

    def calcola(self, x1, x2):
        s = self.pesi[0] * x1 + self.pesi[1] * x2
        return 1 if s >= self.soglia else 0

    def tabella(self):
        return [self.calcola(a, b) for a in [0, 1] for b in [0, 1]]


# Esercizio 5
# Creare un NeuroneSoglia che calcola la funzione "x1 AND NOT x2":
# uscita 1 solo per x1 = 1 e x2 = 0.
neurone_es5 = NeuroneSoglia([1, -1], 0.5)


# ---------------- Controlli: non modificare ----------------
def controlla(numero, prova):
    try:
        esito = prova()
    except Exception as e:
        print(f"Esercizio {numero}: errore {type(e).__name__}")
        return
    print(f"Esercizio {numero}: " + ("corretto" if esito else "da rivedere"))


controlla(1, lambda: conta_sopra_soglia([3, 7, 5, 9, 1], 5) == 3 and conta_sopra_soglia([], 1) == 0)
controlla(2, lambda: normalizza([10, 20, 15]) == [0.0, 1.0, 0.5])
controlla(3, lambda: medie_per_studente([("Ada", 8), ("Alan", 6), ("Ada", 6)]) == {"Ada": 7.0, "Alan": 6.0})
controlla(4, lambda: NeuroneSoglia([1, 1], 1.5).tabella() == [0, 0, 0, 1]
          and NeuroneSoglia([1, 1], 0.5).calcola(0, 1) == 1)
controlla(5, lambda: neurone_es5.tabella() == [0, 0, 1, 0])
