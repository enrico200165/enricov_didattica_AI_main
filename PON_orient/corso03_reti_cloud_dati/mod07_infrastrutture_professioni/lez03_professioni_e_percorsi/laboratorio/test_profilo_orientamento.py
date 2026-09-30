"""Test di profilo_orientamento.py. Esecuzione: python test_profilo_orientamento.py"""

import builtins
import contextlib
import io
import os
import tempfile

import profilo_orientamento as p

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


tutti = {a: 5 for a in p.ATTIVITA}
verifica("tutti i voti a 5: 100% per ogni professione", set(p.punteggi(tutti).values()) == {100})
verifica("tutti i voti a 1: 20% per ogni professione", set(p.punteggi({a: 1 for a in p.ATTIVITA}).values()) == {20})
verifica("ogni professione è collegata ad almeno due attività",
         all(sum(1 for _, pesi in p.ATTIVITA.values() if pesi.get(k)) >= 2 for k in p.PROFESSIONI))

voti = {a: 1 for a in p.ATTIVITA}
voti.update(cablaggio=5, indirizzi=5, diagnosi=5)
verifica("preferenza per le reti: network engineer al primo posto", list(p.punteggi(voti))[0] == "network")
voti = {a: 1 for a in p.ATTIVITA}
voti.update(container=5, costi=5, architettura=5)
verifica("preferenza per il cloud: cloud engineer al primo posto", list(p.punteggi(voti))[0] == "cloud")

v = p.leggi_voti("risposte_esempio.csv")
verifica("file di esempio: 12 risposte", len(v) == 12)
verifica("file di esempio: data engineer al primo posto con il 90%", list(p.punteggi(v).items())[0] == ("data", 90))

cartella = tempfile.mkdtemp()
incompleto = os.path.join(cartella, "r.csv")
with open(incompleto, "w", encoding="utf-8") as f:
    f.write("attivita,voto\nsql,5\n")
try:
    p.leggi_voti(incompleto)
    errore = False
except ValueError:
    errore = True
verifica("risposte mancanti segnalate", errore)

risposte = iter(["7", "abc"] + ["4"] * len(p.ATTIVITA))
originale = builtins.input
builtins.input = lambda _="": next(risposte)
with contextlib.redirect_stdout(io.StringIO()) as uscita:
    chiesti = p.chiedi_voti()
builtins.input = originale
verifica("risposte non valide richieste di nuovo", chiesti == {a: 4 for a in p.ATTIVITA}
         and uscita.getvalue().count("rispondere con un numero") == 2)

print(f"\nTest superati: {superati}, falliti: {falliti}")
