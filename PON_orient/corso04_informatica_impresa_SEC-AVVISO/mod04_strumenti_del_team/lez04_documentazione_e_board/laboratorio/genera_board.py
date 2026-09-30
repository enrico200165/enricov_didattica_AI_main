"""Genera la board Kanban del team dal backlog.

Uso:
    python genera_board.py docs\\backlog.md docs\\board.md
    python genera_board.py docs\\backlog.md docs\\board.md --limite-in-corso 3 --limite-in-revisione 2

La fonte unica è la tabella di riepilogo del backlog (| ID | Titolo | Priorità | Stima | Stato |).
La colonna Stato può contenere, tra parentesi, chi lavora sulla storia:
    da fare | in corso (Giulia) | in revisione (Sara) | fatto
Le storie Won't non compaiono nella board. Il programma scrive board.md con il
diagramma Mermaid kanban e la tabella equivalente, e avvisa se una colonna
supera il limite di lavoro in corso.
"""

import argparse
import re
import sys
from pathlib import Path

RIGA = re.compile(r"^\|\s*(US-\d{2}[a-z]?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
COLONNE = [("da fare", "daFare", "Da fare"), ("in corso", "inCorso", "In corso"),
           ("in revisione", "inRevisione", "In revisione"), ("fatto", "fatto", "Fatto")]
PRIORITA_MERMAID = {"must": "Very High", "should": "High", "could": "Low"}


class ErroreBacklog(Exception):
    """Errore nel backlog."""


def leggi_storie(testo):
    """Restituisce l'elenco delle storie della tabella, con stato normalizzato e assegnatario."""
    storie = []
    for numero, riga in enumerate(testo.splitlines(), start=1):
        trovata = RIGA.match(riga)
        if not trovata:
            continue
        codice, titolo, priorita, stima, stato = trovata.groups()
        persona = re.search(r"\(([^)]*)\)", stato)
        stato_base = re.sub(r"\(.*?\)", "", stato).strip().lower()
        if stato_base not in [c[0] for c in COLONNE]:
            raise ErroreBacklog(f"riga {numero}: stato \"{stato}\" non valido; ammessi: da fare, in corso, "
                                "in revisione, fatto, con il nome tra parentesi se serve")
        storie.append({"id": codice, "titolo": titolo, "priorita": priorita.strip().lower(),
                       "stima": stima, "stato": stato_base,
                       "persona": persona.group(1).strip() if persona and persona.group(1).strip() != "kit" else ""})
    if not storie:
        raise ErroreBacklog("nessuna storia nella tabella di riepilogo del backlog")
    return storie


def pulisci(testo, virgolette=False):
    """Toglie i caratteri che interrompono la sintassi del diagramma Mermaid.

    Nel testo di una scheda non sono ammesse parentesi quadre e graffe; nei valori
    dei metadati, scritti tra apici, non sono ammessi nemmeno apici e virgolette.
    """
    caratteri = r"[\[\]{}'\"]" if virgolette else r"[\[\]{}]"
    return re.sub(caratteri, "", testo)


def board_mermaid(storie, limiti):
    righe = ["kanban"]
    for stato, id_colonna, nome in COLONNE:
        schede = [s for s in storie if s["stato"] == stato]
        etichetta = nome
        if stato in limiti:
            etichetta += f", {len(schede)} su massimo {limiti[stato]}"
        righe.append(f"  {id_colonna}[{etichetta}]")
        for s in schede:
            metadati = [f"ticket: '{s['id']}'"]
            if s["persona"]:
                metadati.append(f"assigned: '{pulisci(s['persona'], virgolette=True)}'")
            if s["priorita"] in PRIORITA_MERMAID:
                metadati.append(f"priority: '{PRIORITA_MERMAID[s['priorita']]}'")
            testo = pulisci(s["titolo"]) + (f", {s['stima']} punti" if s["stima"] else "")
            righe.append(f"    {s['id'].lower().replace('-', '')}[{testo}]@{{ {', '.join(metadati)} }}")
    return "\n".join(righe)


def tabella(storie):
    celle = []
    for stato, _, _ in COLONNE:
        celle.append(", ".join(s["id"] + (f" ({s['persona']})" if s["persona"] else "")
                               for s in storie if s["stato"] == stato))
    return ("| " + " | ".join(n for _, _, n in COLONNE) + " |\n|---|---|---|---|\n| " +
            " | ".join(celle) + " |")


def genera(testo_backlog, limiti):
    """Restituisce (testo di board.md, elenco degli avvisi)."""
    storie = [s for s in leggi_storie(testo_backlog) if not s["priorita"].startswith("won")]
    avvisi = []
    for stato, massimo in limiti.items():
        presenti = sum(1 for s in storie if s["stato"] == stato)
        if presenti > massimo:
            avvisi.append(f"colonna \"{stato}\": {presenti} schede, limite {massimo}: finire prima di iniziare")
    for s in storie:
        if s["stato"] in ("in corso", "in revisione") and not s["persona"]:
            avvisi.append(f"{s['id']} è {s['stato']} ma non indica chi ci lavora")
    punti_fatti = sum(int(s["stima"]) for s in storie if s["stato"] == "fatto" and s["stima"].isdigit())
    testo = ("# Board del team\n\n"
             "File generato con genera_board.py dal backlog: per cambiare lo stato di una storia "
             "si modifica la colonna Stato del backlog e si rigenera la board.\n\n"
             "```mermaid\n" + board_mermaid(storie, limiti) + "\n```\n\n" + tabella(storie) +
             f"\n\nPunti completati: {punti_fatti}\n")
    return testo, avvisi


def main(argv=None):
    parser = argparse.ArgumentParser(description="Board Kanban generata dal backlog")
    parser.add_argument("backlog", help="file backlog.md")
    parser.add_argument("board", help="file board.md da scrivere")
    parser.add_argument("--limite-in-corso", type=int, default=3)
    parser.add_argument("--limite-in-revisione", type=int, default=2)
    argomenti = parser.parse_args(argv)
    try:
        testo = Path(argomenti.backlog).read_text(encoding="utf-8")
        board, avvisi = genera(testo, {"in corso": argomenti.limite_in_corso,
                                       "in revisione": argomenti.limite_in_revisione})
    except (ErroreBacklog, OSError) as e:
        print(f"Errore: {e}")
        return 1
    Path(argomenti.board).write_text(board, encoding="utf-8")
    print(f"Board scritta in {argomenti.board}")
    for avviso in avvisi:
        print(f"ATTENZIONE: {avviso}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
