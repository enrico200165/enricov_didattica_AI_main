"""Test di registro_rischi.py. Esecuzione: python test_registro_rischi.py"""

import contextlib
import io
import shutil
import tempfile
from pathlib import Path

import registro_rischi as rr

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


verifica("livelli ai confini", [rr.livello(p) for p in (4, 5, 9, 10, 16, 20)] ==
         ["basso", "medio", "medio", "alto", "alto", "critico"])

rischi = rr.leggi_rischi("rischi_esempio.csv")
per_id = {r["id"]: r for r in rischi}
verifica("esempio: sei rischi", len(rischi) == 6)
verifica("esempio: R02 16 punti, alto", (per_id["R02"]["punteggio"], per_id["R02"]["livello"]) == (16, "alto"))
segnalazioni = rr.controlla(rischi)
verifica("esempio: R04 senza responsabile", ("R04", "DA SISTEMARE", "manca il responsabile") in segnalazioni)
verifica("esempio: R05 alto accettato e senza azione",
         {m for c, _, m in segnalazioni if c == "R05"} ==
         {"rischio alto accettato senza intervenire: va motivato", "rischio alto senza azione"})
verifica("esempio: R03 medio accettato non segnalato", not any(c == "R03" for c, _, _ in segnalazioni))
verifica("basso senza responsabile non segnalato",
         rr.controlla([{"id": "X", "livello": "basso", "strategia": "accettare", "azione": "", "responsabile": ""}]) == [])

tabella = rr.matrice(rischi)
verifica("matrice: R02 e R05 nella cella impatto 4, probabilità 4", "| **4** | R06 |  |  | R02 R05 |  |" in tabella)
verifica("matrice: sei righe di dati più intestazione", len(tabella.splitlines()) == 7)


def errore(contenuto):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "r.csv"
        f.write_text("id,rischio,probabilita,impatto,strategia,azione,responsabile\n" + contenuto, encoding="utf-8")
        try:
            rr.leggi_rischi(f)
        except rr.ErroreRischi as e:
            return str(e)
    return ""


verifica("strategia non valida", "strategia \"ignorare\"" in errore("R1,X,2,2,ignorare,,\n"))
verifica("probabilità fuori intervallo", "tra 1 e 5" in errore("R1,X,6,2,ridurre,,\n"))
verifica("id ripetuto", "ripetuto" in errore("R1,X,2,2,ridurre,a,b\nR1,Y,2,2,ridurre,a,b\n"))
verifica("strategia con maiuscola accettata", errore("R1,X,2,2,Ridurre,a,b\n") == "")

with tempfile.TemporaryDirectory() as d:
    shutil.copy("rischi_esempio.csv", d)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = rr.main([str(Path(d) / "rischi_esempio.csv")])
    righe = out.getvalue().splitlines()
    verifica("esecuzione: ordine per punteggio, R02 e R05 prima di R01", righe[1].startswith("R02") and righe[3].startswith("R01"))
    verifica("esecuzione: codice 1 con rischi da sistemare e matrice scritta",
             codice == 1 and (Path(d) / "rischi_esempio.matrice.md").exists())

print(f"\nTest superati: {superati}, falliti: {falliti}")
