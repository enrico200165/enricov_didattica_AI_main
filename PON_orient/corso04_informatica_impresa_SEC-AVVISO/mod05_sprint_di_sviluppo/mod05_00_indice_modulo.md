---
title: "Modulo 5: Due sprint di sviluppo"
subtitle: "Informatica per l'Impresa e Soft Skills Digitale"
lang: it
---

# Modulo 5: Due sprint di sviluppo

Durata: 8 ore (lezioni 5.1-5.8), da svolgere in sessioni di due ore consecutive.

Obiettivi del modulo:

- pianificare uno sprint: obiettivo, capacità, storie, compiti, definizione di "fatto"
- sviluppare a partire dai criteri di accettazione trasformati in test, con un ramo per storia
- condurre il daily scrum, gestire gli ostacoli, misurare l'avanzamento con il burndown, integrare spesso
- condurre revisione e retrospettiva, misurare la velocità e il miglioramento tra sprint
- conoscere tipi di test e copertura, trovare e correggere difetti con metodo e con il debugger
- gestire una richiesta di modifica del cliente con l'analisi di impatto; riconoscere e registrare il debito tecnico

Prerequisiti: moduli 1-4 (repository del team condiviso, backlog con priorità, stime e criteri).

Fonti: contenuto originale. Riferimenti verificati a settembre 2026: La Guida a Scrum 2020 (CC BY-SA 4.0, solo citata); documentazione di Python (unittest, trace, ast); documentazione di Visual Studio Code (debugging); Wikipedia (Test-driven development, Burn down chart, Change request, Technical debt, Code refactoring). Verifica sull'esistenza di materiali open source riutilizzabili: le lezioni sono costruite sul progetto del corso e sui suoi strumenti; non esistono materiali aperti adattabili senza riscriverli.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 5.1 | Pianificazione dello sprint 1 | `lez01_pianificazione_sprint_1/` |
| 5.2 | Sviluppo con branch e test | `lez02_sviluppo_con_branch_e_test/` |
| 5.3 | Integrazione e daily scrum | `lez03_integrazione_e_daily_scrum/` |
| 5.4 | Revisione e retrospettiva dello sprint 1 | `lez04_revisione_e_retrospettiva_1/` |
| 5.5 | Qualità: test e debugging | `lez05_qualita_test_e_debugging/` |
| 5.6 | Pianificazione dello sprint 2 | `lez06_pianificazione_sprint_2/` |
| 5.7 | Sviluppo e integrazione dello sprint 2 | `lez07_sviluppo_e_integrazione_sprint_2/` |
| 5.8 | Revisione e retrospettiva dello sprint 2 | `lez08_revisione_e_retrospettiva_2/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Materiali e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 5.1 | `pianifica_sprint.py`, `test_pianifica_sprint.py`, `backlog_esempio.md`, `definizione_di_fatto.md` | 10 test superati su 10: lettura di priorità, stime e criteri; storie già fatte, senza stima, senza criteri, inesistenti; capacità superata; storie Must escluse; file dello sprint scritto solo senza problemi da sistemare. Il backlog di esempio supera `controlla_storie.py` (modulo 2) per le storie con criteri |
| 5.2 | `criteri_in_test.py`, `test_criteri_in_test.py`; `soluzioni_docente/` (logica, comandi, test e dati per US-01, US-02, US-03) | 11 test superati su 11: divisione dei criteri, varianti Data e Allora, virgolette nei criteri, scheletro valido che fallisce finché non viene scritto, nessuna sovrascrittura. Soluzione copiata in una copia del kit: 43 test superati; comandi `giorno` e `cancella` provati nel terminale |
| 5.3 | `burndown.py`, `test_burndown.py`, `registro_daily_scrum.md` | 11 test superati su 11: punti rimanenti dal backlog e dallo sprint, linea ideale, grafico Mermaid (visualizzato in Chromium), registrazione, errori |
| 5.4 | `metriche_sprint.py`, `test_metriche_sprint.py`, `scaletta_revisione.md`, `retrospettiva.md` | 12 test superati su 12: chiusura dello sprint con risultato registrato, stime della pianificazione, sprint già chiuso, confronto tra sprint con risultati invariati dopo le modifiche del backlog |
| 5.5 | `kit_con_difetti/` (con `.vscode/launch.json` e `dati_prova/`), `segnalazioni_utenti.md`, `copertura.py`, `test_copertura.py`, `test_esercizio_difetti.py`, `soluzioni_docente.md` | copertura: 8 test superati su 8; esercizio: 11 controlli superati su 11 (sei difetti riproducibili, 22 test verdi nel kit con difetti, con le correzioni i file tornano identici al kit e passano i 27 test originali) |
| 5.6 | `richiesta_cliente_sprint2.md`, `analisi_impatto.md`; `soluzioni_docente/` (US-16, ore di lezione) | soluzione: 6 test superati su 6; comando `prenota-ore` integrato nella soluzione dello sprint 1 e provato nel terminale (prenotazione, sovrapposizione, ora non valida), 43 test del progetto superati |
| 5.7 | `debito_tecnico.py`, `test_debito_tecnico.py` | 12 test superati su 12: docstring mancanti (escluse le funzioni interne), lunghezza, parametri, TODO e FIXME, esclusione di test e cartelle nascoste, registro Markdown, errori di sintassi, analisi del kit (4 segnali) |
| 5.8 | `confronto_sprint.md` | usa gli script delle lezioni 5.3 e 5.4; esempio di confronto verificato |

## Note per il docente

- **Sessioni**: le otto lezioni si svolgono a coppie (5.1+5.2, 5.3+5.4, 5.5+5.6, 5.7+5.8). Conviene distribuire tutte le cartelle `laboratorio` del modulo all'inizio, in `C:\corso-impresa\lab51` ... `lab58`, perché gli script di una lezione si usano anche nelle successive (per esempio `burndown.py` dalla 5.1).
- **Lavoro a casa**: facoltativo e concordato nel team; la pianificazione deve essere realistica per il tempo in classe.
- **Soluzioni**: `lez02_.../laboratorio/soluzioni_docente/` (sprint 1) e `lez06_.../laboratorio/soluzioni_docente/` (richiesta di modifica) sono per il docente: servono a confrontare le soluzioni dei team o ad aiutare un team bloccato, non vanno distribuite prima delle revisioni.
- **Un test del kit che si rompe**: con US-01, il test del kit `test_id_successivo_al_massimo` fallisce perché usa prenotazioni incomplete. È una situazione istruttiva, spiegata in `soluzioni_docente/LEGGIMI.md` della lezione 5.2 e richiamata nella lezione.
- **Lezione 5.5**: la cartella `kit_con_difetti` si distribuisce così com'è; `soluzioni_docente.md` e `test_esercizio_difetti.py` sono per il docente. Le configurazioni di debug usano la cartella `dati_prova`, così le prove non modificano i dati di esempio.
- **Lezione 5.6**: la richiesta di modifica è il requisito "nascosto" della scheda del cliente (lezione 2.1). Se un team l'aveva già scoperta nell'intervista, la storia è già nel backlog: l'analisi di impatto si fa comunque, su un'altra richiesta scelta dal docente (per esempio la capienza, US-10).
- **Numeri degli esempi**: gli output di esempio delle lezioni (velocità 7, capacità 6...) vengono dal team di fantasia del backlog di esempio; i team avranno numeri diversi.
