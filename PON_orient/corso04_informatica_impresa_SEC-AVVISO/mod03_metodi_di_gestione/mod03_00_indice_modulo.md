---
title: "Modulo 3: Metodi di gestione"
subtitle: "Informatica per l'Impresa e Soft Skills Digitale"
lang: it
---

# Modulo 3: Metodi di gestione

Durata: 4 ore (lezioni 3.1-3.4).

Obiettivi del modulo:

- descrivere il ciclo di vita del software e il modello a cascata, con vantaggi, limiti e ambiti d'uso
- pianificare un progetto con diagramma di Gantt, dipendenze e percorso critico
- conoscere valori e principi agili e il framework Scrum; sperimentarlo in una simulazione
- usare una board Kanban con limiti al lavoro in corso, stimare con il planning poker, usare la velocità, gestire i rischi
- conoscere come lavorano le aziende ICT: tipi di aziende, ruoli, contratti e preventivi, norme sulla qualità e sui dati

Prerequisiti: moduli 1 e 2 (backlog ordinato nella copia di riferimento del progetto).

Fonti: lezione 3.2, sezioni 3.2.2-3.2.4, adattate da "La Guida a Scrum" 2020 di Ken Schwaber e Jeff Sutherland (licenza CC BY-SA 4.0; le sezioni adattate mantengono la stessa licenza); citazioni del Manifesto Agile (traduzione italiana). Il resto è contenuto originale. Riferimenti verificati a settembre 2026: Wikipedia (Waterfall model, Kanban (development), Planning poker, Risk matrix); documentazione di Mermaid (gantt, kanban); ISO (9001, 25010:2023, 27001:2022); Garante per la protezione dei dati personali; AgID. Verifica sull'esistenza di materiali open source riutilizzabili: la Guida a Scrum è stata adattata come previsto dal syllabus; non sono stati trovati altri materiali aperti in italiano adatti.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 3.1 | Ciclo di vita e modello a cascata | `lez01_ciclo_di_vita_e_modello_a_cascata/` |
| 3.2 | Agile e Scrum | `lez02_agile_e_scrum/` |
| 3.3 | Kanban, stime e pianificazione | `lez03_kanban_stime_e_pianificazione/` |
| 3.4 | Come lavorano le aziende ICT | `lez04_come_lavorano_le_aziende_ict/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Materiali e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 3.1 | `attivita_cascata.csv`, `attivita_modificate.csv`, `piano_cascata.py`, `test_piano_cascata.py`, `soluzioni_docente.md` | 20 test superati su 20: giorni lavorativi e fine settimana, date del piano di esempio, margini, percorso critico, traguardi, diagramma Gantt, dipendenze inesistenti o circolari, confronto con il piano modificato; diagramma controllato con il motore di Mermaid e visualizzato in Chromium; soluzioni verificate eseguendo lo script sulle varianti del piano |
| 3.2 | `regole_simulazione.md`, `sprint_esempio.csv`, `registro_sprint.py`, `test_registro_sprint.py` | 13 test superati su 13: velocità, precisione, qualità, impegno proposto, grafico Mermaid `xychart-beta` (visualizzato in Chromium), errori nel registro |
| 3.3 | `stime_esempio.csv`, `planning_poker.py`, `test_planning_poker.py`, `rischi_esempio.csv`, `registro_rischi.py`, `test_registro_rischi.py` | planning poker: 14 test superati su 14 (ultimo giro, accordo, quasi accordo, carte lontane, "?", carte non valide, velocità, scrittura nel backlog); rischi: 15 test superati su 15 (livelli, controlli su azione e responsabile, matrice, errori) |
| 3.4 | `attivita_preventivo.csv`, `tariffe_esempio.json`, `preventivo.py`, `test_preventivo.py`, `domande_per_il_docente.md`, `traccia_docente.md` | 14 test superati su 14: costo, riserva, margine, IVA, confronto tra contratti a corpo e a tempo e materiali, formato italiano degli importi, errori; soluzioni della traccia verificate con lo script |

## Note per il docente

- **Lezione 3.2, simulazione**: servono carta di recupero (almeno 30 fogli per team) e un segno sul pavimento a 3 metri; conviene svolgerla in un'aula con spazio libero. Nello sprint 3 il docente, come cliente, può aggiungere un criterio (per esempio "l'aeroplano ha un finestrino disegnato"), da comunicare solo nella pianificazione.
- **Lezione 3.2, licenze**: il Manifesto Agile è citato (quattro valori, frase finale e tre principi) con rimando al testo completo, invece di essere riportato per intero come indicato nel file di avvertenze del corso; le sezioni adattate dalla Guida a Scrum sono delimitate nel testo e mantengono la licenza CC BY-SA 4.0.
- **Lezione 3.3**: la velocità di 10 punti usata nell'esempio è un'ipotesi; la velocità reale si misura nello sprint 1 (lezione 5.4). I file `stime.csv`, `rischi.csv` e la matrice dei rischi vanno salvati in `docs` della copia del progetto.
- **Lezione 3.4**: la lezione è condotta dal docente; `traccia_docente.md` propone scaletta, spunti per il racconto dell'esperienza personale, attenzioni e soluzioni dell'attività sul preventivo. Le tariffe dell'esempio sono di fantasia.
- I test di `planning_poker.py` usano un backlog costruito nel test stesso: funzionano anche se la cartella del laboratorio è copiata fuori dalla struttura del corso.
