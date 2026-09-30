-- Lezione 4.4, parte 3: modifiche dei dati e vincoli.
-- Lavorare su una COPIA del database: copy biblioteca.db prove.db, poi "SQLite: Use Database" su prove.db.
-- Eseguire un'istruzione alla volta (selezionarla, poi "SQLite: Run Selected Query")
-- e annotare il risultato. In SQLite il controllo delle chiavi esterne va attivato in ogni sessione
-- con PRAGMA foreign_keys = ON: per questo le istruzioni che lo richiedono iniziano con il PRAGMA
-- sulla stessa riga, così vengono selezionate ed eseguite insieme.

-- 1. Nuova studentessa: verificare poi con una SELECT
INSERT INTO studenti (id_studente, nome, cognome, classe) VALUES (42, 'Rita', 'Galli', '3A');

-- 2. Nuovo prestito del libro "Il cavaliere inesistente" (copia 46) alla studentessa 42
PRAGMA foreign_keys = ON; INSERT INTO prestiti (id_copia, id_studente, data_prestito, data_scadenza)
VALUES (46, 42, '2026-06-10', '2026-07-10');
-- id_prestito non è indicato: SQLite assegna il numero successivo (chiave INTEGER PRIMARY KEY)

-- 3. Restituzione del prestito appena inserito
UPDATE prestiti SET data_restituzione = '2026-06-20'
WHERE id_copia = 46 AND data_restituzione IS NULL;

-- 4. Correzione di un dato: la copia 5 è stata sostituita con una nuova
UPDATE copie SET stato = 'buono' WHERE id_copia = 5;

-- 5. Istruzioni che devono essere RIFIUTATE: quale vincolo interviene?
PRAGMA foreign_keys = ON; INSERT INTO prestiti (id_copia, id_studente, data_prestito, data_scadenza) VALUES (999, 1, '2026-06-10', '2026-07-10');
INSERT INTO copie VALUES (47, 1, 'A1-1', 'buono');
UPDATE copie SET stato = 'rotta' WHERE id_copia = 1;
PRAGMA foreign_keys = ON; DELETE FROM studenti WHERE id_studente = 21;

-- 6. Attenzione: UPDATE e DELETE senza WHERE modificano TUTTE le righe.
-- Prima di eseguirli, scrivere la SELECT con la stessa condizione e controllare le righe coinvolte:
SELECT * FROM prestiti WHERE data_restituzione IS NULL AND data_scadenza < '2026-01-01';
