"""Test di piano_cascata.py. Esecuzione: python test_piano_cascata.py"""

import contextlib
import io
import shutil
import tempfile
from datetime import date
from pathlib import Path

import piano_cascata as p

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def piano_da(testo):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "a.csv"
        f.write_text("id,attivita,fase,durata,dipende_da\n" + testo, encoding="utf-8")
        return p.leggi_attivita(f)


lunedi = date(2026, 11, 2)
verifica("giorni lavorativi: 0 giorni dal lunedì è lo stesso lunedì", p.giorno_lavorativo(lunedi, 0) == lunedi)
verifica("giorni lavorativi: 5 giorni dal lunedì è il lunedì successivo", p.giorno_lavorativo(lunedi, 5) == date(2026, 11, 9))
verifica("giorni lavorativi: partenza di sabato spostata al lunedì", p.giorno_lavorativo(date(2026, 10, 31), 0) == lunedi)
verifica("fine di un'attività di 5 giorni dal lunedì: venerdì", p.data_fine(lunedi, 5) == date(2026, 11, 6))

piano = p.leggi_attivita("attivita_cascata.csv")
durata = p.calcola(piano)
verifica("esempio: 13 attività, 25 giorni lavorativi", len(piano) == 13 and durata == 25)
verifica("esempio: fine il 4 dicembre 2026", p.data_fine(lunedi, durata) == date(2026, 12, 4))
verifica("esempio: S2 critica, S1 con margine 4, S4 con margine 9",
         piano["S2"]["margine"] == 0 and piano["S1"]["margine"] == 4 and piano["S4"]["margine"] == 9)
verifica("esempio: T1 inizia dopo la più lunga tra S1, S2 e S3", piano["T1"]["inizio"] == piano["S2"]["fine"] == 16)

modificato = p.leggi_attivita("attivita_modificate.csv")
verifica("modifica: 38 giorni, 13 di ritardo", p.calcola(modificato) == 38)

semplice = piano_da("A,Uno,F,2,\nB,Due,F,3,A\nC,Tre,F,1,A\nD,Fine,F,0,B C\n")
p.calcola(semplice)
verifica("attività in parallelo: margine della più breve", semplice["C"]["margine"] == 2 and semplice["B"]["margine"] == 0)

testo = p.gantt_mermaid(semplice, lunedi, "Prova")
verifica("Gantt: attività critica marcata crit con data calcolata", "Due :crit, B, 2026-11-04, 3d" in testo)
verifica("Gantt: attività con margine senza crit", "Tre :C, 2026-11-04, 1d" in testo)
verifica("Gantt: traguardo nell'ultimo giorno delle attività precedenti", "Fine :milestone, D, 2026-11-06, 0d" in testo)
verifica("Gantt: esclusione dei fine settimana", "excludes weekends" in testo)


def errore(testo):
    try:
        p.calcola(piano_da(testo))
    except p.ErrorePiano as e:
        return str(e)
    return ""


verifica("dipendenza inesistente", "dipende da Z" in errore("A,Uno,F,2,Z\n"))
verifica("dipendenze circolari", "circolari" in errore("A,Uno,F,2,B\nB,Due,F,2,A\n"))
verifica("durata non numerica con numero di riga", errore("A,Uno,F,due,\n").startswith("riga 2"))
verifica("codice ripetuto", "ripetuto" in errore("A,Uno,F,2,\nA,Due,F,2,\n"))

with tempfile.TemporaryDirectory() as d:
    for nome in ("attivita_cascata.csv", "attivita_modificate.csv"):
        shutil.copy(nome, d)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = p.main([str(Path(d) / "attivita_cascata.csv"), "--confronta", str(Path(d) / "attivita_modificate.csv")])
    testo = out.getvalue()
    verifica("esecuzione: ritardo di 13 giorni e attività aggiunte",
             codice == 0 and "Ritardo sulla consegna: 13 giorni lavorativi" in testo
             and "Attività aggiunte: M1, M2, M3, M4, M5" in testo)
    verifica("esecuzione: due diagrammi scritti",
             (Path(d) / "attivita_cascata.gantt.md").exists() and (Path(d) / "attivita_modificate.gantt.md").exists())

print(f"\nTest superati: {superati}, falliti: {falliti}")
