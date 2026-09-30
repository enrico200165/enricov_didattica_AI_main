"""Funzioni del registro dei voti: versione CORRETTA (soluzione per il docente, laboratorio 5.2)."""

import html
import re
import sqlite3
import urllib.parse


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
    """Studenti con il cognome indicato: query parametrica, il valore viaggia separato dal codice SQL."""
    sql = "SELECT cognome, nome, classe FROM studenti WHERE cognome = ?"
    return conn.execute(sql, (cognome,)).fetchall()


# I nomi di colonna non possono essere parametri: si confrontano con una lista di valori ammessi
CAMPI_ORDINAMENTO = {"cognome": "cognome", "classe": "classe, cognome", "voto": "voto"}


def studenti_ordinati(conn, campo):
    """Tutti gli studenti ordinati per un campo scelto tra quelli ammessi."""
    if campo not in CAMPI_ORDINAMENTO:
        raise ValueError(f"campo di ordinamento non ammesso: {campo!r}")
    return conn.execute(
        f"SELECT cognome, nome, classe, voto FROM studenti ORDER BY {CAMPI_ORDINAMENTO[campo]}").fetchall()


FORMATO_VOTO = re.compile(r"\d{1,2}([.,]\d{1,2})?")


def valida_voto(testo):
    """Voto da 1 a 10: prima il formato (lista di caratteri ammessi), poi l'intervallo."""
    testo = testo.strip()
    if not FORMATO_VOTO.fullmatch(testo):
        raise ValueError(f"formato del voto non valido: {testo!r}")
    voto = float(testo.replace(",", "."))
    if not 1 <= voto <= 10:
        raise ValueError(f"voto fuori intervallo: {voto}")
    return voto


def riga_tabella_html(cognome, nome, commento):
    """Riga di tabella: ogni valore è codificato per il contesto HTML."""
    celle = "".join(f"<td>{html.escape(v, quote=True)}</td>" for v in (cognome, nome, commento))
    return f"<tr>{celle}</tr>"


def link_profilo(cognome, nome):
    """Collegamento con i parametri codificati per il contesto URL."""
    return "/profilo?" + urllib.parse.urlencode({"cognome": cognome, "nome": nome})
