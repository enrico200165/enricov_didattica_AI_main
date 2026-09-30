"""Stima del costo mensile di scenari cloud con un listino di esempio, e confronto con un server locale.

Uso:
    python costi_cloud.py                         tutti gli scenari di scenari.json
    python costi_cloud.py piattaforma_verifiche   un solo scenario, con il dettaglio delle voci
    python costi_cloud.py --locale                confronto con un server acquistato dalla scuola
I prezzi di listino_esempio.json sono inventati: servono a ragionare sulle voci di costo, non a
confrontare fornitori reali.
"""

import json
import sys


def carica(percorso):
    with open(percorso, encoding="utf-8") as f:
        return json.load(f)


def costo_scenario(s, listino):
    """Restituisce un dizionario voce -> costo mensile in euro (arrotondato al centesimo)."""
    voci = {}
    calcolo = 0.0
    for gruppo in s["vm"]:
        prezzo = listino["macchine_virtuali"][gruppo["tipo"]]["euro_ora"]
        if gruppo.get("impegno_1_anno"):
            prezzo *= 1 - listino["sconto_impegno_1_anno"]      # sconto in cambio dell'impegno per un anno
        calcolo += prezzo * gruppo["quantita"] * gruppo["ore_mese"]
    voci["calcolo (macchine virtuali)"] = calcolo
    voci["dischi"] = s["disco_gb"] * listino["disco_euro_gb_mese"]
    voci["database gestito"] = s["database_ore_mese"] * listino["database_gestito_euro_ora"]
    voci["archiviazione a oggetti"] = s["oggetti_gb"] * listino["oggetti_euro_gb_mese"]
    voci["richieste agli oggetti"] = s["richieste_oggetti_mese"] / 1000 * listino["richieste_oggetti_euro_1000"]
    uscita = max(0, s["traffico_uscita_gb"] - listino["traffico_uscita_gratuito_gb"])   # prima parte gratuita
    voci["traffico in uscita"] = uscita * listino["traffico_uscita_euro_gb"]
    return {k: round(v, 2) for k, v in voci.items()}


def costo_locale(prezzo_server=4000, anni=5, watt=250, euro_kwh=0.30, manutenzione_anno=400):
    """Costo mensile di un server acquistato: ammortamento, energia (sempre acceso), manutenzione.
    Non comprende locali, raffreddamento, rete, copie di sicurezza e tempo del personale."""
    ammortamento = prezzo_server / (anni * 12)
    energia = watt / 1000 * 730 * euro_kwh                  # kW x ore al mese x prezzo del kWh
    return {"ammortamento": round(ammortamento, 2), "energia": round(energia, 2),
            "manutenzione": round(manutenzione_anno / 12, 2)}


def stampa_dettaglio(nome, voci):
    print(f"\n{nome}")
    for voce, euro in sorted(voci.items(), key=lambda v: -v[1]):
        print(f"  {voce:<30}{euro:>10.2f} EUR")
    print(f"  {'totale mensile':<30}{sum(voci.values()):>10.2f} EUR   (annuale {12 * sum(voci.values()):.2f})")


def main(argomenti):
    listino = carica("listino_esempio.json")
    scenari = carica("scenari.json")
    if argomenti == ["--locale"]:
        stampa_dettaglio("Server locale (4000 EUR, 5 anni)", costo_locale())
        stampa_dettaglio("Cloud: sito_biblioteca", costo_scenario(scenari["sito_biblioteca"], listino))
        return
    nomi = argomenti or list(scenari)
    for nome in nomi:
        voci = costo_scenario(scenari[nome], listino)
        if argomenti:
            print(scenari[nome]["descrizione"])
            stampa_dettaglio(nome, voci)
        else:
            principale = max(voci, key=voci.get)
            print(f"{nome:<24}{sum(voci.values()):>10.2f} EUR/mese   voce principale: {principale}")


if __name__ == "__main__":
    main(sys.argv[1:])
