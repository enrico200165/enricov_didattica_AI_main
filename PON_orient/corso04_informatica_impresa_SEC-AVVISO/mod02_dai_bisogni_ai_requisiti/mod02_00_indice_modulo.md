---
title: "Modulo 2: Dai bisogni ai requisiti"
subtitle: "Informatica per l'Impresa e Soft Skills Digitale"
lang: it
---

# Modulo 2: Dai bisogni ai requisiti

Durata: 4 ore (lezioni 2.1-2.4).

Obiettivi del modulo:

- raccogliere i bisogni del cliente con un'intervista e tradurli in requisiti funzionali, non funzionali e vincoli verificabili
- scrivere storie utente con criteri di accettazione nella forma Dato, Quando, Allora, e valutarle con i criteri INVEST
- ordinare il backlog per valore e sforzo con il metodo MoSCoW; definire obiettivo del prodotto e prodotto minimo funzionante
- costruire prototipi a bassa fedeltà e applicare tecniche di problem solving: brainstorming, 5 perché, diagramma causa-effetto, matrice di decisione

Prerequisiti: modulo 1 (team formati, kit di partenza funzionante).

Fonti: contenuto originale. Riferimenti verificati a settembre 2026: Wikipedia (Requirements elicitation, Non-functional requirement, User story, Website wireframe, Brainstorming, Five whys, Diagramma di Ishikawa, Decision matrix); Bill Wake, INVEST (xp123.com); Cucumber, parole chiave di Gherkin in italiano; Agile Business Consortium, MoSCoW (DSDM); La Guida a Scrum 2020 (CC BY-SA 4.0), citata per le definizioni di backlog e obiettivo del prodotto, senza adattarne il testo. Verifica sull'esistenza di materiali open source riutilizzabili: non sono stati trovati materiali aperti in italiano adatti al livello del corso; le lezioni sono originali.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 2.1 | Ascoltare il cliente | `lez01_ascoltare_il_cliente/` |
| 2.2 | Storie utente e criteri di accettazione | `lez02_storie_utente_e_criteri_di_accettazione/` |
| 2.3 | Priorità e backlog | `lez03_priorita_e_backlog/` |
| 2.4 | Prototipi e problem solving | `lez04_prototipi_e_problem_solving/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Materiali e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 2.1 | `modello_verbale_intervista.md`, `requisiti_esempio.md`, `requisiti_ambigui.py`, `test_requisiti_ambigui.py`, `scheda_cliente_docente.md` | 17 test superati su 17: parole vaghe (anche plurali, espressioni di più parole, solo parole intere), requisiti non funzionali senza numero, più frasi, più azioni unite da "e", lunghezza, codici ripetuti o non validi, requisiti da completare, file di esempio |
| 2.2 | `backlog_da_correggere.md`, `scheda_revisione_storie.md`, `controlla_storie.py`, `test_controlla_storie.py`, `soluzioni_docente.md` | 16 test superati su 16: tutti i difetti del backlog da correggere, backlog del kit (US-00 esclusa, 13 storie senza criteri), criteri delle soluzioni del docente riconosciuti come corretti, varianti Data/Quando/Allora, parole vaghe, codici ripetuti, troppi criteri |
| 2.3 | `valutazioni_esempio.csv`, `obiettivo_prodotto.md`, `priorita.py`, `test_priorita.py` | 19 test superati su 19: ordinamento, quote di sforzo, coordinate del diagramma, errori nel CSV con numero di riga, aggiornamento del backlog del kit (priorità, ordine, copia .bak, sezioni delle storie invariate), storie assenti dal backlog; diagramma generato controllato con il motore di Mermaid e visualizzato in Chromium |
| 2.4 | `prototipi_interfaccia.drawio`, `matrice_esempio.csv`, `analisi_problema.md`, `matrice_decisione.py`, `test_matrice_decisione.py` | 17 test superati su 17: totali, parità, sensibilità ai pesi (cambio di vincitore e parità), errori nel CSV, distacco minimo; file Draw.io controllato come XML valido |

I test di `controlla_storie.py` e `priorita.py` che usano il backlog del kit vengono saltati, con un messaggio, se la cartella del laboratorio è copiata fuori dalla struttura del corso.

## Note per il docente

- **Il docente è il cliente.** La scheda `lez01_ascoltare_il_cliente/laboratorio/scheda_cliente_docente.md` contiene le risposte da dare, le priorità del cliente e tre requisiti "nascosti" da rivelare solo a chi fa la domanda giusta; uno di essi (le ore di lezione al posto degli orari liberi) può servire come richiesta di modifica nello sprint 2 (lezione 5.6).
- **Copia di riferimento del progetto.** Dalla lezione 2.2 ogni team tiene una copia del kit, `C:\corso-impresa\progetto_<team>`, sul PC del Product Owner o su una chiavetta; i documenti del modulo (backlog aggiornato, obiettivo del prodotto, prototipi, decisioni) vanno nella sua cartella `docs`. Nella lezione 4.1 questa copia diventa il repository del team: prima di crearlo si ripristina `dati/prenotazioni.json` dal kit originale, così il repository parte da dati puliti e conserva i documenti del modulo 2. Il fatto che più membri lavorino su copie diverse degli stessi file è un buon esempio del problema che Git risolve.
- **Lezione 2.1**: con sei team le interviste durano circa 18 minuti; gli altri team ascoltano e annotano. Se i team sono di più, conviene ridurre a 2 minuti ciascuno o fare le interviste in due gruppi.
- **Lezione 2.3**: il colloquio sulle priorità avviene team per team mentre gli altri lavorano; le priorità del cliente sono nella scheda della lezione 2.1. Nella matrice valore-sforzo i punteggi 3 cadono sul confine tra i quadranti: sono storie di media importanza o di medio sforzo.
- **Lezione 2.4**: i due prototipi di interfaccia sono volutamente alternativi. Il kit usa i comandi con argomenti; se un team sceglie il menu interattivo, la scelta diventa una storia del backlog da negoziare con il cliente, con il costo che comporta.
- Soluzioni della lezione 2.2 in `lez02_storie_utente_e_criteri_di_accettazione/laboratorio/soluzioni_docente.md`.
