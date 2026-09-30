---
title: "Lezione 5.1: soluzioni dei casi"
subtitle: "Modulo 5: Sicurezza delle applicazioni web. Materiale per il docente"
lang: it
---

# Lezione 5.1: soluzioni dei casi

| Caso | Categoria | Proprietà | Contromisura |
|---|---|---|---|
| 1 | A01 Broken Access Control | riservatezza | il server verifica che lo studente autenticato possa vedere quei voti; l'identificativo nell'indirizzo non è una prova di autorizzazione |
| 2 | A02 Security Misconfiguration; anche A10 | riservatezza | messaggi di errore generici per l'utente, dettagli solo nei log; modalità di debug disattivata in produzione |
| 3 | A04 Cryptographic Failures | riservatezza | hash lento con sale (Argon2id, scrypt, PBKDF2); accessi al database limitati e registrati |
| 4 | A03 Software Supply Chain Failures | riservatezza, integrità, disponibilità | inventario delle dipendenze; analisi automatica (pip-audit, npm audit); aggiornamenti pianificati |
| 5 | A05 Injection | riservatezza e integrità (potenzialmente) | query parametriche; il difetto emerge già con dati legittimi |
| 6 | A05 Injection (cross-site scripting) | integrità, riservatezza | codifica dell'output per il contesto HTML; `textContent` in JavaScript; Content-Security-Policy |
| 7 | A06 Insecure Design; anche A07 | riservatezza, integrità | recupero con collegamento monouso inviato all'indirizzo registrato, con scadenza breve; MFA |
| 8 | A07 Authentication Failures | riservatezza | lunghezza minima di 15 caratteri o MFA; limiti e ritardi crescenti dopo gli errori; avvisi (lezione 2.1) |
| 9 | A08 Software or Data Integrity Failures | integrità | verifica della firma digitale dell'aggiornamento prima dell'esecuzione (lezione 3.2) |
| 10 | A09 Security Logging and Alerting Failures | tutte, indirettamente | registrazione di accessi, errori e operazioni sensibili; allarmi; conservazione dei log (modulo 6) |
| 11 | A10 Mishandling of Exceptional Conditions; anche A01 | integrità, riservatezza | in caso di errore l'operazione va negata ("fallire in modo sicuro"); test sui casi di errore |
| 12 | A02 Security Misconfiguration; anche A07 | tutte | cambio delle credenziali predefinite; pannello raggiungibile solo dalla rete interna o tramite VPN; MFA |

Spunto per la discussione finale: i casi 7 e 9 sono soprattutto di progettazione (servono scelte diverse prima di scrivere il codice); i casi 5, 6 e 11 sono errori di programmazione; i casi 2, 4 e 12 riguardano la gestione del sistema in esercizio.
