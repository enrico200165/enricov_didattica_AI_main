"""Calcoli di base per progettare un'architettura cloud: disponibilità e capacità.

- componenti in serie (servono tutti): disponibilità = prodotto delle disponibilità
- componenti in parallelo (basta uno): indisponibilità = prodotto delle indisponibilità
- tempo di fermo corrispondente a una percentuale di disponibilità
- numero di server necessari per un carico, con un margine

Uso: python disponibilita.py
"""

import math

ORE_ANNO = 365 * 24


def serie(*disponibilita):
    risultato = 1.0
    for d in disponibilita:
        risultato *= d
    return risultato


def parallelo(*disponibilita):
    indisponibile = 1.0
    for d in disponibilita:
        indisponibile *= 1 - d          # si ferma tutto solo se si fermano tutti insieme
    return 1 - indisponibile


def fermo_annuo(disponibilita):
    """Ore di fermo in un anno."""
    return (1 - disponibilita) * ORE_ANNO


def formato_fermo(ore):
    if ore >= 24:
        return f"{ore / 24:.1f} giorni"
    if ore >= 1:
        return f"{ore:.1f} ore"
    return f"{ore * 60:.0f} minuti"


def server_necessari(richieste_al_secondo, capacita_server, margine=0.3, riserva=1):
    """Server per sostenere il carico con un margine di sicurezza, più quelli di riserva (N+1)."""
    return math.ceil(richieste_al_secondo * (1 + margine) / capacita_server) + riserva


def dimostrazione():
    print("Disponibilità e fermo annuo:")
    for d in (0.99, 0.999, 0.9999):
        print(f"  {d:.2%}  ->  {formato_fermo(fermo_annuo(d))} all'anno")

    server = 0.995            # una macchina virtuale
    bilanciatore = 0.9999     # servizio di bilanciamento del carico del fornitore
    database = 0.9995         # database gestito con replica
    singolo = serie(server, database)
    ridondato = serie(bilanciatore, parallelo(server, server), database)
    print("\nServizio della biblioteca:")
    print(f"  un server + database:                 {singolo:.4%}  fermo {formato_fermo(fermo_annuo(singolo))}")
    print(f"  bilanciatore + 2 server + database:   {ridondato:.4%}  fermo {formato_fermo(fermo_annuo(ridondato))}")

    print("\nCapacità: 900 richieste al secondo nel picco, 200 per server")
    print(f"  server necessari (margine 30%, uno di riserva): {server_necessari(900, 200)}")


if __name__ == "__main__":
    dimostrazione()
