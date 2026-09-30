"""Funzioni di un piccolo registro dei voti: versione DA CORREGGERE (laboratorio 5.2).

Ogni funzione contiene un errore nel trattamento dei dati in ingresso o in uscita.
I test in test_registro.py descrivono il comportamento corretto.
Solo libreria standard di Python.
"""

import sqlite3


def crea_database():
    """Database in memoria con alcuni studenti di prova."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE studenti (id INTEGER PRIMARY KEY, cognome TEXT, nome TEXT, classe TEXT, voto REAL)")
    conn.executemany("INSERT INTO studenti (cognome, nome, classe, voto) VALUES (?, ?, ?, ?)", [
        ("Rossi", "Marco", "4A", 7.5),
        ("D'Amico", "Giulia", "4A", 8.0),
        ("Esposito", "Luca", "4B", 6.0),
        ("Dell'Orto", "Sara", "4B", 9.0),
    ])
    return conn


def cerca_studenti(conn, cognome):
    """Studenti con il cognome indicato."""
    sql = f"SELECT cognome, nome, classe FROM studenti WHERE cognome = '{cognome}'"
    return conn.execute(sql).fetchall()


def studenti_ordinati(conn, campo):
    """Tutti gli studenti ordinati per il campo indicato dall'utente (cognome, classe o voto)."""
    return conn.execute(f"SELECT cognome, nome, classe, voto FROM studenti ORDER BY {campo}").fetchall()


def valida_voto(testo):
    """Voto inserito in un modulo: numero da 1 a 10, anche con la virgola decimale."""
    return float(testo.replace(",", "."))


def riga_tabella_html(cognome, nome, commento):
    """Riga di una tabella HTML con i dati di uno studente e il commento del docente."""
    return f"<tr><td>{cognome}</td><td>{nome}</td><td>{commento}</td></tr>"


def link_profilo(cognome, nome):
    """Collegamento alla pagina del profilo di uno studente."""
    return f"/profilo?cognome={cognome}&nome={nome}"
