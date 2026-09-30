"""Chiude uno sprint registrandone il risultato, e confronta più sprint.

Uso:
    python metriche_sprint.py chiudi docs\\backlog.md docs\\sprint1.md
    python metriche_sprint.py confronta docs\\sprint1.md docs\\sprint2.md

chiudi: legge le storie dello sprint (sezione "## Storie" del file dello sprint)
e il loro stato nel backlog; aggiunge al file dello sprint la sezione
"## Risultato" con punti pianificati, punti completati (velocità), storie
completate e non completate. Le storie non completate tornano nel backlog.

confronta: legge le sezioni "## Risultato" di più sprint e mostra velocità,
percentuale completata e capacità proposta per lo sprint successivo.
"""

import re
import sys
from pathlib import Path

RIGA_BACKLOG = re.compile(r"^\|\s*(US-\d{2}[a-z]?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
RIGA_SPRINT = re.compile(r"^\|\s*(US-\d{2}[a-z]?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
RISULTATO = re.compile(r"^- (Punti pianificati|Punti completati): (\d+)", re.MULTILINE)


class ErroreSprint(Exception):
    """Errore nei file dello sprint o del backlog."""


def storie_dello_sprint(testo_sprint):
    """Elenco (id, stima pianificata) dalla sezione "## Storie"."""
    storie, dentro = [], False
    for riga in testo_sprint.splitlines():
        if riga.startswith("## "):
            dentro = riga.strip() == "## Storie"
        elif dentro:
            trovata = RIGA_SPRINT.match(riga)
            if trovata and trovata.group(1) != "ID":
                stima = trovata.group(3).strip()
                storie.append((trovata.group(1), int(stima) if stima.isdigit() else 0))
    if not storie:
        raise ErroreSprint("nessuna storia nella sezione \"## Storie\" del file dello sprint")
    return storie


def stati_backlog(testo_backlog):
    return {m.group(1): m.group(5).lower() for m in map(RIGA_BACKLOG.match, testo_backlog.splitlines()) if m}


def risultato(storie, stati):
    """Restituisce (pianificati, completati, fatte, non_fatte)."""
    mancanti = [c for c, _ in storie if c not in stati]
    if mancanti:
        raise ErroreSprint("storie dello sprint assenti dal backlog: " + ", ".join(mancanti))
    fatte = [c for c, _ in storie if stati[c].startswith("fatto")]
    non_fatte = [c for c, _ in storie if c not in fatte]
    pianificati = sum(s for _, s in storie)
    completati = sum(s for c, s in storie if c in fatte)
    return pianificati, completati, fatte, non_fatte


def chiudi(percorso_backlog, percorso_sprint):
    testo_sprint = Path(percorso_sprint).read_text(encoding="utf-8")
    if "## Risultato" in testo_sprint:
        raise ErroreSprint("lo sprint è già chiuso: la sezione \"## Risultato\" esiste")
    pianificati, completati, fatte, non_fatte = risultato(
        storie_dello_sprint(testo_sprint), stati_backlog(Path(percorso_backlog).read_text(encoding="utf-8")))
    sezione = ["", "## Risultato", "",
               f"- Punti pianificati: {pianificati}",
               f"- Punti completati: {completati}",
               f"- Storie completate: {', '.join(fatte) or 'nessuna'}",
               f"- Storie non completate (tornano nel backlog): {', '.join(non_fatte) or 'nessuna'}", ""]
    Path(percorso_sprint).write_text(testo_sprint.rstrip("\n") + "\n" + "\n".join(sezione), encoding="utf-8")
    return pianificati, completati, fatte, non_fatte


def leggi_risultato(percorso_sprint):
    testo = Path(percorso_sprint).read_text(encoding="utf-8")
    if "## Risultato" not in testo:
        raise ErroreSprint(f"{percorso_sprint}: sprint non ancora chiuso (usare il comando chiudi)")
    valori = dict(RISULTATO.findall(testo.split("## Risultato", 1)[1]))
    return int(valori["Punti pianificati"]), int(valori["Punti completati"])


def percentuale(parte, totale):
    return round(100 * parte / totale) if totale else 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        if len(argv) == 3 and argv[0] == "chiudi":
            pianificati, completati, fatte, non_fatte = chiudi(argv[1], argv[2])
            print(f"Punti pianificati: {pianificati}; completati: {completati} "
                  f"({percentuale(completati, pianificati)}%)")
            print(f"Velocità dello sprint: {completati} punti")
            print(f"Storie non completate, da riportare nel backlog: {', '.join(non_fatte) or 'nessuna'}")
            print(f"Risultato aggiunto a {argv[2]}")
        elif len(argv) >= 2 and argv[0] == "confronta":
            print(f"{'Sprint':<24}{'Pianificati':>12}{'Completati':>12}{'%':>6}")
            velocita = []
            for percorso in argv[1:]:
                pianificati, completati = leggi_risultato(percorso)
                velocita.append(completati)
                print(f"{Path(percorso).stem:<24}{pianificati:>12}{completati:>12}{percentuale(completati, pianificati):>5}%")
            if len(velocita) > 1:
                variazione = velocita[-1] - velocita[-2]
                print(f"\nVariazione della velocità rispetto allo sprint precedente: {variazione:+d} punti")
            print(f"Capacità proposta per il prossimo sprint (media delle velocità): {round(sum(velocita) / len(velocita))} punti")
        else:
            print("Uso: python metriche_sprint.py chiudi backlog.md sprintN.md")
            print("     python metriche_sprint.py confronta sprint1.md sprint2.md")
            return 2
    except (ErroreSprint, OSError, KeyError) as e:
        print(f"Errore: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
