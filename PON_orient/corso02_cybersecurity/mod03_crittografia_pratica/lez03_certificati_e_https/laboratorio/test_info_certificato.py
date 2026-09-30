"""Test di info_certificato.py con una piccola autorità di certificazione di prova, tutta locale.

Richiede il comando openssl (incluso in Git for Windows: C:\\strumenti\\PortableGit\\usr\\bin\\openssl.exe).
Esecuzione: python test_info_certificato.py
Nessuna connessione a Internet: il server di prova ascolta solo su 127.0.0.1.
"""

import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

from info_certificato import leggi_certificato, durata_giorni, giorni_rimanenti

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def openssl(*argomenti, cartella):
    subprocess.run(["openssl", *argomenti], cwd=cartella, check=True, capture_output=True)


def crea_pki(d):
    """Autorità radice di prova e certificato per 'localhost' firmato da essa."""
    openssl("req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", "ca.key", "-out", "ca.crt",
            "-days", "30", "-subj", "/O=Scuola di prova/CN=CA di prova del laboratorio", cartella=d)
    openssl("req", "-newkey", "rsa:2048", "-nodes", "-keyout", "server.key", "-out", "server.csr",
            "-subj", "/CN=localhost", cartella=d)
    (d / "ext.cnf").write_text("subjectAltName=DNS:localhost\n", encoding="ascii")
    openssl("x509", "-req", "-in", "server.csr", "-CA", "ca.crt", "-CAkey", "ca.key", "-CAcreateserial",
            "-out", "server.crt", "-days", "20", "-extfile", "ext.cnf", cartella=d)


def avvia_server(d):
    """Server TLS minimo che accetta connessioni finché il test non termina."""
    contesto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contesto.load_cert_chain(d / "server.crt", d / "server.key")
    ascolto = socket.socket()
    ascolto.bind(("127.0.0.1", 0))
    ascolto.listen()

    def servi():
        while True:
            try:
                conn, _ = ascolto.accept()
            except OSError:
                return
            try:
                with contesto.wrap_socket(conn, server_side=True) as tls:
                    tls.recv(1)
            except (ssl.SSLError, OSError):
                pass

    threading.Thread(target=servi, daemon=True).start()
    return ascolto, ascolto.getsockname()[1]


if shutil.which("openssl") is None:
    print("Comando openssl non trovato: aggiungere al PATH la cartella usr\\bin di Git for Windows.")
    sys.exit(2)

with tempfile.TemporaryDirectory() as cartella:
    d = Path(cartella)
    crea_pki(d)
    ascolto, porta = avvia_server(d)

    fiducia = ssl.create_default_context(cafile=str(d / "ca.crt"))
    info = leggi_certificato("localhost", porta, contesto=fiducia)
    verifica("connessione verificata con la CA di prova", info["soggetto"]["commonName"] == "localhost")
    verifica("emittente letto correttamente", info["emittente"]["commonName"] == "CA di prova del laboratorio")
    verifica("nomi alternativi", info["nomi_alternativi"] == ["localhost"])
    verifica("durata di 20 giorni", durata_giorni(info) == 20)
    verifica("giorni rimanenti tra 18 e 20", 18 <= giorni_rimanenti(info) <= 20)
    verifica("protocollo TLS 1.2 o 1.3", info["protocollo"] in ("TLSv1.2", "TLSv1.3"))

    try:
        leggi_certificato("localhost", porta)       # fiducia predefinita: la CA di prova non è tra le radici
        verifica("CA sconosciuta rifiutata", False)
    except ssl.SSLCertVerificationError as e:
        verifica("CA sconosciuta rifiutata", "unable to get local issuer certificate" in e.verify_message)

    try:
        leggi_certificato("127.0.0.1", porta, contesto=fiducia)   # il certificato copre solo 'localhost'
        verifica("nome non corrispondente rifiutato", False)
    except ssl.SSLCertVerificationError as e:
        verifica("nome non corrispondente rifiutato", "mismatch" in e.verify_message.lower())

    ascolto.close()

print(f"Test superati: {superati}, falliti: {falliti}")
