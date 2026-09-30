"""Test di burndown.py. Esecuzione: python test_burndown.py"""

import contextlib
import io
import tempfile
from pathlib import Path

import burndown as b

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


BACKLOG = """| ID | Titolo | Priorità | Stima | Stato |
|---|---|---|---|---|
| US-01 | Uno | Must | 5 | in corso (Giulia) |
| US-02 | Due | Must | 2 | fatto |
| US-03 | Tre | Must | 3 | da fare |
| US-04 | Quattro | Should | 2 | da fare |
"""
SPRINT = """# Sprint 1

## Storie

| ID | Titolo | Stima |
|---|---|---|
| US-01 | Uno | 5 |
| US-02 | Due | 2 |
| US-03 | Tre | 3 |

## Compiti

| US-04 | righe fuori dalla sezione Storie non contano | |
"""

verifica("punti rimanenti: 5 + 3, esclusa la storia fatta e quella fuori sprint", b.punti_rimanenti(BACKLOG, SPRINT) == 8)
try:
    b.punti_rimanenti(BACKLOG, SPRINT.replace("| US-03 | Tre | 3 |", "| US-09 | Nove | 3 |"))
    verifica("storia dello sprint assente dal backlog", False)
except ValueError as e:
    verifica("storia dello sprint assente dal backlog", "US-09" in str(e))
try:
    b.punti_rimanenti(BACKLOG, "# Sprint vuoto\n")
    verifica("sprint senza storie", False)
except ValueError:
    verifica("sprint senza storie", True)

verifica("linea ideale su 3 lezioni", b.ideale(9, 3) == [9, 6, 3, 0])
verifica("linea ideale con decimali", b.ideale(10, 4) == [10, 7.5, 5, 2.5, 0])
testo = b.grafico([("5.1", 10), ("5.2", 8)], 3)
verifica("grafico: etichette e due linee",
         "x-axis [inizio, L1, L2, L3]" in testo and "line [10.0, 6.7, 3.3, 0.0]" in testo and "line [10, 8]" in testo)

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    (d / "backlog.md").write_text(BACKLOG.replace("| fatto |", "| da fare |"), encoding="utf-8")
    (d / "sprint1.md").write_text(SPRINT, encoding="utf-8")
    csv_file = d / "burndown.csv"
    argomenti = [str(csv_file), "--backlog", str(d / "backlog.md"), "--sprint", str(d / "sprint1.md")]
    with contextlib.redirect_stdout(io.StringIO()):
        b.main(argomenti + ["--registra", "5.1"])
    (d / "backlog.md").write_text(BACKLOG, encoding="utf-8")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = b.main(argomenti + ["--registra", "5.2"])
    verifica("registrazione: due righe nel CSV", b.leggi_andamento(csv_file) == [("5.1", 10), ("5.2", 8)])
    verifica("in ritardo rispetto all'ideale (8 contro 6,7)", codice == 0 and "In ritardo di 1.3 punti" in out.getvalue())
    verifica("grafico scritto", (d / "burndown.grafico.md").exists())
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = b.main([str(d / "vuoto.csv")])
    verifica("file inesistente senza --registra: errore", codice == 1 and "nessun dato" in out.getvalue())
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = b.main([str(csv_file), "--registra", "5.3"])
    verifica("--registra senza backlog e sprint: errore", codice == 1 and "servono anche" in out.getvalue())

print(f"\nTest superati: {superati}, falliti: {falliti}")
