---
marp: true
paginate: true
lang: it
---

## Lezione 2.3: Priorità e backlog

Modulo 2: Dai bisogni ai requisiti. Informatica per l'Impresa e Soft Skills Digitale

---

## Perché ordinare

- Il tempo non basta mai per tutto
- Backlog del prodotto: elenco ordinato, unica fonte del lavoro del team
- In cima storie piccole e chiare; in fondo possono restare vaghe

---

## Valore e sforzo

```mermaid
quadrantChart
    x-axis Sforzo basso --> Sforzo alto
    y-axis Valore basso --> Valore alto
    quadrant-1 Grandi progetti
    quadrant-2 Vittorie rapide
    quadrant-3 Riempitivi
    quadrant-4 Da evitare
```

---

## MoSCoW

- **Must**: senza, il prodotto non serve
- **Should**: importante, ma c'è un'alternativa
- **Could**: desiderabile, margine se il tempo non basta
- **Won't**: escluso questa volta, in modo esplicito
- DSDM: Must al massimo il 60% dello sforzo, Could circa il 20%

---

## Obiettivo e prodotto minimo

```mermaid
flowchart LR
    K["Kit"] --> V1["Sprint 1<br/>Must"]
    V1 --> V2["Sprint 2<br/>Should e Could"]
    V2 --> R["Rilascio 1.0.0"]
```

- Obiettivo del prodotto: per chi, quale problema, come si verifica

---

## Laboratorio

1. Valore, sforzo e MoSCoW in `valutazioni.csv`
2. Incontro con il cliente sulle priorità
3. `python priorita.py valutazioni.csv --backlog ...\docs\backlog.md`; 19 test
4. Obiettivo del prodotto

---

## Aspetti orientativi

- Decidere le priorità significa dire di no
- Product Owner e product manager
- Il cliente ha cambiato le priorità? Perché?
