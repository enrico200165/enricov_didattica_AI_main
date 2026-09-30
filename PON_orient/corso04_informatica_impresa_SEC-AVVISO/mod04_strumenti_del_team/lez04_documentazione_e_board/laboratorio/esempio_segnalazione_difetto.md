# D-01: una prenotazione che si sovrappone a un'altra viene accettata

- **Segnalato da**: tecnico di laboratorio (cliente)
- **Data**: 14/10/2026
- **Versione o commit**: kit di partenza
- **Gravità**: grave
- **Stato**: aperto
- **Storia collegata**: US-01

## Passi per riprodurre

1. Partire dai dati di esempio del kit (`dati/prenotazioni.json`), in cui LAB-INF1 è prenotato il 12/10/2026 dalle 9:00 alle 11:00.
2. Eseguire `python prenotazioni.py prenota LAB-INF1 2026-10-12 10:00 12:00 "L. Verdi"`.

## Risultato atteso

La prenotazione è rifiutata con un messaggio che indica la prenotazione già presente.

## Risultato ottenuto

```text
Prenotazione 6 registrata: LAB-INF1, 2026-10-12, 10:00-12:00, L. Verdi
```

## Note

Succede sempre. Anche nei dati di esempio le prenotazioni 3 e 4 dell'aula magna si sovrappongono.

## Correzione

...
