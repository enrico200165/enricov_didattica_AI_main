"""Verifica dei dati esposti in chiaro in una cattura di rete (formati pcapng e pcap).

Uso: python analizza_cattura.py cattura.pcapng

Lo script legge i pacchetti Ethernet/IPv4 con TCP o UDP e riporta:
- le conversazioni (coppie di indirizzi e porta del servizio) con il numero di pacchetti
- le richieste DNS e i nomi dei siti richiesti nelle connessioni TLS (SNI)
- i dati sensibili visibili in chiaro: campi password nei moduli HTTP,
  autenticazione HTTP Basic, comandi USER e PASS di FTP
Serve a controllare il traffico di sistemi propri o di prova, come nel laboratorio 4.4.
Solo libreria standard di Python.
"""

import base64
import struct
import sys
import urllib.parse
from collections import Counter

CAMPI_SENSIBILI = ("password", "pass", "pwd", "passwd", "pin")


# ------------------------------------------------------------------ lettura dei file

def leggi_pacchetti(percorso):
    """Sequenza di (numero, byte del frame Ethernet); accetta pcapng e pcap classico."""
    with open(percorso, "rb") as f:
        dati = f.read()
    magia = dati[:4]
    if magia == b"\x0a\x0d\x0d\x0a":
        yield from _pcapng(dati)
    elif magia in (b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4", b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d"):
        yield from _pcap(dati)
    else:
        raise ValueError("formato non riconosciuto: servono file .pcapng o .pcap")


def _pcapng(dati):
    pos, ordine, numero, tipi_link = 0, "<", 0, []
    while pos + 12 <= len(dati):
        if dati[pos:pos + 4] == b"\x0a\x0d\x0d\x0a":            # Section Header Block
            ordine = "<" if dati[pos + 8:pos + 12] == b"\x4d\x3c\x2b\x1a" else ">"
            tipi_link = []
        tipo, lunghezza = struct.unpack(ordine + "II", dati[pos:pos + 8])
        if lunghezza < 12:
            raise ValueError("blocco pcapng non valido")
        corpo = dati[pos + 8:pos + lunghezza - 4]
        if tipo == 1:                                           # Interface Description Block
            tipi_link.append(struct.unpack(ordine + "H", corpo[:2])[0])
        elif tipo == 6:                                         # Enhanced Packet Block
            interfaccia, _, _, catturati, _ = struct.unpack(ordine + "IIIII", corpo[:20])
            numero += 1
            if tipi_link[interfaccia] == 1:                     # 1 = Ethernet
                yield numero, corpo[20:20 + catturati]
        pos += lunghezza


def _pcap(dati):
    ordine = "<" if dati[:4] in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1") else ">"
    tipo_link = struct.unpack(ordine + "I", dati[20:24])[0]
    pos, numero = 24, 0
    while pos + 16 <= len(dati):
        _, _, catturati, _ = struct.unpack(ordine + "IIII", dati[pos:pos + 16])
        numero += 1
        if tipo_link == 1:
            yield numero, dati[pos + 16:pos + 16 + catturati]
        pos += 16 + catturati


# ------------------------------------------------------------------ decodifica dei protocolli

def decodifica(frame):
    """Dizionario con indirizzi, protocollo, porte e dati applicativi, o None se non è IPv4 TCP/UDP."""
    if len(frame) < 34 or frame[12:14] != b"\x08\x00":
        return None
    ip = frame[14:]
    ihl = (ip[0] & 0x0F) * 4
    lunghezza_totale = struct.unpack("!H", ip[2:4])[0]
    proto = ip[9]
    src, dst = ".".join(map(str, ip[12:16])), ".".join(map(str, ip[16:20]))
    seg = ip[ihl:lunghezza_totale]
    if proto == 6 and len(seg) >= 20:
        sport, dport = struct.unpack("!HH", seg[:4])
        offset = (seg[12] >> 4) * 4
        flag = seg[13]
        return {"proto": "tcp", "src": src, "dst": dst, "sport": sport, "dport": dport,
                "syn": bool(flag & 0x02), "dati": seg[offset:]}
    if proto == 17 and len(seg) >= 8:
        sport, dport = struct.unpack("!HH", seg[:4])
        return {"proto": "udp", "src": src, "dst": dst, "sport": sport, "dport": dport,
                "syn": False, "dati": seg[8:]}
    return None


def nome_dns(dati, pos=12):
    """Nome richiesto nella prima domanda di un messaggio DNS."""
    parti = []
    while pos < len(dati) and dati[pos] != 0:
        n = dati[pos]
        parti.append(dati[pos + 1:pos + 1 + n].decode("ascii", "replace"))
        pos += 1 + n
    return ".".join(parti)


def sni_tls(dati):
    """Nome del server indicato nel ClientHello TLS (estensione server_name), se presente."""
    try:
        if dati[0] != 0x16 or dati[5] != 0x01:                  # record handshake, ClientHello
            return None
        pos = 9 + 2 + 32                                        # intestazioni, versione, random
        pos += 1 + dati[pos]                                    # session id
        pos += 2 + struct.unpack("!H", dati[pos:pos + 2])[0]    # cipher suite
        pos += 1 + dati[pos]                                    # metodi di compressione
        fine = pos + 2 + struct.unpack("!H", dati[pos:pos + 2])[0]
        pos += 2
        while pos + 4 <= fine:
            tipo, lung = struct.unpack("!HH", dati[pos:pos + 4])
            if tipo == 0:                                       # server_name
                n = struct.unpack("!H", dati[pos + 7:pos + 9])[0]
                return dati[pos + 9:pos + 9 + n].decode("ascii", "replace")
            pos += 4 + lung
    except (IndexError, struct.error):
        return None
    return None


def dati_sensibili_http(testo):
    """Voci sensibili in una richiesta HTTP in chiaro."""
    trovati = []
    intestazioni, _, corpo = testo.partition("\r\n\r\n")
    for riga in intestazioni.split("\r\n")[1:]:
        nome, _, valore = riga.partition(":")
        if nome.strip().lower() == "authorization" and valore.strip().lower().startswith("basic "):
            decodificato = base64.b64decode(valore.strip()[6:]).decode("utf-8", "replace")
            trovati.append(f"autenticazione HTTP Basic: {decodificato}")
    if corpo:
        for campo, valori in urllib.parse.parse_qs(corpo).items():
            if campo.lower() in CAMPI_SENSIBILI:
                trovati.append(f"campo '{campo}' del modulo: {valori[0]}")
    return trovati


# ------------------------------------------------------------------ analisi

def analizza(percorso):
    risultato = {"pacchetti": 0, "conversazioni": Counter(), "dns": [], "tls": [], "in_chiaro": []}
    for numero, frame in leggi_pacchetti(percorso):
        risultato["pacchetti"] += 1
        p = decodifica(frame)
        if p is None:
            continue
        servizio = min(p["sport"], p["dport"])
        client, server = (p["src"], p["dst"]) if p["dport"] == servizio else (p["dst"], p["src"])
        risultato["conversazioni"][(p["proto"], client, server, servizio)] += 1
        d = p["dati"]
        if not d:
            continue
        if p["proto"] == "udp" and p["dport"] == 53:
            risultato["dns"].append((numero, p["src"], nome_dns(d)))
        elif p["proto"] == "tcp" and p["dport"] == 443:
            nome = sni_tls(d)
            if nome:
                risultato["tls"].append((numero, p["src"], nome))
        elif p["proto"] == "tcp" and p["dport"] in (80, 8080):
            testo = d.decode("latin-1")
            for voce in dati_sensibili_http(testo):
                risultato["in_chiaro"].append((numero, p["src"], "HTTP", voce))
        elif p["proto"] == "tcp" and p["dport"] == 21:
            riga = d.decode("latin-1").strip()
            comando = riga.split(" ", 1)[0].upper()
            if comando in ("USER", "PASS"):
                risultato["in_chiaro"].append((numero, p["src"], "FTP", riga))
    return risultato


def stampa(r):
    print(f"Pacchetti letti: {r['pacchetti']}\n")
    print("Conversazioni (protocollo, client, server, porta del servizio, pacchetti):")
    for (proto, client, server, porta), n in sorted(r["conversazioni"].items(), key=lambda x: x[0][3]):
        print(f"  {proto:3} {client:>15} -> {server:<15} porta {porta:<5} {n:4} pacchetti")
    print("\nRichieste DNS:")
    for numero, src, nome in r["dns"]:
        print(f"  pacchetto {numero:4}  {src}  {nome}")
    print("\nConnessioni TLS (nome del sito, visibile anche se il contenuto è cifrato):")
    for numero, src, nome in r["tls"]:
        print(f"  pacchetto {numero:4}  {src}  {nome}")
    print("\nDATI SENSIBILI IN CHIARO:" if r["in_chiaro"] else "\nNessun dato sensibile in chiaro trovato.")
    for numero, src, protocollo, voce in r["in_chiaro"]:
        print(f"  pacchetto {numero:4}  {src}  {protocollo}: {voce}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    stampa(analizza(sys.argv[1]))
