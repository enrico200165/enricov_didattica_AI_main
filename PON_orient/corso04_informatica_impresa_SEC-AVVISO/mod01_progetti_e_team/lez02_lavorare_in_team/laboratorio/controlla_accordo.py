"""Controlla che l'accordo di team sia completo.

Uso:
    python controlla_accordo.py accordo_di_team.md

Il programma controlla la forma, non il contenuto: che ci siano tutte le
sezioni, che siano compilate, che i membri siano 4 o 5 e che non ci siano
dati di contatto personali. Le regole le decide il team.
"""

import re
import sys

SEZIONI = ["Team", "Membri", "Obiettivo comune", "Comunicazione", "Riunioni",
           "Decisioni", "Lavoro e impegni", "Conflitti", "Revisione dell'accordo"]

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
TELEFONO = re.compile(r"(?:\+?\d[\s.-]?){9,}")          # almeno 9 cifre, anche separate
DATE_E_ORARI = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}:\d{2}")


def dividi_sezioni(testo):
    """Restituisce un dizionario {titolo della sezione: righe}, per i titoli di livello 2 (##)."""
    sezioni, corrente = {}, None
    for riga in testo.splitlines():
        if riga.startswith("## "):
            corrente = riga[3:].strip()
            sezioni[corrente] = []
        elif corrente is not None:
            sezioni[corrente].append(riga)
    return sezioni


def righe_utili(righe):
    """Righe con contenuto: esclude righe vuote e suggerimenti tra parentesi quadre."""
    return [r.strip() for r in righe
            if r.strip() and not (r.strip().startswith("[") and r.strip().endswith("]"))]


def controlla(testo):
    """Restituisce l'elenco dei problemi, ciascuno come (livello, messaggio)."""
    problemi = []
    sezioni = dividi_sezioni(testo)
    for nome in SEZIONI:
        if nome not in sezioni:
            problemi.append(("DA SISTEMARE", f"manca la sezione \"{nome}\""))
            continue
        utili = righe_utili(sezioni[nome])
        if not utili:
            problemi.append(("DA SISTEMARE", f"la sezione \"{nome}\" è vuota"))
        elif any("..." in r for r in utili):
            problemi.append(("DA SISTEMARE", f"la sezione \"{nome}\" contiene ancora \"...\" da sostituire"))

    membri = [r for r in righe_utili(sezioni.get("Membri", [])) if r.startswith("- ") and "..." not in r]
    if membri and len(membri) not in (4, 5):
        livello = "ATTENZIONE" if len(membri) in (3, 6) else "DA SISTEMARE"
        problemi.append((livello, f"membri indicati: {len(membri)}; i team sono di 4 o 5 persone"))

    for numero, riga in enumerate(testo.splitlines(), start=1):
        senza_date = DATE_E_ORARI.sub(" ", riga)      # date e orari non sono numeri di telefono
        if EMAIL.search(riga) or TELEFONO.search(senza_date):
            problemi.append(("DA SISTEMARE",
                             f"riga {numero}: sembra un indirizzo di posta o un numero di telefono; "
                             "nell'accordo non vanno dati di contatto personali"))
    return problemi


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Uso: python controlla_accordo.py accordo_di_team.md")
        return 2
    try:
        with open(argv[0], encoding="utf-8") as f:
            testo = f.read()
    except OSError as e:
        print(f"Impossibile leggere il file: {e}")
        return 2
    problemi = controlla(testo)
    for livello, messaggio in problemi:
        print(f"{livello}: {messaggio}")
    da_sistemare = sum(1 for livello, _ in problemi if livello == "DA SISTEMARE")
    if not problemi:
        print("Accordo completo.")
    else:
        print(f"\nProblemi trovati: {da_sistemare} da sistemare, {len(problemi) - da_sistemare} di attenzione")
    return 0 if da_sistemare == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
