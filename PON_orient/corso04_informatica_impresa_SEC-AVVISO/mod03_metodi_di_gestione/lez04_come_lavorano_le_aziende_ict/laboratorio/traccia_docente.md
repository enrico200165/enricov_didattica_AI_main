# Traccia per il docente: lezione 3.4

La lezione è condotta dal docente come testimone di come le aziende ICT gestiscono i progetti. La lezione scritta fornisce contenuti e riferimenti; questa traccia propone come usarli e dove inserire la propria esperienza.

## Scaletta (60 minuti)

| Tempo | Parte | Suggerimenti |
|---|---|---|
| 5 min | Apertura | il proprio percorso professionale in breve; in quali tipi di aziende o progetti si è lavorato |
| 10 min | Tipi di aziende e ruoli (3.4.1-3.4.2) | un progetto reale raccontato attraverso i ruoli coinvolti: chi c'era, che cosa faceva ciascuno |
| 15 min | Contratti e preventivi (3.4.3), con `preventivo.py` | un caso di progetto andato oltre la stima: com'è stato gestito, chi ha pagato la differenza |
| 10 min | Qualità, norme, sicurezza (3.4.4) | come la norma o il cliente hanno cambiato il modo di lavorare (documentazione, verifiche, dati personali) |
| 5 min | Strumenti e team distribuiti (3.4.5) | mostrare facoltativamente, con il proprio account, una board o un sistema di segnalazione reale, senza dati riservati |
| 15 min | Domande dei team | dal file `domande_per_il_docente.md`, a rotazione tra i team |

## Spunti per il racconto

- Un progetto in cui i requisiti sono cambiati molto: che cosa ha funzionato per gestirlo?
- La differenza tra lavorare per un cliente esterno e per il reparto informatico della propria organizzazione.
- Un esempio di stima sbagliata e di che cosa si è imparato.
- Come si entra in un'azienda ICT dopo il diploma e che cosa si impara nei primi mesi.
- Le competenze trasversali che si sono rivelate più importanti.

## Attenzioni

- Non citare nomi di clienti, colleghi o dati riservati; per i casi reali, anonimizzare.
- Gli strumenti professionali online si mostrano con il proprio account, alla lavagna; gli studenti non si registrano.
- Le tariffe del file `tariffe_esempio.json` sono di fantasia, scelte per rendere il calcolo leggibile: se si citano tariffe reali, indicare che variano molto per ruolo, esperienza, territorio e tipo di azienda.

## Soluzioni dell'attività sul preventivo

1. Il contratto a corpo va in perdita quando il costo reale supera l'imponibile: 13.940 x (1 + s) > 17.634,10, cioè per uno scostamento oltre il 26,5% circa (con 26% il fornitore guadagna ancora, con 27% perde).
2. Con scostamento 0 il cliente paga 17.634,10 euro a corpo e 15.334 euro a tempo e materiali: a corpo paga anche la riserva per i rischi, cioè il "prezzo" per trasferire il rischio al fornitore.
3. Esempio di attività aggiuntive: analisi della modifica (analista, 2 giorni), revisione dei documenti (analista, 2), modifica di regole e comandi (sviluppatore, 5), manuale (analista, 1), nuovi test (tester, 4); il prezzo si calcola con un CSV che contiene solo queste attività.
4. Tempo e materiali, o contratti a corpo per singoli rilasci con ambito concordato sprint per sprint: l'ambito di un progetto agile cambia per definizione, mentre il contratto a corpo lo fissa all'inizio.
