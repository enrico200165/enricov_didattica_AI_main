---
title: "Modulo 4: Basi di dati"
subtitle: "Reti, Cloud e Gestione dei Dati"
lang: it
---

# Modulo 4: Basi di dati

Durata: 5 ore (lezioni 4.1-4.5).

Obiettivi del modulo:

- spiegare il modello relazionale: tabelle, tipi, chiavi primarie ed esterne, vincoli
- progettare un database con il modello entità-relazione e tradurlo in tabelle
- interrogare un database con SQL: filtri, ordinamenti, funzioni, join, raggruppamenti
- creare tabelle con vincoli e modificare i dati in sicurezza
- usare un database da Python con parametri e transazioni

Prerequisiti: Python di base (Corso 1 o modulo 1); nessuna conoscenza di database.

Fonti: sezioni 4.1.2 e 4.1.3 adattate da Microsoft, "Data Science for Beginners", lezione "Working with Data: Relational Databases", licenza MIT (esempio delle città e delle precipitazioni); il resto è contenuto originale. Riferimenti verificati a settembre 2026: documentazione di SQLite (tipi, chiavi esterne, SELECT, funzioni), documentazione Python del modulo `sqlite3`, documentazione di Mermaid sui diagrammi entità-relazione, pagine di Wikipedia in italiano "Modello relazionale" e "Modello E-R", estensione SQLite per VS Code, DB Browser for SQLite.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 4.1 | Dati e modello relazionale | `lez01_dati_e_modello_relazionale/` |
| 4.2 | Progettazione concettuale | `lez02_progettazione_er/` |
| 4.3 | SQL, interrogazioni | `lez03_sql_interrogazioni/` |
| 4.4 | SQL, join, aggregazioni e modifiche | `lez04_sql_join_aggregazioni_modifiche/` |
| 4.5 | Python e database | `lez05_python_e_database/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Strumenti usati nel modulo

- Visual Studio Code con l'estensione SQLite (alexcvzz.vscode-sqlite), che include il programma SQLite; alternativa portatile: DB Browser for SQLite 3.13.1, archivio ZIP per Windows
- Visual Studio Code con l'estensione Draw.io Integration, per i diagrammi E-R
- Python (libreria standard: `sqlite3`, `csv`, `datetime`, `hashlib`)

## Il database del modulo

`biblioteca.sql` (lezione 4.1) crea il database `biblioteca.db` di una biblioteca scolastica: 15 autori, 29 libri, 46 copie, 41 studenti, 200 prestiti tra settembre 2025 e giugno 2026. Titoli, autori e anni di prima pubblicazione sono reali; studenti, collocazioni e prestiti sono inventati. Il file `.db` non è incluso: si crea con `python crea_database.py` e si copia nelle cartelle delle lezioni successive. La data di riferimento degli esercizi è il 10 giugno 2026.

## Script e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 4.1 | `biblioteca.sql`, `crea_database.py`, `esplora.sql`, `test_crea_database.py` | 12 test superati su 12: numero di righe, nessuna chiave esterna orfana, nessuna copia prestata due volte nello stesso periodo, scadenze a 30 giorni, vincoli PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL |
| 4.2 | `soluzioni_docente.md` | diagrammi Mermaid verificati; lo schema corrispondente è controllato nella lezione 4.4 |
| 4.3 | `esercizi_4_3.sql`, `correttore.py`, `attesi_4_3.json`, `soluzioni_esercizi_4_3.sql`, `test_correttore.py` | 15 test superati su 15; le soluzioni ottengono 14 su 14; rilevati ordine sbagliato, colonne o righe diverse, errori SQL, istruzioni di modifica (database aperto in sola lettura) |
| 4.4 | `esercizi_4_4.sql`, `attesi_4_4.json`, `soluzioni_esercizi_4_4.sql`, `modifiche.sql`, `controlla_schema.py`, `soluzione_schema.sql`, `dati_prova.sql`, `test_controlla_schema.py` | 12 test superati su 12; le soluzioni della 4.4 ottengono 12 su 12 con il correttore della 4.3; `modifiche.sql` eseguito su una copia: 4 modifiche accettate, 4 rifiutate dai vincoli come previsto |
| 4.5 | `gestione_prestiti.py`, `nuovi_prestiti.csv`, `nuovi_prestiti_errati.csv`, `test_gestione_prestiti.py` | 15 test superati su 15: controlli delle righe, transazione tutto o niente, reimportazione rifiutata, ricerca con parametri (apici e testo malevolo), rapporto Markdown |

Note per il docente:

- materiale per il docente, da non distribuire prima degli esercizi: `lez02_progettazione_er/laboratorio/soluzioni_docente.md`, `soluzioni_esercizi_4_3.sql`, `soluzioni_esercizi_4_4.sql`, `soluzione_schema.sql`; i file `attesi_4_3.json` e `attesi_4_4.json` contengono solo impronte e si possono distribuire
- comandi e voci dell'estensione SQLite (**SQLite: Open Database**, **SQLite: Use Database**, **SQLite: Run Query** con `Ctrl+Shift+Q`, **SQLite: Run Selected Query**, **Show Table**, pannello **SQLite Explorer**) verificati nel file di configurazione dell'estensione (versione 0.14.1); l'estensione non è aggiornata dal 2022: se dà problemi (per esempio con l'attendibilità dell'area di lavoro, comando **SQLite: Change Workspace Trust**) si usa DB Browser for SQLite
- in SQLite le chiavi esterne vanno attivate per ogni connessione: gli script Python lo fanno; nei file SQL eseguiti dall'estensione il `PRAGMA` è scritto sulla stessa riga delle istruzioni che ne dipendono
- per riportare il database allo stato iniziale basta rieseguire `crea_database.py`
