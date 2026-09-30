"""Cerca i segnali di debito tecnico nel codice Python del progetto.

Uso, nella cartella del progetto:
    python debito_tecnico.py
    python debito_tecnico.py C:\\corso-impresa\\progetto_orione --righe 25 --registro docs\\debito_tecnico.md

Segnali cercati nei file .py (esclusa la cartella tests):
    - funzioni più lunghe di N righe (predefinito 25): difficili da capire e da provare
    - funzioni con più di 6 parametri
    - funzioni e classi senza docstring
    - commenti TODO, FIXME, XXX: lavoro lasciato in sospeso
I segnali non sono errori: sono punti da valutare, e il team decide se e
quando intervenire. Con --registro il programma scrive l'elenco in un file
Markdown, da tenere nel repository e aggiornare.
"""

import argparse
import ast
import re
import sys
from pathlib import Path

IN_SOSPESO = re.compile(r"#.*\b(TODO|FIXME|XXX)\b(.*)")
MAX_PARAMETRI = 6


def analizza_file(percorso, max_righe):
    """Restituisce l'elenco dei segnali del file: (riga, tipo, descrizione)."""
    testo = Path(percorso).read_text(encoding="utf-8")
    albero = ast.parse(testo, filename=str(percorso))
    segnali = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if ast.get_docstring(nodo) is None and not nodo.name.startswith("_"):
                genere = "classe" if isinstance(nodo, ast.ClassDef) else "funzione"
                segnali.append((nodo.lineno, "documentazione", f"{genere} {nodo.name} senza docstring"))
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lunghezza = nodo.end_lineno - nodo.lineno + 1
            if lunghezza > max_righe:
                segnali.append((nodo.lineno, "lunghezza",
                                f"funzione {nodo.name} di {lunghezza} righe (massimo {max_righe}): dividerla?"))
            parametri = len(nodo.args.args) + len(nodo.args.kwonlyargs)
            if parametri > MAX_PARAMETRI:
                segnali.append((nodo.lineno, "parametri",
                                f"funzione {nodo.name} con {parametri} parametri (massimo {MAX_PARAMETRI})"))
    for numero, riga in enumerate(testo.splitlines(), start=1):
        trovato = IN_SOSPESO.search(riga)
        if trovato:
            segnali.append((numero, "in sospeso", f"{trovato.group(1)}{trovato.group(2).rstrip()}"))
    return sorted(segnali)


def analizza_progetto(cartella, max_righe):
    """Restituisce {nome del file: segnali} per i .py del progetto, esclusi test e cartelle nascoste."""
    risultati = {}
    base = Path(cartella)
    for percorso in sorted(base.rglob("*.py")):
        relativo = percorso.relative_to(base)
        if relativo.parts[0] in ("tests", ".venv") or any(p.startswith(".") for p in relativo.parts):
            continue
        risultati[str(relativo)] = analizza_file(percorso, max_righe)
    return risultati


def registro_markdown(risultati):
    righe = ["# Registro del debito tecnico", "",
             "Generato con debito_tecnico.py. Per ogni segnale il team decide: intervenire subito, "
             "creare una storia tecnica nel backlog, o accettarlo motivando.", "",
             "| File | Riga | Tipo | Descrizione | Decisione |", "|---|---|---|---|---|"]
    for nome, segnali in risultati.items():
        righe += [f"| {nome} | {riga} | {tipo} | {descrizione} | |" for riga, tipo, descrizione in segnali]
    return "\n".join(righe) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Segnali di debito tecnico")
    parser.add_argument("cartella", nargs="?", default=".")
    parser.add_argument("--righe", type=int, default=25, help="lunghezza massima di una funzione")
    parser.add_argument("--registro", help="file Markdown in cui scrivere il registro")
    argomenti = parser.parse_args(argv)
    try:
        risultati = analizza_progetto(argomenti.cartella, argomenti.righe)
    except (OSError, SyntaxError) as e:
        print(f"Errore: {e}")
        return 1
    totale = 0
    for nome, segnali in risultati.items():
        for riga, tipo, descrizione in segnali:
            print(f"{nome}:{riga:<5} {tipo:<15} {descrizione}")
        totale += len(segnali)
    print(f"\nFile analizzati: {len(risultati)}; segnali: {totale}")
    if argomenti.registro:
        Path(argomenti.registro).write_text(registro_markdown(risultati), encoding="utf-8")
        print(f"Registro scritto in {argomenti.registro}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
