"""Test di mac_e_arp.py. Esecuzione: python test_mac_e_arp.py"""

from mac_e_arp import normalizza_mac, analizza_mac, mac_multicast_ipv4, leggi_tabella_arp

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def errore(funzione, *argomenti):
    """True se la funzione solleva ValueError."""
    try:
        funzione(*argomenti)
    except ValueError:
        return True
    return False


verifica("formato Windows normalizzato", normalizza_mac("3c-52-82-4e-10-20") == "3C:52:82:4E:10:20")
verifica("formato con i due punti normalizzato", normalizza_mac("3c:52:82:4e:10:20") == "3C:52:82:4E:10:20")
verifica("formato senza separatori accettato", normalizza_mac("3c52824e1020") == "3C:52:82:4E:10:20")
verifica("separatori misti rifiutati", errore(normalizza_mac, "3c-52:82-4e-10-20"))
verifica("cinque byte rifiutati", errore(normalizza_mac, "3c-52-82-4e-10"))

a = analizza_mac("00-1b-21-3a-5c-01")
verifica("00:1B:21:... unicast, universale, OUI 00:1B:21",
         a["destinatari"] == "unicast" and a["amministrazione"].startswith("universale") and a["oui"] == "00:1B:21")
b = analizza_mac("7a-2f-91-c4-08-e3")
verifica("7A = 01111010: unicast amministrato localmente (MAC casuale), senza OUI",
         b["binario_primo_byte"] == "01111010" and b["destinatari"] == "unicast"
         and b["amministrazione"] == "locale" and b["oui"] is None)
verifica("FF:FF:FF:FF:FF:FF broadcast", analizza_mac("ff-ff-ff-ff-ff-ff")["destinatari"] == "broadcast")
verifica("01:00:5E:... multicast", analizza_mac("01-00-5e-00-00-16")["destinatari"] == "multicast")

verifica("224.0.0.22 -> 01:00:5E:00:00:16", mac_multicast_ipv4("224.0.0.22") == "01:00:5E:00:00:16")
verifica("239.255.255.250 -> 01:00:5E:7F:FF:FA (bit alto del secondo byte perso)",
         mac_multicast_ipv4("239.255.255.250") == "01:00:5E:7F:FF:FA")
verifica("192.168.1.1 non è multicast", errore(mac_multicast_ipv4, "192.168.1.1"))

with open("arp_esempio.txt", encoding="utf-8") as f:
    voci = leggi_tabella_arp(f.read())
verifica("otto voci lette dal file di esempio", len(voci) == 8)
verifica("interfaccia e tipo letti", voci[0]["interfaccia"] == "192.168.1.20" and voci[0]["tipo"] == "dinamico")
verifica("tre voci unicast", sum(analizza_mac(v["mac"])["destinatari"] == "unicast" for v in voci) == 3)
verifica("ogni voce multicast del file rispetta la regola 01:00:5E",
         all(mac_multicast_ipv4(v["ip"]) == v["mac"] for v in voci if v["ip"].startswith(("224.", "239."))))

inglese = """Interface: 10.0.0.5 --- 0x7
  Internet Address      Physical Address      Type
  10.0.0.1              a4-91-b1-00-00-01     dynamic
"""
v = leggi_tabella_arp(inglese)
verifica("output di Windows in inglese letto", len(v) == 1 and v[0]["interfaccia"] == "10.0.0.5" and v[0]["tipo"] == "dynamic")

print(f"\nTest superati: {superati}, falliti: {falliti}")
