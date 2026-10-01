---
title: "Modulo 2 - Password e autenticazione"
subtitle: "B.4 - Cybersicurezza e IA. Traccia docenti"
lang: it
---

# Modulo 2 - Traccia docenti

## Collocazione e finalità del modulo

Il modulo 2 (lezioni L5-L7) è quello con la ricaduta più immediata sul comportamento degli studenti: al termine possono cambiare il modo in cui scelgono, conservano e proteggono le proprie credenziali. Riprende da L3 hash, sale e funzioni lente, e da L4 gli infostealer; prepara L8, dove il phishing con inoltro in tempo reale spiega perché servono metodi resistenti al phishing.

Segmento di traccia docenti in aula: 10-15 minuti al termine di L7, su gestione degli account personali degli studenti, politiche della scuola sulle credenziali, esercizi ponte con B.8.

## Logica della progettazione

### Attacchi come meccanismi, laboratori dal lato del difensore

Le famiglie di attacco alle password sono presentate a livello di meccanismo: che cosa sfruttano (abitudini umane, riuso, assenza di limiti fuori linea) e perché certe password cadono. Il corso non mostra strumenti di attacco né procedure operative: non servono a scegliere password migliori e non sono adatti a studenti minorenni.

I laboratori adottano il punto di vista di chi gestisce un servizio (controllo delle password alla registrazione in L5, verifica con k-anonimato in L6) o di chi implementa un meccanismo di difesa (TOTP in L7). Lo studente capisce l'attacco osservando quali password il difensore deve rifiutare e perché.

### L5: l'entropia vale solo per password casuali

Il concetto chiave della lezione è la differenza tra entropia teorica e prevedibilità reale. La formula L × log2(N) è utile per ragionare su lunghezza e alfabeto, ma gli studenti tendono ad applicarla a qualunque password ("la mia ha 12 caratteri di ogni tipo, quindi 78 bit"). Il notebook mostra entrambi i lati: prima i numeri della formula, poi la funzione `valuta_password`, che rifiuta password "complesse" costruite con schemi umani.

Le velocità di attacco del notebook sono ordini di grandezza dichiarati come ipotesi. Non vanno presentate come prestazioni di strumenti reali: servono a mostrare che la stessa password può essere robusta o fragile a seconda di come il servizio la conserva.

### L5: IA e password, una posizione misurata

La stampa ha dato ampio spazio a notizie sull'IA che "indovina le password in pochi secondi". La lezione presenta lo stato delle conoscenze senza allarmismi: i modelli generativi addestrati su password trapelate funzionano, ma il loro vantaggio si concentra sulle password scelte da persone, che sono prevedibili anche con i metodi tradizionali. Il messaggio operativo non cambia: password lunghe, casuali, uniche, gestite da un password manager.

### L6: le raccomandazioni NIST contro le regole diffuse

Molti studenti (e molti docenti) conoscono le regole "almeno un simbolo, cambio ogni 90 giorni". La tabella NIST mostra che sono superate e perché. È un'occasione per un tema di metodo: in sicurezza le regole si basano su prove e cambiano quando le prove cambiano. Conviene far leggere direttamente la sezione sulle password del documento NIST (in inglese), almeno i nove punti dell'elenco dei requisiti.

### L7: il concetto di resistenza al phishing

La lezione non si limita a dire "attivate la MFA": distingue i metodi in base a ciò che proteggono. Il diagramma dell'inoltro del codice è il punto centrale: gli studenti capiscono che un codice SMS o TOTP protegge dalla password rubata in una violazione, ma non da un sito falso ben costruito. Le passkey risolvono il problema perché sono legate al dominio, lo stesso concetto di dominio registrato introdotto in L2.

L'implementazione del TOTP con la sola libreria standard dimostra che il meccanismo non è magico: un segreto condiviso, l'ora, un HMAC. La verifica con i valori ufficiali della RFC introduce una pratica professionale: un'implementazione si controlla con dati di prova pubblicati.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L5_robustezza_password.ipynb` | L5 | librerie: standard, matplotlib |
| `L6_passphrase_kanonimato.ipynb` | L6 | solo libreria standard; nessuna connessione di rete |
| `L7_totp.ipynb` | L7 | solo libreria standard |
| KeePassXC portable | L6 | https://keepassxc.org/download/ |

I notebook funzionano in JupyterLite (https://jupyter.org/try-jupyter/lab/) e in WinPython.

### Checklist prima di L6

- scaricare l'archivio ZIP portable di KeePassXC per Windows e verificare che si avvii con l'account degli studenti. Se manca il pacchetto Microsoft Visual C++ Redistributable, KeePassXC non parte: chiedere al tecnico di installarlo una volta su tutte le postazioni, oppure svolgere l'esercizio 1 come dimostrazione
- decidere dove gli studenti salvano l'archivio `laboratorio.kdbx` (cartella personale, chiavetta); ricordare che contiene solo voci fittizie
- verificare che Have I Been Pwned sia raggiungibile dalla rete della scuola

### Checklist prima di L7

- verificare l'orologio delle postazioni: se è sbagliato di più di 30 secondi, il codice del notebook non coincide con quello dell'app
- decidere se gli studenti configurano un'app di autenticazione sul proprio telefono. L'uso del telefono personale va valutato con le regole della scuola; l'app va configurata solo con il segreto di prova del notebook e l'account di prova può essere eliminato dall'app a fine lezione. In alternativa, dimostrazione dal telefono del docente proiettato

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L5 | 25 min: fattori (3), in linea e fuori linea (7), famiglie di attacco e riuso (7), entropia e prevedibilità (8) | 30 min | 5 min |
| L6 | 25 min: NIST (8), passphrase (5), password manager e KeePassXC (7), HIBP e k-anonimato (5) | 30 min | 5 min |
| L7 | 25 min: metodi e punti deboli (7), resistenza al phishing e passkey (10), TOTP e biometria (8) | 25 min | 10-15 min di traccia docenti |

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| "la mia password è sicura perché ha simboli e numeri" | chiedere se segue uno schema (parola + anno + simbolo); mostrare il risultato di `valuta_password` su password analoghe inventate |
| confusione tra entropia teorica e reale | riprendere il diagramma "generata a caso o scelta da una persona" |
| studenti che vogliono verificare le proprie password reali | spiegare perché non si inseriscono password reali in siti o notebook, e che la verifica vera la fanno i password manager |
| "se uso un password manager e lo attaccano perdo tutto" | confrontare il rischio con quello del riuso; l'archivio è cifrato con la password principale; la MFA protegge l'account |
| "la MFA è scomoda" | la si attiva una volta; molti servizi ricordano i dispositivi fidati; le passkey sono più rapide di una password |
| il codice TOTP del notebook non coincide con l'app | verificare l'orologio del PC e del telefono e che il segreto sia stato digitato correttamente |

### Gestione degli account personali degli studenti

Durante il modulo emergono spesso situazioni reali: password condivise con amici, stessa password ovunque, account senza MFA, account compromessi. Indicazioni:

- non chiedere mai di mostrare o dire password, neppure "per aiutare"
- suggerire come compito facoltativo, da svolgere a casa e senza consegna, l'attivazione della MFA sulla casella di posta principale e la revisione delle password riusate
- se uno studente segnala un account compromesso, indicare i passi di L4 (cambiare la password da un dispositivo sicuro, chiudere le sessioni, attivare la MFA, avvisare i contatti) e coinvolgere la famiglia se necessario

### Politiche della scuola

Il modulo offre l'occasione di confrontare le regole sulle credenziali della scuola (registro elettronico, piattaforme didattiche, rete) con le raccomandazioni NIST. Uno dei progetti finali (L17) chiede proprio una proposta di regole per la scuola. Conviene informare in anticipo l'animatore digitale o il referente informatico.

## Considerazioni sugli strumenti per la didattica

### Notebook con codice fornito

Gli studenti di B.4 non sono tenuti a programmare. I notebook sono costruiti con celle già scritte e commentate, domande nelle celle di testo e pochi valori da modificare. Il codice resta visibile e spiegato: chi ha frequentato B.8 può leggerlo e modificarlo, gli altri possono usarlo come strumento. Questa impostazione evita che la difficoltà del linguaggio nasconda il concetto di sicurezza.

Esercizi ponte con B.8:

- scrivere una propria versione di `valuta_password` con una regola aggiuntiva (per esempio rifiutare le password che contengono il nome utente)
- implementare il generatore di passphrase con `random` e con `secrets` e discutere perché il primo non va usato per i segreti
- implementare HOTP e TOTP da zero seguendo la specifica, verificandoli con i valori di prova

### KeePassXC

Punti di forza: archivio locale, nessun account, open source, versione portable. Mostra concretamente come funziona un password manager senza legare gli studenti a un servizio commerciale.

Limiti: interfaccia ricca; la sincronizzazione tra dispositivi è a carico dell'utente. Per l'uso personale molti studenti troveranno più comodo il gestore integrato nel browser o nel sistema del telefono: è una scelta ragionevole, purché con MFA sull'account e password principale robusta.

### Have I Been Pwned

Il servizio è affidabile e ampiamente usato. Due indicazioni didattiche:

- la ricerca per email rivela in quali violazioni compare un indirizzo; farla con l'indirizzo della scuola o con indirizzi personali è una scelta dello studente, da non imporre
- la sezione Passwords va usata solo con password di esempio; la simulazione del notebook L6 spiega il k-anonimato senza bisogno di rete

## Valutazione del modulo

Verifica di modulo (15-20 minuti, individuale):

- classificare cinque password inventate come accettabili o no secondo NIST, con motivazione
- calcolare l'entropia di una password casuale e di una passphrase con elenco di dimensione data
- spiegare con un diagramma perché un codice TOTP non protegge da un sito falso e una passkey sì
- indicare due misure che un servizio deve adottare per proteggere le password degli utenti

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| distingue attacco in linea e fuori linea | L5, esercizio 2 |
| spiega perché una password "complessa" può essere debole | L5, esercizio 3 |
| usa un password manager con password generate | L6, esercizio 1 |
| spiega che cosa conosce il servizio nel k-anonimato | L6, esercizio 3 |
| spiega il funzionamento del TOTP e il limite dei codici | L7, esercizi 1 e 5 |

## Soluzioni degli esercizi

### L5

- Esercizio 1: 8 minuscole valgono 37,6 bit; 12 minuscole 56,4 bit; 8 caratteri di ogni tipo 52,4 bit. Aggiungere quattro caratteri conviene più che ampliare l'alfabeto.
- Esercizio 2: con le ipotesi del notebook, 8 minuscole casuali resistono secoli in linea, mesi fuori linea con funzione lenta, secondi con funzione veloce. La differenza dipende dal servizio: limitazione dei tentativi, funzione di hash, protezione dell'archivio.
- Esercizio 3:
  - `juventus2008`, `Estate2026!`, `Scu0la2026`, `P4ssw0rd!`: troppo corte e costruite con una parola della lista seguita da numeri o simboli; le sostituzioni (`0` al posto di `o`, `4` al posto di `a`) non ingannano il controllo
  - `qwertyuiop`: sequenza della tastiera presente nella lista di blocco
  - `Tr0ub4dor&3`: rifiutata per la lunghezza; è l'esempio della vignetta xkcd "Password Strength" (https://xkcd.com/936/), che confronta una parola con sostituzioni e una passphrase di quattro parole casuali
  - `ilmiocanesichiamaFuffy`: accettata dal controllo automatico, ma è una frase personale prevedibile per chi conosce la persona o ne legge i social. Il controllo non può sapere nulla della vita dell'utente: è il limite di ogni controllo automatico
  - `tavolo-pianeta-muschio-lanterna` e `k7#Qm2!vLp9@xZ4r`: accettate; la prima è una passphrase di quattro parole casuali (32 bit con l'elenco del notebook: accettabile solo con un secondo fattore), la seconda è una password casuale di 16 caratteri
- Esercizio 4: con le parole di contesto, `Galilei2026!!!!!` viene rifiutata. `itis-galilei-roma` e `G4lil3i_laboratorio` vengono accettate: il controllo confronta l'intera password e lo schema "parola + numeri"; le combinazioni di più parole prevedibili sfuggono. È un buon punto di discussione: le parole legate al servizio sono tra le prime che un attaccante prova, e nessuna lista di blocco sostituisce una password generata a caso.

### L6

- Esercizio 2: 4 parole 32 bit, 6 parole 48 bit, 8 parole 64 bit con l'elenco di 256 parole; per superare i 52,4 bit di 8 caratteri di ogni tipo servono 7 parole (56 bit).
- Esercizio 3: il servizio conosce solo i primi 5 caratteri dell'hash; la password è indistinguibile dalle altre centinaia che condividono il prefisso. Più suffissi vengono restituiti, meno informazione ricava il servizio.
- Esercizio 5: 70,5 / 8 = 8,8, quindi 9 parole con l'elenco di 256; 70,5 / 12,9 = 5,5, quindi 6 parole con l'elenco di 7.776. Un elenco più lungo dà più bit per parola.

### L7

- Esercizio 2: i codici calcolati coincidono con quelli della specifica per tutti e cinque gli istanti. Verificare con dati pubblicati garantisce che l'implementazione produca gli stessi codici delle altre implementazioni conformi (app, servizi).
- Esercizio 4: la funzione accetta il codice con uno scarto di 30 secondi (intervallo adiacente); a 60 e 90 secondi lo rifiuta. Con valori vicini al cambio di intervallo il risultato può variare di un intervallo.
- Esercizio 5: chi fotografa il QR ottiene il segreto e può generare tutti i codici futuri, come l'app della vittima. Un sito falso non ha bisogno del segreto: chiede alla vittima il codice corrente e lo inoltra subito al sito vero, entro la sua validità. Le passkey e le chiavi fisiche impediscono l'attacco perché la firma è legata al dominio e sul dominio del sito falso non viene prodotta.

## Materiale open source

Verifica puntuale per L5-L7: le lezioni e i notebook sono stati scritti da zero. L'elenco di 256 parole del notebook L6 è stato creato per il corso. L'algoritmo TOTP segue la specifica pubblica RFC 6238; i valori di prova sono quelli pubblicati nella specifica.

Materiali di approfondimento:

- NIST SP 800-63B-4, sezione sulle password: https://pages.nist.gov/800-63-4/sp800-63b.html
- xkcd, Password Strength (vignetta, licenza CC BY-NC 2.5): https://xkcd.com/936/
- KeePassXC, documentazione: https://keepassxc.org/docs/
