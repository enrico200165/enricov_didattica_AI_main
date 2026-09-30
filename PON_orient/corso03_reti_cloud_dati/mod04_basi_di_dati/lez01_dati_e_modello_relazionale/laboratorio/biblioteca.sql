-- Database didattico: biblioteca scolastica
-- Dati inventati (studenti, prestiti, collocazioni); titoli, autori e anni di prima pubblicazione reali.
-- Creazione: python crea_database.py  (oppure: sqlite3 biblioteca.db < biblioteca.sql)

PRAGMA foreign_keys = ON;

CREATE TABLE autori (
    id_autore     INTEGER PRIMARY KEY,
    nome          TEXT NOT NULL,
    cognome       TEXT NOT NULL,
    nazionalita   TEXT,
    anno_nascita  INTEGER
);

CREATE TABLE libri (
    id_libro      INTEGER PRIMARY KEY,
    titolo        TEXT NOT NULL,
    id_autore     INTEGER NOT NULL REFERENCES autori(id_autore),
    genere        TEXT,
    anno          INTEGER          -- anno di prima pubblicazione
);

CREATE TABLE copie (
    id_copia      INTEGER PRIMARY KEY,
    id_libro      INTEGER NOT NULL REFERENCES libri(id_libro),
    collocazione  TEXT NOT NULL UNIQUE,   -- scaffale e posizione, per esempio A1-2
    stato         TEXT NOT NULL CHECK (stato IN ('buono', 'usurato', 'smarrita'))
);

CREATE TABLE studenti (
    id_studente   INTEGER PRIMARY KEY,
    nome          TEXT NOT NULL,
    cognome       TEXT NOT NULL,
    classe        TEXT NOT NULL
);

CREATE TABLE prestiti (
    id_prestito        INTEGER PRIMARY KEY,
    id_copia           INTEGER NOT NULL REFERENCES copie(id_copia),
    id_studente        INTEGER NOT NULL REFERENCES studenti(id_studente),
    data_prestito      TEXT NOT NULL,     -- date nel formato AAAA-MM-GG
    data_scadenza      TEXT NOT NULL,
    data_restituzione  TEXT               -- NULL se il libro non è ancora stato restituito
);


-- autori: 14 righe
INSERT INTO autori VALUES (1, 'Alessandro', 'Manzoni', 'italiana', 1785);
INSERT INTO autori VALUES (2, 'Italo', 'Calvino', 'italiana', 1923);
INSERT INTO autori VALUES (3, 'Primo', 'Levi', 'italiana', 1919);
INSERT INTO autori VALUES (4, 'Elsa', 'Morante', 'italiana', 1912);
INSERT INTO autori VALUES (5, 'Natalia', 'Ginzburg', 'italiana', 1916);
INSERT INTO autori VALUES (6, 'Cesare', 'Pavese', 'italiana', 1908);
INSERT INTO autori VALUES (7, 'Giovanni', 'Verga', 'italiana', 1840);
INSERT INTO autori VALUES (8, 'Luigi', 'Pirandello', 'italiana', 1867);
INSERT INTO autori VALUES (9, 'George', 'Orwell', 'britannica', 1903);
INSERT INTO autori VALUES (10, 'Mary', 'Shelley', 'britannica', 1797);
INSERT INTO autori VALUES (11, 'Jules', 'Verne', 'francese', 1828);
INSERT INTO autori VALUES (12, 'Isaac', 'Asimov', 'statunitense', 1920);
INSERT INTO autori VALUES (13, 'Umberto', 'Eco', 'italiana', 1932);
INSERT INTO autori VALUES (14, 'Italo', 'Svevo', 'italiana', 1861);

-- libri: 28 righe
INSERT INTO libri VALUES (1, 'I promessi sposi', 1, 'romanzo storico', 1827);
INSERT INTO libri VALUES (2, 'Il barone rampante', 2, 'romanzo', 1957);
INSERT INTO libri VALUES (3, 'Il visconte dimezzato', 2, 'romanzo', 1952);
INSERT INTO libri VALUES (4, 'Le città invisibili', 2, 'romanzo', 1972);
INSERT INTO libri VALUES (5, 'Il sentiero dei nidi di ragno', 2, 'romanzo', 1947);
INSERT INTO libri VALUES (6, 'Marcovaldo', 2, 'racconti', 1963);
INSERT INTO libri VALUES (7, 'Se questo è un uomo', 3, 'memorie', 1947);
INSERT INTO libri VALUES (8, 'La tregua', 3, 'memorie', 1963);
INSERT INTO libri VALUES (9, 'Il sistema periodico', 3, 'racconti', 1975);
INSERT INTO libri VALUES (10, 'L''isola di Arturo', 4, 'romanzo', 1957);
INSERT INTO libri VALUES (11, 'La Storia', 4, 'romanzo storico', 1974);
INSERT INTO libri VALUES (12, 'Lessico famigliare', 5, 'romanzo', 1963);
INSERT INTO libri VALUES (13, 'La luna e i falò', 6, 'romanzo', 1950);
INSERT INTO libri VALUES (14, 'La casa in collina', 6, 'romanzo', 1948);
INSERT INTO libri VALUES (15, 'I Malavoglia', 7, 'romanzo', 1881);
INSERT INTO libri VALUES (16, 'Mastro-don Gesualdo', 7, 'romanzo', 1889);
INSERT INTO libri VALUES (17, 'Il fu Mattia Pascal', 8, 'romanzo', 1904);
INSERT INTO libri VALUES (18, 'Uno, nessuno e centomila', 8, 'romanzo', 1926);
INSERT INTO libri VALUES (19, '1984', 9, 'fantascienza', 1949);
INSERT INTO libri VALUES (20, 'La fattoria degli animali', 9, 'romanzo', 1945);
INSERT INTO libri VALUES (21, 'Frankenstein', 10, 'fantascienza', 1818);
INSERT INTO libri VALUES (22, 'Ventimila leghe sotto i mari', 11, 'avventura', 1870);
INSERT INTO libri VALUES (23, 'Il giro del mondo in ottanta giorni', 11, 'avventura', 1872);
INSERT INTO libri VALUES (24, 'Io, robot', 12, 'fantascienza', 1950);
INSERT INTO libri VALUES (25, 'Fondazione', 12, 'fantascienza', 1951);
INSERT INTO libri VALUES (26, 'Il nome della rosa', 13, 'romanzo storico', 1980);
INSERT INTO libri VALUES (27, 'La coscienza di Zeno', 14, 'romanzo', 1923);
INSERT INTO libri VALUES (28, 'Novelle per un anno', 8, 'racconti', 1922);

-- copie: 45 righe
INSERT INTO copie VALUES (1, 1, 'A1-1', 'usurato');
INSERT INTO copie VALUES (2, 1, 'A1-2', 'buono');
INSERT INTO copie VALUES (3, 1, 'A1-3', 'buono');
INSERT INTO copie VALUES (4, 2, 'A2-1', 'buono');
INSERT INTO copie VALUES (5, 3, 'A3-1', 'usurato');
INSERT INTO copie VALUES (6, 3, 'A3-2', 'buono');
INSERT INTO copie VALUES (7, 4, 'A4-1', 'buono');
INSERT INTO copie VALUES (8, 5, 'A5-1', 'buono');
INSERT INTO copie VALUES (9, 6, 'B1-1', 'buono');
INSERT INTO copie VALUES (10, 6, 'B1-2', 'buono');
INSERT INTO copie VALUES (11, 7, 'B2-1', 'buono');
INSERT INTO copie VALUES (12, 7, 'B2-2', 'buono');
INSERT INTO copie VALUES (13, 7, 'B2-3', 'buono');
INSERT INTO copie VALUES (14, 8, 'B3-1', 'buono');
INSERT INTO copie VALUES (15, 9, 'B4-1', 'buono');
INSERT INTO copie VALUES (16, 9, 'B4-2', 'buono');
INSERT INTO copie VALUES (17, 10, 'B5-1', 'usurato');
INSERT INTO copie VALUES (18, 11, 'C1-1', 'buono');
INSERT INTO copie VALUES (19, 12, 'C2-1', 'buono');
INSERT INTO copie VALUES (20, 12, 'C2-2', 'buono');
INSERT INTO copie VALUES (21, 13, 'C3-1', 'buono');
INSERT INTO copie VALUES (22, 14, 'C4-1', 'buono');
INSERT INTO copie VALUES (23, 15, 'C5-1', 'buono');
INSERT INTO copie VALUES (24, 15, 'C5-2', 'buono');
INSERT INTO copie VALUES (25, 16, 'D1-1', 'buono');
INSERT INTO copie VALUES (26, 17, 'D2-1', 'buono');
INSERT INTO copie VALUES (27, 18, 'D3-1', 'buono');
INSERT INTO copie VALUES (28, 18, 'D3-2', 'buono');
INSERT INTO copie VALUES (29, 19, 'D4-1', 'buono');
INSERT INTO copie VALUES (30, 19, 'D4-2', 'usurato');
INSERT INTO copie VALUES (31, 19, 'D4-3', 'buono');
INSERT INTO copie VALUES (32, 20, 'D5-1', 'buono');
INSERT INTO copie VALUES (33, 21, 'E1-1', 'buono');
INSERT INTO copie VALUES (34, 21, 'E1-2', 'buono');
INSERT INTO copie VALUES (35, 22, 'E2-1', 'buono');
INSERT INTO copie VALUES (36, 23, 'E3-1', 'buono');
INSERT INTO copie VALUES (37, 24, 'E4-1', 'buono');
INSERT INTO copie VALUES (38, 24, 'E4-2', 'usurato');
INSERT INTO copie VALUES (39, 25, 'E5-1', 'buono');
INSERT INTO copie VALUES (40, 26, 'F1-1', 'buono');
INSERT INTO copie VALUES (41, 26, 'F1-2', 'buono');
INSERT INTO copie VALUES (42, 26, 'F1-3', 'buono');
INSERT INTO copie VALUES (43, 27, 'F2-1', 'buono');
INSERT INTO copie VALUES (44, 27, 'F2-2', 'buono');
INSERT INTO copie VALUES (45, 28, 'F3-1', 'smarrita');

-- studenti: 40 righe
INSERT INTO studenti VALUES (1, 'Luca', 'Rossi', '3A');
INSERT INTO studenti VALUES (2, 'Giulia', 'Marino', '3B');
INSERT INTO studenti VALUES (3, 'Marco', 'Costa', '4A');
INSERT INTO studenti VALUES (4, 'Sara', 'Santoro', '4B');
INSERT INTO studenti VALUES (5, 'Andrea', 'Leone', '5A');
INSERT INTO studenti VALUES (6, 'Chiara', 'Coppola', '3A');
INSERT INTO studenti VALUES (7, 'Matteo', 'Ferrari', '3B');
INSERT INTO studenti VALUES (8, 'Francesca', 'Bruno', '4A');
INSERT INTO studenti VALUES (9, 'Davide', 'Rizzo', '4B');
INSERT INTO studenti VALUES (10, 'Elena', 'Rinaldi', '5A');
INSERT INTO studenti VALUES (11, 'Simone', 'Gentile', '3A');
INSERT INTO studenti VALUES (12, 'Martina', 'D''Angelo', '3B');
INSERT INTO studenti VALUES (13, 'Alessio', 'Romano', '4A');
INSERT INTO studenti VALUES (14, 'Valentina', 'Conti', '4B');
INSERT INTO studenti VALUES (15, 'Federico', 'Moretti', '5A');
INSERT INTO studenti VALUES (16, 'Alice', 'Ferrara', '3A');
INSERT INTO studenti VALUES (17, 'Lorenzo', 'Vitale', '3B');
INSERT INTO studenti VALUES (18, 'Beatrice', 'Parisi', '4A');
INSERT INTO studenti VALUES (19, 'Tommaso', 'Ricci', '4B');
INSERT INTO studenti VALUES (20, 'Aurora', 'Mancini', '5A');
INSERT INTO studenti VALUES (21, 'Riccardo', 'Fontana', '3A');
INSERT INTO studenti VALUES (22, 'Sofia', 'Martini', '3B');
INSERT INTO studenti VALUES (23, 'Gabriele', 'Serra', '4A');
INSERT INTO studenti VALUES (24, 'Anna', 'Bianchi', '4B');
INSERT INTO studenti VALUES (25, 'Pietro', 'Greco', '5A');
INSERT INTO studenti VALUES (26, 'Noemi', 'Giordano', '3A');
INSERT INTO studenti VALUES (27, 'Edoardo', 'Mariani', '3B');
INSERT INTO studenti VALUES (28, 'Irene', 'Longo', '4A');
INSERT INTO studenti VALUES (29, 'Filippo', 'De Santis', '4B');
INSERT INTO studenti VALUES (30, 'Greta', 'Esposito', '5A');
INSERT INTO studenti VALUES (31, 'Nicola', 'Gallo', '3A');
INSERT INTO studenti VALUES (32, 'Camilla', 'Lombardi', '3B');
INSERT INTO studenti VALUES (33, 'Stefano', 'Caruso', '4A');
INSERT INTO studenti VALUES (34, 'Ludovica', 'Martinelli', '4B');
INSERT INTO studenti VALUES (35, 'Samuele', 'Marchetti', '5A');
INSERT INTO studenti VALUES (36, 'Elisa', 'Colombo', '3A');
INSERT INTO studenti VALUES (37, 'Daniele', 'De Luca', '3B');
INSERT INTO studenti VALUES (38, 'Bianca', 'Barbieri', '4A');
INSERT INTO studenti VALUES (39, 'Jacopo', 'Galli', '4B');
INSERT INTO studenti VALUES (40, 'Marta', 'Lombardo', '5A');

-- prestiti: 200 righe
INSERT INTO prestiti VALUES (1, 11, 21, '2025-09-17', '2025-10-17', '2025-11-01');
INSERT INTO prestiti VALUES (2, 30, 40, '2025-09-20', '2025-10-20', '2025-10-07');
INSERT INTO prestiti VALUES (3, 38, 5, '2025-09-20', '2025-10-20', '2025-10-05');
INSERT INTO prestiti VALUES (4, 27, 37, '2025-09-24', '2025-10-24', '2025-10-04');
INSERT INTO prestiti VALUES (5, 19, 33, '2025-09-25', '2025-10-25', '2025-11-06');
INSERT INTO prestiti VALUES (6, 8, 32, '2025-09-26', '2025-10-26', '2025-10-29');
INSERT INTO prestiti VALUES (7, 12, 8, '2025-09-27', '2025-10-27', '2025-10-14');
INSERT INTO prestiti VALUES (8, 2, 8, '2025-09-29', '2025-10-29', '2025-11-04');
INSERT INTO prestiti VALUES (9, 41, 21, '2025-09-29', '2025-10-29', '2025-10-16');
INSERT INTO prestiti VALUES (10, 43, 34, '2025-09-29', '2025-10-29', '2025-11-02');
INSERT INTO prestiti VALUES (11, 33, 21, '2025-09-30', '2025-10-30', '2025-11-02');
INSERT INTO prestiti VALUES (12, 6, 23, '2025-10-03', '2025-11-02', '2025-11-01');
INSERT INTO prestiti VALUES (13, 40, 17, '2025-10-04', '2025-11-03', '2025-10-12');
INSERT INTO prestiti VALUES (14, 31, 6, '2025-10-05', '2025-11-04', '2025-11-10');
INSERT INTO prestiti VALUES (15, 27, 20, '2025-10-06', '2025-11-05', '2025-10-24');
INSERT INTO prestiti VALUES (16, 26, 16, '2025-10-07', '2025-11-06', '2025-10-27');
INSERT INTO prestiti VALUES (17, 4, 27, '2025-10-08', '2025-11-07', '2025-10-24');
INSERT INTO prestiti VALUES (18, 16, 25, '2025-10-08', '2025-11-07', '2025-11-05');
INSERT INTO prestiti VALUES (19, 32, 35, '2025-10-10', '2025-11-09', '2025-11-02');
INSERT INTO prestiti VALUES (20, 30, 28, '2025-10-11', '2025-11-10', '2025-10-30');
INSERT INTO prestiti VALUES (21, 29, 11, '2025-10-12', '2025-11-11', '2025-11-03');
INSERT INTO prestiti VALUES (22, 42, 9, '2025-10-12', '2025-11-11', '2025-11-16');
INSERT INTO prestiti VALUES (23, 20, 35, '2025-10-13', '2025-11-12', '2025-11-06');
INSERT INTO prestiti VALUES (24, 13, 21, '2025-10-15', '2025-11-14', '2025-10-30');
INSERT INTO prestiti VALUES (25, 3, 13, '2025-10-16', '2025-11-15', '2025-11-08');
INSERT INTO prestiti VALUES (26, 1, 39, '2025-10-17', '2025-11-16', '2025-11-24');
INSERT INTO prestiti VALUES (27, 37, 4, '2025-10-19', '2025-11-18', '2025-11-29');
INSERT INTO prestiti VALUES (28, 41, 9, '2025-10-20', '2025-11-19', '2025-12-04');
INSERT INTO prestiti VALUES (29, 18, 17, '2025-10-24', '2025-11-23', '2025-11-19');
INSERT INTO prestiti VALUES (30, 40, 10, '2025-10-27', '2025-11-26', '2025-11-27');
INSERT INTO prestiti VALUES (31, 27, 35, '2025-10-29', '2025-11-28', '2025-11-27');
INSERT INTO prestiti VALUES (32, 6, 31, '2025-11-02', '2025-12-02', '2025-11-29');
INSERT INTO prestiti VALUES (33, 25, 33, '2025-11-02', '2025-12-02', '2025-12-12');
INSERT INTO prestiti VALUES (34, 12, 3, '2025-11-03', '2025-12-03', '2025-11-18');
INSERT INTO prestiti VALUES (35, 45, 12, '2025-11-03', '2025-12-03', NULL);
INSERT INTO prestiti VALUES (36, 33, 39, '2025-11-04', '2025-12-04', '2025-11-22');
INSERT INTO prestiti VALUES (37, 28, 21, '2025-11-06', '2025-12-06', '2025-11-22');
INSERT INTO prestiti VALUES (38, 10, 21, '2025-11-08', '2025-12-08', '2025-11-25');
INSERT INTO prestiti VALUES (39, 11, 28, '2025-11-08', '2025-12-08', '2025-11-22');
INSERT INTO prestiti VALUES (40, 22, 3, '2025-11-09', '2025-12-09', '2025-11-30');
INSERT INTO prestiti VALUES (41, 15, 20, '2025-11-10', '2025-12-10', '2025-12-10');
INSERT INTO prestiti VALUES (42, 29, 32, '2025-11-11', '2025-12-11', '2025-12-01');
INSERT INTO prestiti VALUES (43, 30, 10, '2025-11-13', '2025-12-13', '2025-12-07');
INSERT INTO prestiti VALUES (44, 20, 10, '2025-11-14', '2025-12-14', '2025-12-26');
INSERT INTO prestiti VALUES (45, 24, 24, '2025-11-15', '2025-12-15', '2025-12-08');
INSERT INTO prestiti VALUES (46, 19, 32, '2025-11-17', '2025-12-17', '2025-12-19');
INSERT INTO prestiti VALUES (47, 13, 12, '2025-11-18', '2025-12-18', '2025-12-30');
INSERT INTO prestiti VALUES (48, 34, 34, '2025-11-18', '2025-12-18', '2025-12-05');
INSERT INTO prestiti VALUES (49, 2, 35, '2025-11-20', '2025-12-20', '2025-12-13');
INSERT INTO prestiti VALUES (50, 4, 38, '2025-11-20', '2025-12-20', '2025-12-31');
INSERT INTO prestiti VALUES (51, 7, 35, '2025-11-20', '2025-12-20', '2025-11-30');
INSERT INTO prestiti VALUES (52, 35, 3, '2025-11-21', '2025-12-21', '2025-12-11');
INSERT INTO prestiti VALUES (53, 16, 3, '2025-11-23', '2025-12-23', '2026-01-06');
INSERT INTO prestiti VALUES (54, 18, 32, '2025-11-23', '2025-12-23', '2025-12-07');
INSERT INTO prestiti VALUES (55, 3, 32, '2025-11-24', '2025-12-24', '2025-12-28');
INSERT INTO prestiti VALUES (56, 5, 15, '2025-11-25', '2025-12-25', '2026-01-01');
INSERT INTO prestiti VALUES (57, 31, 34, '2025-11-25', '2025-12-25', '2026-01-04');
INSERT INTO prestiti VALUES (58, 38, 31, '2025-11-27', '2025-12-27', '2025-12-13');
INSERT INTO prestiti VALUES (59, 9, 40, '2025-11-28', '2025-12-28', '2025-12-22');
INSERT INTO prestiti VALUES (60, 40, 8, '2025-11-28', '2025-12-28', '2025-12-11');
INSERT INTO prestiti VALUES (61, 42, 4, '2025-11-29', '2025-12-29', '2025-12-25');
INSERT INTO prestiti VALUES (62, 44, 33, '2025-11-29', '2025-12-29', '2025-12-18');
INSERT INTO prestiti VALUES (63, 10, 1, '2025-12-04', '2026-01-03', '2026-01-06');
INSERT INTO prestiti VALUES (64, 11, 17, '2025-12-04', '2026-01-03', '2026-01-04');
INSERT INTO prestiti VALUES (65, 12, 20, '2025-12-05', '2026-01-04', '2025-12-13');
INSERT INTO prestiti VALUES (66, 36, 6, '2025-12-05', '2026-01-04', '2025-12-22');
INSERT INTO prestiti VALUES (67, 26, 14, '2025-12-06', '2026-01-05', '2025-12-30');
INSERT INTO prestiti VALUES (68, 1, 17, '2025-12-07', '2026-01-06', '2026-01-09');
INSERT INTO prestiti VALUES (69, 33, 8, '2025-12-07', '2026-01-06', '2026-01-20');
INSERT INTO prestiti VALUES (70, 39, 35, '2025-12-08', '2026-01-07', '2025-12-15');
INSERT INTO prestiti VALUES (71, 28, 1, '2025-12-09', '2026-01-08', '2025-12-19');
INSERT INTO prestiti VALUES (72, 37, 26, '2025-12-11', '2026-01-10', '2026-01-16');
INSERT INTO prestiti VALUES (73, 29, 28, '2025-12-13', '2026-01-12', '2026-01-16');
INSERT INTO prestiti VALUES (74, 41, 26, '2025-12-15', '2026-01-14', '2026-01-04');
INSERT INTO prestiti VALUES (75, 39, 12, '2025-12-16', '2026-01-15', '2026-01-21');
INSERT INTO prestiti VALUES (76, 30, 26, '2025-12-17', '2026-01-16', '2025-12-24');
INSERT INTO prestiti VALUES (77, 40, 29, '2025-12-19', '2026-01-18', '2025-12-30');
INSERT INTO prestiti VALUES (78, 8, 34, '2025-12-22', '2026-01-21', '2026-01-15');
INSERT INTO prestiti VALUES (79, 34, 24, '2025-12-22', '2026-01-21', '2026-01-11');
INSERT INTO prestiti VALUES (80, 24, 18, '2025-12-23', '2026-01-22', '2026-01-31');
INSERT INTO prestiti VALUES (81, 38, 36, '2025-12-24', '2026-01-23', '2026-01-07');
INSERT INTO prestiti VALUES (82, 36, 1, '2025-12-25', '2026-01-24', '2026-01-19');
INSERT INTO prestiti VALUES (83, 12, 23, '2025-12-27', '2026-01-26', '2026-01-29');
INSERT INTO prestiti VALUES (84, 42, 33, '2025-12-27', '2026-01-26', '2026-01-24');
INSERT INTO prestiti VALUES (85, 35, 29, '2025-12-29', '2026-01-28', '2026-02-09');
INSERT INTO prestiti VALUES (86, 19, 30, '2025-12-30', '2026-01-29', '2026-01-20');
INSERT INTO prestiti VALUES (87, 20, 37, '2025-12-30', '2026-01-29', '2026-02-04');
INSERT INTO prestiti VALUES (88, 44, 6, '2025-12-30', '2026-01-29', '2026-01-12');
INSERT INTO prestiti VALUES (89, 2, 20, '2025-12-31', '2026-01-30', '2026-02-11');
INSERT INTO prestiti VALUES (90, 13, 33, '2026-01-01', '2026-01-31', '2026-01-24');
INSERT INTO prestiti VALUES (91, 25, 21, '2026-01-01', '2026-01-31', '2026-01-29');
INSERT INTO prestiti VALUES (92, 4, 13, '2026-01-03', '2026-02-02', '2026-01-25');
INSERT INTO prestiti VALUES (93, 23, 27, '2026-01-06', '2026-02-05', '2026-01-15');
INSERT INTO prestiti VALUES (94, 31, 19, '2026-01-08', '2026-02-07', '2026-01-17');
INSERT INTO prestiti VALUES (95, 30, 18, '2026-01-09', '2026-02-08', '2026-02-07');
INSERT INTO prestiti VALUES (96, 38, 25, '2026-01-12', '2026-02-11', '2026-01-24');
INSERT INTO prestiti VALUES (97, 40, 29, '2026-01-12', '2026-02-11', '2026-02-16');
INSERT INTO prestiti VALUES (98, 16, 19, '2026-01-13', '2026-02-12', '2026-02-07');
INSERT INTO prestiti VALUES (99, 22, 2, '2026-01-13', '2026-02-12', '2026-02-02');
INSERT INTO prestiti VALUES (100, 7, 2, '2026-01-14', '2026-02-13', '2026-01-29');
INSERT INTO prestiti VALUES (101, 11, 23, '2026-01-14', '2026-02-13', '2026-01-24');
INSERT INTO prestiti VALUES (102, 3, 3, '2026-01-15', '2026-02-14', '2026-02-09');
INSERT INTO prestiti VALUES (103, 26, 21, '2026-01-15', '2026-02-14', '2026-02-14');
INSERT INTO prestiti VALUES (104, 17, 35, '2026-01-16', '2026-02-15', '2026-02-01');
INSERT INTO prestiti VALUES (105, 44, 8, '2026-01-16', '2026-02-15', '2026-02-21');
INSERT INTO prestiti VALUES (106, 6, 30, '2026-01-17', '2026-02-16', '2026-03-01');
INSERT INTO prestiti VALUES (107, 37, 1, '2026-01-19', '2026-02-18', '2026-02-21');
INSERT INTO prestiti VALUES (108, 5, 39, '2026-01-20', '2026-02-19', '2026-02-28');
INSERT INTO prestiti VALUES (109, 27, 10, '2026-01-20', '2026-02-19', '2026-02-22');
INSERT INTO prestiti VALUES (110, 31, 5, '2026-01-20', '2026-02-19', '2026-03-01');
INSERT INTO prestiti VALUES (111, 41, 35, '2026-01-24', '2026-02-23', '2026-03-06');
INSERT INTO prestiti VALUES (112, 10, 16, '2026-01-25', '2026-02-24', '2026-02-02');
INSERT INTO prestiti VALUES (113, 1, 31, '2026-01-28', '2026-02-27', '2026-03-08');
INSERT INTO prestiti VALUES (114, 4, 35, '2026-01-29', '2026-02-28', '2026-02-22');
INSERT INTO prestiti VALUES (115, 34, 11, '2026-01-30', '2026-03-01', '2026-03-07');
INSERT INTO prestiti VALUES (116, 29, 14, '2026-01-31', '2026-03-02', '2026-02-26');
INSERT INTO prestiti VALUES (117, 13, 21, '2026-02-04', '2026-03-06', '2026-02-14');
INSERT INTO prestiti VALUES (118, 14, 27, '2026-02-04', '2026-03-06', '2026-02-20');
INSERT INTO prestiti VALUES (119, 8, 6, '2026-02-05', '2026-03-07', '2026-03-13');
INSERT INTO prestiti VALUES (120, 33, 31, '2026-02-05', '2026-03-07', '2026-03-17');
INSERT INTO prestiti VALUES (121, 11, 19, '2026-02-07', '2026-03-09', '2026-03-07');
INSERT INTO prestiti VALUES (122, 17, 8, '2026-02-07', '2026-03-09', '2026-03-18');
INSERT INTO prestiti VALUES (123, 38, 37, '2026-02-09', '2026-03-11', '2026-03-09');
INSERT INTO prestiti VALUES (124, 39, 31, '2026-02-09', '2026-03-11', '2026-02-26');
INSERT INTO prestiti VALUES (125, 25, 36, '2026-02-10', '2026-03-12', '2026-02-28');
INSERT INTO prestiti VALUES (126, 9, 19, '2026-02-11', '2026-03-13', '2026-03-26');
INSERT INTO prestiti VALUES (127, 12, 27, '2026-02-11', '2026-03-13', '2026-03-04');
INSERT INTO prestiti VALUES (128, 42, 27, '2026-02-11', '2026-03-13', '2026-03-04');
INSERT INTO prestiti VALUES (129, 10, 36, '2026-02-12', '2026-03-14', '2026-03-27');
INSERT INTO prestiti VALUES (130, 24, 38, '2026-02-13', '2026-03-15', '2026-02-23');
INSERT INTO prestiti VALUES (131, 7, 34, '2026-02-15', '2026-03-17', '2026-03-02');
INSERT INTO prestiti VALUES (132, 13, 16, '2026-02-15', '2026-03-17', '2026-03-24');
INSERT INTO prestiti VALUES (133, 3, 7, '2026-02-20', '2026-03-22', '2026-03-27');
INSERT INTO prestiti VALUES (134, 30, 7, '2026-02-23', '2026-03-25', '2026-03-11');
INSERT INTO prestiti VALUES (135, 16, 9, '2026-02-25', '2026-03-27', '2026-03-28');
INSERT INTO prestiti VALUES (136, 40, 40, '2026-02-26', '2026-03-28', '2026-03-31');
INSERT INTO prestiti VALUES (137, 2, 26, '2026-02-28', '2026-03-30', '2026-04-03');
INSERT INTO prestiti VALUES (138, 4, 21, '2026-03-06', '2026-04-05', '2026-04-19');
INSERT INTO prestiti VALUES (139, 37, 29, '2026-03-06', '2026-04-05', '2026-03-24');
INSERT INTO prestiti VALUES (140, 21, 26, '2026-03-08', '2026-04-07', '2026-03-26');
INSERT INTO prestiti VALUES (141, 12, 2, '2026-03-09', '2026-04-08', '2026-04-19');
INSERT INTO prestiti VALUES (142, 5, 11, '2026-03-10', '2026-04-09', '2026-03-25');
INSERT INTO prestiti VALUES (143, 29, 36, '2026-03-13', '2026-04-12', '2026-04-27');
INSERT INTO prestiti VALUES (144, 44, 34, '2026-03-13', '2026-04-12', '2026-03-26');
INSERT INTO prestiti VALUES (145, 31, 25, '2026-03-16', '2026-04-15', '2026-04-28');
INSERT INTO prestiti VALUES (146, 11, 8, '2026-03-17', '2026-04-16', '2026-04-12');
INSERT INTO prestiti VALUES (147, 33, 14, '2026-03-18', '2026-04-17', '2026-04-18');
INSERT INTO prestiti VALUES (148, 41, 23, '2026-03-19', '2026-04-18', '2026-04-23');
INSERT INTO prestiti VALUES (149, 42, 33, '2026-03-22', '2026-04-21', '2026-04-16');
INSERT INTO prestiti VALUES (150, 1, 37, '2026-03-25', '2026-04-24', '2026-04-15');
INSERT INTO prestiti VALUES (151, 13, 33, '2026-03-26', '2026-04-25', '2026-04-11');
INSERT INTO prestiti VALUES (152, 21, 17, '2026-03-27', '2026-04-26', '2026-04-11');
INSERT INTO prestiti VALUES (153, 30, 23, '2026-03-29', '2026-04-28', '2026-05-04');
INSERT INTO prestiti VALUES (154, 37, 36, '2026-03-30', '2026-04-29', '2026-04-18');
INSERT INTO prestiti VALUES (155, 32, 31, '2026-04-01', '2026-05-01', '2026-04-23');
INSERT INTO prestiti VALUES (156, 18, 5, '2026-04-04', '2026-05-04', '2026-04-16');
INSERT INTO prestiti VALUES (157, 10, 30, '2026-04-08', '2026-05-08', '2026-05-23');
INSERT INTO prestiti VALUES (158, 15, 3, '2026-04-09', '2026-05-09', '2026-05-11');
INSERT INTO prestiti VALUES (159, 44, 20, '2026-04-09', '2026-05-09', '2026-04-16');
INSERT INTO prestiti VALUES (160, 2, 18, '2026-04-10', '2026-05-10', '2026-04-17');
INSERT INTO prestiti VALUES (161, 3, 12, '2026-04-13', '2026-05-13', '2026-05-17');
INSERT INTO prestiti VALUES (162, 5, 27, '2026-04-13', '2026-05-13', '2026-05-14');
INSERT INTO prestiti VALUES (163, 19, 37, '2026-04-14', '2026-05-14', '2026-04-29');
INSERT INTO prestiti VALUES (164, 40, 21, '2026-04-16', '2026-05-16', '2026-05-03');
INSERT INTO prestiti VALUES (165, 9, 17, '2026-04-18', '2026-05-18', '2026-05-01');
INSERT INTO prestiti VALUES (166, 2, 39, '2026-04-19', '2026-05-19', '2026-05-25');
INSERT INTO prestiti VALUES (167, 1, 34, '2026-04-20', '2026-05-20', '2026-05-03');
INSERT INTO prestiti VALUES (168, 33, 9, '2026-04-20', '2026-05-20', '2026-05-15');
INSERT INTO prestiti VALUES (169, 13, 24, '2026-04-24', '2026-05-24', '2026-05-15');
INSERT INTO prestiti VALUES (170, 34, 27, '2026-04-24', '2026-05-24', '2026-05-26');
INSERT INTO prestiti VALUES (171, 11, 2, '2026-04-26', '2026-05-26', '2026-06-06');
INSERT INTO prestiti VALUES (172, 27, 24, '2026-04-29', '2026-05-29', '2026-06-09');
INSERT INTO prestiti VALUES (173, 41, 20, '2026-05-01', '2026-05-31', '2026-05-10');
INSERT INTO prestiti VALUES (174, 16, 39, '2026-05-04', '2026-06-03', '2026-06-10');
INSERT INTO prestiti VALUES (175, 38, 17, '2026-05-05', '2026-06-04', '2026-05-27');
INSERT INTO prestiti VALUES (176, 42, 23, '2026-05-06', '2026-06-05', '2026-06-06');
INSERT INTO prestiti VALUES (177, 12, 17, '2026-05-07', '2026-06-06', '2026-05-23');
INSERT INTO prestiti VALUES (178, 40, 2, '2026-05-07', '2026-06-06', '2026-05-27');
INSERT INTO prestiti VALUES (179, 22, 15, '2026-05-09', '2026-06-08', NULL);
INSERT INTO prestiti VALUES (180, 39, 1, '2026-05-09', '2026-06-08', NULL);
INSERT INTO prestiti VALUES (181, 43, 12, '2026-05-11', '2026-06-10', NULL);
INSERT INTO prestiti VALUES (182, 19, 8, '2026-05-13', '2026-06-12', '2026-06-09');
INSERT INTO prestiti VALUES (183, 29, 14, '2026-05-13', '2026-06-12', '2026-06-01');
INSERT INTO prestiti VALUES (184, 31, 35, '2026-05-13', '2026-06-12', '2026-05-21');
INSERT INTO prestiti VALUES (185, 9, 4, '2026-05-15', '2026-06-14', NULL);
INSERT INTO prestiti VALUES (186, 30, 38, '2026-05-17', '2026-06-16', '2026-05-27');
INSERT INTO prestiti VALUES (187, 23, 39, '2026-05-18', '2026-06-17', NULL);
INSERT INTO prestiti VALUES (188, 7, 20, '2026-05-22', '2026-06-21', '2026-06-09');
INSERT INTO prestiti VALUES (189, 1, 10, '2026-05-23', '2026-06-22', NULL);
INSERT INTO prestiti VALUES (190, 44, 10, '2026-05-24', '2026-06-23', NULL);
INSERT INTO prestiti VALUES (191, 31, 9, '2026-05-26', '2026-06-25', '2026-06-03');
INSERT INTO prestiti VALUES (192, 34, 4, '2026-05-27', '2026-06-26', NULL);
INSERT INTO prestiti VALUES (193, 37, 11, '2026-05-27', '2026-06-26', NULL);
INSERT INTO prestiti VALUES (194, 17, 21, '2026-05-29', '2026-06-28', NULL);
INSERT INTO prestiti VALUES (195, 41, 20, '2026-05-30', '2026-06-29', NULL);
INSERT INTO prestiti VALUES (196, 12, 18, '2026-05-31', '2026-06-30', NULL);
INSERT INTO prestiti VALUES (197, 38, 16, '2026-05-31', '2026-06-30', NULL);
INSERT INTO prestiti VALUES (198, 3, 18, '2026-06-02', '2026-07-02', NULL);
INSERT INTO prestiti VALUES (199, 13, 22, '2026-06-02', '2026-07-02', NULL);
INSERT INTO prestiti VALUES (200, 40, 19, '2026-06-03', '2026-07-03', NULL);

-- nuove acquisizioni e iscrizioni, ancora senza prestiti
INSERT INTO autori VALUES (15, 'Grazia', 'Deledda', 'italiana', 1871);
INSERT INTO libri VALUES (29, 'Il cavaliere inesistente', 2, 'romanzo', 1959);
INSERT INTO copie VALUES (46, 29, 'F4-1', 'buono');
INSERT INTO studenti VALUES (41, 'Tiziana', 'Neri', '3B');
