"""Test di monitoraggio.py. Esecuzione: python test_monitoraggio.py"""

import os
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import monitoraggio as m

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


r = m.analizza("registro_controlli_esempio.csv")
verifica("1440 controlli, uno al minuto per un giorno", r["controlli"] == 1440)
verifica("16 controlli falliti: disponibilità 98,89%", round(r["disponibilita_misurata"], 4) == round(1424 / 1440, 4))
verifica("due interruzioni, 16 minuti di fermo", (r["interruzioni"], r["fermo_secondi"]) == (2, 960))
verifica("MTTR 8 minuti", r["mttr_secondi"] == 480)
verifica("MTBF: tempo di funzionamento diviso per il numero di guasti",
         r["mtbf_secondi"] == (1439 * 60 - 960) / 2)
verifica("95° percentile maggiore della mediana (ore di lezione più lente)",
         r["risposta_95_ms"] > r["risposta_mediana_ms"])

verifica("MTBF 999 h, MTTR 1 h: disponibilità 99,9%", m.disponibilita_attesa(999, 1) == 0.999)
verifica("PUE: 150 kW totali, 100 kW informatici = 1,5", m.pue(150, 100) == 1.5)

cartella = tempfile.mkdtemp()
p = os.path.join(cartella, "r.csv")
with open(p, "w", encoding="utf-8") as f:
    f.write("istante,riuscito,millisecondi,esito\n2026-01-01T10:00:00,1,10,200\n"
            "2026-01-01T10:01:00,0,3000,TimeoutError\n2026-01-01T10:02:00,0,3000,TimeoutError\n")
r2 = m.analizza(p)
verifica("interruzione ancora in corso alla fine del registro", r2["interruzioni"] == 1 and r2["fermo_secondi"] == 60)


class Prova(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200 if self.path == "/ok" else 503)
        self.end_headers()

    def log_message(self, *a):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), Prova)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_address[1]}"
verifica("controllo riuscito", m.controlla(base + "/ok")[0] is True)
verifica("risposta 503: controllo fallito con il codice", m.controlla(base + "/altro")[::2] == (False, 503))
server.shutdown()
server.server_close()
esito = m.controlla(base + "/ok", timeout=1)
verifica("servizio spento: controllo fallito con il tipo di errore", esito[0] is False and isinstance(esito[2], str))

registro = os.path.join(cartella, "reg.csv")
server = ThreadingHTTPServer(("127.0.0.1", 0), Prova)
threading.Thread(target=server.serve_forever, daemon=True).start()
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    m.registra(f"http://127.0.0.1:{server.server_address[1]}/ok", 3, 0.1, registro)
server.shutdown()
verifica("registrazione: 3 controlli nel file CSV", m.analizza(registro)["controlli"] == 3)

print(f"\nTest superati: {superati}, falliti: {falliti}")
