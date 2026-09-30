# Scheda del cliente (riservata al docente)

Il docente interpreta il cliente del progetto. La scheda raccoglie le risposte da dare ai team, in modo che tutti ricevano le stesse informazioni. Si risponde solo a ciò che viene chiesto: un requisito che nessun team scopre con le domande resta nascosto fino alle revisioni degli sprint, come succede nella realtà.

## Chi è il cliente

Responsabile dei laboratori della scuola, delegato dal dirigente scolastico. Conosce bene i problemi quotidiani, poco la tecnologia. Parla di "prenotare le ore", non di "record" o "file".

## Situazione attuale

- Le prenotazioni si fanno su un foglio settimanale appeso alla porta di ogni laboratorio, oppure scrivendo ai tecnici.
- Circa 90 docenti; 3 tecnici di laboratorio; 8 tra aule speciali, laboratori e palestra (quelle del kit).
- Problemi principali, in ordine di gravità per il cliente:
  1. due classi nello stesso laboratorio alla stessa ora (succede circa due volte al mese);
  2. i tecnici non sanno quali laboratori preparare la mattina;
  3. il foglio si consulta solo passando davanti al laboratorio;
  4. nessuno sa quanto è usato ciascun laboratorio: il dirigente lo chiede per decidere gli acquisti.

## Risposte alle domande più probabili

| Domanda | Risposta |
|---|---|
| Chi usa il programma? | Docenti per prenotare; tecnici per organizzarsi; il dirigente per i riepiloghi |
| Da dove? | Dai PC della sala docenti e dei laboratori, con Windows; il programma e i dati stanno in una cartella condivisa della scuola |
| Quando si può prenotare? | Dal lunedì al sabato, dalle 8:00 alle 18:00; non nei giorni di chiusura (vacanze, festività) |
| Con quanto anticipo? | Fino a fine anno scolastico; non nel passato |
| Chi può cancellare? | Chi ha prenotato; i tecnici possono cancellare qualunque prenotazione (per esempio per un guasto) |
| Serve una password? | Per ora no: basta scrivere il proprio nome. Il cliente è disposto a discuterne |
| Quali dati personali? | Nome e iniziale del cognome di chi prenota; niente dati degli studenti. Le prenotazioni si possono cancellare a fine anno scolastico |
| Numero di studenti? | Sì, sarebbe utile: i laboratori hanno un numero massimo di posti per sicurezza |
| Prenotazioni ricorrenti? | Molto richieste dai docenti di laboratorio: stessa ora ogni settimana |
| Esportazione? | La vicepresidenza vorrebbe un foglio di calcolo settimanale da appendere in sala docenti |
| Quanto veloce? | "Deve rispondere subito": se il team chiede un numero, meno di 2 secondi anche con tutte le prenotazioni di un anno (circa 5000) |
| Priorità? | Prima di tutto evitare le sovrapposizioni e dare ai tecnici l'elenco del giorno; poi cancellazione e "le mie prenotazioni"; statistiche e ricorrenze sono utili ma possono aspettare |
| Scadenza? | Una prima versione usabile dopo il primo sprint, la versione completa a fine corso |

## Requisiti nascosti

Da rivelare solo se un team fa la domanda giusta:

- **Aula fuori servizio**: capita che un laboratorio resti chiuso per giorni per un guasto (domanda utile: "che cosa succede quando un'aula non è disponibile?").
- **Orari scolastici**: i docenti ragionano per "ore di lezione" (prima ora 8:00-9:00, ecc.), non per orari liberi (domanda utile: "come indicano l'orario i docenti?"). La richiesta si può usare come richiesta di modifica nello sprint 2 (lezione 5.6).
- **Codici delle aule**: i docenti non conoscono codici come LAB-INF1; usano "informatica 1" (domanda utile: "come chiamano le aule i docenti?").

## Comportamento da tenere

- Rispondere in modo non tecnico; se il team usa termini tecnici, chiedere di spiegarli.
- Qualche volta dare risposte vaghe ("deve essere facile", "deve essere veloce"): il team deve chiedere che cosa significa in concreto.
- Non suggerire soluzioni tecniche; se il team chiede "è meglio A o B?", rispondere con i bisogni ("i tecnici hanno poco tempo la mattina").
