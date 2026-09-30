# Backlog del prodotto

Richieste del cliente per "Prenotazioni dei laboratori", scritte come storie utente. Il backlog è ordinato dal Product Owner con il cliente (lezione 2.3) e si aggiorna per tutto il progetto: le storie si possono riscrivere, dividere, aggiungere o eliminare.

- **Priorità**: metodo MoSCoW (Must, Should, Could, Won't), da assegnare nella lezione 2.3.
- **Stima**: punti relativi, da assegnare con il planning poker nella lezione 3.3.
- **Stato**: da fare, in corso, in revisione, fatto.

## Riepilogo

| ID | Titolo | Priorità | Stima | Stato |
|---|---|---|---|---|
| US-00 | Elenco delle aule e nuova prenotazione | | | fatto (kit) |
| US-01 | Nessuna prenotazione sovrapposta | | | da fare |
| US-02 | Prenotazioni di un giorno | | | da fare |
| US-03 | Cancellare una prenotazione | | | da fare |
| US-04 | Le mie prenotazioni | | | da fare |
| US-05 | Aule libere in una fascia oraria | | | da fare |
| US-06 | Niente prenotazioni nel passato o nei giorni di chiusura | | | da fare |
| US-07 | Spostare una prenotazione | | | da fare |
| US-08 | Riepilogo settimanale di un'aula | | | da fare |
| US-09 | Esportazione in CSV | | | da fare |
| US-10 | Numero di studenti e capienza | | | da fare |
| US-11 | Prenotazioni ricorrenti | | | da fare |
| US-12 | Aula fuori servizio | | | da fare |
| US-13 | Ruoli: docente e tecnico | | | da fare |
| US-14 | Messaggi e aiuto in italiano | | | da fare |
| US-15 | Statistiche di utilizzo delle aule | | | da fare |

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

Criteri di accettazione: da scrivere (lezione 2.2).

### US-04 Le mie prenotazioni

Come docente voglio vedere l'elenco delle mie prenotazioni future, per ricordare quando ho prenotato un laboratorio.

Criteri di accettazione: da scrivere.

### US-05 Aule libere in una fascia oraria

Come docente voglio sapere quali aule di un certo tipo sono libere in un giorno e in una fascia oraria, per scegliere dove portare la classe.

Criteri di accettazione: da scrivere.

### US-06 Niente prenotazioni nel passato o nei giorni di chiusura

Come segreteria voglio che non si possano prenotare giorni già passati, domeniche e giorni di chiusura della scuola, per avere un archivio senza prenotazioni impossibili.

Criteri di accettazione: da scrivere. Domanda aperta per il cliente: dove sono indicati i giorni di chiusura?

### US-07 Spostare una prenotazione

Come docente voglio cambiare giorno o orario di una mia prenotazione, senza cancellarla e rifarla, per adattarmi ai cambi di orario.

Criteri di accettazione: da scrivere.

### US-08 Riepilogo settimanale di un'aula

Come tecnico di laboratorio voglio vedere, per un'aula, le prenotazioni della settimana dal lunedì al sabato, per organizzare la manutenzione nelle ore libere.

Criteri di accettazione: da scrivere.

### US-09 Esportazione in CSV

Come vicepreside voglio esportare le prenotazioni di un periodo in un file CSV, per aprirle con un foglio di calcolo e appenderle in bacheca.

Criteri di accettazione: da scrivere.

### US-10 Numero di studenti e capienza

Come docente voglio indicare quanti studenti porto e che il programma rifiuti la prenotazione se superano i posti dell'aula, per rispettare le norme di sicurezza.

Criteri di accettazione: da scrivere.

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
