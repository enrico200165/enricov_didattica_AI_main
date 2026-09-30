"""Ordina il backlog per priorità e disegna la matrice valore-sforzo.

Uso:
    python priorita.py valutazioni.csv
    python priorita.py valutazioni.csv --backlog docs\\backlog.md

Il file CSV ha le colonne id, titolo, moscow, valore, sforzo:
    moscow   M (Must), S (Should), C (Could), W (Won't, non in questo progetto)
    valore   da 1 a 5, stabilito dal cliente con il Product Owner
    sforzo   da 1 a 5, stima approssimativa del team

Il programma:
    1. stampa le storie in ordine: prima per MoSCoW, poi per valore/sforzo;
    2. controlla la quota di sforzo delle storie Must (DSDM consiglia al massimo il 60%);
    3. scrive matrice_valore_sforzo.md con il diagramma Mermaid;
    4. con --backlog, scrive la priorità nella tabella del backlog e la riordina.
"""

import argparse
import csv
import re
import shutil
import sys
from pathlib import Path

NOMI_MOSCOW = {"M": "Must", "S": "Should", "C": "Could", "W": "Won't"}
ORDINE_MOSCOW = "MSCW"
MASSIMO_MUST = 60     # percentuale massima di sforzo per le storie Must (DSDM)


class ErroreDati(Exception):
    """Errore nel file delle valutazioni."""


def leggi_valutazioni(percorso):
    """Legge il CSV e restituisce un elenco di dizionari con valori controllati."""
    storie, visti = [], set()
    with open(percorso, encoding="utf-8", newline="") as f:
        lettore = csv.DictReader(f)
        mancanti = {"id", "titolo", "moscow", "valore", "sforzo"} - set(lettore.fieldnames or [])
        if mancanti:
            raise ErroreDati("colonne mancanti: " + ", ".join(sorted(mancanti)))
        for numero, riga in enumerate(lettore, start=2):     # la riga 1 è l'intestazione
            codice = riga["id"].strip()
            if codice in visti:
                raise ErroreDati(f"riga {numero}: {codice} ripetuto")
            visti.add(codice)
            moscow = riga["moscow"].strip().upper()[:1]
            if moscow not in NOMI_MOSCOW:
                raise ErroreDati(f"riga {numero}: moscow deve essere M, S, C o W, non \"{riga['moscow']}\"")
            try:
                valore, sforzo = int(riga["valore"]), int(riga["sforzo"])
            except ValueError:
                raise ErroreDati(f"riga {numero}: valore e sforzo devono essere numeri interi") from None
            if not (1 <= valore <= 5 and 1 <= sforzo <= 5):
                raise ErroreDati(f"riga {numero}: valore e sforzo devono essere tra 1 e 5")
            storie.append({"id": codice, "titolo": riga["titolo"].strip(), "moscow": moscow,
                           "valore": valore, "sforzo": sforzo})
    return storie


def ordina(storie):
    """Ordina per MoSCoW, poi per rapporto valore/sforzo decrescente, poi per valore."""
    return sorted(storie, key=lambda s: (ORDINE_MOSCOW.index(s["moscow"]),
                                         -s["valore"] / s["sforzo"], -s["valore"], s["id"]))


def quote_sforzo(storie):
    """Percentuale dello sforzo totale (escluse le W) per ciascuna categoria M, S, C."""
    totale = sum(s["sforzo"] for s in storie if s["moscow"] != "W")
    if totale == 0:
        return {k: 0 for k in "MSC"}
    return {k: round(100 * sum(s["sforzo"] for s in storie if s["moscow"] == k) / totale)
            for k in "MSC"}


def coordinata(punteggio):
    """Porta un punteggio da 1 a 5 nell'intervallo 0,1-0,9 del diagramma."""
    return 0.1 + (punteggio - 1) * 0.2


def matrice_mermaid(storie):
    """Restituisce il testo del diagramma Mermaid quadrantChart."""
    righe = ['%%{init: {"quadrantChart": {"chartWidth": 700, "chartHeight": 600, "pointLabelFontSize": 13}}}%%',
             "quadrantChart",
             "    title Valore e sforzo",
             "    x-axis Sforzo basso --> Sforzo alto",
             "    y-axis Valore basso --> Valore alto",
             "    quadrant-1 Grandi progetti",
             "    quadrant-2 Vittorie rapide",
             "    quadrant-3 Riempitivi",
             "    quadrant-4 Da evitare"]
    gia_usate = {}
    for s in storie:
        chiave = (s["sforzo"], s["valore"])
        spostamento = 0.04 * gia_usate.get(chiave, 0)     # punti uguali leggermente sfalsati
        gia_usate[chiave] = gia_usate.get(chiave, 0) + 1
        x = round(coordinata(s["sforzo"]) + spostamento, 2)
        y = round(coordinata(s["valore"]) - spostamento, 2)
        righe.append(f"    {s['id']} {s['moscow']}: [{x}, {y}]")
    return "\n".join(righe)


def aggiorna_backlog(percorso, ordinate):
    """Scrive la priorità nella tabella del backlog e ne riordina le righe.

    Le righe che non compaiono nel CSV (per esempio US-00 del kit) restano in cima.
    Prima di scrivere salva una copia con estensione .bak.
    """
    testo = Path(percorso).read_text(encoding="utf-8")
    righe = testo.splitlines()
    riga_storia = re.compile(r"^\|\s*(US-\d{2})\s*\|")
    posizioni = [i for i, r in enumerate(righe) if riga_storia.match(r)]
    if not posizioni:
        raise ErroreDati("nel backlog non c'è la tabella di riepilogo con righe US-NN")
    per_codice = {riga_storia.match(righe[i]).group(1): righe[i] for i in posizioni}
    nel_csv = {s["id"]: s for s in ordinate}
    sconosciute = [c for c in nel_csv if c not in per_codice]
    if sconosciute:
        raise ErroreDati("storie del CSV assenti dal backlog: " + ", ".join(sconosciute))

    nuove = [per_codice[c] for c in per_codice if c not in nel_csv]
    for s in ordinate:
        celle = per_codice[s["id"]].split("|")
        celle[3] = f" {NOMI_MOSCOW[s['moscow']]} "      # colonna Priorità
        nuove.append("|".join(celle))
    if posizioni != list(range(posizioni[0], posizioni[-1] + 1)):
        raise ErroreDati("le righe US-NN della tabella di riepilogo devono essere consecutive")
    righe[posizioni[0]:posizioni[-1] + 1] = nuove        # sostituisce il blocco delle righe
    shutil.copy(percorso, str(percorso) + ".bak")
    Path(percorso).write_text("\n".join(righe) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Priorità del backlog e matrice valore-sforzo")
    parser.add_argument("valutazioni", help="file CSV con id, titolo, moscow, valore, sforzo")
    parser.add_argument("--backlog", help="backlog.md da aggiornare con le priorità")
    argomenti = parser.parse_args(argv)
    try:
        storie = leggi_valutazioni(argomenti.valutazioni)
        ordinate = ordina(storie)
        print(f"{'N.':>3}  {'ID':<6} {'MoSCoW':<7} {'Val':>3} {'Sfo':>3}  Titolo")
        for n, s in enumerate(ordinate, start=1):
            print(f"{n:>3}  {s['id']:<6} {NOMI_MOSCOW[s['moscow']]:<7} {s['valore']:>3} {s['sforzo']:>3}  {s['titolo']}")
        quote = quote_sforzo(storie)
        print(f"\nSforzo: Must {quote['M']}%, Should {quote['S']}%, Could {quote['C']}% (esclusi i Won't)")
        if quote["M"] > MASSIMO_MUST:
            print(f"ATTENZIONE: le storie Must superano il {MASSIMO_MUST}% dello sforzo: "
                  "se qualcosa va storto non resta margine. Rivedere le priorità con il cliente.")
        uscita = Path(argomenti.valutazioni).with_name("matrice_valore_sforzo.md")
        uscita.write_text("# Matrice valore-sforzo\n\n```mermaid\n" + matrice_mermaid(ordinate) +
                          "\n```\n", encoding="utf-8")
        print(f"Diagramma scritto in {uscita}")
        if argomenti.backlog:
            aggiorna_backlog(argomenti.backlog, ordinate)
            print(f"Backlog aggiornato: {argomenti.backlog} (copia precedente in {argomenti.backlog}.bak)")
    except (ErroreDati, OSError) as e:
        print(f"Errore: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
