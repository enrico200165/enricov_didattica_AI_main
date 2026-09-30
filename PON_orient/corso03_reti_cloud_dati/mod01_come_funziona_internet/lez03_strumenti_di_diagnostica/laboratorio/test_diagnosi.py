"""Test di diagnosi.py con un server locale (nessuna connessione a Internet). Esecuzione: python test_diagnosi.py"""

import http.server
import socket
import threading

from diagnosi import diagnosi, indirizzo_locale

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


class Risposta(http.server.BaseHTTPRequestHandler):
    codice = 200

    def do_HEAD(self):
        self.send_response(self.codice)
        self.end_headers()

    def log_message(self, *argomenti):
        pass


server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Risposta)
porta = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()

verifica("indirizzo locale in formato IPv4", len(indirizzo_locale().split(".")) == 4)

passi = diagnosi("127.0.0.1", porta, ip_locale="192.168.1.20")
verifica("tutti e quattro i passi superati", [p for p, e, _ in passi] ==
         ["configurazione", "dns", "trasporto", "applicazione"] and all(e for _, e, _ in passi))
verifica("risposta HTTP 200 riportata", "200" in passi[-1][2])

passi = diagnosi("127.0.0.1", porta, ip_locale="169.254.12.7")
verifica("indirizzo 169.254: fermo alla configurazione", len(passi) == 1 and passi[0][1] is False)

passi = diagnosi("sito-inesistente.invalid", porta, ip_locale="192.168.1.20")
verifica("nome inesistente: fermo al DNS", passi[-1][0] == "dns" and passi[-1][1] is False)

with socket.socket() as s:                      # porta libera, senza alcun servizio in ascolto
    s.bind(("127.0.0.1", 0))
    porta_chiusa = s.getsockname()[1]
passi = diagnosi("127.0.0.1", porta_chiusa, ip_locale="192.168.1.20", timeout=2)
verifica("porta chiusa: fermo al trasporto", passi[-1][0] == "trasporto" and passi[-1][1] is False)

Risposta.codice = 503
passi = diagnosi("127.0.0.1", porta, ip_locale="192.168.1.20")
verifica("errore 503 del server: problema a livello di applicazione",
         passi[-1][0] == "applicazione" and passi[-1][1] is False)
server.shutdown()

print(f"Test superati: {superati}, falliti: {falliti}")
