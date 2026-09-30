---
title: "Modulo 5: DOM ed eventi"
subtitle: "Sviluppo Software e Coding Laboratoriale"
lang: it
---

# Modulo 5: DOM ed eventi

Durata: 5 ore (lezioni 5.1-5.5).

Obiettivi del modulo:

- leggere e modificare una pagina web con JavaScript attraverso il DOM
- generare elementi della pagina a partire da dati (array di oggetti)
- scrivere programmi guidati dagli eventi: mouse, dito, tastiera, modifica di campi
- comprendere le closure e organizzare lo stato di un'interfaccia
- conservare dati nel browser con localStorage e JSON

Prerequisiti: modulo 3 (JavaScript) e modulo 4 (HTML, CSS, progetto del terrario).

Progetti del modulo: completamento del **terrario** (piante trascinabili, conteggio, riordino) e **gioco di digitazione** con record e storico dei risultati.

Fonti: le lezioni sono adattamenti delle lezioni 10, 11 e 13 del corso Microsoft "Web Development for Beginners" (licenza MIT), con attribuzione completa nei file delle lezioni. Il codice è stato riscritto con nomi in italiano, `addEventListener`, `createElement` al posto di `innerHTML`; estensioni originali: conteggio e riordino nel terrario, velocità in parole al minuto, storico in JSON.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 5.1 | Il DOM | `lez01_dom/` |
| 5.2 | Eventi del mouse: il terrario | `lez02_eventi_mouse_terrario/` |
| 5.3 | Closure e stato | `lez03_closure_e_stato/` |
| 5.4 | Programmazione a eventi: gioco di digitazione (parte 1) | `lez04_gioco_digitazione_parte1/` |
| 5.5 | Gioco di digitazione (parte 2) e memorizzazione locale | `lez05_gioco_digitazione_parte2/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`).

Materiali aggiuntivi:

- immagini del risultato atteso (`mod05_lez0N_*.png`) nelle directory delle lezioni 5.3, 5.4 e 5.5
- `lez03_closure_e_stato/soluzione_terrario_interattivo/`: soluzione completa del terrario (HTML, CSS, JavaScript, script per le immagini)
- `lez05_gioco_digitazione_parte2/soluzione_gioco_digitazione/`: soluzione completa del gioco

Le soluzioni sono state verificate in un browser: trascinamento, conteggio e riordino nel terrario; tutti i casi di digitazione, record, storico dopo il ricaricamento e azzeramento nel gioco.

Cartelle di laboratorio usate dagli studenti: `terrario` (dal modulo 4), `gioco-digitazione`; ciascuna con il proprio repository Git.
