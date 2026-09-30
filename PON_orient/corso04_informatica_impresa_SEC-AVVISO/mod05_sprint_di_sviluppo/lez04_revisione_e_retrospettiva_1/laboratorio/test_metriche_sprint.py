"""Test di metriche_sprint.py. Esecuzione: python test_metriche_sprint.py"""

import contextlib
import io
import tempfile
from pathlib import Path

import metriche_sprint as m

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
| US-01 | Uno | Must | 5 | fatto |
| US-02 | Due | Must | 2 | Fatto |
| US-03 | Tre | Must | 3 | in revisione (Sara) |
| US-04 | Quattro | Should | 2 | da fare |
"""


def sprint(righe):
    return "# Sprint\n\n## Storie\n\n| ID | Titolo | Stima |\n|---|---|---|\n" + "".join(
        f"| {c} | x | {s} |\n" for c, s in righe) + "\n## Compiti\n\n| US-04 | fuori sezione | 2 |\n"


verifica("storie della sezione Storie, con stima pianificata",
         m.storie_dello_sprint(sprint([("US-01", 5), ("US-02", 2), ("US-03", 3)])) == [("US-01", 5), ("US-02", 2), ("US-03", 3)])
verifica("risultato: 10 pianificati, 7 completati, US-03 non completata",
         m.risultato([("US-01", 5), ("US-02", 2), ("US-03", 3)], m.stati_backlog(BACKLOG)) == (10, 7, ["US-01", "US-02"], ["US-03"]))
verifica("la stima pianificata vale anche se nel backlog è cambiata",
         m.risultato([("US-01", 8)], m.stati_backlog(BACKLOG))[1] == 8)
try:
    m.risultato([("US-09", 1)], m.stati_backlog(BACKLOG))
    verifica("storia assente dal backlog", False)
except m.ErroreSprint:
    verifica("storia assente dal backlog", True)
verifica("percentuale con totale zero", m.percentuale(0, 0) == 0)

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    (d / "backlog.md").write_text(BACKLOG, encoding="utf-8")
    (d / "sprint1.md").write_text(sprint([("US-01", 5), ("US-02", 2), ("US-03", 3)]), encoding="utf-8")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = m.main(["chiudi", str(d / "backlog.md"), str(d / "sprint1.md")])
    verifica("chiudi: velocità 7 e storie da riportare",
             codice == 0 and "Velocità dello sprint: 7 punti" in out.getvalue() and "riportare nel backlog: US-03" in out.getvalue())
    verifica("chiudi: sezione Risultato scritta", m.leggi_risultato(d / "sprint1.md") == (10, 7))
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = m.main(["chiudi", str(d / "backlog.md"), str(d / "sprint1.md")])
    verifica("sprint già chiuso non viene chiuso di nuovo", codice == 1 and "già chiuso" in out.getvalue())

    # lo sprint 2 riprende US-03 e aggiunge US-04; nel frattempo il backlog cambia
    (d / "backlog.md").write_text(BACKLOG.replace("in revisione (Sara)", "fatto").replace("| da fare |", "| fatto |"),
                                  encoding="utf-8")
    (d / "sprint2.md").write_text(sprint([("US-03", 3), ("US-04", 2)]), encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()):
        m.main(["chiudi", str(d / "backlog.md"), str(d / "sprint2.md")])
    verifica("il risultato dello sprint 1 resta quello registrato", m.leggi_risultato(d / "sprint1.md") == (10, 7))
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = m.main(["confronta", str(d / "sprint1.md"), str(d / "sprint2.md")])
    testo = out.getvalue()
    verifica("confronta: variazione -2 e capacità proposta 6",
             codice == 0 and "rispetto allo sprint precedente: -2 punti" in testo and "velocità): 6 punti" in testo)
    (d / "sprint3.md").write_text(sprint([("US-04", 2)]), encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = m.main(["confronta", str(d / "sprint3.md")])
    verifica("confronta uno sprint non chiuso: errore", codice == 1 and "non ancora chiuso" in out.getvalue())
    with contextlib.redirect_stdout(io.StringIO()):
        codice = m.main(["apri"])
    verifica("comando sconosciuto: messaggio d'uso", codice == 2)

print(f"\nTest superati: {superati}, falliti: {falliti}")
