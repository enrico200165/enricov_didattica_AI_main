---
title: "Modulo 7: Infrastrutture e professioni"
subtitle: "Reti, Cloud e Gestione dei Dati"
lang: it
---

# Modulo 7: Infrastrutture e professioni

Durata: 3 ore (lezioni 7.1-7.3).

Obiettivi del modulo:

- descrivere un data center, la ridondanza e i livelli di affidabilità
- misurare la disponibilità di un servizio con il monitoraggio e calcolare MTBF, MTTR, PUE, RPO e RTO
- progettare e presentare in gruppo un'infrastruttura completa: rete, dati, cloud
- conoscere le professioni del settore e i percorsi di studio, e riflettere sulle proprie preferenze

Prerequisiti: moduli 1-6. Il progetto finale riusa gli strumenti di tutto il corso.

Fonti: contenuto originale. Riferimenti verificati a settembre 2026: Uptime Institute (classificazione Tier); pagina di Wikipedia in italiano "Power usage effectiveness"; ESCO; European e-Competence Framework; Sistema informativo Excelsior; aree tecnologiche degli ITS Academy (OrizzonteScuola, sintesi del decreto); Universitaly.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 7.1 | Data center e affidabilità | `lez01_data_center_e_affidabilita/` |
| 7.2 | Progetto finale | `lez02_progetto_finale/` |
| 7.3 | Professioni e percorsi | `lez03_professioni_e_percorsi/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Script e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 7.1 | `monitoraggio.py`, `registro_controlli_esempio.csv`, `test_monitoraggio.py`, `soluzioni_docente.md` | 13 test superati su 13: interruzioni, fermo, MTTR, MTBF, percentili, interruzione in corso a fine registro, controlli verso un server di prova attivo, in errore e spento, registrazione su file |
| 7.2 | `modello_presentazione_marp.md`, `controlla_consegna.py`, `test_controlla_consegna.py` | 11 test superati su 11: consegna completa, file mancanti, sezioni e valori mancanti nella relazione, Draw.io non valido, tabella senza chiave primaria, errore SQL, reti sovrapposte o non valide, presentazione senza intestazione Marp |
| 7.3 | `profilo_orientamento.py`, `risposte_esempio.csv`, `scheda_orientamento.md`, `test_profilo_orientamento.py` | 9 test superati su 9: punteggi limite, profili prevalenti, lettura del file, risposte mancanti, risposte non valide ripetute |

Note per il docente:

- lezione 7.1: il calcolo della disponibilità di componenti in serie e in parallelo è svolto nella lezione 6.5 con `disponibilita.py`; la 7.1 lo richiama e aggiunge la disponibilità misurata con il monitoraggio, MTBF e MTTR, PUE, RPO e RTO (syllabus, versione del 30/09/2026 ore 21:15). Per la parte 2 serve la cartella della lezione 5.3 con `biblioteca.db`
- lezione 7.2: il progetto finale riunisce i prodotti dei laboratori 2.4, 3.4, 4.4, 5.3, 6.4 e 6.5, tutti dedicati alla biblioteca della scuola; conviene chiedere ai gruppi, fin dal modulo 2, di copiare questi file in una cartella di progetto. A casa si preparano solo relazione breve e slide; in classe 15 minuti per completare e 45 per le presentazioni. Gli scenari alternativi (azienda, museo) sono facoltativi, fuori orario
- il registro `registro_controlli_esempio.csv` è costruito a scopo didattico (un giorno di controlli con due interruzioni)
- il questionario della lezione 7.3 non salva né invia le risposte; i pesi tra attività e professioni sono una scelta didattica, da discutere con la classe
- le certificazioni professionali citate richiedono in genere un account e un esame a pagamento: sono indicate come possibilità dopo il diploma, non come attività del corso
