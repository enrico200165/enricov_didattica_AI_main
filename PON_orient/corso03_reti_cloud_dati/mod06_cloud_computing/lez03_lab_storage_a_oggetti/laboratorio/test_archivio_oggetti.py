"""Test di archivio_oggetti.py. Esecuzione: python test_archivio_oggetti.py
Avvia l'emulatore moto dentro il test, su una porta libera: non serve avviarlo a parte."""

import logging
import os
import socket
import tempfile
import urllib.error
import urllib.request

from botocore.exceptions import ClientError
from moto.server import ThreadedMotoServer

import archivio_oggetti as a

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def porta_libera():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def stato_http(url):
    """Codice di stato di una GET senza credenziali (proxy di sistema escluso)."""
    apri = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with apri.open(url) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""


logging.getLogger("werkzeug").setLevel(logging.ERROR)   # niente righe di registro del server
porta = porta_libera()
server = ThreadedMotoServer(ip_address="127.0.0.1", port=porta, verbose=False)
server.start()
endpoint = f"http://127.0.0.1:{porta}"
s3 = a.client(endpoint)

a.crea_bucket(s3)
verifica("bucket creato", [b["Name"] for b in s3.list_buckets()["Buckets"]] == ["biblioteca-scuola"])

chiavi = a.carica_cartella(s3, "esempi", "esempi/")
verifica("cartella caricata: 3 oggetti, sottocartella nella chiave con '/'",
         sorted(chiavi) == ["esempi/immagini/segnaposto_copertina.svg", "esempi/orari.json", "esempi/regolamento.txt"])
a.carica(s3, os.path.join("esempi", "regolamento.txt"), "documenti/regolamento.txt", {"classe": "4A"})
verifica("elenco completo: 4 oggetti", len(a.elenco(s3)) == 4)
verifica("elenco per prefisso", [k for k, _ in a.elenco(s3, "documenti/")] == ["documenti/regolamento.txt"])
verifica("dimensione uguale a quella del file",
         dict(a.elenco(s3))["esempi/orari.json"] == os.path.getsize(os.path.join("esempi", "orari.json")))

i = a.info(s3, "documenti/regolamento.txt")
verifica("tipo di contenuto ricavato dall'estensione", i["tipo"] == "text/plain")
verifica("metadati personalizzati conservati", i["metadati"] == {"classe": "4A"})
verifica("SVG con il tipo image/svg+xml", a.info(s3, "esempi/immagini/segnaposto_copertina.svg")["tipo"] == "image/svg+xml")

destinazione = os.path.join(tempfile.mkdtemp(), "copia.txt")
a.scarica(s3, "documenti/regolamento.txt", destinazione)
with open(destinazione, "rb") as f1, open(os.path.join("esempi", "regolamento.txt"), "rb") as f2:
    verifica("file scaricato identico all'originale", f1.read() == f2.read())

a.carica(s3, os.path.join("esempi", "orari.json"), "documenti/regolamento.txt")
verifica("stessa chiave: l'oggetto viene sostituito", a.info(s3, "documenti/regolamento.txt")["tipo"] == "application/json")

url_diretto = f"{endpoint}/biblioteca-scuola/esempi/regolamento.txt"
verifica("oggetto privato: 403 senza credenziali", stato_http(url_diretto)[0] == 403)
codice, corpo = stato_http(a.link_temporaneo(s3, "esempi/regolamento.txt", 60))
verifica("link firmato: 200 e contenuto", codice == 200 and corpo.startswith(b"Regolamento"))
a.rendi_pubblico(s3, "esempi/orari.json")
verifica("oggetto reso pubblico: 200 senza credenziali",
         stato_http(f"{endpoint}/biblioteca-scuola/esempi/orari.json")[0] == 200)

a.cancella(s3, "documenti/regolamento.txt")
try:
    a.info(s3, "documenti/regolamento.txt")
    codice_errore = None
except ClientError as e:
    codice_errore = e.response["Error"]["Code"]
verifica("dopo la cancellazione: 404", codice_errore == "404")

server.stop()
print(f"\nTest superati: {superati}, falliti: {falliti}")
