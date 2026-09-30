"""Test di server_didattico.py e delle richieste di richieste.http. Esecuzione: python test_server_didattico.py"""

import http.client
import json
import re
import threading
from http.server import ThreadingHTTPServer

import server_didattico
from server_didattico import Gestore

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


Gestore.mostra_richieste = False
server = ThreadingHTTPServer(("127.0.0.1", 0), Gestore)
porta = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()


def richiesta(metodo, percorso, corpo=None, intestazioni=None):
    conn = http.client.HTTPConnection("127.0.0.1", porta, timeout=5)
    conn.request(metodo, percorso, body=corpo, headers=intestazioni or {})
    r = conn.getresponse()
    dati = r.read()
    conn.close()
    return r.status, dict(r.getheaders()), dati.decode("utf-8")


codice, intest, corpo = richiesta("GET", "/")
verifica("GET /: 200 e HTML", codice == 200 and intest["Content-Type"].startswith("text/html") and "<h1>" in corpo)
verifica("intestazione Server", intest["Server"].startswith("ServerDidattico/1.0"))
verifica("GET /saluto con parametro", richiesta("GET", "/saluto?nome=Giulia")[2] == "Ciao, Giulia!")
verifica("parametro con caratteri codificati", richiesta("GET", "/saluto?nome=Anna%20Maria")[2] == "Ciao, Anna Maria!")
codice, intest, corpo = richiesta("GET", "/api/ora")
verifica("GET /api/ora: JSON con data e ora", codice == 200 and set(json.loads(corpo)) == {"data", "ora"})
codice, intest, corpo = richiesta("HEAD", "/")
verifica("HEAD: intestazioni senza corpo", codice == 200 and corpo == "" and int(intest["Content-Length"]) > 0)
codice, _, corpo = richiesta("POST", "/api/messaggi", json.dumps({"testo": "prova"}), {"Content-Type": "application/json"})
verifica("POST valido: 201 e numero assegnato", codice == 201 and json.loads(corpo)["numero"] == 1)
verifica("POST senza campo testo: 400", richiesta("POST", "/api/messaggi", '{"titolo": "x"}')[0] == 400)
verifica("POST con JSON non valido: 400", richiesta("POST", "/api/messaggi", "non json")[0] == 400)
codice, intest, _ = richiesta("GET", "/vecchia-pagina")
verifica("reindirizzamento 301 verso /", codice == 301 and intest["Location"] == "/")
_, intest, corpo = richiesta("GET", "/contatore")
verifica("prima visita: cookie visite=1", corpo.endswith(": 1") and intest["Set-Cookie"].startswith("visite=1"))
_, intest, corpo = richiesta("GET", "/contatore", intestazioni={"Cookie": "visite=4"})
verifica("visita con cookie: contatore incrementato", corpo.endswith(": 5") and intest["Set-Cookie"].startswith("visite=5"))
verifica("pagina inesistente: 404", richiesta("GET", "/nulla")[0] == 404)

# le richieste del file richieste.http, eseguite come farebbe REST Client
server_didattico.MESSAGGI.clear()
testo = open("richieste.http", encoding="utf-8").read()
base = f"http://127.0.0.1:{porta}"
blocchi = testo.split("\n###")[1:]                        # ogni richiesta inizia con una riga ###
attesi = [200, 200, 200, 200, 201, 200, 400, 301, 200, 404]
ottenuti = []
for blocco in blocchi:
    righe = [r for r in blocco.strip().splitlines()[1:]]            # la prima riga è il titolo
    metodo, url = righe[0].split(" ", 1)
    url = url.replace("{{base}}", base)
    percorso = re.sub(r"^http://[^/]+", "", url)
    corpo = "\n".join(righe[righe.index("") + 1:]) if "" in righe else None
    intestazioni = dict(r.split(": ", 1) for r in righe[1:righe.index("")]) if "" in righe else {}
    ottenuti.append(richiesta(metodo, percorso, corpo, intestazioni)[0])
verifica("le 10 richieste di richieste.http danno i codici attesi", ottenuti == attesi)

server.shutdown()
print(f"Test superati: {superati}, falliti: {falliti}")
