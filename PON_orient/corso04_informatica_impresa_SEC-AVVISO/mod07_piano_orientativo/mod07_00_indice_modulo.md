---
title: "Modulo 7: Piano orientativo"
subtitle: "Informatica per l'Impresa e Soft Skills Digitale"
lang: it
---

# Modulo 7: Piano orientativo

Durata: 4 ore (lezioni 7.1-7.4).

Obiettivi del modulo:

- collegare ruoli e attività del progetto alle professioni ICT reali, usando ESCO, i profili europei delle professioni ICT e l'e-CF
- conoscere i percorsi dopo il diploma (ITS Academy, università, lavoro e apprendistato) e le fonti per informarsi; confrontare due percorsi con criteri personali e fonti verificabili
- leggere un annuncio, scrivere un CV e una lettera di presentazione, affrontare un colloquio con il metodo STAR
- costruire un piano orientativo personale con obiettivi SMART, preparare il colloquio con il docente tutor su E-Portfolio e capolavoro

Prerequisiti: moduli 1-6, in particolare la riflessione personale e la scheda delle competenze della lezione 6.3.

Fonti: contenuto originale. Riferimenti verificati a settembre 2026: ESCO, https://esco.ec.europa.eu/it ; CEN CWA 16458-1:2018, profili europei delle professioni ICT (solo nomi dei profili, documento con diritti riservati); EXIN, sintesi dell'e-CF, https://www.exin.com/e-cf-competences/ ; Regione Lazio, ITS Academy, https://www.regione.lazio.it/cittadini/scuola-universita/istituti-tecnici-superiori ; Universitaly, https://www.universitaly.it/ ; AlmaLaurea, https://www.almalaurea.it/ ; Excelsior, https://excelsior.unioncamere.net/ ; Europass, https://europass.europa.eu/it/create-europass-cv ; Wikipedia (criteri SMART, metodo STAR); circolare MIM n. 1616 del 17/05/2024. Verifica sull'esistenza di materiali open source riutilizzabili: i quadri europei sono citati e riassunti; le attività sono costruite sul progetto del corso.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 7.1 | Professioni del progetto ICT | `lez01_professioni_del_progetto_ict/` |
| 7.2 | Percorsi dopo il diploma | `lez02_percorsi_dopo_il_diploma/` |
| 7.3 | Candidarsi: CV e colloquio | `lez03_candidarsi_cv_e_colloquio/` |
| 7.4 | Il mio piano orientativo | `lez04_il_mio_piano_orientativo/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Materiali e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 7.1 | `professioni_ict.py`, `professioni.json`, `risposte_esempio.csv`, `test_professioni_ict.py` | 13 test superati su 13: coerenza dei dati (12 attività, 8 professioni, ogni attività usata), classifica dell'esempio, ordine a parità, media arrotondata, questionario con risposte non valide ripetute, errori nel file delle risposte, scheda Markdown, salvataggio e rilettura delle risposte |
| 7.2 | `confronta_percorsi.py`, `criteri_esempio.csv`, `percorsi_esempio.csv`, `test_confronta_percorsi.py` | 15 test superati su 15: totali dell'esempio (50 e 48 su 65), criteri da cui dipende la scelta, pareggi, informazioni e fonti mancanti, fonti senza indirizzo web, punteggi e pesi non validi, criteri mancanti o sconosciuti, scheda Markdown, confronto non calcolato con dati incompleti |
| 7.3 | `cv_e_annuncio.py`, `cv_esempio.md`, `cv_da_migliorare.md`, `annuncio_stage.md`, `annuncio_apprendistato.md`, `domande_colloquio.md`, `griglia_colloquio.md`, `test_cv_e_annuncio.py` | 16 test superati su 16: sezioni, parti da completare, e-mail, dati personali non necessari (data di nascita, stato civile, codice fiscale, fotografia), espressioni generiche, lunghezza, lettura dei requisiti, confronto con i due annunci (7 su 8 e 2 su 5, con il falso positivo discusso nella lezione) |
| 7.4 | `piano_orientativo.py`, `piano_esempio.md`, `modello_piano.md`, `colloquio_docente_tutor.md`, `test_piano_orientativo.py` | 17 test superati su 17: lettura della tabella, priorità, stati e date non validi, scadenze passate, obiettivi oltre 24 mesi, obiettivi vaghi, limite di obiettivi in corso, tappa vicina, obiettivo Must, linea del tempo Mermaid (verificata e visualizzata in Chromium) |

Gli output di esempio riportati nelle lezioni sono stati ottenuti eseguendo gli script sui file di esempio.

## Note per il docente

- **Sessioni**: con sessioni da 2 ore, 7.1+7.2 e 7.3+7.4; con sessioni da 3 ore, 6.3+7.1+7.2 e 7.3+7.4, con l'ora restante per i colloqui con i docenti tutor o per recuperare attività rimaste indietro. La lezione 7.4 chiude il corso.
- **Dati personali**: questionari, confronti, CV e piani restano agli studenti; non vanno nel repository del team né consegnati, salvo che lo studente lo scelga. Nella simulazione del CV si possono omettere telefono e indirizzo.
- **Nessun account**: ESCO, Universitaly, AlmaLaurea, Excelsior e i siti degli ITS si consultano senza registrazione. L'editor Europass si usa come ospite (il CV si scarica, non resta sul sito); se in futuro chiedesse un profilo, si usa il CV in Markdown. LinkedIn e GitHub non si usano nel corso.
- **Annunci**: gli annunci del laboratorio sono di fantasia. Se si vogliono usare annunci reali, conviene sceglierli prima della lezione, togliendo eventuali riferimenti personali.
- **Dati sui percorsi**: i dati di esempio (monitoraggio INDIRE 2025, offerta ITS del Lazio) vanno aggiornati ogni anno; la lezione 7.2 insegna a verificarne fonte e data.
- **Colloquio con il docente tutor**: la traccia `colloquio_docente_tutor.md` collega il corso alle attività di orientamento della scuola; conviene concordare con i docenti tutor delle classi i tempi dei colloqui.
- **Simulazione di colloquio**: le domande non pertinenti (stato civile, religione, opinioni) sono discusse per insegnare a riconoscerle; il selezionatore non le usa nella simulazione.
