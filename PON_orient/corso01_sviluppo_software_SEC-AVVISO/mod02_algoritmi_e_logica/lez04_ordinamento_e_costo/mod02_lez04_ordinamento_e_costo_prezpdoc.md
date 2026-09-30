---
title: "Lezione 2.4: Ordinamento e costo degli algoritmi"
subtitle: "Modulo 2: Algoritmi e logica. Sviluppo Software e Coding Laboratoriale"
lang: it
---

## Contenuti

- Selection sort
- Costo degli algoritmi
- Laboratorio 2.4: misurare i tempi
- Aspetti orientativi

## Selection sort

- Si cerca il minimo e lo si porta in prima posizione, poi in seconda, ...
- Scambio con variabile di appoggio `temp`

| i | Array dopo il passo |
|---|---|
| 0 | [**10**, 29, 14, 37, 13] |
| 1 | [**10, 13**, 14, 37, 29] |
| 2 | [**10, 13, 14**, 37, 29] |
| 3 | [**10, 13, 14, 29, 37**] |

Animazione: https://visualgo.net/en/sorting

## Costo degli algoritmi

- Si contano le operazioni fondamentali (confronti), non i secondi
- Selection sort: n(n - 1) / 2 confronti, sempre

| Classe | Esempio | n raddoppia |
|---|---|---|
| Logaritmica | ricerca binaria | +1 operazione |
| Lineare | ricerca lineare, massimo | operazioni x 2 |
| Quadratica | selection sort | operazioni x 4 |

## Laboratorio 2.4: misurare i tempi

```javascript
let t0 = performance.now();
selectionSort(a);
const tempoSelection = performance.now() - t0;

b.sort((x, y) => x - y);   // sort predefinito, criterio numerico
```

- n = 1000, 2000, 4000, 8000, 16000
- Verifica: tempo del selection sort circa x 4 a ogni raddoppio
- Prima misura anomala: compilazione JIT
- Commit Git del lavoro

## Aspetti orientativi

- "Algoritmi e strutture dati": nucleo dei corsi universitari di informatica
- Esercizi su algoritmi e costo nei colloqui tecnici
- Nel lavoro si usano le librerie, ma serve riconoscere un algoritmo troppo costoso
- Quali servizi quotidiani dipendono da algoritmi efficienti?
