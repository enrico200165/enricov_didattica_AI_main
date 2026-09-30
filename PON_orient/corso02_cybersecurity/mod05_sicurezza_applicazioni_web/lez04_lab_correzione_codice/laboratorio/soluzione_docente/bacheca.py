"""Bacheca degli annunci della classe: versione CORRETTA (soluzione per il docente).

Ogni correzione è indicata con un commento "CORREZIONE" e la categoria OWASP Top 10:2025.
Funziona solo in locale: python bacheca.py, poi http://127.0.0.1:8000
Solo libreria standard di Python.
"""

import hashlib
import hmac
import html
import logging
import secrets
import sqlite3
import urllib.parse
from http.cookies import SimpleCookie
from wsgiref.simple_server import make_server

DB = "bacheca.db"
ITERAZIONI = 600_000
NOME_COOKIE = "sessione"

# CORREZIONE A09/A10: gli errori si registrano nel log del server, non si mostrano all'utente
logging.basicConfig(filename="bacheca.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

# CORREZIONE A02: intestazioni di sicurezza su tutte le risposte
INTESTAZIONI_SICUREZZA = [
    ("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'; form-action 'self'"),
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
]


class ErroreRichiesta(Exception):
    """Errore dovuto ai dati della richiesta: produce una risposta 400."""


def connessione():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# CORREZIONE A04/A07: password conservate con sale e funzione lenta (lezione 2.2)
def hash_password(password, sale=None):
    sale = sale or secrets.token_bytes(16)
    valore = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), sale, ITERAZIONI)
    return sale.hex(), valore.hex()


def inizializza(utenti=(("anna", "tavolo-razzo-neve"), ("bruno", "fiume-lampada-otto"))):
    with connessione() as conn:
        conn.executescript("""
            DROP TABLE IF EXISTS utenti; DROP TABLE IF EXISTS annunci; DROP TABLE IF EXISTS sessioni;
            CREATE TABLE utenti (id INTEGER PRIMARY KEY, nome TEXT UNIQUE, sale TEXT, hash TEXT);
            CREATE TABLE annunci (id INTEGER PRIMARY KEY, autore TEXT, titolo TEXT, testo TEXT);
            CREATE TABLE sessioni (token TEXT PRIMARY KEY, nome TEXT);
        """)
        for nome, password in utenti:
            sale, valore = hash_password(password)
            # CORREZIONE A05: query parametriche ovunque
            conn.execute("INSERT INTO utenti (nome, sale, hash) VALUES (?, ?, ?)", (nome, sale, valore))


# ------------------------------------------------------------------ operazioni sui dati

def verifica_login(nome, password):
    with connessione() as conn:
        riga = conn.execute("SELECT sale, hash FROM utenti WHERE nome = ?", (nome,)).fetchone()
    if riga is None:
        hash_password(password)          # stesso tempo di risposta anche per utenti inesistenti
        return False
    _, calcolato = hash_password(password, bytes.fromhex(riga["sale"]))
    return hmac.compare_digest(calcolato, riga["hash"])


# CORREZIONE A07: sessione con identificativo casuale conservato sul server
def crea_sessione(nome):
    token = secrets.token_urlsafe(32)
    with connessione() as conn:
        conn.execute("INSERT INTO sessioni (token, nome) VALUES (?, ?)", (token, nome))
    return token


def crea_annuncio(autore, titolo, testo):
    titolo, testo = titolo.strip(), testo.strip()
    # validazione: lunghezze ammesse
    if not 1 <= len(titolo) <= 100 or len(testo) > 1000:
        raise ErroreRichiesta("titolo o testo di lunghezza non valida")
    with connessione() as conn:
        conn.execute("INSERT INTO annunci (autore, titolo, testo) VALUES (?, ?, ?)", (autore, titolo, testo))


def cerca_annunci(parola=""):
    with connessione() as conn:
        return conn.execute("SELECT * FROM annunci WHERE titolo LIKE ? ORDER BY id",
                            (f"%{parola}%",)).fetchall()


# CORREZIONE A01: si elimina solo se l'annuncio appartiene all'utente
def elimina_annuncio(id_annuncio, utente):
    with connessione() as conn:
        riga = conn.execute("SELECT autore FROM annunci WHERE id = ?", (id_annuncio,)).fetchone()
        if riga is None or riga["autore"] != utente:
            return False
        conn.execute("DELETE FROM annunci WHERE id = ?", (id_annuncio,))
    return True


# ------------------------------------------------------------------ pagine

MODULI = """<form method="post" action="/login"><h2>Accesso</h2>
<label>Nome <input name="nome"></label> <label>Password <input name="password" type="password"></label>
<button>Accedi</button></form>
<form method="post" action="/annunci"><h2>Nuovo annuncio</h2>
<label>Titolo <input name="titolo"></label> <label>Testo <input name="testo"></label>
<button>Pubblica</button></form>
<form method="get" action="/"><h2>Ricerca</h2><input name="q"> <button>Cerca</button></form>
<form method="post" action="/elimina"><h2>Eliminazione</h2>
<label>Numero dell'annuncio <input name="id"></label> <button>Elimina</button></form>"""



def pagina(titolo, corpo):
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><title>{html.escape(titolo)}</title></head>
<body><h1>{html.escape(titolo)}</h1>{corpo}</body></html>"""


# CORREZIONE A05 (XSS): ogni dato inserito dagli utenti viene codificato con html.escape
def elenco_html(annunci, parola=""):
    voci = "".join(
        f"<li>{a['id']}. <b>{html.escape(a['titolo'])}</b> ({html.escape(a['autore'])}): {html.escape(a['testo'])}</li>"
        for a in annunci)
    return pagina("Bacheca della classe", f"<p>Ricerca: {html.escape(parola)}</p><ul>{voci}</ul>{MODULI}")


# ------------------------------------------------------------------ applicazione WSGI

def utente_corrente(environ):
    cookie = SimpleCookie(environ.get("HTTP_COOKIE", ""))
    if NOME_COOKIE not in cookie:
        return None
    with connessione() as conn:
        riga = conn.execute("SELECT nome FROM sessioni WHERE token = ?", (cookie[NOME_COOKIE].value,)).fetchone()
    return riga["nome"] if riga else None


def leggi_modulo(environ):
    lunghezza = int(environ.get("CONTENT_LENGTH") or 0)
    if lunghezza > 10_000:
        raise ErroreRichiesta("richiesta troppo grande")
    dati = environ["wsgi.input"].read(lunghezza).decode("utf-8")
    return {k: v[0] for k, v in urllib.parse.parse_qs(dati).items()}


def applicazione(environ, start_response):
    intestazioni = [("Content-Type", "text/html; charset=utf-8")]
    try:
        metodo, percorso = environ["REQUEST_METHOD"], environ.get("PATH_INFO", "/")
        query = {k: v[0] for k, v in urllib.parse.parse_qs(environ.get("QUERY_STRING", "")).items()}

        if metodo == "GET" and percorso == "/":
            parola = query.get("q", "")[:100]
            stato, corpo = "200 OK", elenco_html(cerca_annunci(parola), parola)
        elif metodo == "POST" and percorso == "/login":
            modulo = leggi_modulo(environ)
            nome = modulo.get("nome", "")
            if verifica_login(nome, modulo.get("password", "")):
                token = crea_sessione(nome)
                # CORREZIONE A07: HttpOnly e SameSite; con HTTPS si aggiunge anche Secure
                intestazioni.append(("Set-Cookie", f"{NOME_COOKIE}={token}; Path=/; HttpOnly; SameSite=Lax"))
                logging.info("accesso riuscito: %s", nome)
                stato, corpo = "200 OK", pagina("Accesso eseguito", "<p>Benvenuto</p>")
            else:
                logging.warning("accesso fallito per il nome %r", nome)       # A09: evento registrato
                stato, corpo = "401 Unauthorized", pagina("Accesso negato", "<p>Nome utente o password errati</p>")
        elif metodo == "POST" and percorso == "/annunci":
            utente = utente_corrente(environ)
            if not utente:
                stato, corpo = "401 Unauthorized", pagina("Accesso richiesto", "")
            else:
                modulo = leggi_modulo(environ)
                crea_annuncio(utente, modulo.get("titolo", ""), modulo.get("testo", ""))
                stato, corpo = "201 Created", pagina("Annuncio pubblicato", "")
        elif metodo == "POST" and percorso == "/elimina":
            utente = utente_corrente(environ)
            if not utente:
                stato, corpo = "401 Unauthorized", pagina("Accesso richiesto", "")
            else:
                modulo = leggi_modulo(environ)
                # CORREZIONE A10: validazione del tipo di dato prima dell'uso
                if not modulo.get("id", "").isdigit():
                    raise ErroreRichiesta("identificativo non valido")
                if elimina_annuncio(int(modulo["id"]), utente):
                    stato, corpo = "200 OK", pagina("Annuncio eliminato", "")
                else:
                    logging.warning("eliminazione non consentita: %s, annuncio %s", utente, modulo["id"])
                    stato, corpo = "403 Forbidden", pagina("Operazione non consentita", "")
        else:
            stato, corpo = "404 Not Found", pagina("Pagina inesistente", "")
    except ErroreRichiesta as errore:
        stato, corpo = "400 Bad Request", pagina("Richiesta non valida", "<p>Controllare i dati inseriti.</p>")
        logging.info("richiesta non valida: %s", errore)
        intestazioni = [("Content-Type", "text/html; charset=utf-8")]
    except Exception:
        # CORREZIONE A10: messaggio generico all'utente, dettagli solo nel log
        logging.exception("errore interno")
        stato, corpo = "500 Internal Server Error", pagina("Errore interno", "<p>Riprovare più tardi.</p>")
        intestazioni = [("Content-Type", "text/html; charset=utf-8")]
    start_response(stato, intestazioni + INTESTAZIONI_SICUREZZA)
    return [corpo.encode("utf-8")]


if __name__ == "__main__":
    inizializza()
    print("Bacheca su http://127.0.0.1:8000 (Ctrl+C per terminare)")
    make_server("127.0.0.1", 8000, applicazione).serve_forever()
