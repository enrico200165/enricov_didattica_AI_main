# Segnalazioni degli utenti

Messaggi arrivati al team da docenti e tecnici che provano la versione in `kit_con_difetti`. Sono scritti come li scrivono gli utenti: non indicano la causa, a volte sono imprecisi. Per ciascuno: riprodurre il problema, scrivere la segnalazione con il modello della lezione 4.4, trovare la causa, correggerla con un test.

1. **Da un docente di informatica**: "Ho scritto `lab-inf1` come sempre e il programma mi dice che l'aula non esiste. Eppure c'è!"

2. **Dal tecnico della palestra**: "Il corso pomeridiano finisce alle 18, ma non riesco a prenotare la palestra dalle 17 alle 18. Mi dice che la scuola è aperta fino alle 18: appunto!"

3. **Da una docente di fisica**: "La prenotazione è registrata, ma nel messaggio di conferma l'orario è strano, come se durasse zero minuti."

4. **Dalla segreteria**: "Abbiamo tolto a mano dal file una prenotazione sbagliata. Da allora, le prenotazioni nuove hanno lo stesso numero di una già presente: quale si cancella?"

Il team deve trovare anche **almeno due difetti che nessun utente ha segnalato**. Suggerimenti: la misura della copertura (`copertura.py`), la lettura del codice con la lista di controllo della lezione 4.3, l'apertura del file `dati/prenotazioni.json` dopo aver registrato una prenotazione con il motivo "Attività di laboratorio".
