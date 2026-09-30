"""Misura delle fasi di una richiesta web: DNS, connessione TCP, negoziazione TLS, attesa, scaricamento.

Uso: python misura_richiesta.py https://www.wikipedia.org/

Sono le stesse fasi che la scheda Rete (Network) dei DevTools mostra per ogni richiesta.
Solo libreria standard di Python.
"""

import socket
import ssl
import sys
import time
from urllib.parse import urlsplit


def misura(url, contesto_tls=None, timeout=10):
    """Restituisce un dizionario con indirizzo, codice di stato, byte ricevuti e durata di ogni fase in millisecondi."""
    parti = urlsplit(url)
    sicuro = parti.scheme == "https"
    host = parti.hostname
    porta = parti.port or (443 if sicuro else 80)
    percorso = parti.path or "/"
    if parti.query:
        percorso += "?" + parti.query
    fasi = {}

    t0 = time.perf_counter()
    indirizzi = socket.getaddrinfo(host, porta, type=socket.SOCK_STREAM)        # 1. DNS
    t1 = time.perf_counter()
    fasi["DNS"] = t1 - t0

    errore = None                                                               # 2. connessione TCP
    for famiglia, _, _, _, indirizzo in indirizzi:      # si prova ogni indirizzo (IPv6 e IPv4) finché uno risponde
        sock = socket.socket(famiglia, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect(indirizzo)
            break
        except OSError as e:
            errore = e
            sock.close()
    else:
        raise errore
    t2 = time.perf_counter()
    fasi["Connessione TCP"] = t2 - t1

    if sicuro:                                                                  # 3. negoziazione TLS
        contesto = contesto_tls or ssl.create_default_context()
        sock = contesto.wrap_socket(sock, server_hostname=host)
        t3 = time.perf_counter()
        fasi["TLS"] = t3 - t2
    else:
        t3 = t2

    richiesta = (f"GET {percorso} HTTP/1.1\r\nHost: {host}\r\n"                # 4. invio e attesa
                 f"User-Agent: misura-richiesta/1.0\r\nConnection: close\r\n\r\n")
    sock.sendall(richiesta.encode("ascii"))
    primo_blocco = sock.recv(65536)
    t4 = time.perf_counter()
    fasi["Attesa della risposta"] = t4 - t3

    ricevuti = len(primo_blocco)                                                # 5. scaricamento
    while True:
        blocco = sock.recv(65536)
        if not blocco:
            break
        ricevuti += len(blocco)
    t5 = time.perf_counter()
    fasi["Scaricamento"] = t5 - t4
    sock.close()

    riga_stato = primo_blocco.split(b"\r\n", 1)[0].decode("latin-1")
    return {
        "indirizzo": indirizzo[0],
        "stato": riga_stato,
        "byte": ricevuti,
        "fasi_ms": {nome: durata * 1000 for nome, durata in fasi.items()},
        "totale_ms": (t5 - t0) * 1000,
    }


def stampa(url, r):
    print(f"URL:        {url}")
    print(f"Indirizzo:  {r['indirizzo']}")
    print(f"Risposta:   {r['stato']}  ({r['byte']} byte, intestazioni comprese)")
    for nome, ms in r["fasi_ms"].items():
        barra = "#" * max(1, round(ms / r["totale_ms"] * 40))
        print(f"  {nome:<22} {ms:8.1f} ms  {barra}")
    print(f"  {'Totale':<22} {r['totale_ms']:8.1f} ms")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    stampa(sys.argv[1], misura(sys.argv[1]))
