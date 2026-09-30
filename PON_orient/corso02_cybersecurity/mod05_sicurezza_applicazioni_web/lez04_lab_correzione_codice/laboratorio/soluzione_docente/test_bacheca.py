"""Test di sicurezza e di funzionamento della bacheca. Esecuzione: python test_bacheca.py

Sulla versione da correggere molti test falliscono: l'obiettivo del laboratorio è farli passare tutti.
I test usano un database temporaneo e chiamano l'applicazione direttamente, senza avviare il server.
"""

import io
import os
import sqlite3
import tempfile
import urllib.parse
from http.cookies import SimpleCookie
from wsgiref.util import setup_testing_defaults

import bacheca

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def richiesta(metodo, percorso, dati=None, cookie=None, query=""):
    """Esegue una richiesta sull'applicazione; restituisce (codice, intestazioni, corpo)."""
    corpo = urllib.parse.urlencode(dati or {}).encode("utf-8")
    environ = {"REQUEST_METHOD": metodo, "PATH_INFO": percorso, "QUERY_STRING": query,
               "CONTENT_LENGTH": str(len(corpo)), "wsgi.input": io.BytesIO(corpo)}
    if cookie:
        environ["HTTP_COOKIE"] = cookie
    setup_testing_defaults(environ)
    risposta = {}

    def start_response(stato, intestazioni, exc_info=None):
        risposta["codice"] = int(stato.split()[0])
        risposta["intestazioni"] = intestazioni

    testo = b"".join(bacheca.applicazione(environ, start_response)).decode("utf-8")
    return risposta["codice"], risposta["intestazioni"], testo


def intestazione(intestazioni, nome):
    return [v for k, v in intestazioni if k.lower() == nome.lower()]


def accedi(nome, password):
    codice, intestazioni, _ = richiesta("POST", "/login", {"nome": nome, "password": password})
    valori = intestazione(intestazioni, "Set-Cookie")
    return codice, (valori[0] if valori else "")


def solo_coppia(set_cookie):
    """Da 'nome=valore; attributi' a 'nome=valore', come lo rimanda il browser."""
    return set_cookie.split(";")[0]


def esegui():
    cartella = tempfile.mkdtemp()
    bacheca.DB = os.path.join(cartella, "prova.db")
    bacheca.inizializza()

    # --- funzionamento di base
    codice, cookie_anna = accedi("anna", "tavolo-razzo-neve")
    verifica("accesso con credenziali corrette", codice == 200 and cookie_anna)
    anna = solo_coppia(cookie_anna)
    codice, _, _ = richiesta("POST", "/annunci", {"titolo": "Ripetizioni di matematica", "testo": "Il martedì"}, anna)
    verifica("pubblicazione di un annuncio", codice == 201)

    # --- A05 Injection: dati con apostrofi (nomi e parole italiane comuni)
    codice, _, _ = richiesta("POST", "/annunci",
                             {"titolo": "Libri di Dell'Acqua", "testo": "Vendo l'antologia"}, anna)
    verifica("annuncio con apostrofo nel titolo pubblicato", codice == 201)
    codice, _, pagina = richiesta("GET", "/", query="q=" + urllib.parse.quote("Dell'Acqua"))
    verifica("ricerca con apostrofo: annuncio trovato", codice == 200 and "Acqua" in pagina)

    # --- XSS: il testo degli utenti deve comparire come testo, non come codice HTML
    richiesta("POST", "/annunci", {"titolo": "Calcolatrice", "testo": "Vendo <b>quasi nuova</b>"}, anna)
    _, _, pagina = richiesta("GET", "/")
    verifica("testo dell'annuncio codificato in HTML", "&lt;b&gt;quasi nuova&lt;/b&gt;" in pagina)
    _, _, pagina = richiesta("GET", "/", query="q=" + urllib.parse.quote("<i>"))
    verifica("parola cercata codificata in HTML", "<i>" not in pagina and "&lt;i&gt;" in pagina)

    # --- A07 Autenticazione e sessioni
    valore = SimpleCookie(cookie_anna)
    nome_cookie = next(iter(valore))
    verifica("il cookie di sessione non contiene il nome utente", "anna" not in valore[nome_cookie].value)
    verifica("il cookie di sessione è lungo e casuale (almeno 32 caratteri)", len(valore[nome_cookie].value) >= 32)
    verifica("cookie con attributo HttpOnly", "httponly" in cookie_anna.lower())
    verifica("cookie con attributo SameSite", "samesite" in cookie_anna.lower())
    codice, _, _ = richiesta("POST", "/annunci", {"titolo": "x", "testo": "y"}, "utente=anna")
    verifica("cookie costruito a mano con il nome utente: rifiutato", codice == 401)
    codice1, c1 = accedi("anna", "sbagliata")
    codice2, c2 = accedi("carla", "qualsiasi")
    verifica("password errata e utente inesistente: stessa risposta, nessun cookie",
             codice1 == codice2 == 401 and not c1 and not c2)

    # --- A04 Conservazione delle password
    with sqlite3.connect(bacheca.DB) as conn:
        contenuto = " ".join(str(v) for riga in conn.execute("SELECT * FROM utenti") for v in riga)
    verifica("password non salvate in chiaro nel database", "tavolo-razzo-neve" not in contenuto)

    # --- A01 Controllo degli accessi
    _, cookie_bruno = accedi("bruno", "fiume-lampada-otto")
    bruno = solo_coppia(cookie_bruno)
    with sqlite3.connect(bacheca.DB) as conn:
        id_anna = conn.execute("SELECT id FROM annunci WHERE titolo = 'Ripetizioni di matematica'").fetchone()[0]
    codice, _, _ = richiesta("POST", "/elimina", {"id": str(id_anna)}, bruno)
    with sqlite3.connect(bacheca.DB) as conn:
        esiste = conn.execute("SELECT COUNT(*) FROM annunci WHERE id = ?", (id_anna,)).fetchone()[0]
    verifica("un utente non può eliminare l'annuncio di un altro", codice == 403 and esiste == 1)
    codice, _, _ = richiesta("POST", "/elimina", {"id": str(id_anna)})
    verifica("eliminazione senza accesso rifiutata", codice == 401)
    codice, _, _ = richiesta("POST", "/elimina", {"id": str(id_anna)}, anna)
    with sqlite3.connect(bacheca.DB) as conn:
        esiste = conn.execute("SELECT COUNT(*) FROM annunci WHERE id = ?", (id_anna,)).fetchone()[0]
    verifica("l'autore può eliminare il proprio annuncio", codice == 200 and esiste == 0)

    # --- A10 Gestione delle condizioni eccezionali
    codice, _, pagina = richiesta("POST", "/elimina", {"id": "quarantadue"}, anna)
    verifica("identificativo non numerico: errore 400", codice == 400)
    verifica("nessun dettaglio interno nella risposta di errore",
             "Traceback" not in pagina and "sqlite3" not in pagina and ".py" not in pagina)

    # --- A02 Configurazione: intestazioni di sicurezza
    _, intestazioni, _ = richiesta("GET", "/")
    verifica("X-Content-Type-Options: nosniff", intestazione(intestazioni, "X-Content-Type-Options") == ["nosniff"])
    verifica("Content-Security-Policy presente", bool(intestazione(intestazioni, "Content-Security-Policy")))
    verifica("Referrer-Policy presente", bool(intestazione(intestazioni, "Referrer-Policy")))


try:
    esegui()
except Exception as errore:          # un errore imprevisto interrompe i test: lo si segnala come fallimento
    falliti += 1
    print("ERRORE  test interrotti da un'eccezione:", type(errore).__name__, errore)
print(f"Test superati: {superati}, falliti: {falliti}")
