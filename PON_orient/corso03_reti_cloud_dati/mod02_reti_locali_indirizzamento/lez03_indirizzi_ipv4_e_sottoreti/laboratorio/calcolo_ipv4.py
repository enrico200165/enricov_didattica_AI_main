"""Calcoli sugli indirizzi IPv4 eseguiti "a mano" con le operazioni sui bit,
e confrontati con il modulo ipaddress della libreria standard di Python.

Uso:
    python calcolo_ipv4.py 192.168.10.77/26     analisi completa, anche in binario
    python calcolo_ipv4.py --esercizi 5         cinque esercizi con correzione
"""

import ipaddress
import random
import sys


def ip_a_intero(testo):
    """'192.168.1.10' -> intero a 32 bit. ValueError se non valido."""
    parti = testo.split(".")
    if len(parti) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parti):
        raise ValueError(f"indirizzo IPv4 non valido: {testo}")
    valore = 0
    for p in parti:
        valore = (valore << 8) | int(p)   # sposta di 8 bit a sinistra e aggiunge il byte
    return valore


def intero_a_ip(valore):
    """Intero a 32 bit -> notazione decimale puntata."""
    return ".".join(str((valore >> spostamento) & 0xFF) for spostamento in (24, 16, 8, 0))


def in_binario(valore):
    """Intero a 32 bit -> quattro gruppi di 8 bit separati da punti."""
    bit = format(valore, "032b")
    return ".".join(bit[i:i + 8] for i in range(0, 32, 8))


def maschera_da_prefisso(prefisso):
    """/26 -> 26 bit a 1 seguiti da 6 bit a 0, come intero."""
    if not 0 <= prefisso <= 32:
        raise ValueError("il prefisso deve essere tra 0 e 32")
    return (0xFFFFFFFF << (32 - prefisso)) & 0xFFFFFFFF


def prefisso_da_maschera(testo):
    """'255.255.255.192' -> 26. ValueError se gli 1 non sono tutti a sinistra."""
    valore = ip_a_intero(testo)
    prefisso = format(valore, "032b").count("1")
    if maschera_da_prefisso(prefisso) != valore:
        raise ValueError(f"maschera non valida: {testo}")
    return prefisso


def classe_storica(valore):
    """Classe dell'indirizzo nel sistema precedente al CIDR, dai primi bit."""
    primo = valore >> 24
    if primo < 128:
        return "A"     # primo bit 0
    if primo < 192:
        return "B"     # primi bit 10
    if primo < 224:
        return "C"     # primi bit 110
    if primo < 240:
        return "D (multicast)"
    return "E (riservata)"


# Blocchi privati definiti dall'RFC 1918
PRIVATI = [("10.0.0.0", 8), ("172.16.0.0", 12), ("192.168.0.0", 16)]


def privato(valore):
    return any(valore & maschera_da_prefisso(p) == ip_a_intero(rete) for rete, p in PRIVATI)


def analizza(cidr):
    """'192.168.10.77/26' -> dizionario con tutti i valori calcolati."""
    indirizzo, prefisso = cidr.split("/")
    ip = ip_a_intero(indirizzo)
    prefisso = int(prefisso)
    maschera = maschera_da_prefisso(prefisso)
    rete = ip & maschera                        # AND: azzera la parte host
    broadcast = rete | (~maschera & 0xFFFFFFFF)  # OR: mette a 1 la parte host
    totale = 2 ** (32 - prefisso)
    if prefisso <= 30:
        primo, ultimo, host = rete + 1, broadcast - 1, totale - 2
    else:
        # /31: collegamenti punto-punto, entrambi gli indirizzi usabili (RFC 3021); /32: un solo host
        primo, ultimo, host = rete, broadcast, totale
    return {
        "indirizzo": intero_a_ip(ip),
        "prefisso": prefisso,
        "maschera": intero_a_ip(maschera),
        "rete": intero_a_ip(rete),
        "broadcast": intero_a_ip(broadcast),
        "primo_host": intero_a_ip(primo),
        "ultimo_host": intero_a_ip(ultimo),
        "indirizzi_totali": totale,
        "host": host,
        "classe_storica": classe_storica(ip),
        "privato": privato(ip),
        "_binari": {"indirizzo": in_binario(ip), "maschera": in_binario(maschera),
                    "rete": in_binario(rete), "broadcast": in_binario(broadcast)},
    }


def calcola_con_ipaddress(cidr):
    """Gli stessi valori ottenuti con il modulo ipaddress, per il confronto."""
    interfaccia = ipaddress.ip_interface(cidr)   # indirizzo con la sua rete
    rete = interfaccia.network
    if rete.prefixlen >= 31:
        host = list(rete.hosts())            # al massimo due indirizzi
        primo, ultimo, numero = host[0], host[-1], len(host)
    else:
        # hosts() esclude rete e broadcast; per reti grandi non si crea l'elenco completo
        primo = next(iter(rete.hosts()))
        ultimo = rete[-2]                    # rete[-1] è il broadcast
        numero = rete.num_addresses - 2
    return {
        "maschera": str(rete.netmask),
        "rete": str(rete.network_address),
        "broadcast": str(rete.broadcast_address),
        "primo_host": str(primo),
        "ultimo_host": str(ultimo),
        "indirizzi_totali": rete.num_addresses,
        "host": numero,
        "privato": interfaccia.ip in ipaddress.ip_network("10.0.0.0/8")
        or interfaccia.ip in ipaddress.ip_network("172.16.0.0/12")
        or interfaccia.ip in ipaddress.ip_network("192.168.0.0/16"),
    }


def concordano(cidr):
    """True se il calcolo a mano e ipaddress danno gli stessi risultati."""
    a_mano = analizza(cidr)
    return all(a_mano[k] == v for k, v in calcola_con_ipaddress(cidr).items())


def stampa(cidr):
    r = analizza(cidr)
    print(f"Indirizzo  {r['indirizzo']:<16} {r['_binari']['indirizzo']}")
    print(f"Maschera   {r['maschera']:<16} {r['_binari']['maschera']}   (/{r['prefisso']})")
    print(f"Rete       {r['rete']:<16} {r['_binari']['rete']}   (indirizzo AND maschera)")
    print(f"Broadcast  {r['broadcast']:<16} {r['_binari']['broadcast']}   (parte host tutta a 1)")
    print(f"Host       da {r['primo_host']} a {r['ultimo_host']}: {r['host']} indirizzi usabili "
          f"su {r['indirizzi_totali']}")
    print(f"Classe storica {r['classe_storica']}; privato (RFC 1918): {'sì' if r['privato'] else 'no'}")
    print(f"Confronto con ipaddress: {'concorde' if concordano(cidr) else 'DIVERSO'}")


def esercizi(quanti, seme=None):
    """Genera esercizi casuali e corregge le risposte con ipaddress."""
    generatore = random.Random(seme)
    punti = 0
    for n in range(1, quanti + 1):
        prefisso = generatore.randint(16, 30)
        ip = intero_a_ip(generatore.choice([ip_a_intero("10.0.0.0"), ip_a_intero("172.16.0.0"),
                                            ip_a_intero("192.168.0.0")]) + generatore.randint(1, 65534))
        cidr = f"{ip}/{prefisso}"
        corretto = calcola_con_ipaddress(cidr)
        print(f"\nEsercizio {n}: {cidr}")
        risposte = {
            "rete": input("  indirizzo di rete: ").strip(),
            "broadcast": input("  indirizzo di broadcast: ").strip(),
            "host": input("  numero di host usabili: ").strip(),
        }
        for chiave, risposta in risposte.items():
            giusto = str(corretto[chiave])
            if risposta == giusto:
                punti += 1
                print(f"  {chiave}: corretto")
            else:
                print(f"  {chiave}: errato, la risposta è {giusto}")
    print(f"\nPunteggio: {punti} su {quanti * 3}")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--esercizi":
        esercizi(int(sys.argv[2]))
    elif len(sys.argv) == 2:
        stampa(sys.argv[1])
    else:
        print(__doc__)
