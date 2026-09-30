---
title: "Modulo 1: Progetti e team"
subtitle: "Informatica per l'Impresa e Soft Skills Digitale"
lang: it
---

# Modulo 1: Progetti e team

Durata: 3 ore (lezioni 1.1-1.3).

Obiettivi del modulo:

- distinguere un progetto da un'attività ripetitiva e riconoscerne obiettivi, vincoli e portatori di interesse
- individuare le cause di fallimento dei progetti a partire da casi reali
- conoscere le condizioni di un team efficace, le regole di comunicazione, riunioni, decisioni e gestione dei conflitti
- formare i team e scriverne l'accordo
- conoscere il prodotto del progetto, verificare gli strumenti, avviare il kit di partenza e i suoi test, assegnare i ruoli

Prerequisiti: nessuno oltre a quelli del corso.

Fonti: contenuto originale. Riferimenti verificati a settembre 2026: Wikipedia (Project management, Legge di Brooks, Mars Climate Orbiter, HealthCare.gov, Tuckman's stages of group development, Psychological safety, Thomas-Kilmann Conflict Mode Instrument); documentazione di Visual Studio Code e di Python; Pro Git (CC BY-NC-SA 3.0). Verifica sull'esistenza di materiali open source riutilizzabili: non sono stati trovati materiali aperti in italiano sugli stessi contenuti con un livello adatto; le lezioni sono quindi originali.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 1.1 | Che cos'è un progetto informatico | `lez01_che_cos_e_un_progetto_informatico/` |
| 1.2 | Lavorare in team | `lez02_lavorare_in_team/` |
| 1.3 | Kit di progetto e squadre | `lez03_kit_di_progetto_e_squadre/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Materiali e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 1.1 | `casi_di_studio.md`, `mappa_portatori.md`, `soluzioni_docente.md` | diagramma Mermaid della mappa controllato con il motore di Mermaid |
| 1.2 | `accordo_di_team.md`, `accordo_esempio.md`, `controlla_accordo.py`, `test_controlla_accordo.py` | 12 test superati su 12: accordo completo, modello vuoto, sezione mancante o vuota, numero di membri, posta e telefono segnalati, date e orari non scambiati per numeri di telefono, codici di uscita |
| 1.3 | `kit_prenotazioni/` (kit di partenza del progetto), `verifica_ambiente.py`, `test_verifica_ambiente.py` | kit: 27 test `unittest` superati su 27 (regole, archivio, riga di comando); verifica dell'ambiente: 14 test superati su 14 |

## Il kit di partenza

Il kit `lez03_kit_di_progetto_e_squadre/laboratorio/kit_prenotazioni/` è la base del progetto per tutto il corso:

- applicazione Python a riga di comando, solo libreria standard: `prenotazioni.py`, `logica.py`, `archivio.py`
- dati di fantasia in `dati/aule.json` (8 aule) e `dati/prenotazioni.json` (5 prenotazioni, di cui due sovrapposte per mostrare il difetto della storia US-01)
- 27 test in `tests/`, eseguibili con `python -m unittest`
- `docs/backlog.md` con 15 storie utente (US-01...US-15); solo US-01 e US-02 hanno i criteri di accettazione, gli altri si scrivono nella lezione 2.2
- `docs/board.md` con la board Kanban in Mermaid e la tabella equivalente
- `README.md`, `CHANGELOG.md` nel formato Keep a Changelog, `.gitignore`

## Note per il docente

- **Formazione dei team**: i team si formano all'inizio del laboratorio 1.2, perché l'accordo di team si scrive nel team definitivo; nella lezione 1.3 si assegnano i ruoli per i due sprint. Rispetto al syllabus del 30/09/2026 ore 21:25, la formazione dei team passa dalla 1.3 alla 1.2 (syllabus aggiornato: versione del 30/09/2026 ore 21:50).
- Criteri suggeriti per i team: 4-5 studenti, classi e competenze di programmazione miste, almeno due studenti a proprio agio con Python per team.
- **Lezione 1.3**: conviene preparare i PC in anticipo (file `000_syllabus_info/corso04_00_info_avvertenze_2026-09-30_2125.md`), in modo che la lezione serva a verificare e non a installare. Lo script `verifica_ambiente.py` indica esattamente che cosa manca.
- Nella lezione 1.3 gli studenti aggiungono prenotazioni al file dei dati: il kit originale va conservato dal docente e ridistribuito pulito prima della lezione 4.1, in cui entra nel repository di ciascun team.
- I messaggi di aiuto generati automaticamente da `argparse` sono in parte in inglese; è voluto, ed è la storia US-14.
- L'accordo di team resta un file dello studente fino alla lezione 4.3, quando entra nel repository del team. Per i canali di comunicazione fuori dal corso è opportuno indicare gli strumenti previsti dalla scuola.
- Soluzioni della lezione 1.1 in `lez01_che_cos_e_un_progetto_informatico/laboratorio/soluzioni_docente.md`.
