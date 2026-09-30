# Backlog da correggere

Backlog di un progetto di fantasia (un'app per il prestito dei libri della biblioteca scolastica) con alcuni errori di forma e di contenuto. Trovarli prima a mano, poi con `python controlla_storie.py backlog_da_correggere.md`.

## Riepilogo

| ID | Titolo | Priorità | Stima | Stato |
|---|---|---|---|---|
| US-01 | Prestito di un libro | | | da fare |
| US-02 | Restituzione | | | da fare |
| US-03 | Database dei libri | | | da fare |
| US-04 | Ricerca per autore | | | da fare |
| US-05 | Gestione completa della biblioteca | | | da fare |

## Storie

### US-01 Prestito di un libro

Come studente voglio prendere in prestito un libro indicando il suo codice, per leggerlo a casa.

Criteri di accettazione:

- Dato che il libro L-120 è disponibile, quando lo prendo in prestito, allora il libro risulta in prestito a mio nome per 30 giorni.
- Dato che il libro L-120 è già in prestito, quando provo a prenderlo, allora il prestito è rifiutato e vedo la data prevista di restituzione.

### US-02 Restituzione dei libri

Come bibliotecario voglio registrare la restituzione di un libro, per renderlo di nuovo disponibile.

Criteri di accettazione:

- Quando registro la restituzione il sistema funziona correttamente.

### US-03 Database dei libri

Il sistema usa un database SQLite con una tabella libri.

Criteri di accettazione:

- Dato il database, quando si avvia il programma, allora la tabella esiste.

### US-04 Ricerca per autore

Come studente voglio cercare i libri di un autore, per sapere se la biblioteca li ha.

Criteri di accettazione: da scrivere.

### US-05 Gestione completa della biblioteca

Come bibliotecario voglio gestire tutti i libri, gli studenti, i prestiti, le restituzioni, i solleciti, gli acquisti, le statistiche e le donazioni, con stampe e esportazioni in tutti i formati, per avere tutta la biblioteca sotto controllo con un solo programma.

Criteri di accettazione:

- Dato un libro, quando lo gestisco, allora è gestito.

### US-06 Solleciti

Come bibliotecario voglio un elenco dei prestiti scaduti, per mandare i solleciti.

Criteri di accettazione:

- Dato che il prestito di L-120 è scaduto ieri, quando chiedo i prestiti scaduti, allora L-120 compare nell'elenco con il nome dello studente e i giorni di ritardo.
- Dato che non ci sono prestiti scaduti, quando chiedo l'elenco, allora vedo "Nessun prestito scaduto".
