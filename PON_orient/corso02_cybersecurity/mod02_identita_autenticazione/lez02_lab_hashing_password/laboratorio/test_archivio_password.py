"""Test automatici di archivio_password.py: eseguire con  python test_archivio_password.py"""
import os
import tempfile

from archivio_password import Archivio, crea_record, verifica_password

superati = 0
falliti = 0


def verifica(descrizione, ottenuto, atteso):
    global superati, falliti
    if ottenuto == atteso:
        superati += 1
        print(f"OK      {descrizione}")
    else:
        falliti += 1
        print(f"FALLITO {descrizione}: atteso {atteso!r}, ottenuto {ottenuto!r}")


r1 = crea_record("Pino-Barca-Neve-42")
r2 = crea_record("Pino-Barca-Neve-42")
verifica("password corretta accettata", verifica_password("Pino-Barca-Neve-42", r1), True)
verifica("password errata rifiutata", verifica_password("pino-barca-neve-42", r1), False)
verifica("stessa password, sali diversi", r1["sale"] != r2["sale"], True)
verifica("stessa password, valori salvati diversi", r1["hash"] != r2["hash"], True)
verifica("il record non contiene la password", "Pino" in str(r1), False)

with tempfile.TemporaryDirectory() as cartella:
    percorso = os.path.join(cartella, "utenti.json")
    a = Archivio(percorso)
    a.registra("anna", "tavolo-razzo-neve-gatto")
    verifica("login corretto", a.login("anna", "tavolo-razzo-neve-gatto"), True)
    verifica("login con password errata", a.login("anna", "tavolo"), False)
    verifica("login di utente inesistente", a.login("carlo", "qualsiasi"), False)
    b = Archivio(percorso)   # riapertura del file salvato
    verifica("login dopo la riapertura del file", b.login("anna", "tavolo-razzo-neve-gatto"), True)
    try:
        b.registra("anna", "altra")
        verifica("registrazione doppia rifiutata", False, True)
    except ValueError:
        verifica("registrazione doppia rifiutata", True, True)

print(f"Test superati: {superati}, falliti: {falliti}")
