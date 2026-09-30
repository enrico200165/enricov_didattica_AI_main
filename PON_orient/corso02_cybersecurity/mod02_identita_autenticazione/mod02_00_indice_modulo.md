---
title: "Modulo 2: Identità e autenticazione"
subtitle: "Cybersecurity ed Ethical Hacking"
lang: it
---

# Modulo 2: Identità e autenticazione

Durata: 4 ore (lezioni 2.1-2.4).

Obiettivi del modulo:

- distinguere identità, autenticazione e autorizzazione, e i fattori di autenticazione
- valutare la robustezza di password e passphrase con il concetto di entropia, e conoscere le raccomandazioni attuali
- spiegare come un servizio deve conservare le password (sale, funzioni di derivazione lente) e realizzarlo in Python
- spiegare il funzionamento di MFA, codici TOTP e passkey, e usare un gestore di password
- applicare i principi di minimo privilegio, separazione dei compiti e gestione del ciclo di vita degli account

Prerequisiti: modulo 1; Python installato (lezione 2.1).

Fonti: contenuto originale, salvo le sezioni 2.4.1 e 2.4.2, che adattano la lezione "IAM key concepts" di Microsoft "Security-101" (licenza CC0). Riferimenti verificati a settembre 2026: NIST SP 800-63B revisione 4 (agosto 2025), OWASP Password Storage Cheat Sheet, RFC 6238, FIDO Alliance, documentazione di Python, KeePassXC e Microsoft.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 2.1 | Password robuste | `lez01_password_robuste/` |
| 2.2 | Laboratorio: hashing delle password | `lez02_lab_hashing_password/` |
| 2.3 | Autenticazione a più fattori e gestori di password | `lez03_mfa_e_gestori_password/` |
| 2.4 | Account e privilegi | `lez04_account_e_privilegi/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio` con gli script Python.

## Script dei laboratori e verifiche

| Lezione | Script | Verifica eseguita |
|---|---|---|
| 2.1 | `entropia.py` (entropia, generatore con `secrets`) | valori della tabella della lezione ricalcolati; test delle funzioni |
| 2.1 | `password_compromessa.py` (facoltativo, Pwned Passwords con k-anonymity) | logica verificata con una risposta simulata nel formato reale del servizio; si invia solo il prefisso di 5 caratteri. La connessione al servizio non è stata provata dall'ambiente di generazione, che non vi aveva accesso: va provata dal docente prima della lezione |
| 2.2 | `archivio_password.py`, `confronto_hash.py`, `test_archivio_password.py` | 10 test superati su 10 |
| 2.3 | `totp.py`, `test_totp.py` | vettori di prova ufficiali della RFC 6238 superati; risultati coincidenti con la libreria indipendente pyotp |
| 2.4 | `permessi.py`, `test_permessi.py` | 8 test superati su 8; attività di revisione verificate |

Gli script usano solo la libreria standard di Python (versione 3.8 o successiva). Tutte le attività si svolgono su dati e account di prova, secondo le regole del laboratorio sottoscritte nella lezione 1.2.
