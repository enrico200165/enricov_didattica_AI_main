"""Correzione automatica di esercizi SQL, senza mostrare le soluzioni.

Il file delle risposte contiene blocchi che iniziano con una riga
"-- esercizio N"; ogni blocco contiene una sola interrogazione SELECT.
Il risultato di ogni interrogazione viene confrontato con un'impronta
(hash SHA-256) del risultato atteso, conservata in un file JSON.

Uso:
    python correttore.py risposte.sql attesi_4_3.json biblioteca.db
Per il docente, per generare il file delle impronte dalle soluzioni:
    python correttore.py --genera soluzioni_esercizi_4_3.sql attesi_4_3.json biblioteca.db
"""

import hashlib
import json
import pathlib
import re
import sqlite3
import sys

MODELLO_BLOCCO = re.compile(r"^--\s*esercizio\s+(\d+)(.*)$", re.IGNORECASE | re.MULTILINE)


def dividi_esercizi(testo):
    """{numero: (interrogazione, ordinato)}; 'ordinato' se l'intestazione contiene '(ordinato)'."""
    esercizi = {}
    intestazioni = list(MODELLO_BLOCCO.finditer(testo))
    for i, m in enumerate(intestazioni):
        fine = intestazioni[i + 1].start() if i + 1 < len(intestazioni) else len(testo)
        corpo = testo[m.end():fine]
        righe = [r for r in corpo.splitlines() if not r.strip().startswith("--")]   # toglie i commenti
        sql = "\n".join(righe).strip()
        esercizi[int(m.group(1))] = (sql, "ordinato" in m.group(2).lower())
    return esercizi


def impronta(righe, ordinato):
    """Hash del risultato: i valori sono resi come testo; se l'ordine non conta, le righe si ordinano."""
    testo = [json.dumps([None if v is None else (round(v, 6) if isinstance(v, float) else v) for v in r],
                        ensure_ascii=False) for r in righe]
    if not ordinato:
        testo.sort()
    return hashlib.sha256("\n".join(testo).encode("utf-8")).hexdigest()


def esegui(connessione, sql):
    if not sql:
        raise ValueError("nessuna interrogazione")
    if not sql.lstrip().upper().startswith(("SELECT", "WITH")):
        raise ValueError("sono ammesse solo interrogazioni SELECT")
    cursore = connessione.execute(sql.rstrip().rstrip(";"))
    return cursore.fetchall(), len(cursore.description)


def genera(percorso_soluzioni, percorso_json, percorso_db):
    with open(percorso_soluzioni, encoding="utf-8") as f:
        esercizi = dividi_esercizi(f.read())
    connessione = sqlite3.connect(percorso_db)
    attesi = {}
    for numero, (sql, ordinato) in sorted(esercizi.items()):
        righe, colonne = esegui(connessione, sql)
        attesi[str(numero)] = {"ordinato": ordinato, "righe": len(righe), "colonne": colonne,
                               "impronta": impronta(righe, ordinato),
                               # per riconoscere le risposte con le righe giuste ma in ordine diverso
                               "impronta_senza_ordine": impronta(righe, False)}
    connessione.close()
    with open(percorso_json, "w", encoding="utf-8") as f:
        json.dump(attesi, f, indent=1)
    return attesi


def correggi(percorso_risposte, percorso_json, percorso_db):
    """Restituisce {numero: esito} con esito 'corretto', 'mancante' o una descrizione dell'errore."""
    with open(percorso_json, encoding="utf-8") as f:
        attesi = json.load(f)
    with open(percorso_risposte, encoding="utf-8") as f:
        risposte = dividi_esercizi(f.read())
    # apertura in sola lettura: le risposte non possono modificare il database
    # as_uri() produce un indirizzo "file:///..." valido anche con i percorsi di Windows
    uri = pathlib.Path(percorso_db).resolve().as_uri() + "?mode=ro"
    connessione = sqlite3.connect(uri, uri=True)
    esiti = {}
    for chiave, atteso in attesi.items():
        numero = int(chiave)
        if numero not in risposte or not risposte[numero][0]:
            esiti[numero] = "mancante"
            continue
        try:
            righe, colonne = esegui(connessione, risposte[numero][0])
        except (sqlite3.Error, ValueError) as errore:
            esiti[numero] = f"errore SQL: {errore}"
            continue
        if impronta(righe, atteso["ordinato"]) == atteso["impronta"]:
            esiti[numero] = "corretto"
        elif colonne != atteso["colonne"]:
            esiti[numero] = f"colonne: {colonne} invece di {atteso['colonne']}"
        elif len(righe) != atteso["righe"]:
            esiti[numero] = f"righe: {len(righe)} invece di {atteso['righe']}"
        elif atteso["ordinato"] and impronta(righe, False) == atteso["impronta_senza_ordine"]:
            esiti[numero] = "righe giuste, ordine sbagliato"
        else:
            esiti[numero] = "valori diversi da quelli attesi"
    connessione.close()
    return esiti


def main(argomenti):
    if len(argomenti) == 4 and argomenti[0] == "--genera":
        attesi = genera(*argomenti[1:])
        print(f"Impronte generate per {len(attesi)} esercizi")
        return
    if len(argomenti) != 3:
        print(__doc__)
        return
    esiti = correggi(*argomenti)
    for numero, esito in sorted(esiti.items()):
        print(f"esercizio {numero:>2}: {esito}")
    corretti = sum(e == "corretto" for e in esiti.values())
    print(f"\nCorretti: {corretti} su {len(esiti)}")


if __name__ == "__main__":
    main(sys.argv[1:])
