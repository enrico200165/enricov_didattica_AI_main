---
title: "Lezione 7.1: soluzioni"
subtitle: "Modulo 7: Infrastrutture e professioni. Materiale per il docente"
lang: it
---

# Lezione 7.1: soluzioni

Valori calcolati con `monitoraggio.py`.

## Parte 1

- Interruzioni: dalle 3:05 alle 3:17 (12 controlli con `TimeoutError`: il servizio non risponde, per esempio processo bloccato o server spento) e dalle 14:02 alle 14:06 (4 controlli con codice `503`: il servizio risponde ma segnala di non essere disponibile, per esempio durante un aggiornamento).
- Il 95° percentile (130 ms) è molto più alto della mediana (48 ms) perché dalle 8:00 alle 13:00 le risposte sono più lente di circa 80 ms: sono le ore di lezione, con più utenti.

## Parte 3

1. MTBF 2000 h, MTTR 4 h: disponibilità 99,80%. Con MTTR di 30 minuti: 99,975%. Ridurre i tempi di ripristino vale quanto rendere i componenti più affidabili.
2. PUE = 1200 / 800 = 1,5. Energia non informatica: 400 kW per 8760 ore = 3 504 000 kWh (3,5 GWh) all'anno.
3. RPO 24 ore (si possono perdere i prestiti dell'ultimo giorno), RTO 4 ore. Per una biblioteca scolastica è in genere accettabile; per il registro elettronico no: voti e assenze di una giornata non possono andare persi e il registro serve durante le lezioni, quindi servono repliche continue e ripristino in minuti.
