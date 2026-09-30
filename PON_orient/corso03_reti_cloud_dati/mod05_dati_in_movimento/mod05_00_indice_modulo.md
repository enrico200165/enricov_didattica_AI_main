---
title: "Modulo 5: Dati in movimento"
subtitle: "Reti, Cloud e Gestione dei Dati"
lang: it
---

# Modulo 5: Dati in movimento

Durata: 3 ore (lezioni 5.1-5.3).

Obiettivi del modulo:

- usare i formati CSV, JSON e XML e gestire correttamente la codifica dei caratteri
- confrontare il modello relazionale con i database a documenti e le altre famiglie NoSQL
- spiegare lo stile REST e interrogare API pubbliche con REST Client e Python
- costruire e osservare un'applicazione web completa: pagina, API, database

Prerequisiti: lezione 1.4 (HTTP, REST Client); modulo 4, in particolare il database `biblioteca.db` creato nella lezione 4.1; per la lezione 5.3, nozioni di base di HTML e JavaScript (Corso 1).

Fonti: sezione 5.1.4 adattata da Microsoft, "Data Science for Beginners", lezione "Working with Data: Non-Relational Data", licenza MIT; il resto è contenuto originale. Riferimenti verificati a settembre 2026: RFC 4180 e 8259; documentazione e condizioni d'uso di Open Library e Open-Meteo; MDN Web Docs (Fetch API, CORS); pagine di Wikipedia in italiano "UTF-8", "Representational state transfer".

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 5.1 | Formati dei dati e database a documenti | `lez01_formati_dei_dati_e_documenti/` |
| 5.2 | API REST | `lez02_api_rest/` |
| 5.3 | Laboratorio: servizio e client | `lez03_lab_servizio_e_client/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Strumenti usati nel modulo

- Visual Studio Code con le estensioni Python e REST Client
- Python (libreria standard: `csv`, `json`, `xml.etree.ElementTree`, `sqlite3`, `urllib`, `http.server`)
- un browser con gli strumenti per sviluppatori (DevTools)
- API pubbliche gratuite e senza registrazione: Open Library (https://openlibrary.org/developers/api ) e Open-Meteo (https://open-meteo.com/ , uso non commerciale, dati CC BY 4.0)

## Script e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 5.1 | `converti_formati.py`, `titoli_excel.csv`, `test_converti_formati.py` | 15 test superati su 15: esportazione in CSV, JSON e XML, rilettura, ricostruzione delle tabelle identiche all'originale, CSV di Excel in Windows-1252 con `;`, confronto dei byte UTF-8 e Windows-1252 |
| 5.2 | `api_pubbliche.http`, `client_api.py`, `test_client_api.py` | 10 test superati su 10 con un server locale che riproduce la struttura documentata delle due API: parametri, intestazione `User-Agent`, campi mancanti, errore 400 con motivo, risposta non JSON, pausa tra le richieste, servizio irraggiungibile |
| 5.3 | `servizio_biblioteca.py`, `static/index.html`, `static/app.js`, `static/stile.css`, `richieste_biblioteca.http`, `test_servizio.py` | 28 test superati su 28; le dieci richieste di `richieste_biblioteca.http` eseguite con i codici attesi; pagina provata in Chromium (ricerca, filtro per genere, copie, prestito riuscito e rifiutato, nessun errore JavaScript) |

Note per il docente:

- `biblioteca.db` va copiato nelle cartelle di lavoro dalla lezione 4.1; per ripristinare i dati si riesegue `crea_database.py`
- le API pubbliche della lezione 5.2 non erano raggiungibili dall'ambiente in cui il materiale è stato preparato: formato delle richieste e struttura delle risposte seguono la documentazione ufficiale e il client è stato verificato con un server simulato. Prima della lezione conviene eseguire una volta le richieste di `api_pubbliche.http` dalla rete della scuola, per controllare che non siano bloccate da filtri o proxy
- le API pubbliche hanno limiti d'uso: con una classe intera che esegue le stesse richieste conviene non ripeterle in ciclo
- il servizio della lezione 5.3 ascolta solo su `127.0.0.1` e non ha autenticazione: è pensato per il proprio PC
