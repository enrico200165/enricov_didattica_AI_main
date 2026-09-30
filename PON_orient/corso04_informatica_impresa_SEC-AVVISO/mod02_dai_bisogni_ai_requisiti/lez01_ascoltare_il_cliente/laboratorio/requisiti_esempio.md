# Requisiti: esempio da migliorare

Primo elenco scritto da un team di fantasia dopo l'intervista al cliente. Alcuni requisiti sono scritti bene, altri vanno riscritti.

## Requisiti funzionali

- RF-01: Il programma rifiuta una prenotazione se l'aula è già prenotata in un orario che si sovrappone.
- RF-02: Il tecnico vede le prenotazioni di un giorno, ordinate per aula e ora di inizio.
- RF-03: Il docente può cancellare le sue prenotazioni e modificarle e vedere quelle degli altri ecc.
- RF-04: Il programma esporta le prenotazioni in un formato comodo.

## Requisiti non funzionali

- RNF-01: Il programma deve essere veloce.
- RNF-02: Un elenco delle prenotazioni di un giorno compare in meno di 2 secondi con 5000 prenotazioni in archivio.
- RNF-03: I messaggi devono essere facili da capire per tutti.
- RNF-04: I dati personali conservati sono solo nome e iniziale del cognome di chi prenota.

## Vincoli

- V-01: Il programma funziona sui PC dei laboratori con Windows e Python, senza installare altri pacchetti.
- V-02: Le prenotazioni si conservano in file JSON.
