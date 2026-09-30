---
title: "Lezione 2.1: Problemi e algoritmi"
subtitle: "Modulo 2: Algoritmi e logica. Sviluppo Software e Coding Laboratoriale"
lang: it
---

## Contenuti

- Algoritmo: definizione
- Variabili e assegnazione
- Pseudocodice
- Diagramma di flusso
- Laboratorio 2.1: il robot umano

## Algoritmo: definizione

- **Algoritmo**: sequenza finita di istruzioni non ambigue che risolve tutti i problemi di una classe
- **Esecutore**: persona, robot, computer
- **Programma**: algoritmo scritto in un linguaggio di programmazione

Proprietà: **finitezza**, **non ambiguità**, **eseguibilità**, **generalità**

```mermaid
flowchart LR
    I["Input"] --> E["Elaborazione"] --> O["Output"]
```

## Variabili e assegnazione

```text
totale ← 0
totale ← totale + 5
```

- **Variabile**: contenitore con un nome
- **Assegnazione** `←`: calcola a destra, scrive a sinistra
- Non è un'equazione matematica

## Pseudocodice

| Pseudocodice | Significato |
|---|---|
| `LEGGI x` / `SCRIVI x` | input / output |
| `x ← espressione` | assegnazione |
| `SE ... ALLORA ... ALTRIMENTI ... FINE SE` | selezione |
| `MENTRE ... ESEGUI ... FINE MENTRE` | ciclo, controllo in testa |
| `PER i DA a A b ESEGUI ... FINE PER` | ciclo con contatore |
| `RIPETI ... FINCHÉ ...` | ciclo, controllo in coda |

## Diagramma di flusso

```mermaid
flowchart TD
    A(["Inizio"]) --> B[/"LEGGI prezzo, percentuale"/]
    B --> C["sconto ← prezzo * percentuale / 100"]
    C --> D["finale ← prezzo - sconto"]
    D --> E[/"SCRIVI finale"/]
    E --> F(["Fine"])
```

Ovale: inizio/fine; parallelogramma: I/O; rettangolo: elaborazione; rombo: decisione

## Laboratorio 2.1: il robot umano

- Griglia 5 x 5, partenza, arrivo, ostacoli
- Istruzioni: `AVANTI`, `GIRA A DESTRA`, `GIRA A SINISTRA`
- Il robot esegue alla lettera
- Errori tipici: orientamento iniziale, destra/sinistra, istruzioni mancanti
- Correzione degli errori: **debugging**
