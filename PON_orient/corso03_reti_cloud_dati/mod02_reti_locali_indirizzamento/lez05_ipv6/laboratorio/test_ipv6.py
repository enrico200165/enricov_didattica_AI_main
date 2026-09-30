"""Test di ipv6.py. Esecuzione: python test_ipv6.py"""

import ipaddress
import random

from ipv6 import espandi, abbrevia, tipo, eui64, indirizzi_da_ipconfig

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
    try:
        funzione(*argomenti)
    except ValueError:
        return True
    return False


verifica("espansione di 2001:db8::ff00:42:8329",
         espandi("2001:db8::ff00:42:8329") == "2001:0db8:0000:0000:0000:ff00:0042:8329")
verifica("espansione di :: e di ::1",
         espandi("::") == ":".join(["0000"] * 8) and espandi("::1").endswith("0000:0001"))
verifica("due '::' rifiutati", errore(espandi, "2001::1::2"))
verifica("gruppo di cinque cifre rifiutato", errore(espandi, "2001:db8::12345"))
verifica("nove gruppi rifiutati", errore(espandi, "1:2:3:4:5:6:7:8:9"))

verifica("abbreviazione dell'esempio classico",
         abbrevia("2001:0db8:0000:0000:0000:ff00:0042:8329") == "2001:db8::ff00:42:8329")
verifica("un solo gruppo a zero non diventa '::'",
         abbrevia("2001:db8:0:1:1:1:1:1") == "2001:db8:0:1:1:1:1:1")
verifica("a parità di lunghezza si abbrevia la prima sequenza",
         abbrevia("2001:db8:0:0:1:0:0:1") == "2001:db8::1:0:0:1")
verifica("si abbrevia la sequenza più lunga",
         abbrevia("2001:0:0:1:0:0:0:1") == "2001:0:0:1::1")
verifica("maiuscole convertite in minuscole", abbrevia("FE80::1") == "fe80::1")

generatore = random.Random(2026)
casi = []
for _ in range(3000):
    # gruppi casuali con molti zeri, per provare tutte le posizioni di '::'
    gruppi = [generatore.choice([0, 0, 0, generatore.getrandbits(16)]) for _ in range(8)]
    casi.append(":".join(format(g, "04x") for g in gruppi))
verifica("abbreviazione concorde con ipaddress su 3000 indirizzi casuali",
         all(abbrevia(x) == ipaddress.IPv6Address(x).compressed for x in casi))
verifica("espansione concorde con ipaddress",
         all(espandi(ipaddress.IPv6Address(x).compressed) == ipaddress.IPv6Address(x).exploded for x in casi))

verifica("tipi: loopback, link-local, ULA, multicast, globale, documentazione",
         [tipo(x) for x in ("::1", "fe80::1", "fd12:3456::1", "ff02::1", "2a00:1450::1", "2001:db8::1")]
         == ["loopback", "link-local", "locale unico (ULA)", "multicast", "unicast globale", "documentazione (esempi)"])

verifica("EUI-64 di 00:1B:21:3A:5C:01", eui64("00-1b-21-3a-5c-01") == "021b:21ff:fe3a:5c01")
verifica("EUI-64 inverte il bit U/L anche da 1 a 0", eui64("02:00:00:00:00:01").startswith("0000:00ff:fe00"))

with open("ipconfig_esempio.txt", encoding="utf-8") as f:
    trovati = indirizzi_da_ipconfig(f.read())
verifica("quattro indirizzi IPv6 trovati in ipconfig_esempio.txt", len(trovati) == 4)
verifica("indice di zona %11 rimosso", ("Gateway predefinito", "fe80::1") in trovati)
verifica("descrizione dell'indirizzo temporaneo letta",
         trovati[1] == ("Indirizzo IPv6 temporaneo", "2001:db8:4a2c:1100:5c9e:a7:e21b:9d04"))
inglese = "   Link-local IPv6 Address . . . . . : fe80::a1b2:c3d4:e5f6:1%7\n   IPv4 Address. . . : 10.0.0.5\n"
verifica("output in inglese", indirizzi_da_ipconfig(inglese) == [("Link-local IPv6 Address", "fe80::a1b2:c3d4:e5f6:1")])

print(f"\nTest superati: {superati}, falliti: {falliti}")
