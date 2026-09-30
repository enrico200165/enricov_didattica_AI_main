---
title: "Modulo 6: Monitoraggio e risposta agli incidenti"
subtitle: "Cybersecurity ed Ethical Hacking"
lang: it
---

# Modulo 6: Monitoraggio e risposta agli incidenti

Durata: 4 ore (lezioni 6.1-6.4).

Obiettivi del modulo:

- spiegare che cosa registrare e perché, e leggere i registri eventi di Windows
- descrivere l'organizzazione del monitoraggio della sicurezza (SOC, SIEM) e il problema dei falsi positivi
- analizzare con uno script Python il registro degli eventi di un'applicazione e conoscere gli indicatori delle principali anomalie
- riconoscere tecniche e segnali dell'ingegneria sociale e del phishing, e verificare le intestazioni di un'email
- descrivere le fasi della risposta agli incidenti e gli obblighi di notifica, e applicarle in un'esercitazione a tavolino

Prerequisiti: moduli 1-5; in particolare la bacheca del laboratorio 5.4 (lezione 6.2), MFA (lezione 2.3), HTTPS e certificati (lezione 3.3).

Fonti: contenuto originale, salvo la sezione 6.1.4, che adatta le lezioni "SecOps key concepts" e "SecOps capabilities" di Microsoft "Security-101" (licenza CC0). Riferimenti verificati a settembre 2026: documentazione Microsoft (Get-WinEvent, evento 4625), catalogo MITRE ATT&CK, OWASP Cheat Sheet Series, NIST SP 800-61r3, progetto No More Ransom, Wikipedia (GDPR, SPF, DKIM, DMARC), sintesi degli obblighi NIS2 di Legiscope.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 6.1 | Log e monitoraggio | `lez01_log_e_monitoraggio/` |
| 6.2 | Laboratorio: analisi di log | `lez02_lab_analisi_log/` |
| 6.3 | Phishing e ingegneria sociale | `lez03_phishing_e_ingegneria_sociale/` |
| 6.4 | Risposta agli incidenti | `lez04_risposta_agli_incidenti/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`, `materiali` o `esercitazione`.

## Laboratori e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 6.1 | `sessioni_pc.py`, `eventi_esempio.csv`, `test_sessioni_pc.py` | 7 test superati su 7 |
| 6.2 | `bacheca.py`, `analizza_log.py`, `test_analizza_log.py` | 13 test superati su 13, compresa l'analisi di un registro prodotto davvero dalla bacheca |
| 6.3 | `messaggi_esempio.md`, `email_sospetta.eml`, `email_legittima.eml`, `analizza_email.py`, `test_analizza_email.py`, `soluzioni_docente.md` | 10 test superati su 10 |
| 6.4 | `scenario_ransomware.md`, `guida_docente.md` | scenario e guida confrontati con le fasi e gli obblighi di notifica della lezione |

Note per il docente:

- nella lezione 6.2 le anomalie (tentativi ripetuti di accesso, password spraying, credential stuffing, ricerca di pagine, cancellazione dei log) sono trattate a livello concettuale, con indicatori, contromisure e collegamenti alle schede MITRE ATT&CK e alle guide OWASP; la parte pratica usa i registri prodotti dagli studenti con il proprio uso della bacheca sul proprio PC, compresi alcuni errori di password fatti di proposito
- tutti i messaggi di esempio della lezione 6.3 riguardano organizzazioni e domini fittizi (dominio riservato `.example`)
- il registro Sicurezza di Windows è leggibile solo con diritti di amministratore: la lezione 6.1 prevede una dimostrazione del docente
- le norme sulle notifiche (GDPR, NIS2) vanno ricondotte, per la scuola, alle decisioni del dirigente e del DPO; la lezione non sostituisce la consulenza del DPO
