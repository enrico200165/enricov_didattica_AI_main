"""Bacheca degli annunci della classe: applicazione web didattica DA CORREGGERE.

Contiene volutamente diversi errori di sicurezza, da individuare e correggere nel laboratorio 5.4.
Funziona solo in locale: python bacheca.py, poi http://127.0.0.1:8000
Solo libreria standard di Python.
"""

import sqlite3
import traceback
import urllib.parse
from http.cookies import SimpleCookie
from wsgiref.simple_server import make_server

DB = "bacheca.db"


def connessione():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def inizializza(utenti=(("anna", "tavolo-razzo-neve"), ("bruno", "fiume-lampada-otto"))):
    with connessione() as conn:
        conn.executescript("""
            DROP TABLE IF EXISTS utenti; DROP TABLE IF EXISTS annunci;
            CREATE TABLE utenti (id INTEGER PRIMARY KEY, nome TEXT UNIQUE, password TEXT);
            CREATE TABLE annunci (id INTEGER PRIMARY KEY, autore TEXT, titolo TEXT, testo TEXT);
        """)
        for nome, password in utenti:
            conn.execute(f"INSERT INTO utenti (nome, password) VALUES ('{nome}', '{password}')")


# ------------------------------------------------------------------ operazioni sui dati

def verifica_login(nome, password):
    with connessione() as conn:
        riga = conn.execute(
            f"SELECT nome FROM utenti WHERE nome = '{nome}' AND password = '{password}'").fetchone()
    return riga is not None


def crea_annuncio(autore, titolo, testo):
    with connessione() as conn:
        conn.execute(f"INSERT INTO annunci (autore, titolo, testo) VALUES ('{autore}', '{titolo}', '{testo}')")


def cerca_annunci(parola=""):
    with connessione() as conn:
        return conn.execute(
            f"SELECT * FROM annunci WHERE titolo LIKE '%{parola}%' ORDER BY id").fetchall()


def elimina_annuncio(id_annuncio, utente):
    with connessione() as conn:
        conn.execute(f"DELETE FROM annunci WHERE id = {id_annuncio}")
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
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><title>{titolo}</title></head>
<body><h1>{titolo}</h1>{corpo}</body></html>"""


def elenco_html(annunci, parola=""):
    voci = "".join(f"<li>{a['id']}. <b>{a['titolo']}</b> ({a['autore']}): {a['testo']}</li>" for a in annunci)
    return pagina("Bacheca della classe", f"<p>Ricerca: {parola}</p><ul>{voci}</ul>{MODULI}")


# ------------------------------------------------------------------ applicazione WSGI

def utente_corrente(environ):
    cookie = SimpleCookie(environ.get("HTTP_COOKIE", ""))
    return cookie["utente"].value if "utente" in cookie else None


def leggi_modulo(environ):
    lunghezza = int(environ.get("CONTENT_LENGTH") or 0)
    dati = environ["wsgi.input"].read(lunghezza).decode("utf-8")
    return {k: v[0] for k, v in urllib.parse.parse_qs(dati).items()}


def applicazione(environ, start_response):
    try:
        metodo, percorso = environ["REQUEST_METHOD"], environ.get("PATH_INFO", "/")
        query = {k: v[0] for k, v in urllib.parse.parse_qs(environ.get("QUERY_STRING", "")).items()}
        intestazioni = [("Content-Type", "text/html; charset=utf-8")]

        if metodo == "GET" and percorso == "/":
            parola = query.get("q", "")
            corpo = elenco_html(cerca_annunci(parola), parola)
            stato = "200 OK"
        elif metodo == "POST" and percorso == "/login":
            modulo = leggi_modulo(environ)
            if verifica_login(modulo.get("nome", ""), modulo.get("password", "")):
                intestazioni.append(("Set-Cookie", f"utente={modulo['nome']}; Path=/"))
                stato, corpo = "200 OK", pagina("Accesso eseguito", "<p>Benvenuto</p>")
            else:
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
            modulo = leggi_modulo(environ)
            elimina_annuncio(modulo.get("id", ""), utente)
            stato, corpo = "200 OK", pagina("Annuncio eliminato", "")
        else:
            stato, corpo = "404 Not Found", pagina("Pagina inesistente", "")
    except Exception:
        stato, corpo = "500 Internal Server Error", "<pre>" + traceback.format_exc() + "</pre>"
        intestazioni = [("Content-Type", "text/html; charset=utf-8")]
    start_response(stato, intestazioni)
    return [corpo.encode("utf-8")]


if __name__ == "__main__":
    inizializza()
    print("Bacheca su http://127.0.0.1:8000 (Ctrl+C per terminare)")
    make_server("127.0.0.1", 8000, applicazione).serve_forever()
