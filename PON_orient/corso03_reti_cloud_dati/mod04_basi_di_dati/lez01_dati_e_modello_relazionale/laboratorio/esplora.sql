-- Lezione 4.1: prime interrogazioni sul database biblioteca.db
-- In VS Code: comando "SQLite: Use Database" e scegliere biblioteca.db,
-- poi selezionare un'interrogazione e usare "SQLite: Run Selected Query".

-- Tutte le colonne e tutte le righe della tabella autori
SELECT * FROM autori;

-- Solo alcune colonne
SELECT titolo, anno FROM libri;

-- Le copie del libro con codice 1 (I promessi sposi)
SELECT * FROM copie WHERE id_libro = 1;

-- Da un prestito alla copia, dalla copia al libro: seguire le chiavi esterne "a mano"
SELECT * FROM prestiti WHERE id_prestito = 1;
SELECT * FROM copie WHERE id_copia = 11;
SELECT * FROM libri WHERE id_libro = 7;

-- La struttura del database, come la conserva SQLite
SELECT name, sql FROM sqlite_master WHERE type = 'table';
