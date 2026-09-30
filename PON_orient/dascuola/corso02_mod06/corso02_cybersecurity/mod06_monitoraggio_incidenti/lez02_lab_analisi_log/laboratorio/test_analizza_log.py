"""Test di analizza_log.py. Esecuzione: python test_analizza_log.py

Prima parte: righe di registro scritte a mano. Seconda parte: un registro prodotto davvero
dalla bacheca, usata in una cartella temporanea con alcuni accessi sbagliati di proposito.
"""

import io
import os
import sys
import tempfile
import urllib.parse
from datetime import timedelta
from wsgiref.util import setup_testing_defaults

from analizza_log import leggi_eventi, fallimenti_ravvicinati, riuscito_dopo_fallimenti, riepilogo

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


# --- parte 1: righe scritte a mano
righe = """2026-10-07 09:00:01,100 INFO accesso riuscito: anna
2026-10-07 09:05:00,000 WARNING accesso fallito per il nome 'bruno'
2026-10-07 09:05:30,000 WARNING accesso fallito per il nome 'bruno'
2026-10-07 09:06:10,000 WARNING accesso fallito per il nome 'bruno'
2026-10-07 09:06:40,000 WARNING accesso fallito per il nome 'bruno'
2026-10-07 09:07:20,000 WARNING accesso fallito per il nome 'bruno'
2026-10-07 09:08:00,000 INFO accesso riuscito: bruno
2026-10-07 10:00:00,000 WARNING accesso fallito per il nome 'carla'
2026-10-07 10:30:00,000 WARNING accesso fallito per il nome 'carla'
2026-10-07 11:00:00,000 WARNING eliminazione non consentita: bruno, annuncio 3
2026-10-07 11:10:00,000 ERROR errore interno
Traceback (most recent call last):
  File "bacheca.py", line 1, in <module>
2026-10-07 11:20:00,000 INFO richiesta non valida: identificativo non valido
""".splitlines(keepends=True)

eventi = leggi_eventi(righe)
verifica("12 eventi letti, righe del traceback ignorate", len(eventi) == 12)
verifica("tipi riconosciuti", {e["tipo"] for e in eventi} == {"accesso riuscito", "accesso fallito",
         "eliminazione negata", "errore interno", "richiesta non valida"})
segnalazioni = fallimenti_ravvicinati(eventi, 5, timedelta(minutes=10))
verifica("5 fallimenti in poco più di 2 minuti: segnalati",
         len(segnalazioni) == 1 and segnalazioni[0][0] == "bruno" and segnalazioni[0][3] == 5)
verifica("2 fallimenti a mezz'ora di distanza: non segnalati", all(s[0] != "carla" for s in segnalazioni))
verifica("soglia 6: nessuna segnalazione", fallimenti_ravvicinati(eventi, 6, timedelta(minutes=10)) == [])
verifica("finestra di 1 minuto: nessuna segnalazione", fallimenti_ravvicinati(eventi, 5, timedelta(minutes=1)) == [])
verifica("accesso riuscito dopo 5 fallimenti", riuscito_dopo_fallimenti(eventi) == [("bruno", eventi[6]["istante"], 5)])
_, per_ora, per_utente = riepilogo(eventi)
verifica("conteggi per utente", per_utente["bruno"]["accesso fallito"] == 5 and per_utente["bruno"]["accesso riuscito"] == 1)
verifica("conteggi per ora", per_ora["2026-10-07 09:00"] == 7)

# --- parte 2: registro prodotto dalla bacheca
cartella_lab = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cartella_lab)
prova = tempfile.mkdtemp()
os.chdir(prova)                      # bacheca.log e bacheca.db vengono creati qui
import bacheca                       # noqa: E402

bacheca.DB = os.path.join(prova, "bacheca.db")
bacheca.inizializza()


def richiesta(percorso, dati, cookie=None):
    corpo = urllib.parse.urlencode(dati).encode()
    environ = {"REQUEST_METHOD": "POST", "PATH_INFO": percorso, "CONTENT_LENGTH": str(len(corpo)),
               "wsgi.input": io.BytesIO(corpo)}
    if cookie:
        environ["HTTP_COOKIE"] = cookie
    setup_testing_defaults(environ)
    esito = {}
    bacheca.applicazione(environ, lambda s, h, e=None: esito.update(stato=s, intestazioni=h))
    cookie = [v for k, v in esito["intestazioni"] if k == "Set-Cookie"]
    return esito["stato"], (cookie[0].split(";")[0] if cookie else None)


for _ in range(5):
    richiesta("/login", {"nome": "anna", "password": "tavolo-razzo"})        # password sbagliata di proposito
_, anna = richiesta("/login", {"nome": "anna", "password": "tavolo-razzo-neve"})
richiesta("/annunci", {"titolo": "Gita a Ravenna", "testo": "Autorizzazioni entro venerdì"}, anna)
_, bruno = richiesta("/login", {"nome": "bruno", "password": "fiume-lampada-otto"})
richiesta("/elimina", {"id": "1"}, bruno)                                      # annuncio di anna: negato
richiesta("/elimina", {"id": "uno"}, anna)                                     # richiesta non valida
richiesta("/elimina", {"id": "1"}, anna)
for gestore in list(bacheca.logging.getLogger().handlers):
    gestore.flush()

with open(os.path.join(prova, "bacheca.log"), encoding="utf-8") as f:
    reali = leggi_eventi(f)
per_tipo, _, _ = riepilogo(reali)
verifica("registro reale: tutti gli eventi riconosciuti", per_tipo.get("altro", 0) == 0 and len(reali) == 11)
verifica("registro reale: 5 accessi falliti segnalati", [s[3] for s in fallimenti_ravvicinati(reali)] == [5])
verifica("registro reale: eliminazione negata e richiesta non valida",
         per_tipo["eliminazione negata"] == 1 and per_tipo["richiesta non valida"] == 1)
verifica("registro reale: pubblicazione ed eliminazione dell'autrice",
         per_tipo["annuncio pubblicato"] == 1 and per_tipo["annuncio eliminato"] == 1)

print(f"Test superati: {superati}, falliti: {falliti}")
