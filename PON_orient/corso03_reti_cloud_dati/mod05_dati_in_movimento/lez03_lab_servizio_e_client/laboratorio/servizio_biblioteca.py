"""Servizio web che espone il database della biblioteca come API JSON e serve la pagina web.

Risorse:
    GET  /                                  pagina web (static/index.html)
    GET  /api/generi                        elenco dei generi
    GET  /api/libri?cerca=...&genere=...    libri con copie totali e disponibili
    GET  /api/libri/<id>                    un libro con le sue copie
    POST /api/prestiti                      nuovo prestito: {"collocazione": "A1-2", "id_studente": 3}
    POST /api/prestiti/<id>/restituzione    restituzione di un prestito
I dati degli studenti non sono esposti: l'API restituisce solo ciò che serve alla pagina.

Uso: python servizio_biblioteca.py [porta]      (predefinita 8000; database biblioteca.db)
Il servizio ascolta solo su 127.0.0.1, cioè sul proprio PC.
"""

import datetime
import json
import os
import re
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

DATABASE = "biblioteca.db"
CARTELLA_STATICA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
TIPI = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8"}
DURATA_PRESTITO = 30


class ErroreApi(Exception):
    """Errore da restituire al client con un codice di stato HTTP e un messaggio."""

    def __init__(self, codice, messaggio):
        super().__init__(messaggio)
        self.codice = codice
        self.messaggio = messaggio


def connetti():
    connessione = sqlite3.connect(Gestore.percorso_db)
    connessione.execute("PRAGMA foreign_keys = ON")
    connessione.row_factory = sqlite3.Row
    return connessione


# ---------------------------------------------------------------- operazioni sui dati

CONSULTA_LIBRI = """
    SELECT l.id_libro AS id, l.titolo, a.nome || ' ' || a.cognome AS autore, l.anno, l.genere,
           COUNT(c.id_copia) AS copie_totali,
           SUM(c.stato <> 'smarrita' AND NOT EXISTS (
               SELECT 1 FROM prestiti p WHERE p.id_copia = c.id_copia AND p.data_restituzione IS NULL
           )) AS copie_disponibili
    FROM libri l JOIN autori a ON l.id_autore = a.id_autore
    LEFT JOIN copie c ON c.id_libro = l.id_libro
"""


def elenco_libri(c, cerca="", genere=""):
    condizioni, valori = [], []
    if cerca:
        condizioni.append("(l.titolo LIKE ? OR a.cognome LIKE ?)")
        valori += [f"%{cerca}%", f"%{cerca}%"]
    if genere:
        condizioni.append("l.genere = ?")
        valori.append(genere)
    sql = CONSULTA_LIBRI + (" WHERE " + " AND ".join(condizioni) if condizioni else "")
    sql += " GROUP BY l.id_libro ORDER BY l.titolo"
    return [dict(r) for r in c.execute(sql, valori)]


def dettaglio_libro(c, id_libro):
    libro = c.execute(CONSULTA_LIBRI + " WHERE l.id_libro = ? GROUP BY l.id_libro", (id_libro,)).fetchone()
    if libro is None:
        raise ErroreApi(404, f"libro {id_libro} inesistente")
    risultato = dict(libro)
    risultato["copie"] = [dict(r) for r in c.execute("""
        SELECT c.collocazione, c.stato,
               NOT EXISTS (SELECT 1 FROM prestiti p WHERE p.id_copia = c.id_copia AND p.data_restituzione IS NULL)
               AND c.stato <> 'smarrita' AS disponibile
        FROM copie c WHERE c.id_libro = ? ORDER BY c.collocazione""", (id_libro,))]
    for copia in risultato["copie"]:
        copia["disponibile"] = bool(copia["disponibile"])     # da 0/1 a false/true in JSON
    return risultato


def nuovo_prestito(c, dati, oggi):
    if not isinstance(dati, dict) or "collocazione" not in dati or "id_studente" not in dati:
        raise ErroreApi(400, "servono i campi collocazione e id_studente")
    if not isinstance(dati["id_studente"], int):
        raise ErroreApi(400, "id_studente deve essere un numero intero")
    try:
        data = datetime.date.fromisoformat(dati.get("data_prestito", oggi))
    except (TypeError, ValueError):
        raise ErroreApi(400, "data_prestito nel formato AAAA-MM-GG")
    copia = c.execute("SELECT id_copia, stato FROM copie WHERE collocazione = ?", (dati["collocazione"],)).fetchone()
    if copia is None:
        raise ErroreApi(404, f"nessuna copia con collocazione {dati['collocazione']}")
    if c.execute("SELECT 1 FROM studenti WHERE id_studente = ?", (dati["id_studente"],)).fetchone() is None:
        raise ErroreApi(404, f"nessuno studente con codice {dati['id_studente']}")
    if copia["stato"] == "smarrita":
        raise ErroreApi(409, "la copia risulta smarrita")
    if c.execute("SELECT 1 FROM prestiti WHERE id_copia = ? AND data_restituzione IS NULL",
                 (copia["id_copia"],)).fetchone():
        raise ErroreApi(409, "la copia è già in prestito")
    scadenza = data + datetime.timedelta(days=DURATA_PRESTITO)
    with c:                                                   # transazione
        cursore = c.execute("INSERT INTO prestiti (id_copia, id_studente, data_prestito, data_scadenza) "
                            "VALUES (?, ?, ?, ?)",
                            (copia["id_copia"], dati["id_studente"], data.isoformat(), scadenza.isoformat()))
    return {"id_prestito": cursore.lastrowid, "collocazione": dati["collocazione"],
            "data_prestito": data.isoformat(), "data_scadenza": scadenza.isoformat()}


def restituzione(c, id_prestito, dati, oggi):
    data = (dati or {}).get("data", oggi)
    prestito = c.execute("SELECT data_prestito, data_restituzione FROM prestiti WHERE id_prestito = ?",
                         (id_prestito,)).fetchone()
    if prestito is None:
        raise ErroreApi(404, f"prestito {id_prestito} inesistente")
    if prestito["data_restituzione"] is not None:
        raise ErroreApi(409, "prestito già restituito")
    if data < prestito["data_prestito"]:
        raise ErroreApi(400, "la restituzione non può precedere il prestito")
    with c:
        c.execute("UPDATE prestiti SET data_restituzione = ? WHERE id_prestito = ?", (data, id_prestito))
    return {"id_prestito": id_prestito, "data_restituzione": data}


# ---------------------------------------------------------------- HTTP

class Gestore(BaseHTTPRequestHandler):
    percorso_db = DATABASE
    oggi = None                     # data fissa per i test; None = data odierna

    def data_odierna(self):
        return self.oggi or datetime.date.today().isoformat()

    def do_GET(self):
        parti = urlsplit(self.path)
        parametri = {k: v[0] for k, v in parse_qs(parti.query).items()}
        try:
            if parti.path == "/":
                self.file_statico("index.html")
            elif parti.path.startswith("/static/"):
                self.file_statico(parti.path[len("/static/"):])
            elif parti.path == "/api/generi":
                c = connetti()
                self.json(200, [r[0] for r in c.execute("SELECT DISTINCT genere FROM libri ORDER BY genere")])
                c.close()
            elif parti.path == "/api/libri":
                c = connetti()
                self.json(200, elenco_libri(c, parametri.get("cerca", ""), parametri.get("genere", "")))
                c.close()
            elif m := re.fullmatch(r"/api/libri/(\d+)", parti.path):
                c = connetti()
                try:
                    self.json(200, dettaglio_libro(c, int(m.group(1))))
                finally:
                    c.close()
            else:
                raise ErroreApi(404, "risorsa inesistente")
        except ErroreApi as e:
            self.json(e.codice, {"errore": e.messaggio})

    def do_POST(self):
        percorso = urlsplit(self.path).path
        try:
            lunghezza = int(self.headers.get("Content-Length", 0))
            try:
                dati = json.loads(self.rfile.read(lunghezza) or b"{}")
            except json.JSONDecodeError:
                raise ErroreApi(400, "il corpo della richiesta non è JSON valido")
            c = connetti()
            try:
                if percorso == "/api/prestiti":
                    self.json(201, nuovo_prestito(c, dati, self.data_odierna()))
                elif m := re.fullmatch(r"/api/prestiti/(\d+)/restituzione", percorso):
                    self.json(200, restituzione(c, int(m.group(1)), dati, self.data_odierna()))
                else:
                    raise ErroreApi(404, "risorsa inesistente")
            finally:
                c.close()
        except ErroreApi as e:
            self.json(e.codice, {"errore": e.messaggio})

    def json(self, codice, dati):
        corpo = json.dumps(dati, ensure_ascii=False).encode("utf-8")
        self.send_response(codice)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def file_statico(self, nome):
        # solo file della cartella static, senza sottocartelle: impedisce richieste come /static/../dati
        if not re.fullmatch(r"[A-Za-z0-9_\-]+\.(html|js|css)", nome):
            raise ErroreApi(404, "file inesistente")
        percorso = os.path.join(CARTELLA_STATICA, nome)
        if not os.path.isfile(percorso):
            raise ErroreApi(404, "file inesistente")
        with open(percorso, "rb") as f:
            corpo = f.read()
        self.send_response(200)
        self.send_header("Content-Type", TIPI[os.path.splitext(nome)[1]])
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, formato, *argomenti):
        print(f"{self.command} {self.path} -> {argomenti[1] if len(argomenti) > 1 else ''}")


def avvia(porta=8000, percorso_db=DATABASE):
    Gestore.percorso_db = percorso_db
    return ThreadingHTTPServer(("127.0.0.1", porta), Gestore)


if __name__ == "__main__":
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    if not os.path.exists(DATABASE):
        sys.exit("biblioteca.db non trovato: copiarlo dalla cartella della lezione 4.1")
    server = avvia(porta)
    print(f"Servizio attivo: http://127.0.0.1:{porta}/  (Ctrl+C per terminare)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
