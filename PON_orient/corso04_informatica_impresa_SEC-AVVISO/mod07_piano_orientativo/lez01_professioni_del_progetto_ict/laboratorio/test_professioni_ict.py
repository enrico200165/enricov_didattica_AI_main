"""Test di professioni_ict.py. Esecuzione: python test_professioni_ict.py"""

import contextlib
import io
import tempfile
from pathlib import Path

import professioni_ict as p

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


attivita, professioni = p.carica_professioni()
verifica("dati: 12 attività e 8 professioni", len(attivita) == 12 and len(professioni) == 8)
verifica("ogni attività è usata da almeno una professione",
         set(attivita) == {a for pr in professioni for a in pr["attivita"]})

risposte = p.leggi_risposte("risposte_esempio.csv", attivita)
risultati = p.classifica(risposte, professioni)
verifica("esempio: prima lo sviluppatore software (3,67 su 4)",
         risultati[0][1]["nome"] == "Sviluppatore software" and risultati[0][0] == 3.67)
pari = p.classifica({a: 3 for a in attivita}, professioni)
verifica("a parità di affinità, ordine alfabetico", [r[1]["nome"] for r in pari] == sorted(r[1]["nome"] for r in pari))
verifica("esempio: ultimo lo Scrum Master", risultati[-1][1]["nome"] == "Scrum Master")
verifica("affinità come media arrotondata", p.classifica({**risposte, "facilitare": 2}, professioni)[-1][0] == 1.67)

risposte_date = iter(["", "5", "tre", "4"] + ["2"] * 11)
with contextlib.redirect_stdout(io.StringIO()) as out:
    da_questionario = p.questionario(attivita, chiedi=lambda _: next(risposte_date))
verifica("questionario: le risposte non valide si ripetono",
         da_questionario["intervistare"] == 4 and out.getvalue().count("Scrivi un numero da 1 a 4") == 3)


def errore(testo):
    with tempfile.TemporaryDirectory() as cartella:
        f = Path(cartella) / "r.csv"
        f.write_text(testo, encoding="utf-8")
        try:
            p.leggi_risposte(f, attivita)
        except p.ErroreDati as e:
            return str(e)
    return ""


verifica("attività non prevista", "non prevista" in errore("attivita,livello\ncucinare,3\n"))
verifica("livello non valido", "da 1 a 4" in errore("attivita,livello\nprogrammare,0\n"))
verifica("risposte mancanti", errore("attivita,livello\nprogrammare,3\n").startswith("mancano le risposte"))

testo = p.scheda_markdown(risposte, attivita, risultati)
verifica("scheda: attività preferite e tre professioni",
         "- scrivere codice Python (4)" in testo and testo.count("### ") == 3 and "| Scrum Master | 1.33 |" in testo)

with tempfile.TemporaryDirectory() as cartella:
    salvate = Path(cartella) / "salvate.csv"
    scheda = Path(cartella) / "scheda.md"
    sequenza = iter(["3"] * 12)
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = p.main(["--salva", str(salvate), "--scheda", str(scheda)], chiedi=lambda _: next(sequenza))
    riletti = p.leggi_risposte(salvate, attivita)
verifica("esecuzione: risposte salvate e rilette, scheda scritta",
         codice == 0 and riletti == {a: 3 for a in attivita} and "Scheda scritta" in out.getvalue())

with contextlib.redirect_stdout(io.StringIO()) as out:
    codice = p.main(["--risposte", "inesistente.csv"])
verifica("file inesistente: errore", codice == 1 and out.getvalue().startswith("Errore"))

print(f"\nTest superati: {superati}, falliti: {falliti}")
