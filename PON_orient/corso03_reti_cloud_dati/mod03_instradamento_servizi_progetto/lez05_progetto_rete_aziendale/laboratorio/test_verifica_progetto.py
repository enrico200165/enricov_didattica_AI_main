"""Test di verifica_progetto.py. Esecuzione: python test_verifica_progetto.py"""

from verifica_progetto import leggi_piano, verifica_piano

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def contiene(problemi, nome, frammento):
    return any(p.startswith(nome + ":") and frammento in p for p in problemi)


verifica("piano di esempio corretto: nessun problema",
         verifica_piano(leggi_piano("piano_esempio.csv"), "10.20.0.0/22") == [])
verifica("lo stesso piano con un blocco diverso: tutte le reti fuori dal blocco",
         len(verifica_piano(leggi_piano("piano_esempio.csv"), "10.30.0.0/22")) == 8)

p = verifica_piano(leggi_piano("piano_con_errori.csv"), "10.30.0.0/22")
verifica("DHCP che comprende il gateway", contiene(p, "uffici", "fisso 10.30.0.1"))
verifica("DHCP che comprende un indirizzo statico", contiene(p, "uffici", "fisso 10.30.0.5"))
verifica("VLAN ripetuta", contiene(p, "magazzino", "VLAN 10 già usata"))
verifica("gateway uguale all'indirizzo di rete", contiene(p, "magazzino", "gateway 10.30.0.64"))
verifica("rete con bit di host", contiene(p, "produzione", "rete non valida"))
verifica("VLAN fuori intervallo", contiene(p, "ospiti", "VLAN '5000'"))
verifica("rete fuori dal blocco", contiene(p, "server", "non è contenuta nel blocco"))
verifica("indirizzo statico ripetuto", contiene(p, "server", "ripetuto"))
verifica("intervallo DHCP rovesciato", contiene(p, "stampanti", "inizia dopo la fine"))
verifica("capacità insufficiente", contiene(p, "stampanti", "dispositivi previsti: 6"))
verifica("undici problemi in tutto", len(p) == 11)

sovrapposte = [
    {"nome": "a", "vlan": "10", "rete": "10.0.0.0/25", "gateway": "10.0.0.1", "dhcp_inizio": "", "dhcp_fine": "", "statici": "", "host_richiesti": ""},
    {"nome": "b", "vlan": "20", "rete": "10.0.0.64/26", "gateway": "10.0.0.65", "dhcp_inizio": "", "dhcp_fine": "", "statici": "", "host_richiesti": ""},
]
verifica("sottoreti sovrapposte", contiene(verifica_piano(sovrapposte, "10.0.0.0/24"), "b", "si sovrappone a a"))
senza_dhcp = [{"nome": "c", "vlan": "5", "rete": "10.0.0.0/28", "gateway": "10.0.0.1", "dhcp_inizio": "",
               "dhcp_fine": "", "statici": "", "host_richiesti": "13"}]
verifica("senza DHCP né statici: capacità = host meno il gateway (13 su /28)", verifica_piano(senza_dhcp, "10.0.0.0/24") == [])

print(f"\nTest superati: {superati}, falliti: {falliti}")
