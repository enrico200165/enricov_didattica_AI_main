# Backlog del prodotto

Esempio: backlog del team di fantasia Orione alla fine del modulo 3, con priorità, stime e criteri delle storie più importanti.

Richieste del cliente per "Prenotazioni dei laboratori", scritte come storie utente. Il backlog è ordinato dal Product Owner con il cliente (lezione 2.3) e si aggiorna per tutto il progetto: le storie si possono riscrivere, dividere, aggiungere o eliminare.

- **Priorità**: metodo MoSCoW (Must, Should, Could, Won't), da assegnare nella lezione 2.3.
- **Stima**: punti relativi, da assegnare con il planning poker nella lezione 3.3.
- **Stato**: da fare, in corso, in revisione, fatto.

## Riepilogo

| ID | Titolo | Priorità | Stima | Stato |
|---|---|---|---|---|
| US-00 | Elenco delle aule e nuova prenotazione | | | fatto (kit) |
| US-01 | Nessuna prenotazione sovrapposta | Must | 5 | da fare |
| US-02 | Prenotazioni di un giorno | Must | 2 | da fare |
| US-03 | Cancellare una prenotazione | Must | 3 | da fare |
| US-04 | Le mie prenotazioni | Should | 2 | da fare |
| US-05 | Aule libere in una fascia oraria | Should | 3 | da fare |
| US-06 | Niente prenotazioni nel passato o nei giorni di chiusura | Should | 3 | da fare |
| US-07 | Spostare una prenotazione | Could | 3 | da fare |
| US-08 | Riepilogo settimanale di un'aula | Should | 3 | da fare |
| US-09 | Esportazione in CSV | Could | 2 | da fare |
| US-10 | Numero di studenti e capienza | Should | 2 | da fare |
| US-11 | Prenotazioni ricorrenti | Could | 13 | da fare |
| US-12 | Aula fuori servizio | Could | 3 | da fare |
| US-13 | Ruoli: docente e tecnico | Won't | 8 | da fare |
| US-14 | Messaggi e aiuto in italiano | Could | 2 | da fare |
| US-15 | Statistiche di utilizzo delle aule | Could | 5 | da fare |

## Storie

### US-01 Nessuna prenotazione sovrapposta

Come docente voglio che il programma rifiuti una prenotazione se l'aula è già occupata in quell'orario, per non trovare il laboratorio occupato da un'altra classe.

Criteri di accettazione:

- Dato che LAB-INF1 è prenotato il 12/10 dalle 9:00 alle 11:00, quando prenoto LAB-INF1 il 12/10 dalle 10:00 alle 12:00, allora la prenotazione è rifiutata con un messaggio che indica la prenotazione già presente.
- Dato che LAB-INF1 è prenotato il 12/10 dalle 9:00 alle 11:00, quando prenoto LAB-INF1 il 12/10 dalle 11:00 alle 12:00, allora la prenotazione è accettata (un'ora finisce quando l'altra inizia).
- Dato che LAB-INF1 è prenotato il 12/10 dalle 9:00 alle 11:00, quando prenoto LAB-CHI nello stesso orario, allora la prenotazione è accettata.

### US-02 Prenotazioni di un giorno

Come tecnico di laboratorio voglio vedere tutte le prenotazioni di un giorno, ordinate per aula e per orario, per preparare i laboratori prima dell'arrivo delle classi.

Criteri di accettazione:

- Dato che esistono prenotazioni il 12/10, quando chiedo le prenotazioni del 12/10, allora vedo solo quelle, ordinate per aula e ora di inizio, con orario, richiedente e motivo.
- Dato che non esistono prenotazioni il 13/10, quando chiedo le prenotazioni del 13/10, allora vedo il messaggio "Nessuna prenotazione".

### US-03 Cancellare una prenotazione

Come docente voglio cancellare una mia prenotazione indicandone il numero, per liberare l'aula quando non mi serve più.

Criteri di accettazione:

- Dato che la prenotazione 5 è di M. Bianchi, quando M. Bianchi cancella la prenotazione 5, allora la prenotazione non compare più nell'archivio e il programma conferma la cancellazione.
- Dato che la prenotazione 5 è di M. Bianchi, quando L. Verdi prova a cancellarla, allora la cancellazione è rifiutata con un messaggio.
- Dato che la prenotazione 99 non esiste, quando provo a cancellarla, allora vedo il messaggio "la prenotazione 99 non esiste".

### US-04 Le mie prenotazioni

Come docente voglio vedere l'elenco delle mie prenotazioni future, per ricordare quando ho prenotato un laboratorio.

Criteri di accettazione:

- Dato che M. Bianchi ha due prenotazioni future e una passata, quando chiede le sue prenotazioni, allora vede solo le due future, in ordine di data.
- Dato che S. Russo non ha prenotazioni, quando chiede le sue prenotazioni, allora vede "Nessuna prenotazione".

### US-05 Aule libere in una fascia oraria

Come docente voglio sapere quali aule di un certo tipo sono libere in un giorno e in una fascia oraria, per scegliere dove portare la classe.

Criteri di accettazione:

- Dato che LAB-INF1 è prenotato il 12/10 dalle 9:00 alle 11:00, quando cerco i laboratori liberi il 12/10 dalle 10:00 alle 11:00, allora LAB-INF1 non compare e LAB-INF2 sì.
- Dato che nessuna palestra è libera, quando cerco le palestre libere, allora vedo "Nessuna aula libera".

### US-06 Niente prenotazioni nel passato o nei giorni di chiusura

Come segreteria voglio che non si possano prenotare giorni già passati, domeniche e giorni di chiusura della scuola, per avere un archivio senza prenotazioni impossibili.

Criteri di accettazione:

- Dato che oggi è il 12/10, quando prenoto per l'11/10, allora la prenotazione è rifiutata.
- Dato che il 18/10 è domenica, quando prenoto per il 18/10, allora la prenotazione è rifiutata.
- Dato che il 1/11 è nell'elenco dei giorni di chiusura, quando prenoto per il 1/11, allora la prenotazione è rifiutata con il motivo.

### US-07 Spostare una prenotazione

Come docente voglio cambiare giorno o orario di una mia prenotazione, senza cancellarla e rifarla, per adattarmi ai cambi di orario.

Criteri di accettazione: da scrivere.

### US-08 Riepilogo settimanale di un'aula

Come tecnico di laboratorio voglio vedere, per un'aula, le prenotazioni della settimana dal lunedì al sabato, per organizzare la manutenzione nelle ore libere.

Criteri di accettazione:

- Dato che LAB-CHI ha prenotazioni lunedì 12/10 e mercoledì 14/10, quando chiedo il riepilogo della settimana del 12/10 per LAB-CHI, allora vedo le prenotazioni divise per giorno dal lunedì al sabato.
- Dato che LAB-FIS non ha prenotazioni nella settimana del 12/10, quando chiedo il riepilogo, allora vedo "Nessuna prenotazione nella settimana".

### US-09 Esportazione in CSV

Come vicepreside voglio esportare le prenotazioni di un periodo in un file CSV, per aprirle con un foglio di calcolo e appenderle in bacheca.

Criteri di accettazione: da scrivere.

### US-10 Numero di studenti e capienza

Come docente voglio indicare quanti studenti porto e che il programma rifiuti la prenotazione se superano i posti dell'aula, per rispettare le norme di sicurezza.

Criteri di accettazione:

- Dato che LAB-INF1 ha 28 posti, quando prenoto LAB-INF1 per 25 studenti, allora la prenotazione è accettata e registra il numero di studenti.
- Dato che LAB-INF1 ha 28 posti, quando prenoto LAB-INF1 per 30 studenti, allora la prenotazione è rifiutata con un messaggio che indica i posti disponibili.

### US-11 Prenotazioni ricorrenti

Come docente voglio prenotare la stessa aula ogni settimana, nello stesso giorno e orario, fino a una data, per non ripetere la prenotazione tutte le settimane.

Criteri di accettazione: da scrivere. Domanda aperta: che cosa succede se una delle settimane è già occupata?

### US-12 Aula fuori servizio

Come tecnico di laboratorio voglio segnare un'aula come fuori servizio fino a una data, per evitare prenotazioni durante le riparazioni.

Criteri di accettazione: da scrivere.

### US-13 Ruoli: docente e tecnico

Come tecnico di laboratorio voglio che solo i tecnici possano segnare le aule fuori servizio e cancellare prenotazioni di altri, per evitare modifiche per errore.

Criteri di accettazione: da scrivere. Nota: il programma non ha un sistema di accesso con password; il ruolo si indica con un'opzione del comando. Da discutere con il cliente se basta.

### US-14 Messaggi e aiuto in italiano

Come docente voglio che tutti i messaggi, compreso l'aiuto sui comandi, siano in italiano e chiari, per usare il programma senza chiedere aiuto.

Criteri di accettazione: da scrivere.

### US-15 Statistiche di utilizzo delle aule

Come dirigente scolastico voglio sapere quante ore è stata prenotata ogni aula in un mese, per decidere dove investire nei laboratori.

Criteri di accettazione: da scrivere.
