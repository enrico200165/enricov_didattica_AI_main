---
title: "Modulo 7: Dati, privacy e continuità"
subtitle: "Cybersecurity ed Ethical Hacking"
lang: it
---

# Modulo 7: Dati, privacy e continuità

Durata: 3 ore (lezioni 7.1-7.3).

Obiettivi del modulo:

- conoscere definizioni, principi, basi giuridiche e diritti previsti dal GDPR, e analizzare un'informativa privacy
- classificare i dati per sensibilità e scegliere le misure di protezione dei dati a riposo
- applicare minimizzazione, pseudonimizzazione e generalizzazione a un file di dati, valutando il rischio di riconoscimento
- progettare una strategia di backup secondo la regola 3-2-1 e verificarla con una prova di ripristino

Prerequisiti: moduli 1-6; in particolare cifratura e HMAC (modulo 3), impronte SHA-256 (lezione 3.2), violazioni dei dati e ransomware (lezione 6.4).

Fonti: contenuto originale, salvo la sezione 7.2.1, che adatta la lezione "Data security key concepts" di Microsoft "Security-101" (licenza CC0). Riferimenti verificati a settembre 2026: testo del GDPR su EUR-Lex, Wikipedia, documentazione Microsoft sulla crittografia del dispositivo, siti di VeraCrypt e 7-Zip.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 7.1 | GDPR e dati personali | `lez01_gdpr_e_dati_personali/` |
| 7.2 | Classificazione e protezione dei dati | `lez02_classificazione_e_protezione_dati/` |
| 7.3 | Backup e continuità | `lez03_backup_e_continuita/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `attivita` o `laboratorio`.

## Laboratori e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 7.1 | `attivita/scheda_informativa.md` | scheda confrontata con gli articoli 13 e 14 del GDPR (contenuto delle informative) |
| 7.2 | `pseudonimizza.py`, `studenti_fittizi.csv`, `test_pseudonimizza.py` | 12 test superati su 12 |
| 7.3 | `backup.py`, `test_backup.py`, `piano_backup.md`, `soluzione_docente.md` | 10 test superati su 10; creazione, verifica e ripristino provati anche da riga di comando |

Note per il docente:

- `studenti_fittizi.csv` contiene 40 studenti inventati, con nomi e cognomi scelti a caso da elenchi di nomi comuni, matricole fittizie e indirizzi email sul dominio riservato `scuola.example`
- nella lezione 7.1 gli studenti analizzano l'informativa di un servizio che usano, senza modificare impostazioni né condividere dati personali
- la lezione 7.1 presenta i concetti essenziali del GDPR e non sostituisce le indicazioni del DPO della scuola
