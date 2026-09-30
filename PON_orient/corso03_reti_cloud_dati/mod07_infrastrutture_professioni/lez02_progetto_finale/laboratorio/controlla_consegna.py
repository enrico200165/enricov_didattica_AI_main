"""Controllo della cartella di consegna del progetto finale.

Verifica che ci siano i file richiesti e che siano utilizzabili:
- relazione.md con le sezioni previste
- presentazione.md (Marp) con almeno 6 slide
- rete.drawio e architettura.drawio: file XML validi di Draw.io
- schema.sql: crea le tabelle senza errori in un database temporaneo, tutte con chiave primaria
- piano_indirizzi.csv: reti scritte correttamente e senza sovrapposizioni
- costi e disponibilità riportati nella relazione

Uso: python controlla_consegna.py cartella_del_gruppo
"""

import csv
import ipaddress
import os
import re
import sqlite3
import sys
import xml.etree.ElementTree as ET

SEZIONI = ["Requisiti", "Rete", "Dati", "Servizio", "Cloud", "Responsabilità"]


def leggi(percorso):
    with open(percorso, encoding="utf-8") as f:
        return f.read()


def controlla_relazione(cartella):
    percorso = os.path.join(cartella, "relazione.md")
    if not os.path.exists(percorso):
        return ["manca relazione.md"]
    testo = leggi(percorso)
    titoli = [t.strip() for t in re.findall(r"^#{1,3}\s+(.+)$", testo, re.MULTILINE)]
    problemi = [f"relazione.md: manca una sezione con il titolo '{s}'"
                for s in SEZIONI if not any(t.lower().startswith(s.lower()) for t in titoli)]
    if not re.search(r"\d+([.,]\d+)?\s*(euro|EUR|€)", testo):
        problemi.append("relazione.md: non è indicato un costo in euro")
    if not re.search(r"\d+([.,]\d+)?\s*%", testo):
        problemi.append("relazione.md: non è indicata una disponibilità in percentuale")
    return problemi


def controlla_presentazione(cartella):
    percorso = os.path.join(cartella, "presentazione.md")
    if not os.path.exists(percorso):
        return ["manca presentazione.md"]
    testo = leggi(percorso)
    if "marp: true" not in testo:
        return ["presentazione.md: manca l'intestazione 'marp: true'"]
    slide = len(re.findall(r"^## ", testo, re.MULTILINE))
    return [] if slide >= 6 else [f"presentazione.md: {slide} slide, ne servono almeno 6"]


def controlla_drawio(cartella, nome):
    percorso = os.path.join(cartella, nome)
    if not os.path.exists(percorso):
        return [f"manca {nome}"]
    try:
        radice = ET.parse(percorso).getroot()
    except ET.ParseError as e:
        return [f"{nome}: non è un file XML valido ({e})"]
    return [] if radice.tag == "mxfile" else [f"{nome}: non sembra un file di Draw.io"]


def controlla_schema(cartella):
    percorso = os.path.join(cartella, "schema.sql")
    if not os.path.exists(percorso):
        return ["manca schema.sql"]
    c = sqlite3.connect(":memory:")
    try:
        c.executescript(leggi(percorso))
    except sqlite3.Error as e:
        return [f"schema.sql: errore SQL ({e})"]
    tabelle = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
    problemi = [] if len(tabelle) >= 3 else [f"schema.sql: {len(tabelle)} tabelle, ne servono almeno 3"]
    for t in tabelle:
        if not any(col[5] for col in c.execute(f"PRAGMA table_info({t})")):
            problemi.append(f"schema.sql: la tabella {t} non ha chiave primaria")
    return problemi


def controlla_piano(cartella):
    percorso = os.path.join(cartella, "piano_indirizzi.csv")
    if not os.path.exists(percorso):
        return ["manca piano_indirizzi.csv"]
    with open(percorso, newline="", encoding="utf-8") as f:
        righe = list(csv.DictReader(f))
    if not righe or "rete" not in righe[0]:
        return ["piano_indirizzi.csv: serve almeno la colonna 'rete'"]
    problemi, reti = [], []
    for r in righe:
        try:
            rete = ipaddress.ip_network(r["rete"].strip())
        except ValueError as e:
            problemi.append(f"piano_indirizzi.csv: rete non valida {r['rete']} ({e})")
            continue
        problemi += [f"piano_indirizzi.csv: {rete} si sovrappone a {x}" for x in reti if rete.overlaps(x)]
        reti.append(rete)
    return problemi


def controlla(cartella):
    return (controlla_relazione(cartella) + controlla_presentazione(cartella)
            + controlla_drawio(cartella, "rete.drawio") + controlla_drawio(cartella, "architettura.drawio")
            + controlla_schema(cartella) + controlla_piano(cartella))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
    else:
        problemi = controlla(sys.argv[1])
        for p in problemi:
            print("DA SISTEMARE:", p)
        print("Consegna completa." if not problemi else f"\nProblemi trovati: {len(problemi)}")
