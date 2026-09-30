"""Test di instradamento_dinamico.py. Esecuzione: python test_instradamento_dinamico.py"""

from instradamento_dinamico import (grafo_di_esempio, costruisci, rimuovi_collegamento,
                                    vettore_distanze, dijkstra, INFINITO)

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def costi(tabella):
    return {d: c for d, (c, _) in tabella.items()}


grafo = grafo_di_esempio()
verifica("grafo non orientato: A-B e B-A con lo stesso costo", grafo["A"]["B"] == grafo["B"]["A"] == 1)
d = dijkstra(grafo, "A")
verifica("Dijkstra da A: costi 0, 1, 2, 3, 4", costi(d) == {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4})
verifica("Dijkstra: da A tutto passa per B (il collegamento diretto A-C costa 4)", all(p == "B" for r, (c, p) in d.items() if r != "A"))

tabelle, turni = vettore_distanze(grafo)
verifica("vettore di distanze: stessi costi di Dijkstra per ogni router",
         all(costi(tabelle[r]) == costi(dijkstra(grafo, r)) for r in grafo))
verifica("convergenza in 4 turni (diametro della rete in salti)", turni == 4)
verifica("prossimo salto coerente: da E verso A si passa per D", tabelle["E"]["A"][1] == "D")

guasto = rimuovi_collegamento(grafo, "C", "D")
verifica("collegamento C-D rimosso nei due sensi", "D" not in guasto["C"] and "C" not in guasto["D"])
verifica("grafo originale non modificato", "D" in grafo["C"])
verifica("dopo il guasto A raggiunge D con costo 6", dijkstra(guasto, "A")["D"][0] == 6)
nuove, turni_guasto = vettore_distanze(guasto, tabelle_iniziali=tabelle)
verifica("vettore di distanze dopo il guasto: stessi costi di Dijkstra",
         all(costi(nuove[r]) == costi(dijkstra(guasto, r)) for r in guasto))
verifica("dal vecchio stato servono più turni che da zero (6 contro 3)",
         turni_guasto == 6 and vettore_distanze(guasto)[1] == 3)
primo, _ = vettore_distanze(guasto, turni_max=1, tabelle_iniziali=tabelle)
verifica("ciclo temporaneo: dopo un turno C va verso D via B e B via C",
         primo["C"]["D"][1] == "B" and primo["B"]["D"][1] == "C")

# Rete isolata: un router senza collegamenti non compare nelle tabelle degli altri
isolata = costruisci([("X", "Y", 1)])
isolata["Z"] = {}
t, _ = vettore_distanze(isolata)
verifica("router isolato irraggiungibile", "Z" not in t["X"] and "Z" not in dijkstra(isolata, "X"))

# Catena di 17 router con costo 1: oltre 15 salti la destinazione è irraggiungibile (limite di RIP)
catena = costruisci([(f"R{i}", f"R{i + 1}", 1) for i in range(17)])
t, _ = vettore_distanze(catena)
verifica("limite di 15 salti: R15 raggiungibile da R0, R16 no",
         t["R0"]["R15"][0] == 15 and "R16" not in t["R0"] and INFINITO == 16)

print(f"\nTest superati: {superati}, falliti: {falliti}")
