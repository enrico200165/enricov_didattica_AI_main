# Soluzioni per il docente: lezione 5.5

La cartella `kit_con_difetti` è il kit di partenza con sei difetti inseriti di proposito. I test che li avrebbero rivelati sono stati tolti: tutti i 22 test rimasti passano.

| N. | File e riga | Difetto | Sintomo | Test tolto dal kit | Correzione |
|---|---|---|---|---|---|
| 1 | `logica.py`, `cerca_aula` | manca `.upper()` nel confronto del codice | `lab-inf1` non viene trovata (segnalazione 1) | `test_codice_aula_in_minuscolo` | `codice.strip().upper()` |
| 2 | `logica.py`, controllo degli orari | `ora_fine >= CHIUSURA` invece di `>` | una prenotazione che finisce alle 18:00 è rifiutata (segnalazione 2) | `test_orario_di_apertura_completo_accettato` | `ora_fine > CHIUSURA` |
| 3 | `prenotazioni.py`, `comando_prenota` | nella conferma `p['inizio']` compare due volte | "09:00-09:00" (segnalazione 3) | nessuno: il test controllava solo "Prenotazione 1 registrata" | `{p['inizio']}-{p['fine']}` |
| 4 | `logica.py`, `nuova_prenotazione` | numero calcolato con `len(prenotazioni) + 1` invece del massimo più uno | con numeri non consecutivi (una prenotazione tolta) si creano numeri doppi (segnalazione 4) | `test_id_successivo_al_massimo` | `max(..., default=0) + 1` |
| 5 | `logica.py`, controllo del richiedente | `if not richiedente:` senza `.strip()` | un nome fatto solo di spazi è accettato e salvato vuoto (non segnalato; la copertura mostra la riga 60 mai eseguita) | `test_richiedente_mancante` | `if not richiedente.strip():` |
| 6 | `archivio.py`, `salva_prenotazioni` | manca `ensure_ascii=False` | nel file JSON "Attività" diventa `Attività`; il programma legge correttamente, ma il file non è più leggibile per le persone (non segnalato) | `test_lettere_accentate_leggibili_nel_file` | `json.dump(..., ensure_ascii=False, indent=2)` |

## Come arrivarci

- Difetti 1 e 2: il debugger con le configurazioni di `.vscode/launch.json`, un punto di interruzione in `cerca_aula` o sul controllo degli orari, e il pannello delle variabili (`codice`, `ora_fine`, `CHIUSURA`).
- Difetto 3: lettura del codice di `comando_prenota`; il test esistente passa perché controlla solo una parte del messaggio.
- Difetto 4: per riprodurlo si tolgono a mano dal file dei dati di prova le prenotazioni 2 e 3, poi si registrano due prenotazioni; oppure si scrive direttamente un test con numeri non consecutivi.
- Difetto 5: `copertura.py kit_con_difetti` segnala come mai eseguita la riga 60 di `logica.py`, il messaggio "indicare chi prenota": nessun test prova un richiedente mancante.
- Difetto 6: registrare una prenotazione con una lettera accentata nel motivo e aprire il file JSON.

## Punti da discutere

- La copertura del kit con difetti è del 98% e i test passano tutti: copertura alta e test verdi non garantiscono l'assenza di difetti. I test controllano solo ciò per cui sono stati scritti.
- Il difetto 3 è coperto da un test che lo esegue ma non controlla il risultato: una riga eseguita non è una riga verificata.
- Per ogni difetto la correzione giusta comprende un test che fallisce prima della correzione e passa dopo.
