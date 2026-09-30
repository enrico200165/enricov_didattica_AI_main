"""Importazione di nuovi prestiti da un file CSV e rapporto sull'attività della biblioteca.

- ogni riga del CSV viene controllata (copia esistente e disponibile, studente esistente, data valida)
- l'importazione è una transazione: o entrano tutte le righe, o nessuna
- tutte le interrogazioni usano parametri (?), mai valori inseriti nel testo SQL
- il rapporto viene scritto in un file Markdown

Uso:
    python gestione_prestiti.py importa nuovi_prestiti.csv
    python gestione_prestiti.py rapporto [AAAA-MM-GG]
    python gestione_prestiti.py cerca "testo del titolo"
Il database biblioteca.db deve essere nella cartella corrente (copiarlo dalla lezione 4.1).
"""

import csv
import datetime
import sqlite3
import sys

DATABASE = "biblioteca.db"
DURATA_PRESTITO = 30  # giorni


def connetti(percorso=DATABASE):
    connessione = sqlite3.connect(percorso)
    connessione.execute("PRAGMA foreign_keys = ON")
    connessione.row_factory = sqlite3.Row      # le righe si leggono anche per nome di colonna
    return connessione


def controlla_riga(connessione, riga, gia_assegnate):
    """Restituisce (dati del prestito, None) se la riga è valida, altrimenti (None, motivo)."""
    try:
        data = datetime.date.fromisoformat(riga["data_prestito"].strip())
    except ValueError:
        return None, f"data non valida '{riga['data_prestito']}' (formato richiesto AAAA-MM-GG)"
    copia = connessione.execute(
        "SELECT id_copia, stato FROM copie WHERE collocazione = ?", (riga["collocazione"].strip(),)
    ).fetchone()
    if copia is None:
        return None, f"nessuna copia con collocazione {riga['collocazione']}"
    if copia["stato"] == "smarrita":
        return None, f"la copia {riga['collocazione']} risulta smarrita"
    in_prestito = connessione.execute(
        "SELECT COUNT(*) FROM prestiti WHERE id_copia = ? AND data_restituzione IS NULL", (copia["id_copia"],)
    ).fetchone()[0]
    if in_prestito or copia["id_copia"] in gia_assegnate:
        return None, f"la copia {riga['collocazione']} è già in prestito"
    studente = connessione.execute(
        "SELECT id_studente FROM studenti WHERE id_studente = ?", (riga["id_studente"].strip(),)
    ).fetchone()
    if studente is None:
        return None, f"nessuno studente con codice {riga['id_studente']}"
    scadenza = data + datetime.timedelta(days=DURATA_PRESTITO)
    return (copia["id_copia"], studente["id_studente"], data.isoformat(), scadenza.isoformat()), None


def importa(connessione, percorso_csv):
    """Importa i prestiti del CSV. Restituisce (numero importati, elenco degli errori)."""
    with open(percorso_csv, newline="", encoding="utf-8") as f:
        righe = list(csv.DictReader(f))
    validi, errori, assegnate = [], [], set()
    for numero, riga in enumerate(righe, start=2):          # la riga 1 è l'intestazione
        dati, motivo = controlla_riga(connessione, riga, assegnate)
        if motivo:
            errori.append(f"riga {numero}: {motivo}")
        else:
            validi.append(dati)
            assegnate.add(dati[0])                          # la stessa copia non due volte nel file
    if errori:
        return 0, errori                                    # nessuna modifica al database
    try:
        with connessione:                                   # transazione: commit alla fine, rollback se errore
            connessione.executemany(
                "INSERT INTO prestiti (id_copia, id_studente, data_prestito, data_scadenza) VALUES (?, ?, ?, ?)",
                validi)
    except sqlite3.Error as e:
        return 0, [f"errore del database, nessuna riga importata: {e}"]
    return len(validi), []


def cerca_titolo(connessione, testo):
    """Libri il cui titolo contiene il testo: il valore passa come parametro, non nel testo SQL."""
    return [r["titolo"] for r in connessione.execute(
        "SELECT titolo FROM libri WHERE titolo LIKE ? ORDER BY titolo", (f"%{testo}%",))]


def dati_rapporto(connessione, riferimento):
    r = {"riferimento": riferimento}
    r["prestiti_totali"] = connessione.execute("SELECT COUNT(*) FROM prestiti").fetchone()[0]
    r["in_corso"] = connessione.execute(
        "SELECT COUNT(*) FROM prestiti WHERE data_restituzione IS NULL").fetchone()[0]
    r["piu_prestati"] = connessione.execute("""
        SELECT l.titolo, COUNT(*) AS n FROM prestiti p
        JOIN copie c ON p.id_copia = c.id_copia JOIN libri l ON c.id_libro = l.id_libro
        GROUP BY l.id_libro ORDER BY n DESC, l.titolo LIMIT 5""").fetchall()
    r["per_classe"] = connessione.execute("""
        SELECT s.classe, COUNT(*) AS n FROM prestiti p JOIN studenti s ON p.id_studente = s.id_studente
        GROUP BY s.classe ORDER BY s.classe""").fetchall()
    r["scaduti"] = connessione.execute("""
        SELECT s.cognome, s.nome, s.classe, l.titolo, p.data_scadenza,
               CAST(julianday(?) - julianday(p.data_scadenza) AS INTEGER) AS giorni
        FROM prestiti p
        JOIN studenti s ON p.id_studente = s.id_studente
        JOIN copie c ON p.id_copia = c.id_copia JOIN libri l ON c.id_libro = l.id_libro
        WHERE p.data_restituzione IS NULL AND p.data_scadenza < ?
        ORDER BY p.data_scadenza""", (riferimento, riferimento)).fetchall()
    return r


def scrivi_rapporto(r, percorso):
    righe = [f"# Rapporto della biblioteca al {r['riferimento']}", "",
             f"Prestiti registrati: {r['prestiti_totali']}; in corso: {r['in_corso']}.", "",
             "## Libri più prestati", "", "| Titolo | Prestiti |", "|---|---|"]
    righe += [f"| {x['titolo']} | {x['n']} |" for x in r["piu_prestati"]]
    righe += ["", "## Prestiti per classe", "", "| Classe | Prestiti |", "|---|---|"]
    righe += [f"| {x['classe']} | {x['n']} |" for x in r["per_classe"]]
    righe += ["", "## Prestiti scaduti e non restituiti", ""]
    if r["scaduti"]:
        righe += ["| Studente | Classe | Titolo | Scadenza | Giorni di ritardo |", "|---|---|---|---|---|"]
        righe += [f"| {x['cognome']} {x['nome']} | {x['classe']} | {x['titolo']} | {x['data_scadenza']} | {x['giorni']} |"
                  for x in r["scaduti"]]
    else:
        righe.append("Nessuno.")
    with open(percorso, "w", encoding="utf-8") as f:
        f.write("\n".join(righe) + "\n")


def main(argomenti):
    if not argomenti:
        print(__doc__)
        return
    connessione = connetti()
    try:
        if argomenti[0] == "importa" and len(argomenti) == 2:
            importati, errori = importa(connessione, argomenti[1])
            for e in errori:
                print("ERRORE", e)
            print(f"Prestiti importati: {importati}" + ("" if not errori else " (importazione annullata)"))
        elif argomenti[0] == "rapporto":
            riferimento = argomenti[1] if len(argomenti) > 1 else datetime.date.today().isoformat()
            percorso = f"rapporto_{riferimento}.md"
            scrivi_rapporto(dati_rapporto(connessione, riferimento), percorso)
            print(f"Rapporto scritto in {percorso}")
        elif argomenti[0] == "cerca" and len(argomenti) == 2:
            for titolo in cerca_titolo(connessione, argomenti[1]):
                print(titolo)
        else:
            print(__doc__)
    finally:
        connessione.close()


if __name__ == "__main__":
    main(sys.argv[1:])
