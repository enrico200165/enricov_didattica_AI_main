"""Controllo di uno schema SQL e, facoltativamente, di dati di prova.

- crea lo schema in un database temporaneo in memoria, con le chiavi esterne attive
- elenca tabelle, colonne, chiavi primarie ed esterne
- segnala tabelle senza chiave primaria e chiavi esterne verso tabelle o colonne inesistenti
- esegue i dati di prova un'istruzione alla volta e indica quali violano un vincolo
- con --mermaid stampa il diagramma delle tabelle in formato Mermaid (erDiagram)

Uso:
    python controlla_schema.py schema.sql [dati.sql] [--mermaid]
"""

import sqlite3
import sys


def dividi_istruzioni(testo):
    """Divide un file SQL in istruzioni complete, usando sqlite3.complete_statement."""
    istruzioni, corrente = [], ""
    for riga in testo.splitlines(keepends=True):
        if not corrente and riga.strip().startswith("--"):
            continue                                   # commento tra un'istruzione e l'altra
        corrente += riga
        if sqlite3.complete_statement(corrente):       # True quando l'istruzione termina con ';'
            istruzioni.append(corrente.strip())
            corrente = ""
    if corrente.strip():
        istruzioni.append(corrente.strip())
    return istruzioni


def descrivi(connessione):
    """{tabella: {"colonne": [...], "pk": [...], "fk": [(colonna, tabella, colonna_riferita)]}}"""
    struttura = {}
    tabelle = [r[0] for r in connessione.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY rowid")]
    for t in tabelle:
        colonne = connessione.execute(f"PRAGMA table_info({t})").fetchall()
        # table_info: (posizione, nome, tipo, not null, predefinito, posizione nella chiave primaria)
        chiavi = connessione.execute(f"PRAGMA foreign_key_list({t})").fetchall()
        # foreign_key_list: (id, seq, tabella riferita, colonna, colonna riferita, ...)
        struttura[t] = {
            "colonne": [(c[1], c[2] or "(nessun tipo)", bool(c[3])) for c in colonne],
            "pk": [c[1] for c in sorted(colonne, key=lambda c: c[5]) if c[5] > 0],
            "fk": [(k[3], k[2], k[4]) for k in chiavi],
        }
    return struttura


def problemi_schema(struttura, connessione):
    problemi = []
    for t, info in struttura.items():
        if not info["pk"]:
            problemi.append(f"{t}: nessuna chiave primaria")
        for colonna, riferita, colonna_riferita in info["fk"]:
            if riferita not in struttura:
                problemi.append(f"{t}.{colonna}: la tabella riferita '{riferita}' non esiste")
                continue
            if colonna_riferita is None:
                colonna_riferita = struttura[riferita]["pk"][0] if struttura[riferita]["pk"] else None
            unica = colonna_riferita in struttura[riferita]["pk"] or any(
                indice[2] and [c[2] for c in connessione.execute(f"PRAGMA index_info('{indice[1]}')")] == [colonna_riferita]
                for indice in connessione.execute(f"PRAGMA index_list({riferita})"))
            if not unica:
                problemi.append(f"{t}.{colonna}: la colonna riferita {riferita}.{colonna_riferita} "
                                "non esiste o non è chiave primaria o UNIQUE")
    return problemi


def mermaid(struttura):
    righe = ["erDiagram"]
    for t, info in struttura.items():
        righe.append(f"    {t} {{")
        for nome, tipo, _ in info["colonne"]:
            segni = []
            if nome in info["pk"]:
                segni.append("PK")
            if any(nome == fk[0] for fk in info["fk"]):
                segni.append("FK")
            tipo_mermaid = tipo.split("(")[0].replace(" ", "_") if tipo != "(nessun tipo)" else "ANY"
            righe.append(f"        {tipo_mermaid} {nome} {','.join(segni)}".rstrip())
        righe.append("    }")
    for t, info in struttura.items():
        for colonna, riferita, _ in info["fk"]:
            if riferita in struttura:
                righe.append(f'    {riferita} ||--o{{ {t} : "{colonna}"')
    return "\n".join(righe)


def controlla(testo_schema, testo_dati=None):
    connessione = sqlite3.connect(":memory:")
    connessione.execute("PRAGMA foreign_keys = ON")
    connessione.executescript(testo_schema)
    struttura = descrivi(connessione)
    risultato = {"struttura": struttura, "problemi": problemi_schema(struttura, connessione),
                 "dati_validi": 0, "dati_rifiutati": []}
    if testo_dati:
        for istruzione in dividi_istruzioni(testo_dati):
            try:
                connessione.execute(istruzione)
                risultato["dati_validi"] += 1
            except sqlite3.Error as errore:
                risultato["dati_rifiutati"].append((istruzione, str(errore)))
    connessione.close()
    return risultato


def main(argomenti):
    usa_mermaid = "--mermaid" in argomenti
    file = [a for a in argomenti if a != "--mermaid"]
    if not 1 <= len(file) <= 2:
        print(__doc__)
        return
    testi = [open(f, encoding="utf-8").read() for f in file]
    try:
        r = controlla(*testi)
    except sqlite3.Error as errore:
        print("Errore nello schema:", errore)
        return
    if usa_mermaid:
        print(mermaid(r["struttura"]))
        return
    for t, info in r["struttura"].items():
        print(f"{t}  (chiave primaria: {', '.join(info['pk']) or 'nessuna'})")
        for nome, tipo, not_null in info["colonne"]:
            print(f"    {nome:<20}{tipo:<10}{'NOT NULL' if not_null else ''}")
        for colonna, riferita, colonna_riferita in info["fk"]:
            print(f"    chiave esterna: {colonna} -> {riferita}.{colonna_riferita}")
    print("\nProblemi dello schema:", "nessuno" if not r["problemi"] else "")
    for p in r["problemi"]:
        print("  -", p)
    if len(testi) == 2:
        print(f"\nDati di prova: {r['dati_validi']} istruzioni accettate, {len(r['dati_rifiutati'])} rifiutate")
        for istruzione, errore in r["dati_rifiutati"]:
            print(f"  RIFIUTATA: {istruzione}\n     motivo: {errore}")


if __name__ == "__main__":
    main(sys.argv[1:])
