"""Test di servizio_biblioteca.py. Esecuzione: python test_servizio.py
Avvia il servizio su una porta libera con una copia temporanea di biblioteca.db."""

import json
import os
import shutil
import tempfile
import threading
import urllib.error
import urllib.request

import servizio_biblioteca as s

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


originale = "biblioteca.db" if os.path.exists("biblioteca.db") else os.path.join(
    "..", "..", "..", "mod04_basi_di_dati", "lez01_dati_e_modello_relazionale", "laboratorio", "biblioteca.db")
cartella = tempfile.mkdtemp()
copia = os.path.join(cartella, "biblioteca.db")
shutil.copy(originale, copia)
s.Gestore.oggi = "2026-06-10"
s.Gestore.log_message = lambda *a: None                 # nessuna stampa durante i test
server = s.avvia(0, copia)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_address[1]}"


def chiama(metodo, percorso, dati=None, grezzo=None):
    corpo = grezzo if grezzo is not None else (json.dumps(dati).encode() if dati is not None else None)
    richiesta = urllib.request.Request(base + percorso, data=corpo, method=metodo,
                                       headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(richiesta) as r:
            return r.status, r.headers.get("Content-Type"), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type"), e.read()


def api(metodo, percorso, dati=None, grezzo=None):
    codice, _, corpo = chiama(metodo, percorso, dati, grezzo)
    return codice, json.loads(corpo)


codice, tipo, corpo = chiama("GET", "/")
verifica("pagina HTML servita", codice == 200 and tipo.startswith("text/html") and b"Biblioteca" in corpo)
verifica("script JavaScript servito", chiama("GET", "/static/app.js")[1].startswith("text/javascript"))
verifica("percorso con .. rifiutato", chiama("GET", "/static/../servizio_biblioteca.py")[0] == 404)
verifica("file non previsto rifiutato", chiama("GET", "/static/biblioteca.db")[0] == 404)

codice, generi = api("GET", "/api/generi")
verifica("generi: 6, in ordine", codice == 200 and generi[0] == "avventura" and len(generi) == 6)
codice, libri = api("GET", "/api/libri")
verifica("29 libri con copie totali e disponibili", len(libri) == 29 and {"copie_totali", "copie_disponibili"} <= set(libri[0]))
per_titolo = {l["titolo"]: l for l in libri}
verifica("I promessi sposi: 3 copie, 1 disponibile (2 in prestito)",
         (per_titolo["I promessi sposi"]["copie_totali"], per_titolo["I promessi sposi"]["copie_disponibili"]) == (3, 1))
verifica("Novelle per un anno: copia smarrita, 0 disponibili", per_titolo["Novelle per un anno"]["copie_disponibili"] == 0)
verifica("ricerca per cognome dell'autore", [l["titolo"] for l in api("GET", "/api/libri?cerca=levi")[1]]
         == ["Il sistema periodico", "La tregua", "Se questo è un uomo"])
verifica("filtro per genere", len(api("GET", "/api/libri?genere=fantascienza")[1]) == 4)
verifica("parametro con apice gestito", api("GET", "/api/libri?cerca=L%27isola")[1][0]["titolo"] == "L'isola di Arturo")

codice, libro = api("GET", "/api/libri/1")
verifica("dettaglio con copie e disponibilità booleana",
         codice == 200 and [c["disponibile"] for c in libro["copie"]] == [False, True, False])
verifica("libro inesistente: 404 con messaggio JSON", api("GET", "/api/libri/999") == (404, {"errore": "libro 999 inesistente"}))
verifica("risorsa inesistente: 404", api("GET", "/api/altro")[0] == 404)

codice, p = api("POST", "/api/prestiti", {"collocazione": "A1-2", "id_studente": 41})
verifica("nuovo prestito: 201, scadenza a 30 giorni", codice == 201 and p["data_scadenza"] == "2026-07-10")
verifica("dopo il prestito I promessi sposi ha 0 copie disponibili",
         api("GET", "/api/libri/1")[1]["copie_disponibili"] == 0)
verifica("stessa copia di nuovo: 409", api("POST", "/api/prestiti", {"collocazione": "A1-2", "id_studente": 3})[0] == 409)
verifica("copia smarrita: 409", api("POST", "/api/prestiti", {"collocazione": "F3-1", "id_studente": 3})[0] == 409)
verifica("collocazione inesistente: 404", api("POST", "/api/prestiti", {"collocazione": "Z9-9", "id_studente": 3})[0] == 404)
verifica("studente inesistente: 404", api("POST", "/api/prestiti", {"collocazione": "A2-1", "id_studente": 99})[0] == 404)
verifica("campo mancante: 400", api("POST", "/api/prestiti", {"collocazione": "A2-1"})[0] == 400)
verifica("codice studente come testo: 400", api("POST", "/api/prestiti", {"collocazione": "A2-1", "id_studente": "3"})[0] == 400)
verifica("corpo non JSON: 400", api("POST", "/api/prestiti", grezzo=b"collocazione=A2-1")[0] == 400)

id_nuovo = p["id_prestito"]
verifica("restituzione: 200", api("POST", f"/api/prestiti/{id_nuovo}/restituzione", {"data": "2026-06-20"})[0] == 200)
verifica("seconda restituzione: 409", api("POST", f"/api/prestiti/{id_nuovo}/restituzione", {})[0] == 409)
verifica("restituzione di un prestito inesistente: 404", api("POST", "/api/prestiti/9999/restituzione", {})[0] == 404)
verifica("dopo la restituzione la copia è di nuovo disponibile", api("GET", "/api/libri/1")[1]["copie_disponibili"] == 1)
verifica("risposta JSON con accenti in UTF-8", "è" in chiama("GET", "/api/libri?cerca=uomo")[2].decode("utf-8"))

server.shutdown()
server.server_close()
shutil.rmtree(cartella, ignore_errors=True)
print(f"\nTest superati: {superati}, falliti: {falliti}")
