"""Etichetta VLAN IEEE 802.1Q: inserimento e lettura in una trama Ethernet.

Tra l'indirizzo MAC di origine e il campo tipo si inseriscono 4 byte:
- TPID (2 byte) = 0x8100: segnala che segue un'etichetta VLAN
- TCI  (2 byte) = priorità PCP (3 bit) + DEI (1 bit) + identificativo VLAN VID (12 bit)

Uso: python vlan_8021q.py
"""

import struct

TPID = 0x8100


def aggiungi_etichetta(trama, vid, priorita=0):
    """Restituisce la trama con l'etichetta 802.1Q (su una porta trunk)."""
    if not 1 <= vid <= 4094:
        raise ValueError("VID valido da 1 a 4094 (0 e 4095 sono riservati)")
    if not 0 <= priorita <= 7:
        raise ValueError("priorità da 0 a 7")
    tci = (priorita << 13) | vid                  # PCP nei 3 bit alti, DEI = 0, VID nei 12 bit bassi
    etichetta = struct.pack("!HH", TPID, tci)
    return trama[:12] + etichetta + trama[12:]    # dopo i due indirizzi MAC (6 + 6 byte)


def leggi_etichetta(trama):
    """(vid, priorità) se la trama ha l'etichetta, altrimenti None (trama di una porta access)."""
    tpid, tci = struct.unpack("!HH", trama[12:16])
    if tpid != TPID:
        return None
    return tci & 0x0FFF, tci >> 13               # AND con 12 bit a 1; spostamento di 13 bit


def togli_etichetta(trama):
    """Restituisce la trama senza etichetta (verso una porta access)."""
    return trama[:12] + trama[16:] if leggi_etichetta(trama) else trama


def trama_di_esempio():
    destinazione = bytes.fromhex("3c52824e1020")
    origine = bytes.fromhex("001b213a5c01")
    return destinazione + origine + b"\x08\x00" + b"pacchetto IPv4 ..."


if __name__ == "__main__":
    trama = trama_di_esempio()
    etichettata = aggiungi_etichetta(trama, vid=20, priorita=5)
    print("senza etichetta:", trama[:16].hex(" "))
    print("con etichetta:  ", etichettata[:18].hex(" "))
    print("VLAN e priorità lette:", leggi_etichetta(etichettata))
    print("lunghezze:", len(trama), "e", len(etichettata), "byte")
