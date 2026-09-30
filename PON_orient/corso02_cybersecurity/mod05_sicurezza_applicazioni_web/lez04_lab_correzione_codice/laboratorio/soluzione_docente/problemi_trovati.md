---
title: "Lezione 5.4: problemi della bacheca"
subtitle: "Modulo 5: Sicurezza delle applicazioni web. Materiale per il docente"
lang: it
---

# Lezione 5.4: problemi della bacheca

Elenco dei problemi di `app_da_correggere/bacheca.py` e della correzione applicata in `soluzione_docente/bacheca.py`, dove ogni modifica è segnata da un commento `CORREZIONE`. Con la soluzione, `test_bacheca.py` dà 21 test superati su 21; con la versione da correggere 4 su 21.

| N. | Funzione | Problema | Categoria | Correzione |
|---|---|---|---|---|
| 1 | `inizializza`, `verifica_login`, `crea_annuncio`, `cerca_annunci`, `elimina_annuncio` | query composte concatenando i dati: errori con gli apostrofi, possibile alterazione delle query | A05 | query parametriche con `?` |
| 2 | `elenco_html`, `pagina` | titoli, testi, autori e parola cercata inseriti nell'HTML senza codifica | A05 (XSS) | `html.escape` su ogni valore |
| 3 | `inizializza`, `verifica_login` | password salvate e confrontate in chiaro | A04, A07 | PBKDF2-HMAC-SHA256 con sale, 600.000 iterazioni; confronto con `hmac.compare_digest` |
| 4 | `applicazione`, `/login` | il cookie contiene il nome utente: chiunque può costruirlo a mano | A07 | identificativo casuale (`secrets.token_urlsafe(32)`) conservato nella tabella `sessioni` |
| 5 | `/login` | cookie senza `HttpOnly` e `SameSite` | A07, A02 | `HttpOnly; SameSite=Lax` (e `Secure` con HTTPS) |
| 6 | `/elimina` | nessun controllo di accesso né del proprietario dell'annuncio | A01 | accesso obbligatorio (401); cancellazione solo dell'autore (403 negli altri casi) |
| 7 | `/elimina` | identificativo non validato: un valore non numerico produce un'eccezione | A10 | controllo con `isdigit`, risposta 400 |
| 8 | `applicazione`, blocco `except` | la risposta di errore mostra il `traceback` con percorsi e codice | A02, A10 | messaggio generico; dettagli nel log con `logging.exception` |
| 9 | tutte le risposte | intestazioni di sicurezza assenti | A02 | `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy` |
| 10 | tutta l'applicazione | nessuna registrazione di accessi, accessi falliti, operazioni negate | A09 | eventi scritti in `bacheca.log` |
| 11 | `crea_annuncio`, `leggi_modulo` | nessun limite di lunghezza dei dati | A10, disponibilità | titolo 1-100 caratteri, testo massimo 1000, richiesta massimo 10.000 byte |
| 12 | `verifica_login` | tempi di risposta diversi per utente inesistente e password errata | A07 | calcolo dell'hash anche per utenti inesistenti |

Problemi non corretti nemmeno nella soluzione, da discutere con la classe: sezione 5.4.4 della lezione.
