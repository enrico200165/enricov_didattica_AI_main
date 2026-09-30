-- Soluzioni degli esercizi della lezione 4.4 (materiale per il docente)
-- Database: biblioteca.db (lezione 4.1)

-- esercizio 1 (ordinato)
SELECT a.cognome, l.titolo
FROM libri AS l JOIN autori AS a ON l.id_autore = a.id_autore
ORDER BY a.cognome, l.titolo;

-- esercizio 2
SELECT l.titolo, l.anno
FROM libri AS l JOIN autori AS a ON l.id_autore = a.id_autore
WHERE a.cognome = 'Levi';

-- esercizio 3 (ordinato)
SELECT a.cognome, COUNT(*) AS numero_libri
FROM libri AS l JOIN autori AS a ON l.id_autore = a.id_autore
GROUP BY a.id_autore
ORDER BY numero_libri DESC, a.cognome;

-- esercizio 4
SELECT a.cognome, COUNT(*) AS numero_libri
FROM libri AS l JOIN autori AS a ON l.id_autore = a.id_autore
GROUP BY a.id_autore
HAVING COUNT(*) >= 3;

-- esercizio 5 (ordinato)
SELECT l.titolo, COUNT(c.id_copia) AS copie
FROM libri AS l JOIN copie AS c ON c.id_libro = l.id_libro
GROUP BY l.id_libro
ORDER BY l.titolo;

-- esercizio 6 (ordinato)
SELECT s.classe, COUNT(*) AS prestiti
FROM prestiti AS p JOIN studenti AS s ON p.id_studente = s.id_studente
GROUP BY s.classe
ORDER BY s.classe;

-- esercizio 7 (ordinato)
SELECT l.titolo, COUNT(*) AS prestiti
FROM prestiti AS p
JOIN copie AS c ON p.id_copia = c.id_copia
JOIN libri AS l ON c.id_libro = l.id_libro
GROUP BY l.id_libro
ORDER BY prestiti DESC, l.titolo
LIMIT 5;

-- esercizio 8 (ordinato)
SELECT s.cognome, s.nome, s.classe, l.titolo, p.data_scadenza
FROM prestiti AS p
JOIN studenti AS s ON p.id_studente = s.id_studente
JOIN copie AS c ON p.id_copia = c.id_copia
JOIN libri AS l ON c.id_libro = l.id_libro
WHERE p.data_restituzione IS NULL AND p.data_scadenza < '2026-06-10'
ORDER BY p.data_scadenza;

-- esercizio 9
SELECT a.nome, a.cognome
FROM autori AS a LEFT JOIN libri AS l ON l.id_autore = a.id_autore
WHERE l.id_libro IS NULL;

-- esercizio 10
SELECT s.nome, s.cognome, s.classe
FROM studenti AS s LEFT JOIN prestiti AS p ON p.id_studente = s.id_studente
WHERE p.id_prestito IS NULL;

-- esercizio 11 (ordinato)
SELECT l.genere, COUNT(*) AS prestiti
FROM prestiti AS p
JOIN copie AS c ON p.id_copia = c.id_copia
JOIN libri AS l ON c.id_libro = l.id_libro
GROUP BY l.genere
HAVING COUNT(*) > 20
ORDER BY prestiti DESC;

-- esercizio 12 (ordinato)
SELECT l.titolo, COUNT(p.id_prestito) AS prestiti
FROM libri AS l
JOIN copie AS c ON c.id_libro = l.id_libro
LEFT JOIN prestiti AS p ON p.id_copia = c.id_copia
GROUP BY l.id_libro
ORDER BY prestiti, l.titolo
LIMIT 3;
