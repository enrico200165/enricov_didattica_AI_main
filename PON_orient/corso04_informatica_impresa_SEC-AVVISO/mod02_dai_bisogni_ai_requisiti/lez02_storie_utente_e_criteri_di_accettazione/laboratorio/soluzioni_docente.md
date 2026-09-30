# Soluzioni per il docente: lezione 2.2

## Backlog da correggere

| Storia | Problema | Criterio INVEST | Correzione possibile |
|---|---|---|---|
| US-01 | nessuno: storia di riferimento | | |
| US-02 | titolo diverso tra tabella e sezione; criterio senza "Dato" e "allora", vago ("funziona correttamente"); un solo criterio | T | "Dato che L-120 è in prestito a Luca, quando registro la restituzione, allora L-120 risulta disponibile"; aggiungere il caso di un libro non in prestito |
| US-03 | non è una storia: descrive una soluzione tecnica, senza utente né vantaggio | N, V | eliminarla: il database è una scelta del team, che serve alle altre storie |
| US-04 | criteri da scrivere | T | "Dato che la biblioteca ha due libri di Calvino, quando cerco "Calvino", allora vedo i due libri con la disponibilità"; caso senza risultati |
| US-05 | storia enorme ("epica"); criterio vuoto ("è gestito") | S, E, T | dividerla in storie separate: prestito, restituzione, solleciti, statistiche, esportazione... |
| US-06 | sezione presente ma non in tabella | | aggiungere la riga al riepilogo |

Output atteso di `python controlla_storie.py backlog_da_correggere.md`:

- US-02: titolo diverso tra tabella e sezione, un solo criterio, criterio che non inizia con "Dato", senza "allora" e con la parola vaga "correttamente"
- US-03: manca il testo "Come ... voglio ... per ..."; un solo criterio
- US-04: criteri da scrivere
- US-05: storia lunga (41 parole); un solo criterio
- US-06: sezione senza riga nella tabella

Il criterio di US-05 "quando lo gestisco, allora è gestito" è formalmente corretto ma inutile: il programma non può accorgersene, il revisore sì. Allo stesso modo US-03 ha un criterio ben formato, ma la storia non ha valore per un utente.

## Criteri di accettazione per il backlog del progetto

Esempi per le storie più probabili dello sprint 1; i team possono scriverne di diversi, purché verificabili.

### US-03 Cancellare una prenotazione

- Dato che la prenotazione 5 è di M. Bianchi, quando M. Bianchi cancella la prenotazione 5, allora la prenotazione non compare più nell'archivio e il programma conferma la cancellazione.
- Dato che la prenotazione 5 è di M. Bianchi, quando L. Verdi prova a cancellarla, allora la cancellazione è rifiutata con un messaggio.
- Dato che la prenotazione 99 non esiste, quando provo a cancellarla, allora vedo il messaggio "la prenotazione 99 non esiste".

### US-04 Le mie prenotazioni

- Dato che M. Bianchi ha due prenotazioni future e una passata, quando chiede le sue prenotazioni, allora vede solo le due future, in ordine di data.
- Dato che S. Russo non ha prenotazioni, quando chiede le sue prenotazioni, allora vede "Nessuna prenotazione".

### US-05 Aule libere in una fascia oraria

- Dato che LAB-INF1 è prenotato il 12/10 dalle 9:00 alle 11:00, quando cerco i laboratori liberi il 12/10 dalle 10:00 alle 11:00, allora LAB-INF1 non compare e LAB-INF2 sì.
- Dato che nessuna palestra è libera, quando cerco le palestre libere, allora vedo "Nessuna aula libera".

### US-06 Niente prenotazioni nel passato o nei giorni di chiusura

- Dato che oggi è il 12/10, quando prenoto per l'11/10, allora la prenotazione è rifiutata.
- Dato che il 18/10 è domenica, quando prenoto per il 18/10, allora la prenotazione è rifiutata.
- Dato che il 1/11 è nell'elenco dei giorni di chiusura, quando prenoto per il 1/11, allora la prenotazione è rifiutata con il motivo.

Nota: il primo criterio richiede di fissare "oggi" nei test; è un buon argomento per la lezione 5.2.

## Divisione di una storia: US-11 Prenotazioni ricorrenti

Divisione possibile in storie più piccole, ciascuna con valore:

- US-11a: prenotare la stessa aula ogni settimana fino a una data, se tutte le settimane sono libere;
- US-11b: se alcune settimane sono occupate, prenotare le altre e mostrare l'elenco di quelle non prenotate;
- US-11c: cancellare in una volta tutte le prenotazioni di una serie.
