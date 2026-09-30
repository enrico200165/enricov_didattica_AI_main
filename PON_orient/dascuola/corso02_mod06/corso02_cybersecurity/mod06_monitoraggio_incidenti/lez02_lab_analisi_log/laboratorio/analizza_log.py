"""Analisi del registro degli eventi della bacheca (file bacheca.log).

Uso: python analizza_log.py bacheca.log [--soglia N] [--finestra MINUTI]

Riporta:
- il numero di eventi per tipo e per ora
- per ogni nome utente: accessi riusciti e falliti
- le SEGNALAZIONI: almeno N accessi falliti per lo stesso nome entro la finestra indicata
  (valori predefiniti: 5 in 10 minuti), accessi riusciti dopo più fallimenti,
  operazioni negate ed errori interni
Solo libreria standard di Python.
"""

import argparse
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta

RIGA = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d),\d+ (INFO|WARNING|ERROR) (.*)$")

TIPI = [
    ("accesso riuscito", re.compile(r"^accesso riuscito: (?P<nome>.+)$")),
    ("accesso fallito", re.compile(r"^accesso fallito per il nome '(?P<nome>.*)'$")),
    ("annuncio pubblicato", re.compile(r"^annuncio pubblicato: (?P<nome>.+)$")),
    ("annuncio eliminato", re.compile(r"^annuncio eliminato: (?P<nome>.+), annuncio \d+$")),
    ("eliminazione negata", re.compile(r"^eliminazione non consentita: (?P<nome>.+), annuncio \d+$")),
    ("richiesta non valida", re.compile(r"^richiesta non valida: (?P<dettaglio>.+)$")),
    ("errore interno", re.compile(r"^errore interno$")),
]


def leggi_eventi(righe):
    """Eventi come dizionari {istante, livello, tipo, nome}; le righe di continuazione
    (per esempio il traceback che segue un errore interno) vengono ignorate."""
    eventi = []
    for riga in righe:
        m = RIGA.match(riga.rstrip("\n"))
        if not m:
            continue
        istante = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
        messaggio = m.group(3)
        tipo, nome = "altro", None
        for nome_tipo, schema in TIPI:
            trovato = schema.match(messaggio)
            if trovato:
                tipo, nome = nome_tipo, trovato.groupdict().get("nome")
                break
        eventi.append({"istante": istante, "livello": m.group(2), "tipo": tipo, "nome": nome})
    return eventi


def fallimenti_ravvicinati(eventi, soglia=5, finestra=timedelta(minutes=10)):
    """Per ogni nome, i periodi in cui ci sono almeno 'soglia' accessi falliti entro 'finestra'.

    Restituisce una lista di (nome, inizio, fine, numero di fallimenti nel periodo)."""
    per_nome = defaultdict(list)
    for e in eventi:
        if e["tipo"] == "accesso fallito":
            per_nome[e["nome"]].append(e["istante"])
    segnalazioni = []
    for nome, istanti in per_nome.items():
        istanti.sort()
        i = 0
        while i < len(istanti):
            # finestra scorrevole: quanti fallimenti entro 'finestra' a partire da istanti[i]
            j = i
            while j + 1 < len(istanti) and istanti[j + 1] - istanti[i] <= finestra:
                j += 1
            if j - i + 1 >= soglia:
                # estende il periodo finché i fallimenti successivi restano vicini
                while j + 1 < len(istanti) and istanti[j + 1] - istanti[j] <= finestra:
                    j += 1
                segnalazioni.append((nome, istanti[i], istanti[j], j - i + 1))
                i = j + 1
            else:
                i += 1
    return sorted(segnalazioni, key=lambda s: s[1])


def riuscito_dopo_fallimenti(eventi, minimo=3):
    """Accessi riusciti preceduti da almeno 'minimo' fallimenti consecutivi per lo stesso nome."""
    consecutivi = Counter()
    risultato = []
    for e in sorted(eventi, key=lambda e: e["istante"]):
        if e["tipo"] == "accesso fallito":
            consecutivi[e["nome"]] += 1
        elif e["tipo"] == "accesso riuscito":
            if consecutivi[e["nome"]] >= minimo:
                risultato.append((e["nome"], e["istante"], consecutivi[e["nome"]]))
            consecutivi[e["nome"]] = 0
    return risultato


def riepilogo(eventi):
    per_tipo = Counter(e["tipo"] for e in eventi)
    per_ora = Counter(e["istante"].strftime("%Y-%m-%d %H:00") for e in eventi)
    per_utente = defaultdict(Counter)
    for e in eventi:
        if e["tipo"] in ("accesso riuscito", "accesso fallito"):
            per_utente[e["nome"]][e["tipo"]] += 1
    return per_tipo, per_ora, per_utente


def stampa(eventi, soglia, finestra):
    per_tipo, per_ora, per_utente = riepilogo(eventi)
    print(f"Eventi letti: {len(eventi)}")
    if eventi:
        print(f"Periodo: dal {eventi[0]['istante']:%d/%m/%Y %H:%M:%S} al {eventi[-1]['istante']:%d/%m/%Y %H:%M:%S}")
    print("\nEventi per tipo:")
    for tipo, n in per_tipo.most_common():
        print(f"  {tipo:<22} {n:5}")
    print("\nEventi per ora:")
    for ora, n in sorted(per_ora.items()):
        print(f"  {ora}  {n:5}  {'#' * min(n, 50)}")
    print("\nAccessi per nome utente (riusciti / falliti):")
    for nome, c in sorted(per_utente.items()):
        print(f"  {nome:<20} {c['accesso riuscito']:4} / {c['accesso fallito']:<4}")

    print(f"\nSEGNALAZIONI (soglia: {soglia} accessi falliti in {int(finestra.total_seconds() // 60)} minuti)")
    n = 0
    for nome, inizio, fine, quanti in fallimenti_ravvicinati(eventi, soglia, finestra):
        n += 1
        print(f"  accessi falliti ravvicinati: nome {nome!r}, {quanti} tra {inizio:%H:%M:%S} e {fine:%H:%M:%S}")
    for nome, istante, quanti in riuscito_dopo_fallimenti(eventi):
        n += 1
        print(f"  accesso riuscito dopo {quanti} fallimenti: nome {nome!r} alle {istante:%H:%M:%S}")
    for e in eventi:
        if e["tipo"] == "eliminazione negata":
            n += 1
            print(f"  eliminazione negata: utente {e['nome']!r} alle {e['istante']:%H:%M:%S}")
        elif e["tipo"] == "errore interno":
            n += 1
            print(f"  errore interno alle {e['istante']:%H:%M:%S}")
    if n == 0:
        print("  nessuna")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisi del registro degli eventi della bacheca")
    parser.add_argument("file")
    parser.add_argument("--soglia", type=int, default=5)
    parser.add_argument("--finestra", type=int, default=10, help="minuti")
    argomenti = parser.parse_args()
    with open(argomenti.file, encoding="utf-8", errors="replace") as f:
        stampa(leggi_eventi(f), argomenti.soglia, timedelta(minutes=argomenti.finestra))
