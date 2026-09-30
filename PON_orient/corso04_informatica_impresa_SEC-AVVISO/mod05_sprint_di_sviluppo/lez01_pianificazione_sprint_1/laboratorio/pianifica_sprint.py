"""Controlla le storie scelte per uno sprint e crea il file dello Sprint Backlog.

Uso:
    python pianifica_sprint.py docs\\backlog.md --numero 1 --capacita 12 --storie US-01 US-02 US-03
        --obiettivo "I docenti non trovano più laboratori occupati e i tecnici sanno che cosa preparare"

Controlli sulle storie scelte:
    - esistono nel backlog, non sono già fatte, hanno una stima e i criteri di accettazione
    - la somma delle stime non supera la capacità (punti che il team pensa di completare)
    - non si lasciano fuori storie Must mentre si scelgono storie Should o Could
Se non ci sono problemi da sistemare scrive docs\\sprintN.md (nella cartella del backlog).
"""

import argparse
import re
import sys
from pathlib import Path

RIGA = re.compile(r"^\|\s*(US-\d{2}[a-z]?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
TITOLO = re.compile(r"^###\s+(US-\d{2}[a-z]?)\b")
CRITERIO = re.compile(r"^-\s*(dato|data|dati|date)\b.*\bquando\b.*\ballora\b", re.IGNORECASE)
ORDINE = {"must": 0, "should": 1, "could": 2, "won't": 3}


def leggi_backlog(testo):
    """Restituisce {id: storia} con titolo, priorità, stima, stato e numero di criteri."""
    storie, corrente = {}, None
    for riga in testo.splitlines():
        trovata = RIGA.match(riga)
        if trovata:
            codice, titolo, priorita, stima, stato = trovata.groups()
            storie[codice] = {"id": codice, "titolo": titolo, "priorita": priorita.lower(),
                              "stima": int(stima) if stima.isdigit() else None,
                              "stato": stato.lower(), "criteri": 0}
            continue
        titolo = TITOLO.match(riga)
        if titolo:
            corrente = titolo.group(1)
        elif riga.startswith("#"):
            corrente = None
        elif corrente in storie and CRITERIO.match(riga.strip()):
            storie[corrente]["criteri"] += 1
    return storie


def controlla(storie, scelte, capacita, obiettivo):
    """Restituisce l'elenco dei problemi (livello, messaggio)."""
    problemi = []
    for codice in scelte:
        s = storie.get(codice)
        if s is None:
            problemi.append(("DA SISTEMARE", f"{codice} non è nel backlog"))
            continue
        if s["stato"].startswith("fatto"):
            problemi.append(("DA SISTEMARE", f"{codice} è già fatta"))
        if s["stima"] is None:
            problemi.append(("DA SISTEMARE", f"{codice} non ha una stima (planning poker, lezione 3.3)"))
        if s["criteri"] == 0:
            problemi.append(("DA SISTEMARE", f"{codice} non ha criteri di accettazione (lezione 2.2)"))
    totale = sum(storie[c]["stima"] or 0 for c in scelte if c in storie)
    if totale > capacita:
        problemi.append(("ATTENZIONE", f"impegno di {totale} punti oltre la capacità di {capacita}"))
    scelte_note = [storie[c] for c in scelte if c in storie]
    peggiore = max((ORDINE.get(s["priorita"], 3) for s in scelte_note), default=0)
    escluse = [s["id"] for s in storie.values()
               if s["id"] not in scelte and s["priorita"] == "must" and not s["stato"].startswith("fatto")]
    if escluse and peggiore > 0:
        problemi.append(("ATTENZIONE", "storie Must lasciate fuori mentre se ne scelgono di priorità minore: "
                         + ", ".join(escluse)))
    if not obiettivo.strip():
        problemi.append(("ATTENZIONE", "manca l'obiettivo dello sprint (--obiettivo)"))
    return problemi, totale


def testo_sprint(numero, obiettivo, capacita, scelte, storie):
    righe = [f"# Sprint {numero}", "",
             f"Obiettivo dello sprint: {obiettivo or '...'}", "",
             "Date: dal ... al ...", "",
             f"Capacità prevista: {capacita} punti", "",
             "## Storie", "",
             "| ID | Titolo | Stima |", "|---|---|---|"]
    righe += [f"| {c} | {storie[c]['titolo']} | {storie[c]['stima']} |" for c in scelte]
    righe += ["", "Lo stato di ogni storia si aggiorna nel backlog (colonna Stato); la board si rigenera con genera_board.py.",
              "", "## Compiti", ""]
    for c in scelte:
        righe += [f"### {c} {storie[c]['titolo']}", "",
                  "- [ ] scrivere i test dai criteri di accettazione",
                  "- [ ] ...",
                  "- [ ] aggiornare manuale e CHANGELOG",
                  "- [ ] revisione di un compagno e integrazione in main", ""]
    righe += ["## Andamento", "", "Punti rimanenti dopo ogni daily scrum: file burndown.csv (lezione 5.3).", ""]
    return "\n".join(righe)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Pianificazione di uno sprint")
    parser.add_argument("backlog")
    parser.add_argument("--numero", type=int, required=True, help="numero dello sprint")
    parser.add_argument("--capacita", type=int, required=True, help="punti che il team pensa di completare")
    parser.add_argument("--storie", nargs="+", required=True, help="codici delle storie scelte, in ordine")
    parser.add_argument("--obiettivo", default="", help="obiettivo dello sprint, tra virgolette")
    argomenti = parser.parse_args(argv)
    try:
        storie = leggi_backlog(Path(argomenti.backlog).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"Errore: {e}")
        return 1
    scelte = [c.upper() for c in argomenti.storie]
    problemi, totale = controlla(storie, scelte, argomenti.capacita, argomenti.obiettivo)
    for livello, messaggio in problemi:
        print(f"{livello}: {messaggio}")
    print(f"Storie scelte: {len(scelte)}; punti: {totale} su una capacità di {argomenti.capacita}")
    if any(livello == "DA SISTEMARE" for livello, _ in problemi):
        print("Sprint Backlog non scritto: sistemare prima i problemi.")
        return 1
    uscita = Path(argomenti.backlog).with_name(f"sprint{argomenti.numero}.md")
    uscita.write_text(testo_sprint(argomenti.numero, argomenti.obiettivo, argomenti.capacita, scelte, storie),
                      encoding="utf-8")
    print(f"Sprint Backlog scritto in {uscita}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
