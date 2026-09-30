"""Crea il file biblioteca.db eseguendo le istruzioni SQL di biblioteca.sql.

Uso: python crea_database.py
Se biblioteca.db esiste già viene ricreato da zero, con i dati originali.
"""

import os
import sqlite3

SQL = "biblioteca.sql"
DATABASE = "biblioteca.db"


def crea(percorso_db=DATABASE, percorso_sql=SQL):
    if os.path.exists(percorso_db):
        os.remove(percorso_db)                  # si riparte sempre dai dati originali
    with open(percorso_sql, encoding="utf-8") as f:
        istruzioni = f.read()
    connessione = sqlite3.connect(percorso_db)  # crea il file se non esiste
    try:
        connessione.executescript(istruzioni)   # esegue tutte le istruzioni del file
        connessione.commit()
    finally:
        connessione.close()


def riepilogo(percorso_db=DATABASE):
    """Numero di righe di ogni tabella."""
    connessione = sqlite3.connect(percorso_db)
    try:
        tabelle = [r[0] for r in connessione.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")]
        return {t: connessione.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tabelle}
    finally:
        connessione.close()


if __name__ == "__main__":
    crea()
    for tabella, righe in riepilogo().items():
        print(f"{tabella:<10}{righe:>5} righe")
    print(f"Database creato: {os.path.abspath(DATABASE)}")
