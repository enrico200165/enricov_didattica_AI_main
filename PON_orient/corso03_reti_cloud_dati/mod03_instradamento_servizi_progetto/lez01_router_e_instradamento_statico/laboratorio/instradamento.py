"""Instradamento IPv4 con tabelle statiche: scelta della rotta e percorso di un pacchetto.

Ogni router ha una tabella con voci (destinazione, prossimo salto, interfaccia).
Per ogni pacchetto il router sceglie la voce la cui destinazione contiene
l'indirizzo cercato con il prefisso più lungo (longest prefix match),
diminuisce il TTL di 1 e inoltra il pacchetto.

Uso:
    python instradamento.py                   percorso di alcuni pacchetti nella rete di esempio
    python instradamento.py route_esempio.txt  legge la tabella di "route print" di Windows
"""

import ipaddress
import re
import sys


class Router:
    def __init__(self, nome):
        self.nome = nome
        self.tabella = []  # elenco di (rete, prossimo_salto, interfaccia)

    def aggiungi(self, destinazione, prossimo_salto=None, interfaccia=""):
        """prossimo_salto None indica una rete direttamente connessa."""
        self.tabella.append((ipaddress.ip_network(destinazione), prossimo_salto, interfaccia))

    def scegli(self, indirizzo):
        """Voce con il prefisso più lungo che contiene l'indirizzo, oppure None."""
        indirizzo = ipaddress.ip_address(indirizzo)
        candidate = [voce for voce in self.tabella if indirizzo in voce[0]]
        if not candidate:
            return None
        return max(candidate, key=lambda voce: voce[0].prefixlen)


def percorso(routers, primo_router, destinazione, ttl=64):
    """Segue un pacchetto di router in router.

    routers: dizionario indirizzo IP di un'interfaccia -> oggetto Router
    Restituisce (esito, elenco dei router attraversati).
    """
    attraversati = []
    router = primo_router
    while True:
        attraversati.append(router.nome)
        ttl -= 1                                   # ogni router diminuisce il TTL
        if ttl == 0:
            return "TTL scaduto (ICMP time exceeded)", attraversati
        voce = router.scegli(destinazione)
        if voce is None:
            return "destinazione irraggiungibile (ICMP destination unreachable)", attraversati
        rete, prossimo, _ = voce
        if prossimo is None:                       # rete direttamente connessa
            return "consegnato", attraversati
        if prossimo not in routers:
            return f"prossimo salto {prossimo} sconosciuto", attraversati
        router = routers[prossimo]


def rete_di_esempio():
    """Tre reti locali collegate da due router, come nel laboratorio in Filius.

    192.168.1.0/24 --- R1 --- 192.168.2.0/24 --- R2 --- 192.168.3.0/24 --- R3 --- Internet
    """
    r1, r2, r3 = Router("R1"), Router("R2"), Router("R3")
    r1.aggiungi("192.168.1.0/24", None, "192.168.1.1")
    r1.aggiungi("192.168.2.0/24", None, "192.168.2.1")
    r1.aggiungi("192.168.3.0/24", "192.168.2.2", "192.168.2.1")   # rotta statica
    r1.aggiungi("0.0.0.0/0", "192.168.2.2", "192.168.2.1")        # rotta predefinita

    r2.aggiungi("192.168.2.0/24", None, "192.168.2.2")
    r2.aggiungi("192.168.3.0/24", None, "192.168.3.1")
    r2.aggiungi("192.168.1.0/24", "192.168.2.1", "192.168.2.2")
    r2.aggiungi("0.0.0.0/0", "192.168.3.254", "192.168.3.1")

    r3.aggiungi("192.168.3.0/24", None, "192.168.3.254")
    r3.aggiungi("203.0.113.0/24", None, "203.0.113.2")            # rete verso il fornitore
    r3.aggiungi("192.168.0.0/22", "192.168.3.1", "192.168.3.254")  # rotta aggregata verso la scuola
    routers = {"192.168.1.1": r1, "192.168.2.1": r1, "192.168.2.2": r2,
               "192.168.3.1": r2, "192.168.3.254": r3}
    return routers, r1, r2, r3


# Una riga della tabella IPv4 di "route print": destinazione, maschera, gateway, interfaccia, metrica
MODELLO_ROUTE = re.compile(r"^\s*(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s*$")


def leggi_route_print(testo):
    """Estrae le rotte attive IPv4 dall'output di "route print -4" (italiano o inglese)."""
    rotte = []
    for riga in testo.splitlines():
        m = MODELLO_ROUTE.match(riga)
        if m:
            destinazione, maschera, gateway, interfaccia, metrica = m.groups()
            rete = ipaddress.ip_network(f"{destinazione}/{maschera}")
            # "On-link" (o una parola equivalente): rete direttamente connessa
            prossimo = gateway if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", gateway) else None
            rotte.append({"rete": rete, "gateway": prossimo, "interfaccia": interfaccia,
                          "metrica": int(metrica)})
    return rotte


def rotta_per(rotte, indirizzo):
    """Rotta scelta da Windows: prefisso più lungo, a parità la metrica più bassa."""
    indirizzo = ipaddress.ip_address(indirizzo)
    candidate = [r for r in rotte if indirizzo in r["rete"]]
    if not candidate:
        return None
    return min(candidate, key=lambda r: (-r["rete"].prefixlen, r["metrica"]))


def dimostrazione():
    routers, r1, r2, _ = rete_di_esempio()
    for destinazione in ["192.168.3.20", "203.0.113.80", "198.51.100.7"]:
        esito, via = percorso(routers, r1, destinazione)
        print(f"da 192.168.1.x a {destinazione}: {esito}; router: {' -> '.join(via)}")
    # Errore di configurazione: R2 rimanda a R1 il traffico per Internet, R1 lo rimanda a R2
    r2.tabella = [v for v in r2.tabella if v[0].prefixlen != 0]
    r2.aggiungi("0.0.0.0/0", "192.168.2.1", "192.168.2.2")
    esito, via = percorso(routers, r1, "198.51.100.7", ttl=8)
    print(f"con un ciclo di instradamento e TTL 8: {esito}; router: {' -> '.join(via)}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], encoding="utf-8") as f:
            rotte = leggi_route_print(f.read())
        for r in rotte:
            print(f"{str(r['rete']):<20}{r['gateway'] or 'diretta':<16}{r['interfaccia']:<16}{r['metrica']}")
        scelta = rotta_per(rotte, "8.8.8.8")
        print(f"\nRotta per 8.8.8.8: {scelta['rete']} tramite {scelta['gateway'] or 'consegna diretta'}")
    else:
        dimostrazione()
