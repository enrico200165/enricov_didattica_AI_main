---
marp: true
paginate: true
lang: it
---

## Lezione 4.4: SQL, join, aggregazioni e modifiche

Modulo 4: Basi di dati. Reti, Cloud e Gestione dei Dati

---

## JOIN

```sql
SELECT l.titolo, a.cognome
FROM libri AS l JOIN autori AS a ON l.id_autore = a.id_autore;
```

- Alias, join concatenati lungo le chiavi esterne
- LEFT JOIN: anche le righe senza corrispondenza (NULL)
- Senza ON: prodotto cartesiano

---

## GROUP BY e HAVING

```sql
SELECT s.classe, COUNT(*) FROM prestiti AS p
JOIN studenti AS s ON p.id_studente = s.id_studente
GROUP BY s.classe;
```

- WHERE filtra le righe, HAVING filtra i gruppi

---

## Creare e modificare

- CREATE TABLE con PRIMARY KEY, NOT NULL, UNIQUE, CHECK, DEFAULT, REFERENCES
- INSERT, UPDATE, DELETE
- UPDATE e DELETE senza WHERE: tutte le righe
- Istruzioni che violano un vincolo: rifiutate

---

## Laboratorio

1. 12 esercizi con join e aggregazioni, stesso correttore
2. `modifiche.sql` su una copia: vincoli in azione
3. Schema della lezione 4.2: `python controlla_schema.py`; 12 test
4. `--mermaid`: diagramma per la documentazione

---

## Aspetti orientativi

- Rapporti e cruscotti: il lavoro degli analisti di dati
- Prudenza con le modifiche in produzione
- Vincolo nel database o controllo nel programma?
