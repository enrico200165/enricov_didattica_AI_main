"""Controlla un piano orientativo personale e ne disegna la linea del tempo.

Uso:
    python piano_orientativo.py piano.md
    python piano_orientativo.py piano.md --timeline linea_del_tempo.md
    python piano_orientativo.py piano.md --oggi 2026-12-15

Il piano è una tabella Markdown con le colonne:
| Obiettivo | Priorità | Misura | Scadenza | Primo passo | Stato |
Priorità: Must, Should, Could (come nel backlog del progetto).
Scadenza: AAAA-MM-GG. Stato: da fare, in corso, fatto.

I controlli seguono i criteri SMART: obiettivo specifico, misurabile,
realistico, con una scadenza; il primo passo rende l'obiettivo raggiungibile.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

COLONNE = ["obiettivo", "priorità", "misura", "scadenza", "primo passo", "stato"]
PRIORITA = ("Must", "Should", "Could")
STATI = ("da fare", "in corso", "fatto")
PAROLE_VAGHE = ("migliorare", "capire", "pensare", "provare", "di più", "meglio", "informarmi", "impegnarmi")
MASSIMO_IN_CORSO = 3       # come il limite di lavori in corso di una board Kanban
MESI_MASSIMI = 24          # oltre, conviene dividere l'obiettivo in tappe intermedie
MESI_PRIMO_OBIETTIVO = 3   # almeno un obiettivo vicino


def celle(riga):
    return [c.strip() for c in riga.strip().strip("|").split("|")]


def leggi_piano(testo):
    """Trova la tabella del piano e restituisce una lista di dizionari, uno per obiettivo."""
    righe = [r for r in testo.splitlines() if r.strip().startswith("|")]
    for i, riga in enumerate(righe):
        intestazione = [c.lower() for c in celle(riga)]
        if intestazione == COLONNE:
            dati = righe[i + 2:]           # salta la riga |---|---|
            return [dict(zip(COLONNE, celle(r))) for r in dati]
    raise ValueError("tabella non trovata: servono le colonne " + " | ".join(c.capitalize() for c in COLONNE))


def leggi_data(testo):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", testo):
        return None
    try:
        return date.fromisoformat(testo)
    except ValueError:
        return None


def mesi_tra(inizio, fine):
    return (fine.year - inizio.year) * 12 + fine.month - inizio.month


def controlla(obiettivi, oggi):
    problemi = []
    if not obiettivi:
        return [("DA SISTEMARE", "il piano non contiene obiettivi")]
    for n, o in enumerate(obiettivi, start=1):
        nome = f"obiettivo {n}"
        if any(not o.get(c) or "..." in o.get(c, "") for c in COLONNE):
            problemi.append(("DA SISTEMARE", f"{nome}: tutte le colonne vanno completate"))
            continue
        nome = f"obiettivo {n} \"{o['obiettivo']}\""
        if o["priorità"] not in PRIORITA:
            problemi.append(("DA SISTEMARE", f"{nome}: priorità da scegliere tra {', '.join(PRIORITA)}"))
        if o["stato"].lower() not in STATI:
            problemi.append(("DA SISTEMARE", f"{nome}: stato da scegliere tra {', '.join(STATI)}"))
        scadenza = leggi_data(o["scadenza"])
        if scadenza is None:
            problemi.append(("DA SISTEMARE", f"{nome}: scadenza nel formato AAAA-MM-GG"))
            continue
        o["data"] = scadenza
        if scadenza < oggi and o["stato"].lower() != "fatto":
            problemi.append(("ATTENZIONE", f"{nome}: scadenza passata; aggiornare lo stato o ripianificare"))
        if mesi_tra(oggi, scadenza) > MESI_MASSIMI:
            problemi.append(("ATTENZIONE", f"{nome}: oltre {MESI_MASSIMI} mesi; dividerlo in tappe intermedie"))
        vaghe = [p for p in PAROLE_VAGHE if p in o["obiettivo"].lower()]
        if vaghe and not re.search(r"\d", o["misura"]):
            problemi.append(("ATTENZIONE", f"{nome}: poco specifico (\"{vaghe[0]}\"); indicare nella misura "
                             "un numero o un risultato verificabile"))
    if any(l == "DA SISTEMARE" for l, _ in problemi):
        return problemi
    aperti = [o for o in obiettivi if o["stato"].lower() != "fatto"]
    in_corso = sum(1 for o in aperti if o["stato"].lower() == "in corso")
    if in_corso > MASSIMO_IN_CORSO:
        problemi.append(("ATTENZIONE", f"{in_corso} obiettivi in corso: con più di {MASSIMO_IN_CORSO} "
                         "insieme si rischia di non finirne nessuno"))
    if aperti and not any(mesi_tra(oggi, o["data"]) <= MESI_PRIMO_OBIETTIVO for o in aperti):
        problemi.append(("ATTENZIONE", f"nessun obiettivo entro {MESI_PRIMO_OBIETTIVO} mesi: "
                         "serve almeno una tappa vicina"))
    if aperti and not any(o["priorità"] == "Must" for o in aperti):
        problemi.append(("ATTENZIONE", "nessun obiettivo Must: quale conta di più?"))
    return problemi


def timeline(obiettivi):
    """Diagramma Mermaid timeline con gli obiettivi raggruppati per mese di scadenza."""
    per_mese = {}
    for o in sorted(obiettivi, key=lambda o: o["data"]):
        testo = o["obiettivo"].replace(":", ",") + (" (fatto)" if o["stato"].lower() == "fatto" else "")
        per_mese.setdefault(o["data"].strftime("%Y-%m"), []).append(testo)
    righe = ["```mermaid", "timeline", "    title Il mio piano orientativo"]
    righe += [f"    {mese} : " + " : ".join(testi) for mese, testi in per_mese.items()]
    return "\n".join(righe + ["```"])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Controllo del piano orientativo personale")
    parser.add_argument("piano")
    parser.add_argument("--timeline", help="file Markdown in cui scrivere la linea del tempo")
    parser.add_argument("--oggi", help="data di riferimento AAAA-MM-GG (normalmente la data di oggi)")
    argomenti = parser.parse_args(argv)
    oggi = leggi_data(argomenti.oggi) if argomenti.oggi else date.today()
    if oggi is None:
        print("Errore: --oggi nel formato AAAA-MM-GG")
        return 1
    try:
        obiettivi = leggi_piano(Path(argomenti.piano).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"Errore: {e}")
        return 1
    problemi = controlla(obiettivi, oggi)
    for livello, messaggio in problemi:
        print(f"{livello}: {messaggio}")
    da_sistemare = sum(1 for l, _ in problemi if l == "DA SISTEMARE")
    print(f"\nObiettivi: {len(obiettivi)}; da sistemare: {da_sistemare}; attenzione: {len(problemi) - da_sistemare}")
    if argomenti.timeline:
        if da_sistemare:
            print("Linea del tempo non scritta: sistemare prima il piano.")
            return 1
        Path(argomenti.timeline).write_text("# Linea del tempo del mio piano\n\n" + timeline(obiettivi) + "\n",
                                            encoding="utf-8")
        print(f"Linea del tempo scritta in {argomenti.timeline}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
