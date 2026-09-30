"""Matrice di decisione pesata, con analisi della sensibilità ai pesi.

Uso:
    python matrice_decisione.py matrice.csv

Il file CSV ha una riga per criterio:
    criterio,peso,Opzione A,Opzione B[,Opzione C...]
    peso: importanza del criterio, da 1 a 5
    punteggi: quanto ciascuna opzione soddisfa il criterio, da 1 a 5

Il programma calcola per ogni opzione la somma di peso x punteggio, indica la
vincente e controlla se la scelta cambierebbe modificando il peso di un solo
criterio: se basta poco a cambiare il risultato, conviene discuterne ancora.
"""

import csv
import sys


class ErroreMatrice(Exception):
    """Errore nel file della matrice."""


def leggi_matrice(percorso):
    """Restituisce (opzioni, criteri); criteri è un elenco di (nome, peso, [punteggi])."""
    with open(percorso, encoding="utf-8", newline="") as f:
        righe = [r for r in csv.reader(f) if any(c.strip() for c in r)]
    if not righe:
        raise ErroreMatrice("file vuoto")
    intestazione = [c.strip() for c in righe[0]]
    if [c.lower() for c in intestazione[:2]] != ["criterio", "peso"] or len(intestazione) < 4:
        raise ErroreMatrice("l'intestazione deve essere: criterio,peso, e almeno due opzioni")
    opzioni = intestazione[2:]
    criteri = []
    for numero, riga in enumerate(righe[1:], start=2):
        if len(riga) != len(intestazione):
            raise ErroreMatrice(f"riga {numero}: servono {len(intestazione)} valori, ce ne sono {len(riga)}")
        try:
            numeri = [int(c) for c in riga[1:]]
        except ValueError:
            raise ErroreMatrice(f"riga {numero}: peso e punteggi devono essere numeri interi") from None
        if not all(1 <= n <= 5 for n in numeri):
            raise ErroreMatrice(f"riga {numero}: peso e punteggi devono essere tra 1 e 5")
        criteri.append((riga[0].strip(), numeri[0], numeri[1:]))
    if not criteri:
        raise ErroreMatrice("nessun criterio")
    return opzioni, criteri


def totali(criteri, numero_opzioni):
    """Somma di peso x punteggio per ciascuna opzione."""
    return [sum(peso * punteggi[i] for _, peso, punteggi in criteri) for i in range(numero_opzioni)]


def vincente(valori):
    """Indice dell'opzione con il totale più alto; None in caso di parità."""
    massimo = max(valori)
    migliori = [i for i, v in enumerate(valori) if v == massimo]
    return migliori[0] if len(migliori) == 1 else None


def sensibilita(opzioni, criteri):
    """Per ogni criterio, i pesi da 1 a 5 con cui il risultato cambierebbe.

    Restituisce un elenco di (criterio, peso, risultato), dove risultato è il
    nome della nuova opzione vincente oppure "parità".
    """
    attuale = vincente(totali(criteri, len(opzioni)))
    cambi = []
    for i, (nome, peso, punteggi) in enumerate(criteri):
        for nuovo in range(1, 6):
            if nuovo == peso:
                continue
            modificati = list(criteri)
            modificati[i] = (nome, nuovo, punteggi)
            altro = vincente(totali(modificati, len(opzioni)))
            if altro != attuale:
                cambi.append((nome, nuovo, "parità" if altro is None else opzioni[altro]))
    return cambi


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Uso: python matrice_decisione.py matrice.csv")
        return 2
    try:
        opzioni, criteri = leggi_matrice(argv[0])
    except (ErroreMatrice, OSError) as e:
        print(f"Errore: {e}")
        return 1

    larghezza = max(len(nome) for nome, _, _ in criteri + [("Totale", 0, [])])
    col = max([18] + [len(o) for o in opzioni])          # larghezza delle colonne delle opzioni
    print(f"{'Criterio':<{larghezza}}  Peso  " + "  ".join(f"{o:>{col}}" for o in opzioni))
    for nome, peso, punteggi in criteri:
        celle = "  ".join(f"{f'{p} x {peso} = {p * peso}':>{col}}" for p in punteggi)
        print(f"{nome:<{larghezza}}  {peso:>4}  {celle}")
    valori = totali(criteri, len(opzioni))
    massimo = 5 * sum(peso for _, peso, _ in criteri)
    print(f"{'Totale':<{larghezza}}        " + "  ".join(f"{f'{v} su {massimo}':>{col}}" for v in valori))

    migliore = vincente(valori)
    print()
    if migliore is None:
        print("Risultato: parità. Servono altri criteri o una discussione sui pesi.")
    else:
        ordinati = sorted(valori, reverse=True)
        distacco = ordinati[0] - ordinati[1]
        print(f"Risultato: {opzioni[migliore]}, con {distacco} punti di distacco "
              f"({round(100 * distacco / massimo)}% del massimo).")
        if distacco < 0.05 * massimo:
            print("ATTENZIONE: distacco minimo, le opzioni sono quasi equivalenti.")
    cambi = sensibilita(opzioni, criteri)
    if not cambi:
        print("Sensibilità: cambiando il peso di un solo criterio il risultato non cambia.")
    else:
        print("Sensibilità: il risultato cambierebbe con")
        for nome, peso, risultato in cambi:
            print(f"  peso {peso} per \"{nome}\": {risultato}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
