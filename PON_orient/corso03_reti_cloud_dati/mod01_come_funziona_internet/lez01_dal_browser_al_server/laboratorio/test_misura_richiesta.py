"""Test di misura_richiesta.py con server locali HTTP e HTTPS (nessuna connessione a Internet).

Esecuzione: python test_misura_richiesta.py
Per la parte HTTPS serve il comando openssl (incluso in Git for Windows, cartella usr\\bin);
se manca, quella parte viene saltata.
"""

import http.server
import shutil
import ssl
import subprocess
import tempfile
import threading
from pathlib import Path

from misura_richiesta import misura

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


class Pagina(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        corpo = b"<p>pagina di prova</p>" * 100
        self.send_response(200 if self.path == "/" else 404)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *argomenti):
        pass


def avvia(contesto=None):
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Pagina)
    if contesto:
        server.socket = contesto.wrap_socket(server.socket, server_side=True)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]


server, porta = avvia()
r = misura(f"http://localhost:{porta}/")
verifica("HTTP: risposta 200", r["stato"] == "HTTP/1.0 200 OK")
verifica("HTTP: fasi DNS, TCP, attesa, scaricamento", list(r["fasi_ms"]) ==
         ["DNS", "Connessione TCP", "Attesa della risposta", "Scaricamento"])
verifica("HTTP: byte ricevuti comprendono il corpo di 2200 byte", r["byte"] > 2200)
verifica("HTTP: totale uguale alla somma delle fasi", abs(sum(r["fasi_ms"].values()) - r["totale_ms"]) < 1)
verifica("HTTP: pagina inesistente, risposta 404", misura(f"http://localhost:{porta}/nulla")["stato"].endswith("404 Not Found"))
server.shutdown()

if shutil.which("openssl"):
    d = Path(tempfile.mkdtemp())
    subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", str(d / "k.pem"),
                    "-out", str(d / "c.pem"), "-days", "1", "-subj", "/CN=localhost",
                    "-addext", "subjectAltName=DNS:localhost"], check=True, capture_output=True)
    lato_server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    lato_server.load_cert_chain(d / "c.pem", d / "k.pem")
    server, porta = avvia(lato_server)
    fiducia = ssl.create_default_context(cafile=str(d / "c.pem"))
    r = misura(f"https://localhost:{porta}/", contesto_tls=fiducia)
    verifica("HTTPS: risposta 200 e fase TLS misurata", r["stato"].endswith("200 OK") and "TLS" in r["fasi_ms"])
    server.shutdown()
else:
    print("(openssl non trovato: parte HTTPS saltata)")

print(f"Test superati: {superati}, falliti: {falliti}")
