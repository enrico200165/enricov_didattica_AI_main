---
title: "Modulo 4: Strumenti del team"
subtitle: "Informatica per l'Impresa e Soft Skills Digitale"
lang: it
---

# Modulo 4: Strumenti del team

Durata: 4 ore (lezioni 4.1-4.4).

Obiettivi del modulo:

- usare Git per registrare la storia di un progetto con commit ben descritti, dal terminale e da VS Code
- lavorare su rami, integrarli e risolvere i conflitti con l'editor a tre vie di VS Code
- condividere il lavoro del team con un repository comune (`clone`, `pull`, `push`) e rivedere il codice di un compagno
- tenere nel repository documentazione, CHANGELOG, board e segnalazioni di difetti

Prerequisiti: moduli 1-3 (copia di riferimento del progetto con i documenti dei moduli 2 e 3).

Fonti: contenuto originale, salvo `lez03_repository_condiviso_e_revisione/laboratorio/lista_revisione_codice.md`, adattamento di Google, "What to look for in a code review" (licenza CC BY 3.0; l'adattamento mantiene la stessa licenza). Riferimenti verificati a settembre 2026: Pro Git (CC BY-NC-SA 3.0; i capitoli 2, 3 e 4 della versione italiana del sito sono in inglese); documentazione di Git (gitignore); Visual Studio Code (controllo del codice sorgente, conflitti); Chris Beams, regole per i messaggi di commit; Keep a Changelog 1.1.0; documentazione di Mermaid. Verifica sull'esistenza di materiali open source riutilizzabili: Pro Git è il riferimento principale, ma la traduzione italiana di questi capitoli è incompleta e la licenza non commerciale ne consiglia solo la citazione; le lezioni sono quindi originali.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 4.1 | Git, repository e commit | `lez01_git_repository_e_commit/` |
| 4.2 | Branch, merge e conflitti | `lez02_branch_merge_e_conflitti/` |
| 4.3 | Repository condiviso e revisione | `lez03_repository_condiviso_e_revisione/` |
| 4.4 | Documentazione e board | `lez04_documentazione_e_board/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Materiali e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 4.1 | `controlla_repository.py`, `test_controlla_repository.py` | 17 test superati su 17, con repository Git reali creati in cartelle temporanee: messaggi di commit (generici, lunghezza, punto finale, maiuscola, riga vuota), cartella non repository, repository senza commit, repository in ordine, .gitignore mancante o incompleto, file generati registrati, modifiche non registrate, messaggi di merge ignorati; flusso della lezione provato sul kit |
| 4.2 | `prepara_conflitto.py`, `controlla_conflitti.py`, `test_conflitti.py` | 12 test superati su 12: rami creati, conflitto reale in due file, marcatori segnalati una volta per file, risoluzione corretta (4 test), marcatori tolti con codice rovinato, risoluzione sbagliata non rilevabile dal programma, cartella non vuota rifiutata |
| 4.3 | `crea_repository_condivisi.py`, `prima_del_push.py`, `test_repository_condiviso.py`, `lista_revisione_codice.md` | 13 test superati su 13, simulando repository condiviso e due membri del team: creazione dei repository, primo invio, clone, modifiche non registrate, pronto per l'invio, ramo indietro rispetto al condiviso, test che falliscono, marcatori registrati, repository non raggiungibile; flusso della lezione provato sul kit (27 test del kit superati) |
| 4.4 | `genera_board.py`, `test_genera_board.py`, `modello_segnalazione_difetto.md`, `esempio_segnalazione_difetto.md`, `modello_manuale_utente.md` | 17 test superati su 17: lettura di stato e persona, storie Won't escluse, metadati Mermaid, apostrofi, limiti di lavoro in corso, stati non validi; board generata controllata con il motore di Mermaid e visualizzata in Chromium |

## Note per il docente

- **Prima della lezione 4.3** il docente crea i repository condivisi con `crea_repository_condivisi.py`, nella cartella di rete o su chiavette, e prova clone e push da un PC degli studenti. Con le cartelle di rete Git può segnalare "detected dubious ownership": il messaggio indica il comando `safe.directory` da eseguire (file `000_syllabus_info/corso04_00_info_avvertenze_2026-09-30_2125.md`).
- **Lezione 4.1, dati puliti**: prima del primo commit del repository del team si sostituisce `dati/prenotazioni.json` con quello del kit originale; si aggiunge `*.bak` al `.gitignore`, perché gli strumenti delle lezioni 2.3 e 3.3 creano copie `.bak` del backlog.
- **Git in italiano o in inglese**: i messaggi di Git per Windows possono comparire in una delle due lingue secondo la configurazione del sistema; gli esempi della lezione sono in inglese.
- **Ramo principale**: `git init -b main` richiede Git 2.28 o successivo; la versione portatile consigliata nel syllabus è più recente.
- **Test con Git**: i test delle lezioni 4.1-4.3 creano repository in cartelle temporanee e richiedono Git nel PATH; su Windows le cartelle temporanee vengono cancellate ignorando eventuali errori sui file in sola lettura di Git.
- **Lezione 4.2, riflessione**: la parte 2 punto 6 mostra che una risoluzione sbagliata dei conflitti (solo la versione corrente) supera tutti i controlli automatici e i test esistenti, ma perde il lavoro di un compagno: è l'argomento per la revisione del codice della lezione 4.3.
- **Lezione 4.4**: il kit usa nel CHANGELOG le etichette italiane (Non rilasciato, Aggiunto...) mentre il formato originale usa quelle inglesi; la lezione lo spiega.
