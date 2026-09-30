---
title: "Lezione 2.3: Algoritmi su elenchi"
subtitle: "Modulo 2: Algoritmi e logica. Sviluppo Software e Coding Laboratoriale"
lang: it
---

## Contenuti

- Array
- Ricerca lineare e ricerca binaria
- Ricerca binaria in JavaScript

## Array

```javascript
const voti = [7, 5, 9, 6, 8];
voti[2]        // 9 (indici da 0)
voti.length    // 5
```

Schema della **scansione**: un ciclo visita gli elementi e aggiorna il risultato

- **Accumulatore**: somma
- **Contatore condizionato**: quanti voti sono sufficienti
- **Massimo**: parte da `v[0]`, non da 0

## Ricerca lineare e ricerca binaria

- **Lineare**: confronta gli elementi uno alla volta; fino a n confronti
- **Binaria**: array **ordinato**; confronto con l'elemento centrale, intervallo dimezzato

| n | Lineare | Binaria |
|---|---|---|
| 8 | 8 | 4 |
| 1 000 | 1 000 | 10 |
| 1 000 000 | 1 000 000 | 20 |

## Ricerca binaria in JavaScript

```javascript
function ricercaBinaria(v, x) {
  let basso = 0;
  let alto = v.length - 1;
  while (basso <= alto) {
    const medio = Math.floor((basso + alto) / 2);
    if (v[medio] === x) return medio;
    else if (x < v[medio]) alto = medio - 1;
    else basso = medio + 1;
  }
  return -1;
}
```

Attività con 16 carte coperte: ordinate e mescolate
