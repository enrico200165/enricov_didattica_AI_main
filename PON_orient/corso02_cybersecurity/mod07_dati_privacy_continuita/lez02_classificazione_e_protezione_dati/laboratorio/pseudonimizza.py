"""Pseudonimizzazione di un file CSV di dati personali, per un'analisi statistica.

Uso:
    python pseudonimizza.py studenti_fittizi.csv studenti_pseudonimizzati.csv chiave.txt

- gli identificativi diretti (nome, cognome, email) vengono eliminati
- la matricola viene sostituita da uno pseudonimo calcolato con HMAC-SHA256 e una chiave segreta
- la data di nascita viene generalizzata all'anno
- la chiave viene creata, se non esiste, nel file indicato, da conservare separatamente dai dati
Con la chiave, e solo con essa, si ritrova lo pseudonimo di una matricola nota (per esempio per
aggiungere nuovi dati allo stesso studente); senza la chiave lo pseudonimo non si ricalcola.
Solo libreria standard di Python.
"""

import csv
import hashlib
import hmac
import os
import secrets
import sys
from collections import Counter

CAMPI_DA_ELIMINARE = ("nome", "cognome", "email")
QUASI_IDENTIFICATIVI = ("anno_nascita", "comune", "classe")


def leggi_o_crea_chiave(percorso):
    if os.path.exists(percorso):
        with open(percorso, encoding="ascii") as f:
            return bytes.fromhex(f.read().strip())
    chiave = secrets.token_bytes(32)
    with open(percorso, "w", encoding="ascii") as f:
        f.write(chiave.hex())
    return chiave


def pseudonimo(valore, chiave, lunghezza=12):
    """Pseudonimo stabile: stessa matricola e stessa chiave danno sempre lo stesso risultato."""
    return hmac.new(chiave, valore.encode("utf-8"), hashlib.sha256).hexdigest()[:lunghezza]


def trasforma(riga, chiave):
    nuova = {"pseudonimo": pseudonimo(riga["matricola"], chiave)}
    for campo, valore in riga.items():
        if campo == "matricola" or campo in CAMPI_DA_ELIMINARE:
            continue
        if campo == "data_nascita":
            nuova["anno_nascita"] = valore[:4]
        else:
            nuova[campo] = valore
    return nuova


def gruppi_piccoli(righe, k=3, campi=QUASI_IDENTIFICATIVI):
    """Combinazioni di quasi-identificativi condivise da meno di k righe: persone potenzialmente riconoscibili."""
    conteggio = Counter(tuple(r[c] for c in campi) for r in righe)
    return {combinazione: n for combinazione, n in conteggio.items() if n < k}


def main(ingresso, uscita, file_chiave, k=3):
    chiave = leggi_o_crea_chiave(file_chiave)
    with open(ingresso, encoding="utf-8-sig", newline="") as f:
        righe = [trasforma(r, chiave) for r in csv.DictReader(f)]
    with open(uscita, "w", encoding="utf-8", newline="") as f:
        scrittore = csv.DictWriter(f, fieldnames=list(righe[0]))
        scrittore.writeheader()
        scrittore.writerows(righe)
    print(f"Righe pseudonimizzate: {len(righe)}; file creato: {uscita}")
    print(f"Chiave in {file_chiave}: va conservata separatamente dal file dei dati.")
    piccoli = gruppi_piccoli(righe, k)
    if piccoli:
        print(f"\nAttenzione: {len(piccoli)} combinazioni di {', '.join(QUASI_IDENTIFICATIVI)} "
              f"riguardano meno di {k} persone:")
        for combinazione, n in sorted(piccoli.items()):
            print(f"  {combinazione}: {n}")
        print("Chi conosce queste informazioni potrebbe riconoscere le persone: valutare di generalizzare ancora.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    main(*sys.argv[1:])
