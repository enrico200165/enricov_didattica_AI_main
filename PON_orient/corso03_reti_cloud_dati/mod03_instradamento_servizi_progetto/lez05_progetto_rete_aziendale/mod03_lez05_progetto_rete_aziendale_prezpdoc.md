---
title: "Lezione 3.5: Progetto di una rete aziendale"
subtitle: "Modulo 3: Instradamento, servizi e progetto. Reti, Cloud e Gestione dei Dati"
lang: it
---

## Contenuti

- Le fasi del progetto
- Meccanica Esempio S.r.l.
- Lavoro di gruppo
- Valutazione
- Aspetti orientativi

## Le fasi del progetto

```mermaid
flowchart LR
    A["Requisiti"] --> B["Segmentazione"]
    B --> C["Indirizzi"]
    C --> D["Schema"]
    D --> E["Servizi e regole"]
    E --> F["Verifica"]
    F --> G["Documentazione"]
```

## Meccanica Esempio S.r.l.

- Amministrazione 40, progettazione 25, produzione 60
- Wi-Fi dipendenti 150, ospiti 100 (solo Internet)
- Telecamere 16, server 10, gestione 20, collegamento firewall
- Blocco `10.50.0.0/22`, margine 20%, dominio `meccanica.example`

## Lavoro di gruppo

1. Piano: `piano_vlsm.py`, poi `piano_gruppo.csv`
2. Verifica: `python verifica_progetto.py piano_gruppo.csv 10.50.0.0/22`
3. Schema con Draw.io; servizi e regole
4. Modello ridotto in Filius; documento e presentazione

## Valutazione

| Criterio | Peso |
|---|---|
| Requisiti | 10% |
| Piano di indirizzamento | 25% |
| Segmentazione e regole | 20% |
| Schema logico | 15% |
| Servizi, verifica, documentazione | 30% |

## Aspetti orientativi

- Il lavoro del progettista di reti e del system integrator
- La documentazione fa parte del prodotto
- Quali requisiti chiedere ancora al cliente?
