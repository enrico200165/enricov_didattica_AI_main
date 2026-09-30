"""Dimensionamento della rete di un piano di un edificio.

Legge le stanze da un file CSV e calcola, secondo regole di progetto semplici:
- punti rete (prese) per stanza e loro VLAN
- access point Wi-Fi necessari
- porte di switch e numero di switch, con un margine di riserva
- consumo PoE (alimentazione attraverso il cavo di rete) di access point e telecamere
- controllo della lunghezza delle tratte di cavo in rame

Uso: python progetto_piano.py stanze_piano.csv
"""

import csv
import math
import sys

# Regole di progetto (modificabili)
UTENTI_PER_AP = 30          # dispositivi Wi-Fi contemporanei per access point
POTENZA_AP_W = 25.5         # potenza disponibile al dispositivo con PoE+ (IEEE 802.3at)
POTENZA_TELECAMERA_W = 12.95  # potenza disponibile al dispositivo con PoE (IEEE 802.3af)
PORTE_PER_SWITCH = 48
PORTE_UPLINK = 2            # porte riservate al collegamento verso il centro stella
MARGINE = 0.20              # 20% di porte di riserva
LUNGHEZZA_MAX_M = 90        # tratta fissa massima (più 10 m di cavi di collegamento = 100 m)
BUDGET_POE_SWITCH_W = 370   # potenza PoE totale di uno switch (valore tipico, da scheda tecnica)

VLAN = {"didattica": 10, "uffici": 20, "telecamere": 30, "wifi_gestione": 40, "stampanti": 50}


def leggi_stanze(percorso):
    with open(percorso, newline="", encoding="utf-8") as f:
        stanze = []
        for riga in csv.DictReader(f):
            for campo in ("postazioni", "utenti_wifi", "telecamere", "stampanti", "distanza_m"):
                riga[campo] = int(riga[campo])
            stanze.append(riga)
        return stanze


def progetta(stanze):
    risultato = {"stanze": [], "prese_per_vlan": {nome: 0 for nome in VLAN}, "avvisi": []}
    for s in stanze:
        ap = math.ceil(s["utenti_wifi"] / UTENTI_PER_AP)          # arrotondamento per eccesso
        vlan_postazioni = "uffici" if s["tipo"] == "ufficio" else "didattica"
        prese = {vlan_postazioni: s["postazioni"], "telecamere": s["telecamere"],
                 "wifi_gestione": ap, "stampanti": s["stampanti"]}
        for nome, numero in prese.items():
            risultato["prese_per_vlan"][nome] += numero
        totale = sum(prese.values())
        risultato["stanze"].append({"stanza": s["stanza"], "access_point": ap, "prese": totale})
        if s["distanza_m"] > LUNGHEZZA_MAX_M and totale > 0:
            risultato["avvisi"].append(f"{s['stanza']}: {s['distanza_m']} m dall'armadio, oltre {LUNGHEZZA_MAX_M} m: "
                                       "serve un armadio di piano più vicino o una tratta in fibra")
    porte = sum(risultato["prese_per_vlan"].values())
    porte_con_margine = math.ceil(porte * (1 + MARGINE))
    switch = math.ceil(porte_con_margine / (PORTE_PER_SWITCH - PORTE_UPLINK))
    ap_totali = risultato["prese_per_vlan"]["wifi_gestione"]
    telecamere = risultato["prese_per_vlan"]["telecamere"]
    potenza = ap_totali * POTENZA_AP_W + telecamere * POTENZA_TELECAMERA_W
    risultato.update({"porte": porte, "porte_con_margine": porte_con_margine, "switch": switch,
                      "access_point": ap_totali, "potenza_poe_w": round(potenza, 1)})
    if potenza > BUDGET_POE_SWITCH_W * switch:
        risultato["avvisi"].append(f"potenza PoE {potenza:.0f} W oltre il budget di {switch} switch")
    return risultato


def stampa(r):
    print(f"{'Stanza':<18}{'AP':>4}{'Prese':>7}")
    for s in r["stanze"]:
        print(f"{s['stanza']:<18}{s['access_point']:>4}{s['prese']:>7}")
    print("\nPrese per VLAN:")
    for nome, numero in r["prese_per_vlan"].items():
        print(f"  VLAN {VLAN[nome]:<3} {nome:<15}{numero:>4}")
    print(f"\nPorte necessarie: {r['porte']}; con il {MARGINE:.0%} di riserva: {r['porte_con_margine']}")
    print(f"Switch da {PORTE_PER_SWITCH} porte ({PORTE_UPLINK} di uplink): {r['switch']}")
    print(f"Access point: {r['access_point']}; potenza PoE stimata: {r['potenza_poe_w']} W")
    for avviso in r["avvisi"]:
        print("AVVISO:", avviso)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
    else:
        stampa(progetta(leggi_stanze(sys.argv[1])))
