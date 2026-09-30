"""Due famiglie di protocolli di instradamento dinamico a confronto.

- Vettore di distanze (idea di RIP): ogni router conosce solo i vicini e,
  a ogni turno, riceve da loro le distanze che conoscono; scopre le reti
  lontane "per sentito dire" e ha bisogno di più turni per convergere.
- Stato dei collegamenti (idea di OSPF): ogni router conosce la mappa completa
  della rete e calcola da solo i percorsi migliori con l'algoritmo di Dijkstra.

Uso: python instradamento_dinamico.py
"""

import heapq

INFINITO = 16  # come in RIP: 16 salti significa "irraggiungibile"


def grafo_di_esempio():
    """Cinque router e il costo di ogni collegamento (non orientato)."""
    collegamenti = [("A", "B", 1), ("A", "C", 4), ("B", "C", 1),
                    ("B", "D", 5), ("C", "D", 1), ("D", "E", 1), ("C", "E", 6)]
    return costruisci(collegamenti)


def costruisci(collegamenti):
    grafo = {}
    for a, b, costo in collegamenti:
        grafo.setdefault(a, {})[b] = costo
        grafo.setdefault(b, {})[a] = costo
    return grafo


def rimuovi_collegamento(grafo, a, b):
    nuovo = {r: dict(vicini) for r, vicini in grafo.items()}
    nuovo[a].pop(b, None)
    nuovo[b].pop(a, None)
    return nuovo


def vettore_distanze(grafo, turni_max=50, tabelle_iniziali=None):
    """Simula lo scambio periodico delle tabelle tra vicini.

    Restituisce (tabelle, turni necessari per convergere).
    tabelle[router][destinazione] = (costo, prossimo_salto)
    """
    if tabelle_iniziali is None:
        tabelle = {r: {r: (0, r)} for r in grafo}          # all'inizio ognuno conosce solo sé stesso
    else:
        tabelle = {r: dict(t) for r, t in tabelle_iniziali.items()}
    for turno in range(1, turni_max + 1):
        nuove = {}
        for router in grafo:
            tabella = {router: (0, router)}
            # per ogni destinazione annunciata da un vicino: costo del collegamento + costo annunciato
            for vicino, costo_link in grafo[router].items():
                for destinazione, (costo, _) in tabelle[vicino].items():
                    totale = min(costo_link + costo, INFINITO)
                    if totale < INFINITO and (destinazione not in tabella or totale < tabella[destinazione][0]):
                        tabella[destinazione] = (totale, vicino)
            nuove[router] = tabella
        if nuove == tabelle:
            return tabelle, turno - 1                       # nessun cambiamento: convergenza
        tabelle = nuove
    return tabelle, turni_max


def dijkstra(grafo, sorgente):
    """Percorsi minimi da sorgente: {destinazione: (costo, prossimo_salto)}."""
    risultato = {}
    coda = [(0, sorgente, sorgente)]                        # (costo, router, primo salto)
    while coda:
        costo, router, primo = heapq.heappop(coda)          # estrae il router più vicino
        if router in risultato:
            continue
        risultato[router] = (costo, primo)
        for vicino, costo_link in grafo[router].items():
            if vicino not in risultato:
                salto = vicino if router == sorgente else primo
                heapq.heappush(coda, (costo + costo_link, vicino, salto))
    return risultato


def stampa_tabella(nome, tabella):
    voci = ", ".join(f"{d}:{c} via {p}" for d, (c, p) in sorted(tabella.items()) if d != nome)
    print(f"  {nome}: {voci}")


def dimostrazione():
    grafo = grafo_di_esempio()
    tabelle, turni = vettore_distanze(grafo)
    print(f"Vettore di distanze: convergenza in {turni} turni di scambio")
    for r in sorted(tabelle):
        stampa_tabella(r, tabelle[r])
    print("\nStato dei collegamenti (Dijkstra) calcolato da A:")
    stampa_tabella("A", dijkstra(grafo, "A"))

    guasto = rimuovi_collegamento(grafo, "C", "D")
    print("\nGuasto del collegamento C-D")
    print("Dijkstra, ricalcolato subito con la nuova mappa:")
    stampa_tabella("A", dijkstra(guasto, "A"))
    # Nella realtà i router non ripartono da zero: partono dalle tabelle che avevano
    print("Vettore di distanze, a partire dalle tabelle precedenti:")
    for turno in range(1, 4):
        parziali, _ = vettore_distanze(guasto, turni_max=turno, tabelle_iniziali=tabelle)
        c, b = parziali["C"]["D"], parziali["B"]["D"]
        print(f"  turno {turno}: C raggiunge D con costo {c[0]} via {c[1]}; B con costo {b[0]} via {b[1]}")
    nuove, turni = vettore_distanze(guasto, tabelle_iniziali=tabelle)
    print(f"  convergenza dopo {turni} turni:")
    stampa_tabella("A", nuove["A"])


if __name__ == "__main__":
    dimostrazione()
