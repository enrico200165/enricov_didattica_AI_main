"""Verifica automatica di un piano di indirizzamento con VLAN e DHCP.

Il piano è un file CSV con le colonne:
    nome, vlan, rete, gateway, dhcp_inizio, dhcp_fine, statici, host_richiesti
- dhcp_inizio e dhcp_fine vuoti se la sottorete non usa il DHCP
- statici: indirizzi fissi separati da punto e virgola (server, stampanti, apparati)
- host_richiesti: facoltativo, numero di dispositivi previsto

Uso:
    python verifica_progetto.py piano_esempio.csv 10.20.0.0/22
"""

import csv
import ipaddress
import sys


def leggi_piano(percorso):
    with open(percorso, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verifica_piano(righe, blocco):
    """Restituisce l'elenco dei problemi trovati (vuoto se il piano è corretto)."""
    problemi = []
    blocco = ipaddress.ip_network(blocco)
    reti = []            # (nome, rete) delle righe valide, per il controllo delle sovrapposizioni
    vlan_usate = {}
    for riga in righe:
        nome = riga["nome"].strip()

        def errore(testo):
            problemi.append(f"{nome}: {testo}")

        # 1. rete scritta correttamente (indirizzo di rete, senza bit di host)
        try:
            rete = ipaddress.ip_network(riga["rete"].strip())
        except ValueError as e:
            errore(f"rete non valida ({e})")
            continue
        if not rete.subnet_of(blocco):
            errore(f"la rete {rete} non è contenuta nel blocco {blocco}")
        for altro_nome, altra in reti:
            if rete.overlaps(altra):
                errore(f"la rete {rete} si sovrappone a {altro_nome} ({altra})")
        reti.append((nome, rete))

        # 2. VLAN: numero da 1 a 4094, diverso per ogni sottorete
        vlan = riga["vlan"].strip()
        if not vlan.isdigit() or not 1 <= int(vlan) <= 4094:
            errore(f"VLAN '{vlan}' non valida (numero da 1 a 4094)")
        elif vlan in vlan_usate:
            errore(f"VLAN {vlan} già usata da {vlan_usate[vlan]}")
        else:
            vlan_usate[vlan] = nome

        # 3. indirizzi utilizzabili dagli host (per /31 e /32 tutti)
        if rete.prefixlen <= 30:
            primo, ultimo = rete.network_address + 1, rete.broadcast_address - 1
        else:
            primo, ultimo = rete.network_address, rete.broadcast_address

        def utilizzabile(testo, descrizione):
            """Converte l'indirizzo e controlla che sia un host della rete; None se non valido."""
            try:
                indirizzo = ipaddress.ip_address(testo.strip())
            except ValueError:
                errore(f"{descrizione} '{testo}' non è un indirizzo valido")
                return None
            if not primo <= indirizzo <= ultimo:
                errore(f"{descrizione} {indirizzo} non è un indirizzo di host della rete {rete}")
                return None
            return indirizzo

        gateway = utilizzabile(riga["gateway"], "gateway")
        statici = []
        for testo in filter(None, (s.strip() for s in riga["statici"].split(";"))):
            indirizzo = utilizzabile(testo, "indirizzo statico")
            if indirizzo is None:
                continue
            if indirizzo == gateway:
                errore(f"l'indirizzo statico {indirizzo} coincide con il gateway")
            if indirizzo in statici:
                errore(f"indirizzo statico {indirizzo} ripetuto")
                continue
            statici.append(indirizzo)

        # 4. intervallo DHCP dentro la rete, senza gateway né indirizzi statici
        inizio_testo, fine_testo = riga["dhcp_inizio"].strip(), riga["dhcp_fine"].strip()
        dinamici = 0
        if inizio_testo or fine_testo:
            inizio = utilizzabile(inizio_testo, "inizio DHCP")
            fine = utilizzabile(fine_testo, "fine DHCP")
            if inizio and fine:
                if inizio > fine:
                    errore("l'intervallo DHCP inizia dopo la fine")
                else:
                    dinamici = int(fine) - int(inizio) + 1
                    for fisso in ([gateway] if gateway else []) + statici:
                        if inizio <= fisso <= fine:
                            errore(f"l'intervallo DHCP comprende l'indirizzo fisso {fisso}")

        # 5. capacità: indirizzi assegnabili ai dispositivi previsti
        richiesti = riga.get("host_richiesti", "").strip()
        if richiesti.isdigit():
            disponibili = dinamici + len(statici) if (inizio_testo or statici) else int(ultimo) - int(primo)
            if disponibili < int(richiesti):
                errore(f"indirizzi assegnabili: {disponibili}, dispositivi previsti: {richiesti}")
    return problemi


def main(percorso, blocco):
    righe = leggi_piano(percorso)
    problemi = verifica_piano(righe, blocco)
    print(f"Sottoreti controllate: {len(righe)}")
    if not problemi:
        print("Nessun problema trovato.")
    for p in problemi:
        print("PROBLEMA:", p)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
    else:
        main(sys.argv[1], sys.argv[2])
