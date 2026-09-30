"""Test di client_api.py con un server locale che imita le due API.
Esecuzione: python test_client_api.py (non serve la connessione a Internet)."""

import json
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import client_api

superati = falliti = 0
richieste = []


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


class Simulatore(BaseHTTPRequestHandler):
    """Risposte con la stessa struttura documentata dalle due API."""

    def do_GET(self):
        parti = urllib.parse.urlsplit(self.path)
        p = dict(urllib.parse.parse_qsl(parti.query))
        richieste.append((parti.path, p, self.headers.get("User-Agent")))
        if parti.path == "/search.json":
            docs = [{"title": "Il barone rampante", "author_name": ["Italo Calvino"], "first_publish_year": 1957},
                    {"title": "Senza autore"}]
            self.invia(200, {"start": 0, "num_found": 2, "docs": docs[: int(p.get("limit", 10))]})
        elif parti.path == "/v1/forecast":
            if not -90 <= float(p["latitude"]) <= 90:
                self.invia(400, {"error": True, "reason": "Latitude must be in range of -90 to 90"})
                return
            self.invia(200, {"latitude": 41.9, "longitude": 12.5, "timezone": "Europe/Rome",
                             "current_units": {"time": "iso8601", "interval": "seconds",
                                               "temperature_2m": "°C", "wind_speed_10m": "km/h"},
                             "current": {"time": "2026-06-10T10:00", "interval": 900,
                                         "temperature_2m": 24.3, "wind_speed_10m": 7.2}})
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"errore interno non JSON")

    def invia(self, codice, dati):
        corpo = json.dumps(dati).encode("utf-8")
        self.send_response(codice)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *argomenti):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), Simulatore)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_address[1]}"

libri = client_api.cerca_libri("il barone rampante", limite=5, base=base)
verifica("ricerca: titolo, autori, anno", libri[0] == ("Il barone rampante", "Italo Calvino", 1957))
verifica("campi mancanti gestiti", libri[1] == ("Senza autore", "", None))
percorso, parametri, agente = richieste[-1]
verifica("parametri q, limit, fields nell'URL", parametri == {"q": "il barone rampante", "limit": "5",
                                                          "fields": "title,author_name,first_publish_year"})
verifica("intestazione User-Agent inviata", agente == client_api.USER_AGENT)

m = client_api.meteo_attuale(41.89, 12.49, base=base)
verifica("meteo: valori con le unità della risposta", m == {"ora": "2026-06-10T10:00", "temperatura": "24.3 °C",
                                                          "vento": "7.2 km/h"})
verifica("meteo: parametri current e timezone", richieste[-1][1]["current"] == "temperature_2m,wind_speed_10m"
         and richieste[-1][1]["timezone"] == "Europe/Rome")
try:
    client_api.meteo_attuale(200, 12.49, base=base)
    errore = ""
except RuntimeError as e:
    errore = str(e)
verifica("codice 400 con motivo JSON trasformato in errore leggibile", "400" in errore and "Latitude" in errore)
verifica("risposta 500 non JSON gestita", client_api.richiesta_json(base + "/altro", {})[0] == 500)

import time
inizio = time.monotonic()
client_api.richiesta_json(base + "/search.json", {"q": "a"})
client_api.richiesta_json(base + "/search.json", {"q": "b"})
verifica("almeno un secondo tra due richieste consecutive", time.monotonic() - inizio >= 1.0)

import io, contextlib
uscita = io.StringIO()
with contextlib.redirect_stdout(uscita):
    client_api.OPEN_LIBRARY = "http://127.0.0.1:1"          # porta chiusa: servizio irraggiungibile
    client_api.main(["libri", "x"])
verifica("servizio irraggiungibile: messaggio chiaro, nessun errore Python",
         uscita.getvalue().startswith("Servizio non raggiungibile"))

server.shutdown()
print(f"\nTest superati: {superati}, falliti: {falliti}")
