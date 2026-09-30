"""Test di registro_sprint.py. Esecuzione: python test_registro_sprint.py"""

import contextlib
import io
import shutil
import tempfile
from pathlib import Path

import registro_sprint as r

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


righe = r.leggi_registro("sprint_esempio.csv")
proposta = r.analizza(righe)
verifica("esempio: tre sprint letti", [x["sprint"] for x in righe] == [1, 2, 3])
verifica("sprint 1: velocità 3, precisione 60%, qualità 50%",
         (righe[0]["velocita"], righe[0]["precisione"], righe[0]["qualita"]) == (3, 60, 50))
verifica("sprint 3: precisione e qualità 100%", (righe[2]["precisione"], righe[2]["qualita"]) == (100, 100))
verifica("impegno proposto: media di 5 e 7 = 6", proposta == 6)
verifica("un solo sprint: proposta uguale alla sua velocità",
         r.analizza([{"sprint": 1, "pianificati": 5, "realizzati": 4, "accettati": 4}]) == 4)
verifica("nessun oggetto realizzato: qualità 0 senza divisione per zero",
         r.percentuale(0, 0) == 0)

testo = r.grafico_mermaid(righe)
verifica("grafico: etichette, barre e linea",
         "x-axis [S1, S2, S3]" in testo and "bar [3, 5, 7]" in testo and "line [10, 6, 7]" in testo)
verifica("grafico: asse y oltre il massimo", 'y-axis "Oggetti" 0 --> 11' in testo)


def errore(contenuto):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "s.csv"
        f.write_text(contenuto, encoding="utf-8")
        try:
            r.leggi_registro(f)
        except r.ErroreRegistro as e:
            return str(e)
    return ""


verifica("colonna mancante", "colonne mancanti: accettati" in errore("sprint,pianificati,realizzati\n1,5,4\n"))
verifica("accettati oltre i realizzati", "non possono superare" in errore("sprint,pianificati,realizzati,accettati\n1,5,3,4\n"))
verifica("valore non numerico", errore("sprint,pianificati,realizzati,accettati\n1,cinque,3,2\n").startswith("riga 2"))
verifica("registro vuoto", "nessuno sprint" in errore("sprint,pianificati,realizzati,accettati\n"))

with tempfile.TemporaryDirectory() as d:
    shutil.copy("sprint_esempio.csv", d)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = r.main([str(Path(d) / "sprint_esempio.csv")])
    verifica("esecuzione: proposta stampata e grafico scritto",
             codice == 0 and "Impegno proposto per il prossimo sprint: 6" in out.getvalue()
             and (Path(d) / "sprint_esempio.grafico.md").exists())

print(f"\nTest superati: {superati}, falliti: {falliti}")
