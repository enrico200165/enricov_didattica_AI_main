"""Piano di indirizzamento con sottoreti di dimensione variabile (VLSM).

Legge da un file CSV le sottoreti richieste (nome, numero di indirizzi per
dispositivi, gateway compreso) e le ricava da un blocco assegnato,
dalla più grande alla più piccola.

Uso:
    python piano_vlsm.py 10.20.0.0/22 requisiti_scuola.csv
Il piano viene stampato e salvato in piano_calcolato.csv.
"""

import csv
import ipaddress
import sys


def prefisso_necessario(host):
    """Prefisso più lungo (sottorete più piccola) che contiene 'host' indirizzi usabili.

    Una sottorete /p ha 2**(32-p) indirizzi, di cui 2 riservati (rete e broadcast);
    per 2 soli host si usa comunque /30, la scelta tradizionale per i collegamenti tra router.
    """
    if host < 1:
        raise ValueError("serve almeno un host")
    bit_host = 2
    while 2 ** bit_host - 2 < host:
        bit_host += 1
    return 32 - bit_host


def leggi_requisiti(percorso):
    with open(percorso, newline="", encoding="utf-8") as f:
        return [(riga["nome"], int(riga["host"])) for riga in csv.DictReader(f)]


def calcola_piano(blocco, requisiti):
    """Restituisce l'elenco delle sottoreti assegnate e i blocchi rimasti liberi.

    Ordinare dalla più grande alla più piccola garantisce che ogni sottorete
    inizi a un indirizzo multiplo della sua dimensione (allineata).
    """
    blocco = ipaddress.ip_network(blocco)       # ValueError se l'indirizzo non è quello di rete
    ordinati = sorted(requisiti, key=lambda r: r[1], reverse=True)
    piano = []
    prossimo = int(blocco.network_address)
    for nome, host in ordinati:
        prefisso = prefisso_necessario(host)
        dimensione = 2 ** (32 - prefisso)
        # arrotonda al primo indirizzo allineato (necessario solo con ordini diversi)
        prossimo = -(-prossimo // dimensione) * dimensione
        sottorete = ipaddress.ip_network(f"{ipaddress.IPv4Address(prossimo)}/{prefisso}")
        if not sottorete.subnet_of(blocco):
            raise ValueError(f"spazio insufficiente nel blocco {blocco} per {nome}")
        piano.append({"nome": nome, "richiesti": host, "rete": sottorete})
        prossimo += dimensione
    liberi = blocchi_liberi(blocco, [p["rete"] for p in piano])
    return piano, liberi


def blocchi_liberi(blocco, usate):
    """Parti del blocco non assegnate, come elenco di sottoreti."""
    liberi = [blocco]
    for rete in usate:
        nuovi = []
        for libero in liberi:
            if rete.subnet_of(libero):
                nuovi.extend(libero.address_exclude(rete))  # toglie 'rete' da 'libero'
            else:
                nuovi.append(libero)
        liberi = nuovi
    return sorted(ipaddress.collapse_addresses(liberi))


def verifica_piano(blocco, piano):
    """True se tutte le sottoreti sono nel blocco, non si sovrappongono e bastano ai requisiti."""
    blocco = ipaddress.ip_network(blocco)
    reti = [p["rete"] for p in piano]
    nel_blocco = all(r.subnet_of(blocco) for r in reti)
    separate = all(not a.overlaps(b) for i, a in enumerate(reti) for b in reti[i + 1:])
    sufficienti = all(p["rete"].num_addresses - 2 >= p["richiesti"] for p in piano)
    return nel_blocco and separate and sufficienti


def aggrega(reti):
    """Riassume un elenco di reti contigue nel minor numero di prefissi (aggregazione)."""
    return list(ipaddress.collapse_addresses(ipaddress.ip_network(r) for r in reti))


def righe_piano(piano):
    """Per ogni sottorete: valori da mostrare o salvare. Gateway = primo host."""
    righe = []
    for p in piano:
        r = p["rete"]
        disponibili = r.num_addresses - 2
        righe.append({
            "nome": p["nome"], "richiesti": p["richiesti"], "rete": str(r),
            "maschera": str(r.netmask), "gateway": str(r[1]),
            "primo_host": str(r[1]), "ultimo_host": str(r[-2]), "broadcast": str(r[-1]),
            "disponibili": disponibili, "utilizzo": f"{100 * p['richiesti'] / disponibili:.0f}%",
        })
    return righe


def main(blocco, percorso):
    try:
        piano, liberi = calcola_piano(blocco, leggi_requisiti(percorso))
    except ValueError as errore:
        print(f"Piano impossibile: {errore}")   # blocco non valido o troppo piccolo
        return
    righe = righe_piano(piano)
    print(f"{'Nome':<22}{'Rich.':>6}  {'Rete':<18}{'Maschera':<17}{'Gateway':<15}{'Broadcast':<15}{'Disp.':>6}{'Uso':>6}")
    for r in righe:
        print(f"{r['nome']:<22}{r['richiesti']:>6}  {r['rete']:<18}{r['maschera']:<17}"
              f"{r['gateway']:<15}{r['broadcast']:<15}{r['disponibili']:>6}{r['utilizzo']:>6}")
    usati = sum(p["rete"].num_addresses for p in piano)
    totale = ipaddress.ip_network(blocco).num_addresses
    print(f"\nIndirizzi assegnati: {usati} su {totale}; blocchi liberi: {', '.join(map(str, liberi)) or 'nessuno'}")
    print("Verifica (nel blocco, senza sovrapposizioni, sufficienti):",
          "superata" if verifica_piano(blocco, piano) else "NON superata")
    with open("piano_calcolato.csv", "w", newline="", encoding="utf-8") as f:
        scrittore = csv.DictWriter(f, fieldnames=list(righe[0]))
        scrittore.writeheader()
        scrittore.writerows(righe)
    print("Piano salvato in piano_calcolato.csv")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
    else:
        main(sys.argv[1], sys.argv[2])
