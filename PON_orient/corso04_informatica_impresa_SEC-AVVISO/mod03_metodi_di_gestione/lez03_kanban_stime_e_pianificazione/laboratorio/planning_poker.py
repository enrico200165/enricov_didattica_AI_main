"""Analizza le stime del planning poker e le scrive nel backlog.

Uso:
    python planning_poker.py stime.csv
    python planning_poker.py stime.csv --velocita 12
    python planning_poker.py stime.csv --backlog docs\\backlog.md

Il file CSV ha le colonne storia, giro e una colonna per ogni membro del team;
ogni riga contiene le carte mostrate in un giro di stima. Per ogni storia il
programma considera l'ultimo giro e indica se c'è accordo, quasi accordo
(carte vicine nel mazzo) o se serve un'altra discussione, e chi deve spiegare.
"""

import argparse
import csv
import math
import re
import shutil
import sys
from pathlib import Path

MAZZO = ["0", "1", "2", "3", "5", "8", "13", "20", "40", "100", "?"]
STORIA_GRANDE = 13


class ErroreStime(Exception):
    """Errore nel file delle stime."""


def leggi_stime(percorso):
    """Restituisce (membri, {storia: carte dell'ultimo giro})."""
    with open(percorso, encoding="utf-8", newline="") as f:
        lettore = csv.DictReader(f)
        campi = lettore.fieldnames or []
        if campi[:2] != ["storia", "giro"] or len(campi) < 3:
            raise ErroreStime("l'intestazione deve essere: storia,giro, e i nomi dei membri del team")
        membri = campi[2:]
        ultimo = {}
        for numero, riga in enumerate(lettore, start=2):
            try:
                giro = int(riga["giro"])
            except ValueError:
                raise ErroreStime(f"riga {numero}: il giro deve essere un numero") from None
            carte = {m: (riga[m] or "").strip() for m in membri}
            for m, carta in carte.items():
                if carta not in MAZZO:
                    raise ErroreStime(f"riga {numero}: carta \"{carta}\" di {m} non valida; "
                                      "carte ammesse: " + " ".join(MAZZO))
            storia = riga["storia"].strip()
            if storia not in ultimo or giro >= ultimo[storia][0]:
                ultimo[storia] = (giro, carte)
    return membri, {s: carte for s, (_, carte) in ultimo.items()}


def analizza(carte):
    """Restituisce (esito, stima o None, spiegazione)."""
    valori = list(carte.values())
    if "?" in valori:
        chi = ", ".join(m for m, c in carte.items() if c == "?")
        return "da chiarire", None, f"{chi} non ha abbastanza informazioni: chiarire la storia con il Product Owner"
    posizioni = [MAZZO.index(v) for v in valori]
    minimo, massimo = min(posizioni), max(posizioni)
    if minimo == massimo:
        return "accordo", int(MAZZO[minimo]), "tutti uguali"
    if massimo - minimo == 1:
        return "quasi accordo", int(MAZZO[massimo]), "carte vicine: si propone la più alta, per prudenza"
    basso = [m for m, c in carte.items() if MAZZO.index(c) == minimo]
    alto = [m for m, c in carte.items() if MAZZO.index(c) == massimo]
    return ("da discutere", None,
            f"spiegano {', '.join(basso)} ({MAZZO[minimo]}) e {', '.join(alto)} ({MAZZO[massimo]}), poi nuovo giro")


def scrivi_nel_backlog(percorso, stime):
    """Scrive le stime nella colonna Stima della tabella di riepilogo del backlog."""
    righe = Path(percorso).read_text(encoding="utf-8").splitlines()
    riga_storia = re.compile(r"^\|\s*(US-\d{2}[a-z]?)\s*\|")
    scritte = []
    for i, riga in enumerate(righe):
        trovata = riga_storia.match(riga)
        if trovata and trovata.group(1) in stime:
            celle = riga.split("|")
            celle[4] = f" {stime[trovata.group(1)]} "       # colonna Stima
            righe[i] = "|".join(celle)
            scritte.append(trovata.group(1))
    shutil.copy(percorso, str(percorso) + ".bak")
    Path(percorso).write_text("\n".join(righe) + "\n", encoding="utf-8")
    return scritte


def main(argv=None):
    parser = argparse.ArgumentParser(description="Analisi del planning poker")
    parser.add_argument("stime", help="file CSV delle stime")
    parser.add_argument("--velocita", type=int, help="punti che il team completa in uno sprint")
    parser.add_argument("--backlog", help="backlog.md in cui scrivere le stime concordate")
    argomenti = parser.parse_args(argv)
    try:
        membri, ultimo = leggi_stime(argomenti.stime)
    except (ErroreStime, OSError) as e:
        print(f"Errore: {e}")
        return 1
    stimate = {}
    print(f"{'Storia':<8}{'Carte':<22}{'Esito':<15}{'Stima':>5}  Note")
    for storia, carte in ultimo.items():
        esito, stima, nota = analizza(carte)
        if stima is not None:
            stimate[storia] = stima
            if stima >= STORIA_GRANDE:
                nota += "; storia grande: valutare se dividerla"
        mostra = " ".join(carte[m] for m in membri)
        print(f"{storia:<8}{mostra:<22}{esito:<15}{'' if stima is None else stima:>5}  {nota}")
    totale = sum(stimate.values())
    print(f"\nStorie stimate: {len(stimate)} su {len(ultimo)}; punti in tutto: {totale}")
    if argomenti.velocita:
        if argomenti.velocita <= 0:
            print("Errore: la velocità deve essere positiva")
            return 1
        print(f"Con una velocità di {argomenti.velocita} punti per sprint servono "
              f"{math.ceil(totale / argomenti.velocita)} sprint per le storie stimate.")
    if argomenti.backlog:
        scritte = scrivi_nel_backlog(argomenti.backlog, stimate)
        print(f"Stime scritte nel backlog per: {', '.join(scritte) or 'nessuna storia'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
