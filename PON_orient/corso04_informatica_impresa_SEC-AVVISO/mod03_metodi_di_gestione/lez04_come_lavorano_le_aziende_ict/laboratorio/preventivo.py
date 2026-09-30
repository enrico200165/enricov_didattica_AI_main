"""Preventivo di un progetto software e confronto tra tipi di contratto.

Uso:
    python preventivo.py attivita.csv tariffe.json
    python preventivo.py attivita.csv tariffe.json --riserva 15 --margine 10 --scostamento 30

attivita.csv ha le colonne attivita, ruolo, giorni (giorni-persona stimati).
tariffe.json associa a ogni ruolo il costo di una giornata di lavoro in euro.

Il prezzo si costruisce così:
    costo del lavoro = somma di giorni x tariffa
    riserva per i rischi = percentuale del costo del lavoro
    margine = percentuale di (costo + riserva)
    imponibile = costo + riserva + margine;  IVA 22%;  totale = imponibile + IVA

Con --scostamento il programma simula un progetto che richiede più lavoro del
previsto e confronta chi paga la differenza con un contratto a corpo (prezzo
fisso) e con un contratto a tempo e materiali (si paga il lavoro svolto).
"""

import argparse
import csv
import json
import sys

ALIQUOTA_IVA = 22


class ErrorePreventivo(Exception):
    """Errore nei dati del preventivo."""


def leggi(percorso_attivita, percorso_tariffe):
    with open(percorso_tariffe, encoding="utf-8") as f:
        tariffe = json.load(f)
    attivita = []
    with open(percorso_attivita, encoding="utf-8", newline="") as f:
        lettore = csv.DictReader(f)
        mancanti = {"attivita", "ruolo", "giorni"} - set(lettore.fieldnames or [])
        if mancanti:
            raise ErrorePreventivo("colonne mancanti: " + ", ".join(sorted(mancanti)))
        for numero, riga in enumerate(lettore, start=2):
            ruolo = riga["ruolo"].strip()
            if ruolo not in tariffe:
                raise ErrorePreventivo(f"riga {numero}: nessuna tariffa per il ruolo \"{ruolo}\"")
            try:
                giorni = float(riga["giorni"].replace(",", "."))
            except ValueError:
                raise ErrorePreventivo(f"riga {numero}: i giorni devono essere un numero") from None
            if giorni <= 0:
                raise ErrorePreventivo(f"riga {numero}: i giorni devono essere positivi")
            attivita.append({"attivita": riga["attivita"].strip(), "ruolo": ruolo, "giorni": giorni})
    if not attivita:
        raise ErrorePreventivo("nessuna attività")
    return attivita, tariffe


def calcola(attivita, tariffe, riserva, margine):
    """Restituisce un dizionario con le voci del preventivo, in euro arrotondati al centesimo."""
    per_ruolo = {}
    for a in attivita:
        voce = per_ruolo.setdefault(a["ruolo"], {"giorni": 0.0, "costo": 0.0})
        voce["giorni"] += a["giorni"]
        voce["costo"] += a["giorni"] * tariffe[a["ruolo"]]
    costo = sum(v["costo"] for v in per_ruolo.values())
    quota_riserva = costo * riserva / 100
    quota_margine = (costo + quota_riserva) * margine / 100
    imponibile = costo + quota_riserva + quota_margine
    iva = imponibile * ALIQUOTA_IVA / 100
    return {"per_ruolo": per_ruolo, "giorni": sum(v["giorni"] for v in per_ruolo.values()),
            "costo": round(costo, 2), "riserva": round(quota_riserva, 2),
            "margine": round(quota_margine, 2), "imponibile": round(imponibile, 2),
            "iva": round(iva, 2), "totale": round(imponibile + iva, 2)}


def confronta_contratti(voci, scostamento, margine):
    """Confronta a corpo e tempo e materiali se il lavoro reale cresce di scostamento%.

    A corpo: il cliente paga l'imponibile concordato; il fornitore sostiene il costo reale.
    Tempo e materiali: il cliente paga il costo reale del lavoro più il margine; nessuna riserva.
    """
    costo_reale = voci["costo"] * (1 + scostamento / 100)
    a_corpo_cliente = voci["imponibile"]
    a_corpo_fornitore = a_corpo_cliente - costo_reale
    tm_cliente = costo_reale * (1 + margine / 100)
    tm_fornitore = tm_cliente - costo_reale
    return {"costo_reale": round(costo_reale, 2),
            "a_corpo": (round(a_corpo_cliente, 2), round(a_corpo_fornitore, 2)),
            "tempo_materiali": (round(tm_cliente, 2), round(tm_fornitore, 2))}


def euro(valore):
    """Formato italiano: 12.345,60 euro."""
    testo = f"{valore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{testo} euro"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Preventivo di un progetto software")
    parser.add_argument("attivita", help="file CSV con attivita, ruolo, giorni")
    parser.add_argument("tariffe", help="file JSON con la tariffa giornaliera di ogni ruolo")
    parser.add_argument("--riserva", type=float, default=15, help="riserva per i rischi, percentuale (predefinita 15)")
    parser.add_argument("--margine", type=float, default=10, help="margine del fornitore, percentuale (predefinito 10)")
    parser.add_argument("--scostamento", type=float, help="lavoro reale in più rispetto alla stima, percentuale")
    argomenti = parser.parse_args(argv)
    try:
        attivita, tariffe = leggi(argomenti.attivita, argomenti.tariffe)
    except (ErrorePreventivo, OSError, json.JSONDecodeError) as e:
        print(f"Errore: {e}")
        return 1
    voci = calcola(attivita, tariffe, argomenti.riserva, argomenti.margine)
    print(f"{'Ruolo':<20}{'Giorni':>8}{'Tariffa':>16}{'Costo':>20}")
    for ruolo, v in voci["per_ruolo"].items():
        print(f"{ruolo:<20}{v['giorni']:>8g}{euro(tariffe[ruolo]):>16}{euro(v['costo']):>20}")
    print(f"\n{'Costo del lavoro':<34}{euro(voci['costo']):>30}  ({voci['giorni']:g} giorni-persona)")
    print(f"{'Riserva per i rischi ' + format(argomenti.riserva, 'g') + '%':<34}{euro(voci['riserva']):>30}")
    print(f"{'Margine ' + format(argomenti.margine, 'g') + '%':<34}{euro(voci['margine']):>30}")
    print(f"{'Prezzo (imponibile)':<34}{euro(voci['imponibile']):>30}")
    print(f"{'IVA ' + str(ALIQUOTA_IVA) + '%':<34}{euro(voci['iva']):>30}")
    print(f"{'Totale':<34}{euro(voci['totale']):>30}")
    if argomenti.scostamento is not None:
        c = confronta_contratti(voci, argomenti.scostamento, argomenti.margine)
        print(f"\nSe il lavoro reale è il {argomenti.scostamento:g}% in più del previsto "
              f"(costo reale {euro(c['costo_reale'])}), IVA esclusa:")
        print(f"{'Contratto':<22}{'Paga il cliente':>24}{'Guadagno del fornitore':>26}")
        for nome, chiave in (("A corpo", "a_corpo"), ("Tempo e materiali", "tempo_materiali")):
            paga, guadagno = c[chiave]
            print(f"{nome:<22}{euro(paga):>24}{euro(guadagno):>26}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
