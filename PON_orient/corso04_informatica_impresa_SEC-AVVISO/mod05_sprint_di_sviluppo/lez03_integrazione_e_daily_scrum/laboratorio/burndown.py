"""Grafico di avanzamento dello sprint (burndown): punti rimanenti lezione per lezione.

Uso:
    python burndown.py docs\\burndown.csv --backlog docs\\backlog.md --sprint docs\\sprint1.md --registra 5.3
    python burndown.py docs\\burndown.csv --lezioni 3

Il file burndown.csv ha le colonne lezione, rimanenti. Con --registra il
programma calcola i punti rimanenti dello sprint (stime delle storie dello
sprint non ancora "fatto" nel backlog) e aggiunge una riga; se il file non
esiste lo crea. Poi confronta l'andamento con la linea ideale, che scende in
modo regolare fino a zero nell'ultima lezione dello sprint, e scrive il grafico
Mermaid nel file burndown.grafico.md.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

RIGA = re.compile(r"^\|\s*(US-\d{2}[a-z]?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
RIGA_SPRINT = re.compile(r"^\|\s*(US-\d{2}[a-z]?)\s*\|")


def punti_rimanenti(testo_backlog, testo_sprint):
    """Somma delle stime delle storie dello sprint che nel backlog non sono ancora fatte."""
    sprint = []
    nella_tabella = False
    for riga in testo_sprint.splitlines():
        if riga.startswith("## "):
            nella_tabella = riga.strip() == "## Storie"
        elif nella_tabella and RIGA_SPRINT.match(riga):
            sprint.append(RIGA_SPRINT.match(riga).group(1))
    if not sprint:
        raise ValueError("nessuna storia nella sezione \"## Storie\" del file dello sprint")
    backlog = {}
    for riga in testo_backlog.splitlines():
        trovata = RIGA.match(riga)
        if trovata:
            codice, _, _, stima, stato = trovata.groups()
            backlog[codice] = (int(stima) if stima.isdigit() else 0, stato.lower())
    mancanti = [c for c in sprint if c not in backlog]
    if mancanti:
        raise ValueError("storie dello sprint assenti dal backlog: " + ", ".join(mancanti))
    return sum(stima for c in sprint for stima, stato in [backlog[c]] if not stato.startswith("fatto"))


def leggi_andamento(percorso):
    if not Path(percorso).exists():
        return []
    with open(percorso, encoding="utf-8", newline="") as f:
        return [(r["lezione"], int(r["rimanenti"])) for r in csv.DictReader(f)]


def scrivi_andamento(percorso, righe):
    with open(percorso, "w", encoding="utf-8", newline="") as f:
        scrittore = csv.writer(f)
        scrittore.writerow(["lezione", "rimanenti"])
        scrittore.writerows(righe)


def ideale(totale, lezioni):
    """Punti rimanenti ideali: da totale a 0 in parti uguali, per lezioni + 1 punti (inizio compreso)."""
    return [round(totale - totale * i / lezioni, 1) for i in range(lezioni + 1)]


def grafico(righe, lezioni):
    totale = righe[0][1]
    etichette = ["inizio"] + [f"L{i}" for i in range(1, lezioni + 1)]
    reali = [str(r) for _, r in righe]
    return "\n".join([
        "xychart-beta",
        '    title "Punti rimanenti: ideale (prima linea) e reale (seconda linea)"',
        "    x-axis [" + ", ".join(etichette) + "]",
        f'    y-axis "Punti" 0 --> {max(totale, max(r for _, r in righe)) + 1}',
        "    line [" + ", ".join(str(v) for v in ideale(totale, lezioni)) + "]",
        "    line [" + ", ".join(reali) + "]",
    ])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Burndown dello sprint")
    parser.add_argument("andamento", help="file CSV lezione, rimanenti")
    parser.add_argument("--lezioni", type=int, default=3,
                        help="lezioni dello sprint dopo la pianificazione (3 nello sprint 1, 2 nello sprint 2)")
    parser.add_argument("--backlog", help="backlog.md, per calcolare i punti rimanenti")
    parser.add_argument("--sprint", help="file dello sprint, per sapere quali storie contare")
    parser.add_argument("--registra", help="nome della lezione da aggiungere, per esempio 5.3")
    argomenti = parser.parse_args(argv)
    try:
        righe = leggi_andamento(argomenti.andamento)
        if argomenti.registra:
            if not (argomenti.backlog and argomenti.sprint):
                raise ValueError("con --registra servono anche --backlog e --sprint")
            rimanenti = punti_rimanenti(Path(argomenti.backlog).read_text(encoding="utf-8"),
                                        Path(argomenti.sprint).read_text(encoding="utf-8"))
            righe.append((argomenti.registra, rimanenti))
            scrivi_andamento(argomenti.andamento, righe)
            print(f"Registrati {rimanenti} punti rimanenti per la lezione {argomenti.registra}")
        if not righe:
            raise ValueError("nessun dato: registrare la prima riga con --registra all'inizio dello sprint")
    except (ValueError, KeyError, OSError) as e:
        print(f"Errore: {e}")
        return 1
    attesi = ideale(righe[0][1], argomenti.lezioni)
    print(f"{'Lezione':<10}{'Rimanenti':>10}{'Ideale':>8}")
    for i, (lezione, rimanenti) in enumerate(righe):
        valore_ideale = attesi[i] if i < len(attesi) else 0
        print(f"{lezione:<10}{rimanenti:>10}{valore_ideale:>8g}")
    ultimo = len(righe) - 1
    if ultimo < len(attesi):
        differenza = righe[-1][1] - attesi[ultimo]
        if differenza > 0:
            print(f"\nIn ritardo di {differenza:g} punti rispetto alla linea ideale: parlarne nel daily scrum.")
        else:
            print("\nIn linea o in anticipo rispetto alla linea ideale.")
    if len(righe) > argomenti.lezioni + 1:
        print("ATTENZIONE: più righe delle lezioni previste; il grafico mostra solo le prime.")
        righe = righe[:argomenti.lezioni + 1]
    uscita = Path(argomenti.andamento).with_suffix(".grafico.md")
    uscita.write_text("# Burndown dello sprint\n\n```mermaid\n" + grafico(righe, argomenti.lezioni) + "\n```\n",
                      encoding="utf-8")
    print(f"Grafico scritto in {uscita}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
