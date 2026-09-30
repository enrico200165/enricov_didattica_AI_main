"""Registro della simulazione di Scrum: velocità, precisione e qualità di ogni sprint.

Uso:
    python registro_sprint.py sprint.csv

Il file CSV ha una riga per sprint con le colonne:
    sprint       numero dello sprint
    pianificati  oggetti che il team si è impegnato a realizzare (pianificazione)
    realizzati   oggetti completati entro la fine dello sprint
    accettati    oggetti che il cliente ha accettato nella revisione

Il programma calcola:
    velocità     oggetti accettati: solo il lavoro accettato conta come fatto
    precisione   realizzati / pianificati: quanto era realistico l'impegno
    qualità      accettati / realizzati: quanto lavoro rispettava i criteri
e propone l'impegno per lo sprint successivo con la media delle ultime due
velocità, e scrive il grafico Mermaid sprint.grafico.md.
"""

import csv
import sys
from pathlib import Path


class ErroreRegistro(Exception):
    """Errore nel file del registro."""


def leggi_registro(percorso):
    righe = []
    with open(percorso, encoding="utf-8", newline="") as f:
        lettore = csv.DictReader(f)
        mancanti = {"sprint", "pianificati", "realizzati", "accettati"} - set(lettore.fieldnames or [])
        if mancanti:
            raise ErroreRegistro("colonne mancanti: " + ", ".join(sorted(mancanti)))
        for numero, riga in enumerate(lettore, start=2):
            try:
                valori = {k: int(riga[k]) for k in ("sprint", "pianificati", "realizzati", "accettati")}
            except ValueError:
                raise ErroreRegistro(f"riga {numero}: servono numeri interi") from None
            if min(valori.values()) < 0:
                raise ErroreRegistro(f"riga {numero}: valori negativi")
            if valori["accettati"] > valori["realizzati"]:
                raise ErroreRegistro(f"riga {numero}: gli accettati non possono superare i realizzati")
            righe.append(valori)
    if not righe:
        raise ErroreRegistro("nessuno sprint nel registro")
    return righe


def percentuale(parte, totale):
    return round(100 * parte / totale) if totale else 0


def analizza(righe):
    """Aggiunge a ogni riga velocità, precisione e qualità; restituisce l'impegno proposto."""
    for r in righe:
        r["velocita"] = r["accettati"]
        r["precisione"] = percentuale(r["realizzati"], r["pianificati"])
        r["qualita"] = percentuale(r["accettati"], r["realizzati"])
    ultime = [r["velocita"] for r in righe[-2:]]
    return round(sum(ultime) / len(ultime))


def grafico_mermaid(righe):
    etichette = ", ".join(f"S{r['sprint']}" for r in righe)
    massimo = max(max(r["pianificati"], r["realizzati"]) for r in righe) + 1
    return "\n".join([
        "xychart-beta",
        '    title "Pianificati (linea) e accettati (barre)"',
        f"    x-axis [{etichette}]",
        f'    y-axis "Oggetti" 0 --> {massimo}',
        "    bar [" + ", ".join(str(r["accettati"]) for r in righe) + "]",
        "    line [" + ", ".join(str(r["pianificati"]) for r in righe) + "]",
    ])


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Uso: python registro_sprint.py sprint.csv")
        return 2
    try:
        righe = leggi_registro(argv[0])
    except (ErroreRegistro, OSError) as e:
        print(f"Errore: {e}")
        return 1
    proposta = analizza(righe)
    print(f"{'Sprint':>6} {'Pianif.':>8} {'Realizz.':>9} {'Accett.':>8} {'Velocità':>9} {'Precisione':>11} {'Qualità':>8}")
    for r in righe:
        print(f"{r['sprint']:>6} {r['pianificati']:>8} {r['realizzati']:>9} {r['accettati']:>8} "
              f"{r['velocita']:>9} {r['precisione']:>10}% {r['qualita']:>7}%")
    print(f"\nImpegno proposto per il prossimo sprint: {proposta} "
          "(media della velocità degli ultimi due sprint)")
    uscita = Path(argv[0]).with_suffix(".grafico.md")
    uscita.write_text("# Andamento degli sprint\n\n```mermaid\n" + grafico_mermaid(righe) + "\n```\n",
                      encoding="utf-8")
    print(f"Grafico scritto in {uscita}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
