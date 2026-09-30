"""Test di piano_indirizzi.py. Esecuzione: python test_piano_indirizzi.py"""

import ipaddress

from piano_indirizzi import prefisso_per, piano

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


verifica("12 dispositivi: /27", prefisso_per(12) == 27)
verifica("120 dispositivi: /24", prefisso_per(120) == 24)
verifica("400 dispositivi: /22", prefisso_per(400) == 22)
verifica("senza margine, 60 dispositivi: /26", prefisso_per(60, margine=0) == 26)

segmenti = {"a": (10, 400), "b": (20, 120), "c": (30, 60), "d": (40, 12), "e": (50, 12)}
voci = piano("10.20.0.0/20", segmenti)
reti = [v["sottorete"] for v in voci]
verifica("sottoreti tutte dentro il blocco", all(r.subnet_of(ipaddress.ip_network("10.20.0.0/20")) for r in reti))
verifica("nessuna sovrapposizione", all(not a.overlaps(b) for i, a in enumerate(reti) for b in reti[i + 1:]))
verifica("capacità sufficiente con margine", all(v["capacita"] >= v["dispositivi"] * 1.5 for v in voci))
verifica("gateway = primo indirizzo utilizzabile", all(v["gateway"] == v["sottorete"].network_address + 1 for v in voci))
verifica("segmento più grande assegnato per primo", str(voci[0]["sottorete"]) == "10.20.0.0/22")
verifica("VLAN a parità di dimensione in ordine crescente", [v["vlan"] for v in voci[-2:]] == [40, 50])
try:
    piano("192.168.1.0/24", {"troppi": (10, 300)})
    verifica("blocco insufficiente segnalato", False)
except ValueError:
    verifica("blocco insufficiente segnalato", True)

print(f"Test superati: {superati}, falliti: {falliti}")
