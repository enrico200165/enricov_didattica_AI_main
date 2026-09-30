"""Ricostruzione dei periodi di accensione di un PC dal registro eventi di sistema di Windows.

1. In PowerShell (il registro System è leggibile senza diritti di amministratore):

   Get-WinEvent -FilterHashtable @{LogName='System'; Id=6005,6006,6008,41} -MaxEvents 300 |
     Select-Object @{Name='Quando'; Expression={$_.TimeCreated.ToString('s')}}, Id, ProviderName |
     Export-Csv eventi_sistema.csv -NoTypeInformation -Encoding UTF8

2. python sessioni_pc.py eventi_sistema.csv

Eventi usati:
  6005  avvio del servizio Registro eventi (avvio di Windows)
  6006  arresto del servizio Registro eventi (spegnimento regolare)
  6008  lo spegnimento precedente non è stato regolare
  41    riavvio senza spegnimento regolare (Kernel-Power)
Solo libreria standard di Python.
"""

import csv
import sys
from datetime import datetime

AVVIO, ARRESTO, ARRESTO_IMPREVISTO, KERNEL_POWER = 6005, 6006, 6008, 41


def leggi_eventi(percorso):
    """Eventi (istante, id) in ordine cronologico."""
    with open(percorso, encoding="utf-8-sig", newline="") as f:
        eventi = [(datetime.fromisoformat(r["Quando"]), int(r["Id"])) for r in csv.DictReader(f)]
    return sorted(eventi)


def sessioni(eventi):
    """Lista di dizionari con inizio, fine (o None) e modo in cui la sessione è terminata."""
    risultato = []
    corrente = None
    for istante, codice in eventi:
        if codice == AVVIO:
            if corrente is not None:                      # nuovo avvio senza arresto registrato
                corrente["fine"], corrente["esito"] = None, "non regolare"
                risultato.append(corrente)
            corrente = {"inizio": istante, "fine": None, "esito": "in corso"}
        elif codice == ARRESTO and corrente is not None:
            corrente["fine"], corrente["esito"] = istante, "regolare"
            risultato.append(corrente)
            corrente = None
        elif codice in (ARRESTO_IMPREVISTO, KERNEL_POWER) and risultato:
            # l'evento viene scritto all'avvio successivo e riguarda la sessione precedente
            if risultato[-1]["esito"] != "regolare":
                risultato[-1]["esito"] = "non regolare"
    if corrente is not None:
        risultato.append(corrente)
    return risultato


def durata(sessione):
    if sessione["fine"] is None:
        return None
    return sessione["fine"] - sessione["inizio"]


def stampa(elenco):
    print(f"{'Accensione':<20} {'Spegnimento':<20} {'Durata':>9}  Esito")
    for s in elenco:
        fine = s["fine"].strftime("%d/%m/%Y %H:%M") if s["fine"] else "-"
        d = durata(s)
        testo_durata = f"{int(d.total_seconds() // 3600)}h {int(d.total_seconds() % 3600 // 60):02d}m" if d else "-"
        print(f"{s['inizio']:%d/%m/%Y %H:%M}     {fine:<20} {testo_durata:>9}  {s['esito']}")
    irregolari = sum(s["esito"] == "non regolare" for s in elenco)
    print(f"\nSessioni: {len(elenco)}; terminate in modo non regolare: {irregolari}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    stampa(sessioni(leggi_eventi(sys.argv[1])))
