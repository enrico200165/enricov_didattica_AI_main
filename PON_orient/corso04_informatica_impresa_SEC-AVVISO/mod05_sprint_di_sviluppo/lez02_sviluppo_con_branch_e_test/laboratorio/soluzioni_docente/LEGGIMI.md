# Soluzione di riferimento: storie US-01, US-02, US-03

Materiale per il docente: una possibile realizzazione delle tre storie Must dello sprint 1, per confrontarla con quelle dei team o per aiutare un team bloccato. Non va distribuita agli studenti prima della revisione dello sprint.

## File

| File | Che cosa cambia rispetto al kit |
|---|---|
| `logica.py` | nuove funzioni `si_sovrappongono`, `prenotazione_in_conflitto` (US-01), `prenotazioni_del_giorno` (US-02), `cancella_prenotazione` (US-03); `nuova_prenotazione` rifiuta le sovrapposizioni |
| `prenotazioni.py` | nuovi comandi `giorno` (US-02) e `cancella` (US-03) |
| `tests/test_storie_sprint1.py` | 16 test scritti dai criteri di accettazione, più casi limite e prove dei comandi |
| `tests/test_logica.py` | un test del kit modificato (vedi sotto) |
| `dati/prenotazioni.json` | la prenotazione 4 spostata dalle 13:00 alle 14:00, così i dati di esempio non contengono più sovrapposizioni |

Per provarla: copiare i file in una copia del kit, mantenendo le cartelle, ed eseguire `python -m unittest` (43 test superati).

## Un test del kit che si rompe

Con US-01 il test del kit `test_id_successivo_al_massimo` fallisce: prepara prenotazioni incomplete (`{"id": 3}`), e il nuovo controllo delle sovrapposizioni legge aula, giorno e orari di tutte le prenotazioni. Il codice nuovo è corretto; è il test che usava dati irrealistici. La correzione rende complete le prenotazioni del test.

È una situazione frequente e istruttiva: quando una modifica fa fallire un test esistente, bisogna capire se ha sbagliato il codice nuovo o se il test si basava su un'ipotesi che non vale più. Conviene lasciarla scoprire ai team e discuterla nella lezione 5.3 o 5.5.

## Scelte da discutere con i team

- **Confronto dei nomi nella cancellazione**: la soluzione ignora maiuscole e spazi finali. Un team può scegliere diversamente; l'importante è che la scelta sia coerente con i criteri e provata.
- **Messaggio di sovrapposizione**: indica aula, orari, numero e richiedente della prenotazione esistente, come chiede il primo criterio di US-01. Il nome del richiedente è un dato personale minimo (nome e iniziale), già visibile nel foglio attuale.
- **Formato dell'elenco del giorno**: non è fissato dai criteri; la soluzione mostra anche il numero della prenotazione, utile per la cancellazione.
