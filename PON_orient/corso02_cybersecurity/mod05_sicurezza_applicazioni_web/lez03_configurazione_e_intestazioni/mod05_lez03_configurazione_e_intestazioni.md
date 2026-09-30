---
title: "Lezione 5.3: Configurazione e intestazioni di sicurezza"
subtitle: "Modulo 5: Sicurezza delle applicazioni web. Cybersecurity ed Ethical Hacking"
lang: it
---

# Lezione 5.3: Configurazione e intestazioni di sicurezza

> Contenuto originale. Riferimenti: OWASP HTTP Headers Cheat Sheet; MDN Web Docs (Content Security Policy, Strict-Transport-Security, cookie); pip-audit (Python Packaging Authority). Gli script e i file di esempio sono nella cartella `laboratorio`.

Obiettivo: conoscere le intestazioni HTTP che rafforzano la sicurezza di un sito, gli attributi dei cookie di sessione e la gestione delle dipendenze, e valutare la configurazione di siti reali.

## 5.3.1 Configurazione sicura

Molti incidenti non dipendono da errori nel codice ma dalla **configurazione** (categoria A02): credenziali predefinite non cambiate, funzioni di debug lasciate attive, elenchi dei file delle cartelle visibili, messaggi di errore con dettagli interni, servizi e pagine di amministrazione esposti inutilmente, intestazioni di sicurezza mancanti. Principi:

- **configurazione minima**: solo i componenti e le funzioni necessari
- **ambienti separati**: sviluppo, prova e produzione con impostazioni diverse; il debug solo in sviluppo
- **segreti fuori dal codice**: password e chiavi in variabili d'ambiente o archivi dedicati, mai nel codice sorgente o nel repository
- **configurazione ripetibile e verificata**: impostazioni scritte in file, controllate automaticamente

## 5.3.2 Intestazioni HTTP di sicurezza

Le **intestazioni di risposta** permettono al server di chiedere al browser comportamenti più sicuri. Valori raccomandati dall'OWASP (https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html):

- **Strict-Transport-Security** (HSTS)
  il browser userà solo HTTPS per quel sito per il periodo indicato, senza consentire di ignorare errori di certificato. Valore tipico: `max-age=63072000; includeSubDomains; preload` (due anni). Il browser la ignora se ricevuta in HTTP. Riferimento: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security
- **Content-Security-Policy** (CSP)
  elenca da dove la pagina può caricare script, stili, immagini e altre risorse, e chi può incorporarla in un riquadro. Esempio: `default-src 'self'; frame-ancestors 'none'` consente solo risorse dello stesso sito e vieta l'incorporamento in altre pagine. Una CSP con `'unsafe-inline'` per gli script riduce molto la protezione dal cross-site scripting. Riferimento: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
- **X-Content-Type-Options**: `nosniff`
  il browser rispetta il tipo di contenuto dichiarato dal server, senza "indovinarlo" dal contenuto.
- **frame-ancestors** nella CSP, o la vecchia **X-Frame-Options**: `DENY`
  impediscono che la pagina venga inserita in un riquadro di un altro sito, tecnica usata per indurre l'utente a fare clic su elementi nascosti (clickjacking).
- **Referrer-Policy**: `strict-origin-when-cross-origin`
  limita le informazioni sull'indirizzo di provenienza inviate agli altri siti.
- **Permissions-Policy**, per esempio `geolocation=(), camera=(), microphone=()`
  disattiva funzioni del browser che il sito non usa.

Da evitare:

- **X-XSS-Protection** attiva: intestazione obsoleta, va omessa o impostata a `0`
- **Server** e **X-Powered-By** con prodotto e versione (per esempio `Apache/2.4.29`, `PHP/7.2.24`): danno informazioni utili a chi cerca sistemi vulnerabili

## 5.3.3 Cookie di sessione

Dopo l'accesso, il server riconosce l'utente tramite un **cookie di sessione**. Chi ottiene quel valore può presentarsi come l'utente, senza conoscerne la password. Requisiti:

- **valore casuale e lungo**, generato con un generatore crittografico, senza informazioni sull'utente
- **Secure**: il cookie viaggia solo in HTTPS
- **HttpOnly**: il cookie non è leggibile da JavaScript, e quindi da un eventuale script iniettato
- **SameSite**: `Lax` (predefinito nei browser moderni) o `Strict` limitano l'invio del cookie nelle richieste provenienti da altri siti, riducendo il rischio che un altro sito faccia compiere azioni all'utente a sua insaputa (cross-site request forgery)
- prefisso **`__Host-`** nel nome: il browser accetta il cookie solo se è `Secure`, con `Path=/` e senza `Domain`
- **scadenza** della sessione dopo un periodo di inattività, e invalidazione all'uscita

Esempio:

```http
Set-Cookie: __Host-sessione=Zk3x9QbT1wR8mL2pV7cN4sYd0hJ6aE5u; Path=/; Secure; HttpOnly; SameSite=Lax
```

Riferimento: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies

## 5.3.4 Aggiornamenti e dipendenze

Un'applicazione moderna usa decine o centinaia di librerie di terze parti, che a loro volta dipendono da altre librerie. Le vulnerabilità di queste **dipendenze** diventano vulnerabilità dell'applicazione (categoria A03, Software Supply Chain Failures). Pratiche:

- **inventario**: elenco delle dipendenze con le versioni esatte (file come `requirements.txt` per Python, `package-lock.json` per JavaScript); nelle organizzazioni si produce una distinta dei componenti software (SBOM, Software Bill of Materials)
- **analisi automatica**: strumenti che confrontano le versioni usate con le basi di dati delle vulnerabilità note, per esempio `pip-audit` per Python (https://github.com/pypa/pip-audit) e il comando `npm audit` per JavaScript; i servizi di hosting del codice offrono avvisi automatici
- **aggiornamenti** regolari, con test automatici che verificano che l'applicazione funzioni ancora
- **provenienza**: pacchetti solo da archivi ufficiali, con attenzione a nomi simili a quelli di librerie note, e verifica dell'integrità (lezione 3.2)

## 5.3.5 Laboratorio

Tempo indicativo: 50 minuti. Cartella di lavoro `C:\corso-cyber\lab53`, con i file della cartella `laboratorio`.

### Parte 1: intestazioni di siti reali con i DevTools

1. Aprire un sito, premere `F12` e scegliere la scheda **Rete** (Network); ricaricare la pagina.
2. Selezionare la prima richiesta, quella del documento HTML, e nella scheda **Intestazioni** (Headers) individuare le **intestazioni di risposta**.
3. Attivare la visualizzazione in formato grezzo (interruttore **Raw**), copiare le intestazioni di risposta e incollarle in un file di testo, per esempio `sito1.txt`.
4. Nella scheda **Applicazione** (Chrome, Edge) o **Archiviazione** (Firefox), sezione Cookie, osservare gli attributi dei cookie del sito.

Ripetere per almeno tre siti: il sito della scuola, un sito della pubblica amministrazione, un sito scelto dallo studente. Si tratta di normale navigazione: si osserva ciò che ogni browser riceve.

### Parte 2: valutazione con Python

```powershell
python controlla_intestazioni.py sito1.txt
python controlla_intestazioni.py esempio_configurazione_debole.txt
```

```text
ATTENZIONE  Strict-Transport-Security        max-age inferiore a un anno: max-age=3600
MANCA       Content-Security-Policy          nessuna limitazione alle risorse caricabili
MANCA       X-Content-Type-Options           valore atteso: nosniff
MANCA       Protezione dall'incorniciamento  né frame-ancestors nella CSP né X-Frame-Options
MANCA       Referrer-Policy                  valore suggerito: strict-origin-when-cross-origin
ATTENZIONE  X-XSS-Protection                 intestazione obsoleta: va omessa o impostata a 0
ATTENZIONE  Server                           rivela prodotto e versione: Apache/2.4.29 (Ubuntu)
ATTENZIONE  X-Powered-By                     rivela prodotto e versione: PHP/7.2.24
ATTENZIONE  Cookie PHPSESSID                 attributi mancanti: secure, httponly, samesite

OK: 0, ATTENZIONE: 5, MANCA: 4
```

Lo script accetta sia il formato `Nome: valore` sia quello a righe alternate prodotto copiando l'elenco non grezzo di Chrome (`esempio_formato_chrome.txt`). Con l'opzione `--url` esegue esso stesso la richiesta, come farebbe il browser:

```powershell
python controlla_intestazioni.py --url https://www.example.org/
```

Test: `python test_controlla_intestazioni.py` (13 test, compresa una prova con `--url` su un server avviato sul proprio PC).

Domande:

1. Quali intestazioni sono presenti in tutti i siti analizzati, e quali mancano più spesso?
2. Un'intestazione mancante è sempre un problema? Per esempio, che cosa cambia tra una pagina informativa statica e un'applicazione con accesso?
3. Con `--url http://127.0.0.1:8000/` sull'applicazione del laboratorio 5.4, perché HSTS risulta mancante, ed è corretto che sia così?

### Parte 3: dipendenze vulnerabili

Richiede Python 3.10 o successivo e la connessione a Internet.

```powershell
python -m pip install --user pip-audit
python -m pip_audit -r requisiti_esempio.txt
```

Il file `requisiti_esempio.txt` indica versioni del 2018 di due librerie molto diffuse. Il risultato elenca per ogni vulnerabilità nota il pacchetto, la versione, l'identificativo e le versioni che la correggono; sono comprese anche le dipendenze indirette. Alla verifica di settembre 2026 le vulnerabilità segnalate erano 48, in 4 pacchetti: il numero cresce nel tempo, man mano che se ne scoprono di nuove.

```text
Found 48 known vulnerabilities in 4 packages
Name     Version ID              Fix Versions
-------- ------- --------------- -------------
requests 2.19.1  PYSEC-2018-28   2.20.0
...
```

Domande: quali pacchetti non compaiono nel file ma risultano vulnerabili, e perché? Come si decide a quale versione aggiornare?

## 5.3.6 Aspetti orientativi (discussione)

- La configurazione sicura dei server e delle piattaforme cloud è un'attività quotidiana di sistemisti, DevOps engineer e specialisti di sicurezza del cloud.
- La sicurezza della catena di fornitura del software è diventata una priorità dopo incidenti che hanno colpito migliaia di organizzazioni attraverso un solo componente compromesso; esistono ruoli dedicati alla gestione delle dipendenze e dei rilasci.
- Domanda: perché un'organizzazione dovrebbe conoscere l'elenco completo dei componenti software che usa, anche quelli che non ha scelto direttamente?
