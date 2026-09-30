-- Dati di prova per lo schema progettato: le prime istruzioni sono valide,
-- le ultime violano di proposito un vincolo ciascuna.
INSERT INTO editori VALUES (1, 'Editore Esempio', 'Torino');
INSERT INTO autori VALUES (1, 'Italo', 'Calvino');
INSERT INTO autori VALUES (2, 'Autrice', 'Seconda');
INSERT INTO libri VALUES (1, 'Il barone rampante', 1957, 'romanzo', 1);
INSERT INTO libri_autori VALUES (1, 1);
INSERT INTO libri_autori VALUES (1, 2);
INSERT INTO copie (id_copia, id_libro, collocazione) VALUES (1, 1, 'A1-1');
INSERT INTO utenti VALUES (1, 'Luca', 'Rossi', 'studente', '4A', NULL);
INSERT INTO utenti VALUES (2, 'Anna', 'Verdi', 'docente', NULL, 'anna.verdi@scuola.example');
INSERT INTO prestiti VALUES (1, 1, 1, '2026-03-01', '2026-03-31', NULL);
INSERT INTO prenotazioni VALUES (1, 2, '2026-03-05');
-- violazioni
INSERT INTO libri_autori VALUES (1, 1);
INSERT INTO copie VALUES (2, 99, 'A1-2', 'buono');
INSERT INTO utenti VALUES (3, 'Marco', 'Neri', 'studente', NULL, NULL);
INSERT INTO prestiti VALUES (2, 1, 2, '2026-03-10', '2026-03-01', NULL);
INSERT INTO copie VALUES (3, 1, 'A1-1', 'buono');
