"""Analisi di indirizzi MAC e della cache ARP di Windows.

Uso:
    python mac_e_arp.py                      esegue "arp -a" (solo Windows) e analizza l'output
    python mac_e_arp.py arp_esempio.txt      analizza un output salvato in un file
    python mac_e_arp.py --mac 3c-52-82-4e-10-20   analizza un singolo indirizzo MAC
"""

import os
import re
import subprocess
import sys

# Un indirizzo MAC: sei byte esadecimali separati da "-" (Windows) o ":" (Linux, macOS, Filius)
MODELLO_MAC = re.compile(r"^([0-9A-Fa-f]{2})([-:]?)([0-9A-Fa-f]{2})(\2[0-9A-Fa-f]{2}){4}$")
# Una riga della tabella di "arp -a": indirizzo IPv4, indirizzo MAC, tipo
MODELLO_RIGA = re.compile(r"^\s*(\d{1,3}(?:\.\d{1,3}){3})\s+([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})\s+(\S+)")
# Intestazione di ogni interfaccia: "Interfaccia: 192.168.1.20 --- 0xb" o "Interface: ..."
MODELLO_INTERFACCIA = re.compile(r"^\s*Interfac\w*:\s*(\d{1,3}(?:\.\d{1,3}){3})")


def normalizza_mac(testo):
    """Restituisce il MAC come sei byte in maiuscolo separati da ":"; ValueError se non valido."""
    testo = testo.strip()
    if not MODELLO_MAC.match(testo):
        raise ValueError(f"indirizzo MAC non valido: {testo}")
    cifre = re.sub(r"[-:]", "", testo).upper()
    return ":".join(cifre[i:i + 2] for i in range(0, 12, 2))


def analizza_mac(testo):
    """Restituisce un dizionario con le caratteristiche dell'indirizzo MAC."""
    mac = normalizza_mac(testo)
    primo_byte = int(mac[:2], 16)
    if mac == "FF:FF:FF:FF:FF:FF":
        destinatari = "broadcast"
    elif primo_byte & 0b00000001:        # bit I/G: 1 = gruppo (multicast)
        destinatari = "multicast"
    else:
        destinatari = "unicast"
    # bit U/L: 1 = indirizzo amministrato localmente (per esempio MAC casuale del Wi-Fi)
    locale = bool(primo_byte & 0b00000010)
    return {
        "mac": mac,
        "binario_primo_byte": format(primo_byte, "08b"),
        "destinatari": destinatari,
        "amministrazione": "locale" if locale else "universale (assegnato dal produttore)",
        "oui": mac[:8] if not locale else None,  # prefisso del produttore, solo se universale
    }


def mac_multicast_ipv4(indirizzo_ip):
    """MAC di destinazione per un indirizzo IPv4 multicast (224.0.0.0/4).

    Regola: prefisso 01:00:5E seguito dai 23 bit meno significativi dell'indirizzo IP.
    """
    byte = [int(x) for x in indirizzo_ip.split(".")]
    if not 224 <= byte[0] <= 239:
        raise ValueError("non è un indirizzo IPv4 multicast")
    return "01:00:5E:%02X:%02X:%02X" % (byte[1] & 0x7F, byte[2], byte[3])


def leggi_tabella_arp(testo):
    """Converte l'output di "arp -a" in un elenco di voci (interfaccia, ip, mac, tipo)."""
    voci = []
    interfaccia = None
    for riga in testo.splitlines():
        m = MODELLO_INTERFACCIA.match(riga)
        if m:
            interfaccia = m.group(1)
            continue
        m = MODELLO_RIGA.match(riga)
        if m:
            ip, mac, tipo = m.groups()
            voci.append({"interfaccia": interfaccia, "ip": ip,
                         "mac": normalizza_mac(mac), "tipo": tipo.lower()})
    return voci


def esegui_arp():
    """Esegue "arp -a" su Windows e ne restituisce l'output come testo."""
    if os.name != "nt":
        raise OSError("il comando 'arp -a' di questo script è previsto per Windows")
    # "oem" è la codifica della console di Windows (lettere accentate corrette)
    risultato = subprocess.run(["arp", "-a"], capture_output=True, text=True,
                               encoding="oem", errors="replace")
    return risultato.stdout


def stampa_analisi(voci):
    print(f"{'Interfaccia':<16}{'Indirizzo IP':<17}{'MAC':<19}{'Tipo':<10}{'Destinatari':<11} Amministrazione")
    for v in voci:
        a = analizza_mac(v["mac"])
        # il bit U/L interessa solo gli indirizzi unicast, cioè le schede di rete
        amministrazione = a["amministrazione"] if a["destinatari"] == "unicast" else "-"
        print(f"{v['interfaccia'] or '-':<16}{v['ip']:<17}{v['mac']:<19}{v['tipo']:<10}"
              f"{a['destinatari']:<11} {amministrazione}")
    unicast = [v for v in voci if analizza_mac(v["mac"])["destinatari"] == "unicast"]
    print(f"\nVoci: {len(voci)}, di cui unicast (altri dispositivi della rete locale): {len(unicast)}")


def main(argomenti):
    if len(argomenti) == 2 and argomenti[0] == "--mac":
        for chiave, valore in analizza_mac(argomenti[1]).items():
            print(f"{chiave:<20}{valore}")
        return
    if argomenti:
        with open(argomenti[0], encoding="utf-8") as f:
            testo = f.read()
    else:
        testo = esegui_arp()
    stampa_analisi(leggi_tabella_arp(testo))


if __name__ == "__main__":
    main(sys.argv[1:])
