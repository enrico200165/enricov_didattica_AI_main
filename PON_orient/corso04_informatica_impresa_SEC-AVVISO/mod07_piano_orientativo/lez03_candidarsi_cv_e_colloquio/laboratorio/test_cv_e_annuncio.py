"""Test di cv_e_annuncio.py. Esecuzione: python test_cv_e_annuncio.py"""

import contextlib
import io
from pathlib import Path

import cv_e_annuncio as c

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


cv = Path("cv_esempio.md").read_text(encoding="utf-8")
verifica("CV di esempio: nessun problema", c.controlla_cv(cv) == [])

problemi = c.controlla_cv(Path("cv_da_migliorare.md").read_text(encoding="utf-8"))
messaggi = [m for _, m in problemi]
verifica("CV da migliorare: 2 da sistemare e 7 attenzioni",
         sum(1 for l, _ in problemi if l == "DA SISTEMARE") == 2 and len(problemi) == 9)
verifica("sezione mancante e parti da completare",
         "manca la sezione \"lingue\"" in messaggi and any("da completare" in m for m in messaggi))
verifica("dati non necessari: data di nascita e stato civile",
         any(m.startswith("data di nascita") for m in messaggi) and any(m.startswith("stato civile") for m in messaggi))
verifica("codice fiscale riconosciuto", any(m.startswith("codice fiscale") for _, m in c.controlla_cv(cv + "\nRSSLCU08C12H501X\n")))
verifica("fotografia riconosciuta", any(m.startswith("fotografia") for _, m in c.controlla_cv(cv + "\n![foto](foto.jpg)\n")))
verifica("e-mail mancante", ("DA SISTEMARE", "manca un indirizzo e-mail") in c.controlla_cv(cv.replace("luca.rossi.cv@example.com", "")))
verifica("CV troppo lungo", any("parole" in m for _, m in c.controlla_cv(cv + " parola" * 600)))

annuncio = Path("annuncio_stage.md").read_text(encoding="utf-8")
verifica("requisiti: 6 obbligatori e 2 graditi letti dall'annuncio", len(c.requisiti(annuncio)) == 8)
verifica("le attività non sono requisiti", "scrittura dei test automatici" not in c.requisiti(annuncio))
risultati = c.confronta(annuncio, cv)
verifica("stage: 7 requisiti su 8 presenti, manca il framework web",
         sum(1 for _, ok, _ in risultati if ok) == 7 and risultati[-1][:2] == ("Esperienza con framework web", False))
verifica("confronto senza accenti e con le radici",
         c.copertura("Programmazione in Python", "So programmare in python")[1] == []
         and c.normalizza("Capacità") == "capacita")
apprendistato = c.confronta(Path("annuncio_apprendistato.md").read_text(encoding="utf-8"), cv)
verifica("apprendistato: 2 su 5, con un falso positivo sulla parola \"città\"",
         sum(1 for _, ok, _ in apprendistato if ok) == 2 and apprendistato[2][1])

with contextlib.redirect_stdout(io.StringIO()) as out:
    codice = c.main(["annuncio", "annuncio_stage.md", "cv_esempio.md"])
verifica("esecuzione annuncio: riepilogo", codice == 0 and "Requisiti presenti nel CV: 7 su 8" in out.getvalue())
with contextlib.redirect_stdout(io.StringIO()) as out:
    codice = c.main(["annuncio", "cv_esempio.md", "cv_esempio.md"])
verifica("annuncio senza requisiti: errore", codice == 1 and "Nessun requisito" in out.getvalue())
with contextlib.redirect_stdout(io.StringIO()) as out:
    codice = c.main(["controlla", "inesistente.md"])
verifica("file inesistente: errore", codice == 1 and out.getvalue().startswith("Errore"))

print(f"\nTest superati: {superati}, falliti: {falliti}")
