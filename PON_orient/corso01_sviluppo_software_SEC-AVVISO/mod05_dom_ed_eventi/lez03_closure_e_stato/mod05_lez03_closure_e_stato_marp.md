---
marp: true
paginate: true
lang: it
---

## Lezione 5.3: Closure e stato

Modulo 5: DOM ed eventi. Sviluppo Software e Coding Laboratoriale

Fonte: adattamento da Microsoft, "Web Development for Beginners", lezione "DOM Manipulation and JavaScript Closures", licenza MIT
https://github.com/microsoft/Web-Dev-For-Beginners

---

## Closure

```javascript
function creaContatore() {
  let conteggio = 0;
  function incrementa() { conteggio++; return conteggio; }
  return incrementa;
}
const contaA = creaContatore();
const contaB = creaContatore();
contaA(); contaA(); contaB();   // 1, 2, 1
```

- La funzione interna conserva le variabili esterne
- Ogni chiamata crea un insieme di variabili separato
- **Incapsulamento**: nessun accesso diretto dall'esterno

---

## Closure nel terrario

```mermaid
flowchart LR
    subgraph C1["rendiTrascinabile(pianta1)"]
        V1["elemento, xPrec, yPrec"]
    end
    subgraph C2["rendiTrascinabile(pianta2)"]
        V2["elemento, xPrec, yPrec"]
    end
```

Ogni pianta usa le proprie variabili

---

## Stato di un'interfaccia

- Stato di un componente: nella closure
- Stato condiviso: variabile esterna (`zMassimo`)
- Un dato, un solo punto di aggiornamento

```mermaid
flowchart LR
    E["Evento"] --> S["Stato"] --> R["DOM"] --> A["Attesa"] --> E
```

Schema alla base di React, Vue, Angular

---

## Il terrario completo

- Primo piano: `zMassimo++`, `style.zIndex`
- Conteggio: `getBoundingClientRect()`, punto dentro un rettangolo
- Riordino: `style.left = ""`

![Terrario con due piante nel barattolo](mod05_lez03_risultato_terrario_interattivo.png)

---

## Aspetti orientativi

- Trascinamento e stato: bacheche kanban, editor grafici, configuratori
- Gestione dello stato: problema centrale del front-end
- Quali sono lo stato e gli eventi di un'app di uso quotidiano?
