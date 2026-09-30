---
title: "Modulo 6: Progetto di gruppo"
subtitle: "Sviluppo Software e Coding Laboratoriale"
lang: it
---

# Modulo 6: Progetto di gruppo

Durata: 7 ore (lezioni 6.1-6.7).

Obiettivi del modulo:

- analizzare un problema in termini di requisiti verificabili e priorità
- pianificare il lavoro di un gruppo e seguirne l'avanzamento
- organizzare il codice separando dati, logica e interfaccia
- collaborare con Git su un repository condiviso: branch, merge, conflitti
- verificare il prodotto con test automatici e manuali, e documentare gli errori
- presentare il lavoro e analizzare il processo seguito

Prerequisiti: moduli 1-5.

Svolgimento: gruppi di 3 o 4 studenti realizzano una piccola applicazione web a scelta tra quiz, gioco di memoria, lista di attività e convertitore. Ogni lezione corrisponde a una fase del progetto e produce un risultato funzionante.

Fonti: contenuto originale. Riferimenti esterni: Pro Git (capitoli su server e merge, solo tramite link), Wikipedia (algoritmo di Fisher-Yates), repository Microsoft "Web Development for Beginners" come fonte di spunti per i progetti.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 6.1 | Dal requisito al piano | `lez01_requisiti_e_piano/` |
| 6.2 | Sviluppo: struttura HTML e stile | `lez02_sviluppo_interfaccia/` |
| 6.3 | Sviluppo: logica e dati | `lez03_sviluppo_logica_e_dati/` |
| 6.4 | Sviluppo: interazione | `lez04_sviluppo_interazione/` |
| 6.5 | Sviluppo: integrazione | `lez05_integrazione/` |
| 6.6 | Test e revisione | `lez06_test_e_revisione/` |
| 6.7 | Presentazione e retrospettiva | `lez07_presentazione/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`).

Materiali aggiuntivi:

- `lez03_sviluppo_logica_e_dati/esempio_quiz/`: progetto d'esempio completo (dati, logica, interfaccia, test, README), usato come riferimento in tutte le lezioni del modulo. Verifiche eseguite: 18 test automatici superati su 18; funzionamento completo in browser; nessuna violazione rilevata dal motore di accessibilità axe-core.
- `lez04_sviluppo_interazione/mod06_lez04_quiz_risposta.png`: schermata del quiz dopo una risposta errata.

Il flusso Git descritto nelle lezioni 6.2 e 6.5 (repository bare condiviso, clone di un repository vuoto, branch, merge automatico, conflitto e sua risoluzione) è stato provato con Git reale; gli output riportati nelle lezioni provengono da quella prova, con il percorso del repository adattato a Windows.

Documenti prodotti da ogni gruppo nel proprio repository: `REQUISITI.md`, `PIANO.md`, `TEST.md`, `BUGS.md`, `README.md`.
