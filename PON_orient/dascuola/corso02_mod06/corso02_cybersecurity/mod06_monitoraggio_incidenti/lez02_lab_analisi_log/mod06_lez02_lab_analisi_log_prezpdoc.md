---
title: "Lezione 6.2: Laboratorio: analisi di log"
subtitle: "Modulo 6: Monitoraggio e risposta agli incidenti. Cybersecurity ed Ethical Hacking"
lang: it
---

## Contenuti

- Dagli eventi agli indicatori
- Anomalie nei log
- Produrre il registro
- Analisi con Python
- Attività
- Aspetti orientativi

## Dagli eventi agli indicatori

- Conteggi e distribuzioni
- Soglie in una finestra di tempo
- Sequenze: accesso riuscito dopo molti fallimenti
- Confronto con la baseline
- Falsi positivi e soglie

## Anomalie nei log

| Attività | Indicatore | MITRE ATT&CK |
|---|---|---|
| Tentativi su un account | molti fallimenti, stesso nome | T1110.001 |
| Password spraying | pochi fallimenti su molti nomi | T1110.003 |
| Credential stuffing | molti indirizzi, nomi inesistenti | T1110.004 |
| Ricerca di pagine | molti 404 dallo stesso indirizzo | T1595 |
| Cancellazione dei log | evento 1102 | T1070 |

## Produrre il registro

1. `python bacheca.py`, uso normale con `anna` e `bruno`
2. Password sbagliate di proposito, eliminazione negata, dato non valido
3. Lettura di `bacheca.log`

## Analisi con Python

```powershell
python analizza_log.py bacheca.log --soglia 3 --finestra 5
```

- Finestra scorrevole sugli accessi falliti per nome
- Accesso riuscito dopo fallimenti
- Operazioni negate, errori interni
- 13 test

## Attività

- Quali errori "normali" vengono segnalati?
- Scelta di soglia e finestra per il registro elettronico
- Nuova segnalazione con test
- Registri di più coppie riuniti

## Aspetti orientativi

- Programmi di analisi e linguaggi dei SIEM
- Miglioramento continuo delle regole
- Quali informazioni mancano nel registro della bacheca?
