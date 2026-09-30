"""Diagnosi di una connessione a un sito, un livello alla volta, dal basso verso l'alto.

Uso: python diagnosi.py www.wikipedia.org [porta]

Passi, nell'ordine:
  1. configurazione locale: il PC ha un indirizzo IP utilizzabile?
  2. DNS: il nome del sito si traduce in un indirizzo?
  3. trasporto: si apre una connessione TCP verso la porta del servizio?
  4. applicazione: il server risponde a una richiesta HTTP?
Alla prima verifica non superata lo script si ferma e indica dove cercare il problema.
Solo libreria standard di Python.
"""

import http.client
import socket
import ssl
import sys

SUGGERIMENTI = {
    "configurazione": "Controllare cavo o Wi-Fi e l'indirizzo IP con 'ipconfig /all' (un indirizzo 169.254.x.x indica che il DHCP non ha risposto).",
    "dns": "Controllare il nome digitato e il server DNS in 'ipconfig /all'; provare 'nslookup nome'.",
    "trasporto": "Il server non accetta connessioni su quella porta, oppure un firewall le blocca; provare 'Test-NetConnection nome -Port porta'.",
    "applicazione": "La connessione funziona ma il servizio risponde con un errore o non risponde: il problema è nel server o nell'indirizzo della pagina.",
}


def indirizzo_locale():
    """Indirizzo IP con cui il PC uscirebbe verso Internet.

    'Connettere' un socket UDP non invia alcun pacchetto: chiede solo al sistema operativo
    quale interfaccia e quale indirizzo userebbe per quella destinazione."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("192.0.2.1", 9))            # indirizzo riservato alla documentazione
        return s.getsockname()[0]


def diagnosi(host, porta=443, timeout=5, ip_locale=None):
    """Lista di (passo, esito, dettaglio); esito True, False o None (passo non eseguito)."""
    passi = []

    try:
        ip = ip_locale or indirizzo_locale()
        valido = not ip.startswith("169.254.") and ip != "0.0.0.0"
        passi.append(("configurazione", valido, f"indirizzo locale {ip}"))
    except OSError as e:
        passi.append(("configurazione", False, f"nessuna interfaccia utilizzabile ({e})"))
    if not passi[-1][1]:
        return passi

    try:
        indirizzi = sorted({a[4][0] for a in socket.getaddrinfo(host, porta, type=socket.SOCK_STREAM)})
        passi.append(("dns", True, f"{host} -> {', '.join(indirizzi)}"))
    except socket.gaierror as e:
        passi.append(("dns", False, f"nome non risolto ({e.strerror})"))
        return passi

    try:
        with socket.create_connection((host, porta), timeout=timeout):
            passi.append(("trasporto", True, f"connessione TCP alla porta {porta} riuscita"))
    except OSError as e:
        passi.append(("trasporto", False, f"connessione alla porta {porta} non riuscita ({e.__class__.__name__})"))
        return passi

    try:
        if porta == 443:
            conn = http.client.HTTPSConnection(host, porta, timeout=timeout, context=ssl.create_default_context())
        else:
            conn = http.client.HTTPConnection(host, porta, timeout=timeout)
        conn.request("HEAD", "/", headers={"User-Agent": "diagnosi-didattica"})
        risposta = conn.getresponse()
        conn.close()
        passi.append(("applicazione", risposta.status < 500, f"risposta HTTP {risposta.status} {risposta.reason}"))
    except (OSError, http.client.HTTPException) as e:
        passi.append(("applicazione", False, f"nessuna risposta HTTP valida ({e.__class__.__name__})"))
    return passi


def stampa(passi):
    for passo, esito, dettaglio in passi:
        segno = "OK     " if esito else "ERRORE "
        print(f"{segno} {passo:<15} {dettaglio}")
    ultimo = passi[-1]
    if not ultimo[1]:
        print("\nDa verificare:", SUGGERIMENTI[ultimo[0]])
    else:
        print("\nTutti i livelli funzionano.")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        sys.exit(2)
    stampa(diagnosi(sys.argv[1], int(sys.argv[2]) if len(sys.argv) == 3 else 443))
