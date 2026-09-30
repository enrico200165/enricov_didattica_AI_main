-- Schema della biblioteca scolastica progettata nella lezione 4.2 (una soluzione possibile)
-- Materiale per il docente. Verifica: python controlla_schema.py soluzione_schema.sql dati_prova.sql

PRAGMA foreign_keys = ON;

CREATE TABLE editori (
    id_editore   INTEGER PRIMARY KEY,
    nome         TEXT NOT NULL UNIQUE,
    citta        TEXT
);

CREATE TABLE autori (
    id_autore    INTEGER PRIMARY KEY,
    nome         TEXT NOT NULL,
    cognome      TEXT NOT NULL
);

CREATE TABLE libri (
    id_libro     INTEGER PRIMARY KEY,
    titolo       TEXT NOT NULL,
    anno         INTEGER CHECK (anno BETWEEN 1400 AND 2100),
    genere       TEXT,
    id_editore   INTEGER REFERENCES editori(id_editore)
);

-- relazione molti a molti tra libri e autori
CREATE TABLE libri_autori (
    id_libro     INTEGER NOT NULL REFERENCES libri(id_libro),
    id_autore    INTEGER NOT NULL REFERENCES autori(id_autore),
    PRIMARY KEY (id_libro, id_autore)
);

CREATE TABLE copie (
    id_copia     INTEGER PRIMARY KEY,
    id_libro     INTEGER NOT NULL REFERENCES libri(id_libro),
    collocazione TEXT NOT NULL UNIQUE,
    stato        TEXT NOT NULL DEFAULT 'buono' CHECK (stato IN ('buono', 'usurato', 'smarrita'))
);

-- studenti e docenti in un'unica tabella; la classe vale solo per gli studenti
CREATE TABLE utenti (
    id_utente    INTEGER PRIMARY KEY,
    nome         TEXT NOT NULL,
    cognome      TEXT NOT NULL,
    tipo         TEXT NOT NULL CHECK (tipo IN ('studente', 'docente')),
    classe       TEXT,
    email        TEXT UNIQUE,
    CHECK ((tipo = 'studente' AND classe IS NOT NULL) OR (tipo = 'docente' AND classe IS NULL))
);

CREATE TABLE prestiti (
    id_prestito        INTEGER PRIMARY KEY,
    id_copia           INTEGER NOT NULL REFERENCES copie(id_copia),
    id_utente          INTEGER NOT NULL REFERENCES utenti(id_utente),
    data_prestito      TEXT NOT NULL,
    data_scadenza      TEXT NOT NULL,
    data_restituzione  TEXT,
    CHECK (data_scadenza > data_prestito),
    CHECK (data_restituzione IS NULL OR data_restituzione >= data_prestito)
);

-- prenotazione di un libro (non di una copia) quando tutte le copie sono in prestito
CREATE TABLE prenotazioni (
    id_libro     INTEGER NOT NULL REFERENCES libri(id_libro),
    id_utente    INTEGER NOT NULL REFERENCES utenti(id_utente),
    data         TEXT NOT NULL,
    PRIMARY KEY (id_libro, id_utente)
);
