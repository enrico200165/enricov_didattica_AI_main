"""Test di crea_database.py e dei dati di biblioteca.sql. Esecuzione: python test_crea_database.py"""

import os
import sqlite3
import tempfile

from crea_database import crea, riepilogo

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def rifiutata(connessione, sql):
    """True se l'istruzione viene rifiutata da un vincolo."""
    try:
        connessione.execute(sql)
    except sqlite3.IntegrityError:
        return True
    return False


percorso = os.path.join(tempfile.mkdtemp(), "prova.db")
crea(percorso)
verifica("numero di righe delle cinque tabelle",
         riepilogo(percorso) == {"autori": 15, "copie": 46, "libri": 29, "prestiti": 200, "studenti": 41})
crea(percorso)
verifica("ricreando il database i dati non si duplicano", riepilogo(percorso)["prestiti"] == 200)

c = sqlite3.connect(percorso)
c.execute("PRAGMA foreign_keys = ON")      # in SQLite le chiavi esterne vanno attivate per ogni connessione
verifica("nessuna chiave esterna senza riga corrispondente", c.execute("PRAGMA foreign_key_check").fetchall() == [])
sovrapposti = c.execute("""SELECT COUNT(*) FROM prestiti a JOIN prestiti b
    ON a.id_copia = b.id_copia AND a.id_prestito < b.id_prestito
    WHERE b.data_prestito < COALESCE(a.data_restituzione, '9999-12-31')""").fetchone()[0]
verifica("nessuna copia prestata due volte nello stesso periodo", sovrapposti == 0)
verifica("scadenza sempre 30 giorni dopo il prestito", c.execute(
    "SELECT COUNT(*) FROM prestiti WHERE julianday(data_scadenza) - julianday(data_prestito) <> 30").fetchone()[0] == 0)
verifica("restituzione mai prima del prestito", c.execute(
    "SELECT COUNT(*) FROM prestiti WHERE data_restituzione < data_prestito").fetchone()[0] == 0)
verifica("I promessi sposi: Manzoni, 1827", c.execute(
    "SELECT a.cognome, l.anno FROM libri l JOIN autori a ON a.id_autore = l.id_autore WHERE l.id_libro = 1"
).fetchone() == ("Manzoni", 1827))
verifica("chiave esterna: copia di un libro inesistente rifiutata",
         rifiutata(c, "INSERT INTO copie VALUES (100, 999, 'Z9-9', 'buono')"))
verifica("CHECK: stato non ammesso rifiutato", rifiutata(c, "INSERT INTO copie VALUES (100, 1, 'Z9-9', 'nuova')"))
verifica("UNIQUE: collocazione ripetuta rifiutata", rifiutata(c, "INSERT INTO copie VALUES (100, 1, 'A1-1', 'buono')"))
verifica("NOT NULL: studente senza classe rifiutato",
         rifiutata(c, "INSERT INTO studenti (id_studente, nome, cognome) VALUES (100, 'Ada', 'Neri')"))
verifica("chiave primaria ripetuta rifiutata", rifiutata(c, "INSERT INTO autori VALUES (1, 'X', 'Y', NULL, NULL)"))
c.close()
print(f"\nTest superati: {superati}, falliti: {falliti}")
