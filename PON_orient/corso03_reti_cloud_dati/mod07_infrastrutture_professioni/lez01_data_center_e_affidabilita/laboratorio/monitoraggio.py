"""Monitoraggio della disponibilità di un servizio web e indicatori di affidabilità.

- controlla periodicamente un indirizzo e registra l'esito in un file CSV
- dal registro calcola disponibilità misurata, interruzioni, MTTR, MTBF, tempi di risposta
- calcola la disponibilità attesa da MTBF e MTTR e l'efficienza energetica (PUE) di un data center

Uso:
    python monitoraggio.py registra http://127.0.0.1:8000/api/generi 120 5 registro.csv
        (120 controlli, uno ogni 5 secondi)
    python monitoraggio.py analizza registro.csv
    python monitoraggio.py analizza registro_controlli_esempio.csv
"""

import csv
import datetime
import statistics
import sys
import time
import urllib.error
import urllib.request


def controlla(url, timeout=3):
    """Una richiesta GET. Restituisce (riuscito, millisecondi, codice o descrizione dell'errore)."""
    inizio = time.perf_counter()
    apri = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # senza proxy: servizio locale
    try:
        with apri.open(url, timeout=timeout) as risposta:
            codice = risposta.status
    except urllib.error.HTTPError as e:
        codice = e.code
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        return False, round((time.perf_counter() - inizio) * 1000), type(e).__name__
    millisecondi = round((time.perf_counter() - inizio) * 1000)
    return 200 <= codice < 300, millisecondi, codice


def registra(url, quanti, intervallo, percorso):
    with open(percorso, "w", newline="", encoding="utf-8") as f:
        scrittore = csv.writer(f)
        scrittore.writerow(["istante", "riuscito", "millisecondi", "esito"])
        for i in range(quanti):
            riuscito, ms, esito = controlla(url)
            istante = datetime.datetime.now().isoformat(timespec="seconds")
            scrittore.writerow([istante, int(riuscito), ms, esito])
            f.flush()                                    # il file è leggibile anche durante la registrazione
            print(f"{istante}  {'OK     ' if riuscito else 'GUASTO '}{ms:>5} ms  {esito}")
            if i < quanti - 1:
                time.sleep(intervallo)


def analizza(percorso):
    """Indicatori calcolati dal registro dei controlli."""
    with open(percorso, newline="", encoding="utf-8") as f:
        righe = [(datetime.datetime.fromisoformat(r["istante"]), r["riuscito"] == "1", int(r["millisecondi"]))
                 for r in csv.DictReader(f)]
    riusciti = [r for r in righe if r[1]]
    # interruzioni: sequenze consecutive di controlli falliti
    interruzioni, inizio = [], None
    for i, (istante, ok, _) in enumerate(righe):
        if not ok and inizio is None:
            inizio = istante
        if ok and inizio is not None:
            interruzioni.append((inizio, istante))       # termina al primo controllo di nuovo riuscito
            inizio = None
    if inizio is not None:
        interruzioni.append((inizio, righe[-1][0]))      # interruzione ancora in corso alla fine
    durata_totale = (righe[-1][0] - righe[0][0]).total_seconds()
    fermo = sum((fine - ini).total_seconds() for ini, fine in interruzioni)
    tempi = sorted(r[2] for r in riusciti)
    return {
        "controlli": len(righe),
        "disponibilita_misurata": len(riusciti) / len(righe),
        "interruzioni": len(interruzioni),
        "fermo_secondi": fermo,
        # MTTR: tempo medio di ripristino; MTBF: tempo medio di funzionamento tra due guasti
        "mttr_secondi": fermo / len(interruzioni) if interruzioni else 0,
        "mtbf_secondi": (durata_totale - fermo) / len(interruzioni) if interruzioni else durata_totale,
        "risposta_mediana_ms": statistics.median(tempi) if tempi else None,
        "risposta_95_ms": tempi[min(len(tempi) - 1, int(0.95 * len(tempi)))] if tempi else None,
    }


def disponibilita_attesa(mtbf, mttr):
    """Disponibilità = MTBF / (MTBF + MTTR): conta quanto spesso ci si guasta e quanto si impiega a ripartire."""
    return mtbf / (mtbf + mttr)


def pue(potenza_totale_kw, potenza_it_kw):
    """Power Usage Effectiveness: energia totale del data center / energia dei soli apparati informatici."""
    return potenza_totale_kw / potenza_it_kw


def stampa_analisi(r):
    print(f"Controlli:               {r['controlli']}")
    print(f"Disponibilità misurata:  {r['disponibilita_misurata']:.2%}")
    print(f"Interruzioni:            {r['interruzioni']}  (fermo totale {r['fermo_secondi'] / 60:.1f} minuti)")
    print(f"MTTR:                    {r['mttr_secondi'] / 60:.1f} minuti")
    print(f"MTBF:                    {r['mtbf_secondi'] / 3600:.1f} ore")
    print(f"Tempo di risposta:       mediana {r['risposta_mediana_ms']} ms, 95° percentile {r['risposta_95_ms']} ms")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 5 and a[0] == "registra":
        registra(a[1], int(a[2]), float(a[3]), a[4])
    elif len(a) == 2 and a[0] == "analizza":
        stampa_analisi(analizza(a[1]))
    else:
        print(__doc__)
