"""Test di pianifica_sprint.py. Esecuzione: python test_pianifica_sprint.py"""

import contextlib
import io
import shutil
import tempfile
from pathlib import Path

import pianifica_sprint as ps

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


storie = ps.leggi_backlog(Path("backlog_esempio.md").read_text(encoding="utf-8"))
verifica("backlog di esempio: 16 righe con US-00", len(storie) == 16)
verifica("US-01: Must, 5 punti, 3 criteri",
         (storie["US-01"]["priorita"], storie["US-01"]["stima"], storie["US-01"]["criteri"]) == ("must", 5, 3))
verifica("US-07 senza criteri, US-00 senza stima", storie["US-07"]["criteri"] == 0 and storie["US-00"]["stima"] is None)

problemi, totale = ps.controlla(storie, ["US-01", "US-02", "US-03"], 12, "Niente sovrapposizioni")
verifica("scelta corretta: nessun problema, 10 punti", problemi == [] and totale == 10)
problemi, totale = ps.controlla(storie, ["US-01", "US-02", "US-04"], 10, "x")
verifica("Must esclusa mentre si sceglie una Should", problemi == [("ATTENZIONE", "storie Must lasciate fuori mentre "
                                                                    "se ne scelgono di priorità minore: US-03")])
problemi, _ = ps.controlla(storie, ["US-01", "US-02", "US-03", "US-04"], 10, "x")
verifica("capacità superata", ("ATTENZIONE", "impegno di 12 punti oltre la capacità di 10") in problemi)
problemi, _ = ps.controlla(storie, ["US-00", "US-07", "US-99"], 20, "")
messaggi = [m for _, m in problemi]
verifica("storia già fatta, senza stima, senza criteri, inesistente, senza obiettivo",
         {"US-00 è già fatta", "US-00 non ha una stima (planning poker, lezione 3.3)",
          "US-07 non ha criteri di accettazione (lezione 2.2)", "US-99 non è nel backlog",
          "manca l'obiettivo dello sprint (--obiettivo)"} <= set(messaggi))

testo = ps.testo_sprint(1, "Obiettivo di prova", 12, ["US-01", "US-02"], storie)
verifica("file dello sprint: tabella e compiti",
         "| US-01 | Nessuna prenotazione sovrapposta | 5 |" in testo and "### US-02 Prenotazioni di un giorno" in testo
         and "Obiettivo dello sprint: Obiettivo di prova" in testo)

with tempfile.TemporaryDirectory() as d:
    shutil.copy("backlog_esempio.md", Path(d) / "backlog.md")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = ps.main([str(Path(d) / "backlog.md"), "--numero", "1", "--capacita", "12",
                          "--storie", "us-01", "US-02", "US-03", "--obiettivo", "Prova"])
    verifica("esecuzione: codici in minuscolo accettati e sprint1.md scritto",
             codice == 0 and (Path(d) / "sprint1.md").exists())
    with contextlib.redirect_stdout(io.StringIO()):
        codice = ps.main([str(Path(d) / "backlog.md"), "--numero", "2", "--capacita", "12", "--storie", "US-07"])
    verifica("esecuzione: con problemi da sistemare il file non viene scritto",
             codice == 1 and not (Path(d) / "sprint2.md").exists())

print(f"\nTest superati: {superati}, falliti: {falliti}")
