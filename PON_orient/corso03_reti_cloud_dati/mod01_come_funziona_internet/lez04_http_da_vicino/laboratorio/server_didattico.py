"""Piccolo server web didattico per osservare richieste e risposte HTTP.

Uso: python server_didattico.py      poi http://127.0.0.1:8000 nel browser, o le richieste di richieste.http

Percorsi:
  GET  /                  pagina HTML
  GET  /saluto?nome=Anna  testo semplice, con parametro nell'indirizzo
  GET  /api/ora           dati JSON
  POST /api/messaggi      riceve un messaggio JSON e lo restituisce con un numero (codice 201)
  GET  /api/messaggi      elenco dei messaggi ricevuti
  GET  /vecchia-pagina    reindirizzamento permanente (codice 301) verso /
  GET  /contatore         conta le visite con un cookie
  qualsiasi altro         pagina non trovata (codice 404)
Il server stampa nel terminale ogni richiesta ricevuta, con le intestazioni.
Solo libreria standard di Python.
"""

import json
from datetime import datetime
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

MESSAGGI = []


class Gestore(BaseHTTPRequestHandler):
    server_version = "ServerDidattico/1.0"
    mostra_richieste = True

    def rispondi(self, codice, corpo=b"", tipo="text/plain; charset=utf-8", intestazioni=()):
        self.send_response(codice)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        for nome, valore in intestazioni:
            self.send_header(nome, valore)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(corpo)

    def rispondi_json(self, codice, dati):
        corpo = json.dumps(dati, ensure_ascii=False, indent=2).encode("utf-8")
        self.rispondi(codice, corpo, "application/json; charset=utf-8")

    def mostra(self):
        if self.mostra_richieste:
            print(f"\n>>> {self.requestline}")
            for nome, valore in self.headers.items():
                print(f"    {nome}: {valore}")

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        self.mostra()
        parti = urlsplit(self.path)
        parametri = parse_qs(parti.query)
        if parti.path == "/":
            pagina = ("<!doctype html><html lang='it'><head><meta charset='utf-8'><title>Server didattico</title>"
                      "</head><body><h1>Server didattico</h1><p>Prova <a href='/saluto?nome=Anna'>/saluto</a>, "
                      "<a href='/api/ora'>/api/ora</a>, <a href='/contatore'>/contatore</a>.</p></body></html>")
            self.rispondi(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        elif parti.path == "/saluto":
            nome = parametri.get("nome", ["sconosciuto"])[0]
            self.rispondi(200, f"Ciao, {nome}!".encode("utf-8"))
        elif parti.path == "/api/ora":
            adesso = datetime.now()
            self.rispondi_json(200, {"data": adesso.strftime("%Y-%m-%d"), "ora": adesso.strftime("%H:%M:%S")})
        elif parti.path == "/api/messaggi":
            self.rispondi_json(200, MESSAGGI)
        elif parti.path == "/vecchia-pagina":
            self.rispondi(301, b"", intestazioni=[("Location", "/")])
        elif parti.path == "/contatore":
            cookie = SimpleCookie(self.headers.get("Cookie", ""))
            visite = int(cookie["visite"].value) + 1 if "visite" in cookie and cookie["visite"].value.isdigit() else 1
            self.rispondi(200, f"Visite con questo browser: {visite}".encode("utf-8"),
                          intestazioni=[("Set-Cookie", f"visite={visite}; Path=/; SameSite=Lax")])
        else:
            self.rispondi(404, "Pagina non trovata".encode("utf-8"))

    def do_POST(self):
        self.mostra()
        if urlsplit(self.path).path != "/api/messaggi":
            self.rispondi(404, "Pagina non trovata".encode("utf-8"))
            return
        lunghezza = int(self.headers.get("Content-Length", 0))
        try:
            dati = json.loads(self.rfile.read(lunghezza).decode("utf-8"))
            testo = str(dati["testo"])
        except (ValueError, KeyError, TypeError):
            self.rispondi_json(400, {"errore": "serve un oggetto JSON con il campo 'testo'"})
            return
        messaggio = {"numero": len(MESSAGGI) + 1, "testo": testo}
        MESSAGGI.append(messaggio)
        self.rispondi_json(201, messaggio)

    def log_message(self, formato, *argomenti):
        if self.mostra_richieste:
            print("<<< risposta:", formato % argomenti)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Gestore)
    print("Server su http://127.0.0.1:8000 (Ctrl+C per terminare)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer fermato.")
