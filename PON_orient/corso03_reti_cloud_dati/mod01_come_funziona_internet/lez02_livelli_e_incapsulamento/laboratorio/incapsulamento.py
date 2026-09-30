"""Costruzione, livello per livello, del frame Ethernet che trasporta una richiesta HTTP.

Uso: python incapsulamento.py

Lo script parte dal messaggio HTTP (livello di applicazione) e aggiunge in ordine le intestazioni
TCP (trasporto), IP (rete) ed Ethernet (collegamento), mostrando dimensioni e contenuto di ciascuna.
Salva inoltre il frame nel file richiesta.pcap, che si può aprire con Wireshark per un confronto.
Solo libreria standard di Python.
"""

import struct
import time


def somma_di_controllo(dati):
    """Checksum usata da IP e TCP: somma in complemento a uno di parole da 16 bit."""
    if len(dati) % 2:
        dati += b"\x00"
    totale = sum(struct.unpack(f"!{len(dati) // 2}H", dati))
    while totale >> 16:
        totale = (totale & 0xFFFF) + (totale >> 16)
    return ~totale & 0xFFFF


def ip_in_byte(testo):
    return bytes(int(x) for x in testo.split("."))


def mac_in_byte(testo):
    return bytes.fromhex(testo.replace(":", ""))


def intestazione_tcp(ip_sorgente, ip_destinazione, porta_sorgente, porta_destinazione, dati,
                     sequenza=1, conferma=1):
    """Intestazione TCP di 20 byte, con i flag PSH e ACK, e checksum calcolata sulla pseudo-intestazione IP."""
    lunghezza_intestazione = 5 << 4          # 5 parole da 32 bit = 20 byte, nei 4 bit alti
    flag = 0x18                              # PSH + ACK
    finestra = 64240
    senza_checksum = struct.pack("!HHIIBBHHH", porta_sorgente, porta_destinazione, sequenza, conferma,
                                 lunghezza_intestazione, flag, finestra, 0, 0)
    pseudo = ip_in_byte(ip_sorgente) + ip_in_byte(ip_destinazione) + struct.pack("!BBH", 0, 6, 20 + len(dati))
    checksum = somma_di_controllo(pseudo + senza_checksum + dati)
    return senza_checksum[:16] + struct.pack("!H", checksum) + senza_checksum[18:]


def intestazione_ip(ip_sorgente, ip_destinazione, lunghezza_carico, identificativo=4321, ttl=64):
    """Intestazione IPv4 di 20 byte per un carico TCP (protocollo 6)."""
    versione_e_lunghezza = (4 << 4) | 5      # IPv4, intestazione di 5 parole
    lunghezza_totale = 20 + lunghezza_carico
    senza_checksum = struct.pack("!BBHHHBBH4s4s", versione_e_lunghezza, 0, lunghezza_totale, identificativo,
                                 0x4000, ttl, 6, 0, ip_in_byte(ip_sorgente), ip_in_byte(ip_destinazione))
    checksum = somma_di_controllo(senza_checksum)
    return senza_checksum[:10] + struct.pack("!H", checksum) + senza_checksum[12:]


def intestazione_ethernet(mac_destinazione, mac_sorgente):
    """Intestazione Ethernet II di 14 byte; il tipo 0x0800 indica che il carico è un pacchetto IPv4."""
    return mac_in_byte(mac_destinazione) + mac_in_byte(mac_sorgente) + struct.pack("!H", 0x0800)


def costruisci(host="www.scuola.example", percorso="/orari.html",
               ip_client="192.168.1.20", ip_server="203.0.113.80",
               mac_client="3c:52:82:4e:10:20", mac_router="00:1b:21:3a:5c:01", porta_client=51234):
    livelli = []
    http = f"GET {percorso} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: esempio-didattico\r\n\r\n".encode("ascii")
    livelli.append(("Applicazione (HTTP)", http))
    tcp = intestazione_tcp(ip_client, ip_server, porta_client, 80, http)
    livelli.append(("Trasporto (TCP)", tcp))
    ip = intestazione_ip(ip_client, ip_server, len(tcp) + len(http))
    livelli.append(("Rete (IP)", ip))
    eth = intestazione_ethernet(mac_router, mac_client)
    livelli.append(("Collegamento (Ethernet)", eth))
    frame = eth + ip + tcp + http
    return frame, livelli


def salva_pcap(frame, percorso="richiesta.pcap"):
    """File pcap con un solo frame: intestazione globale di 24 byte, poi 16 byte per il frame."""
    adesso = time.time()
    with open(percorso, "wb") as f:
        f.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))   # 1 = Ethernet
        f.write(struct.pack("<IIII", int(adesso), int(adesso % 1 * 1e6), len(frame), len(frame)))
        f.write(frame)


def esadecimale(dati, larghezza=16):
    return "\n".join(f"    {i:04x}  " + " ".join(f"{b:02x}" for b in dati[i:i + larghezza])
                     for i in range(0, len(dati), larghezza))


if __name__ == "__main__":
    frame, livelli = costruisci()
    print("Messaggio HTTP (i byte sono testo leggibile):")
    print("    " + livelli[0][1].decode("ascii").replace("\r\n", "\\r\\n\n    "))
    for nome, intestazione in livelli[1:]:
        print(f"\n+ intestazione {nome}: {len(intestazione)} byte")
        print(esadecimale(intestazione))
    print(f"\nFrame completo: {len(frame)} byte, di cui {len(livelli[0][1])} di dati HTTP "
          f"e {len(frame) - len(livelli[0][1])} di intestazioni")
    salva_pcap(frame)
    print("Frame salvato in richiesta.pcap")
