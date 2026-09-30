"""Piano di indirizzamento per una rete segmentata (VLAN), con sottoreti di dimensione variabile.

Dato un blocco di indirizzi e il numero di dispositivi di ciascun segmento, assegna a ogni
segmento la sottorete più piccola sufficiente, lasciando un margine di crescita, a partire
dai segmenti più grandi. Solo libreria standard di Python.
"""

import ipaddress
import math

MARGINE = 0.5   # 50% di indirizzi in più rispetto ai dispositivi previsti


def prefisso_per(dispositivi, margine=MARGINE):
    """Prefisso della sottorete più piccola che contiene i dispositivi, il margine, il gateway,
    l'indirizzo di rete e quello di broadcast."""
    necessari = math.ceil(dispositivi * (1 + margine)) + 3
    bit_host = max(2, math.ceil(math.log2(necessari)))
    return 32 - bit_host


def piano(blocco, segmenti, margine=MARGINE):
    """Lista di dizionari, uno per segmento, nell'ordine di assegnazione.

    segmenti: dizionario {nome: (vlan, dispositivi)}.
    """
    rete = ipaddress.ip_network(blocco)
    ordinati = sorted(segmenti.items(), key=lambda s: (-s[1][1], s[1][0]))
    prossimo = rete.network_address
    risultato = []
    for nome, (vlan, dispositivi) in ordinati:
        prefisso = prefisso_per(dispositivi, margine)
        sottorete = ipaddress.ip_network(f"{prossimo}/{prefisso}")   # blocchi decrescenti: già allineato
        if not sottorete.subnet_of(rete):
            raise ValueError(f"indirizzi insufficienti nel blocco {rete} per il segmento '{nome}'")
        host = list(sottorete.hosts())
        risultato.append({
            "nome": nome, "vlan": vlan, "dispositivi": dispositivi, "sottorete": sottorete,
            "gateway": host[0], "primo": host[1], "ultimo": host[-1],
            "capacita": len(host) - 1,   # indirizzi utilizzabili escluso il gateway
        })
        prossimo = sottorete.broadcast_address + 1
    return risultato


def stampa(voci):
    print(f"{'VLAN':>4}  {'Segmento':<24} {'Disp.':>5} {'Sottorete':<18} {'Gateway':<15} {'Intervallo':<33} {'Capacità':>8}")
    for v in sorted(voci, key=lambda v: v["vlan"]):
        intervallo = f"{v['primo']} - {v['ultimo']}"
        print(f"{v['vlan']:>4}  {v['nome']:<24} {v['dispositivi']:>5} {str(v['sottorete']):<18} "
              f"{str(v['gateway']):<15} {intervallo:<33} {v['capacita']:>8}")


if __name__ == "__main__":
    scuola = {
        "server e rete": (10, 12),
        "segreteria": (20, 15),
        "docenti": (30, 60),
        "laboratori": (40, 120),
        "Wi-Fi studenti": (50, 400),
        "Wi-Fi ospiti": (60, 50),
        "stampanti e dispositivi": (70, 25),
        "videosorveglianza": (80, 16),
    }
    stampa(piano("10.20.0.0/20", scuola))
