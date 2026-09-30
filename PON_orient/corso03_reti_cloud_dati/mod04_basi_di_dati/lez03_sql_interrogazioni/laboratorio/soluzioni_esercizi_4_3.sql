-- Soluzioni degli esercizi della lezione 4.3 (materiale per il docente)
-- Database: biblioteca.db (lezione 4.1)

-- esercizio 1
SELECT titolo, anno FROM libri;

-- esercizio 2
SELECT titolo, anno FROM libri WHERE genere = 'fantascienza';

-- esercizio 3 (ordinato)
SELECT titolo, anno FROM libri WHERE anno < 1900 ORDER BY anno;

-- esercizio 4 (ordinato)
SELECT cognome, nome FROM studenti WHERE classe = '4A' ORDER BY cognome, nome;

-- esercizio 5
SELECT nome, cognome, nazionalita FROM autori WHERE nazionalita <> 'italiana';

-- esercizio 6
SELECT titolo FROM libri WHERE titolo LIKE 'La %';

-- esercizio 7 (ordinato)
SELECT titolo, anno FROM libri WHERE anno BETWEEN 1940 AND 1960 ORDER BY anno, titolo;

-- esercizio 8 (ordinato)
SELECT DISTINCT genere FROM libri ORDER BY genere;

-- esercizio 9 (ordinato)
SELECT id_prestito, id_copia, data_scadenza FROM prestiti
WHERE data_restituzione IS NULL ORDER BY data_scadenza;

-- esercizio 10
SELECT COUNT(*) FROM prestiti WHERE data_restituzione > data_scadenza;

-- esercizio 11 (ordinato)
SELECT titolo, 2026 - anno AS anni FROM libri ORDER BY anno LIMIT 5;

-- esercizio 12 (ordinato)
SELECT UPPER(titolo), LENGTH(titolo) FROM libri WHERE id_autore = 2
ORDER BY LENGTH(titolo) DESC, titolo;

-- esercizio 13 (ordinato)
SELECT data_prestito, data_restituzione,
       julianday(data_restituzione) - julianday(data_prestito) AS giorni
FROM prestiti
WHERE id_studente = 21 AND data_restituzione IS NOT NULL
ORDER BY data_prestito;

-- esercizio 14
SELECT MIN(anno), MAX(anno), ROUND(AVG(anno)) FROM libri;
