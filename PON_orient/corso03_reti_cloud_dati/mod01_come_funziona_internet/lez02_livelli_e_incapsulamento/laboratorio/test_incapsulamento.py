"""Test di incapsulamento.py. Esecuzione: python test_incapsulamento.py"""

import os
import struct
import tempfile

from incapsulamento import costruisci, somma_di_controllo, salva_pcap, ip_in_byte

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


frame, livelli = costruisci()
nomi = [n for n, _ in livelli]
verifica("quattro livelli, dall'applicazione al collegamento",
         nomi == ["Applicazione (HTTP)", "Trasporto (TCP)", "Rete (IP)", "Collegamento (Ethernet)"])
verifica("intestazioni di 20, 20 e 14 byte", [len(b) for _, b in livelli[1:]] == [20, 20, 14])
verifica("frame = Ethernet + IP + TCP + HTTP", frame == livelli[3][1] + livelli[2][1] + livelli[1][1] + livelli[0][1])
verifica("tipo Ethernet 0x0800 (IPv4)", frame[12:14] == b"\x08\x00")
ip = frame[14:34]
verifica("versione 4 e intestazione di 20 byte", ip[0] == 0x45)
verifica("lunghezza totale IP corretta", struct.unpack("!H", ip[2:4])[0] == len(frame) - 14)
verifica("protocollo 6 (TCP) e TTL 64", ip[9] == 6 and ip[8] == 64)
verifica("checksum IP valida (ricalcolo = 0)", somma_di_controllo(ip) == 0)
tcp_e_dati = frame[34:]
pseudo = ip[12:16] + ip[16:20] + struct.pack("!BBH", 0, 6, len(tcp_e_dati))
verifica("checksum TCP valida (ricalcolo = 0)", somma_di_controllo(pseudo + tcp_e_dati) == 0)
verifica("porta di destinazione 80", struct.unpack("!H", tcp_e_dati[2:4])[0] == 80)
verifica("indirizzo di destinazione nel pacchetto", ip[16:20] == ip_in_byte("203.0.113.80"))
verifica("checksum dell'esempio classico RFC 1071", somma_di_controllo(bytes.fromhex("0001f203f4f5f6f7")) == 0x220d)

percorso = os.path.join(tempfile.mkdtemp(), "prova.pcap")
salva_pcap(frame, percorso)
dati = open(percorso, "rb").read()
verifica("file pcap: 24 + 16 byte di intestazioni più il frame", len(dati) == 40 + len(frame) and dati[40:] == frame)

print(f"Test superati: {superati}, falliti: {falliti}")
