---
title: "Modulo 5: Sicurezza delle applicazioni web"
subtitle: "Cybersecurity ed Ethical Hacking"
lang: it
---

# Modulo 5: Sicurezza delle applicazioni web

Durata: 4 ore (lezioni 5.1-5.4); il laboratorio 5.4 può occupare due unità se il calendario lo consente.

Obiettivi del modulo:

- spiegare come errori di progettazione e di programmazione diventano vulnerabilità, e classificarle con la OWASP Top 10:2025
- trattare i dati non fidati con validazione, query parametriche e codifica dell'output, in Python e in JavaScript
- valutare intestazioni di sicurezza, cookie di sessione e dipendenze di un'applicazione
- eseguire una revisione del codice orientata alla sicurezza e correggere un'applicazione, verificandola con test automatici

Prerequisiti: moduli 1-4 (in particolare hashing delle password, lezione 2.2; HTTPS, lezione 3.3; servizi in ascolto, lezione 4.1); basi di Python e di JavaScript (corso 1 o equivalente).

Fonti: OWASP Top 10:2025 (OWASP Foundation, licenza CC BY 3.0), riassunta e tradotta nella lezione 5.1; Microsoft "Security-101", lezione "AppSec key concepts" (licenza CC0), adattata nella sezione 5.1.2; per il resto contenuto originale. Riferimenti verificati a settembre 2026: OWASP Cheat Sheet Series (SQL Injection Prevention, Cross Site Scripting Prevention, HTTP Headers), OWASP Code Review Guide, MDN Web Docs, documentazione di Python, pip-audit.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 5.1 | OWASP Top 10 | `lez01_owasp_top10/` |
| 5.2 | Validazione degli input | `lez02_validazione_degli_input/` |
| 5.3 | Configurazione e intestazioni di sicurezza | `lez03_configurazione_e_intestazioni/` |
| 5.4 | Laboratorio: correzione di codice vulnerabile | `lez04_lab_correzione_codice/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `attivita` (lezione 5.1) o `laboratorio`. Le soluzioni per il docente sono nei file e nelle cartelle con `docente` nel nome.

## Laboratori e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 5.1 | `attivita/casi.md`, `attivita/soluzioni_docente.md` | classificazione confrontata con le descrizioni ufficiali delle categorie 2025 |
| 5.2 | `registro.py`, `test_registro.py`; `commenti.js`, `commenti.html`, `test_commenti.html`; `soluzione_docente/` | Python: versione da correggere 8 test su 19, soluzione 19 su 19; JavaScript, eseguito in Chromium: versione da correggere 4 su 9, soluzione 9 su 9 |
| 5.3 | `controlla_intestazioni.py`, `test_controlla_intestazioni.py`, tre file di esempio, `requisiti_esempio.txt` | 13 test superati su 13; `--url` provato su un server locale e sull'applicazione della lezione 5.4; `pip-audit` eseguito su `requisiti_esempio.txt` |
| 5.4 | `app_da_correggere/bacheca.py`, `test_bacheca.py`; `soluzione_docente/bacheca.py`, `problemi_trovati.md` | versione da correggere 4 test su 21, soluzione 21 su 21; soluzione provata anche nel browser (accesso, pubblicazione, eliminazione, codifica del testo) |

Note per il docente:

- tutti i test usano solo dati legittimi (cognomi con apostrofo, testi con simboli `<` e `>`, tentativi di eliminare annunci altrui con un secondo account di prova): i difetti emergono con l'uso normale, senza costruire dati di attacco
- le applicazioni ascoltano solo su `127.0.0.1` e usano database locali creati al momento
- l'analisi delle intestazioni riguarda ciò che ogni browser riceve visitando un sito; non richiede strumenti di scansione
- la parte 3 della lezione 5.3 richiede Python 3.10 o successivo e l'accesso a PyPI per installare `pip-audit`; il numero di vulnerabilità segnalate cambia nel tempo
