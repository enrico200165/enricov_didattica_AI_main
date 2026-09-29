---
title: "Modulo 3A - Phishing e phishing potenziato dall'IA"
subtitle: "B.4 - Cybersicurezza e IA. Traccia docenti"
lang: it
---

# Modulo 3A - Traccia docenti

## Collocazione e finalità del modulo

Le lezioni L8 e L9 applicano i prerequisiti del modulo 1 (URL, intestazioni email, leve psicologiche) e del modulo 2 (limiti dei codici e resistenza al phishing) al tema centrale della descrizione del corso: il phishing avanzato e il ruolo dell'IA nell'attacco.

Il filo della lezione è il passaggio dai segnali di forma ai segnali di contenuto e alle procedure:

- L8: si impara a leggere segnali tecnici e di contesto e si introduce la regola della verifica indipendente
- L9: si mostra che l'IA elimina i segnali di forma, e che le difese efficaci sono i segnali di contenuto e le procedure

Segmento di traccia docenti in aula: 10-15 minuti al termine di L9, su uso dell'IA generativa con studenti minorenni, confini degli esercizi di attacco simulato e gestione dei casi personali.

## Logica della progettazione

### Esempi fittizi invece di messaggi reali

Il corpus usa organizzazioni fittizie e domini `.example`. I messaggi fraudolenti reali, pubblicati dal CERT-AGID, sono citati nelle lezioni del modulo 1 come casi di studio, ma non vengono riprodotti come materiale di laboratorio. Motivi:

- un messaggio che imita un'organizzazione reale, se circola fuori dall'aula (fotografato, inoltrato), può essere scambiato per autentico
- i domini fittizi permettono di costruire esattamente le tecniche da insegnare, una per messaggio
- i link non portano a nessun sito, anche se qualcuno li apre

### Due messaggi legittimi nel corpus

Il corpus contiene due messaggi legittimi (2 e 5). Un corpus di soli messaggi fraudolenti insegna a diffidare di tutto, cosa che nella vita reale non è sostenibile e porta a ignorare anche le comunicazioni vere. Gli studenti devono saper giustificare anche il giudizio "legittimo": dominio corretto, nessuna richiesta sensibile, invito ad agire tramite canali già noti.

### L8: il codice come strumento di osservazione

Il notebook `L8_analisi_url.ipynb` automatizza la stessa analisi fatta a occhio. Serve a tre scopi:

- rendere espliciti i criteri (se non si sa descrivere una regola, non la si può programmare)
- mostrare che cosa fa, in piccolo, un filtro antiphishing
- far scoprire i limiti: l'esercizio 3 chiede di trovare un URL ingannevole che il programma non riconosce (per esempio un typosquatting con un dominio ufficiale diverso da quello indicato, o un sito legittimo compromesso)

### L9: modifica rispetto al syllabus

Il syllabus prevedeva, nel laboratorio di L9, che un gruppo di studenti preparasse un messaggio di spear phishing, eventualmente con un assistente di IA, a partire da un profilo fittizio. Nella stesura della lezione l'attività è stata sostituita:

- analisi del profilo fittizio dal punto di vista della ricognizione (quali informazioni sono sfruttabili) e della difesa (come ridurre l'esposizione)
- esperimento con il notebook su messaggi fraudolenti già scritti, "vecchio stile" e con testo curato, per mostrare quali segnali restano utili

Motivi della scelta:

- l'obiettivo didattico (capire che la forma non è più un indicatore) si raggiunge meglio con un confronto controllato tra due gruppi di messaggi
- far scrivere a minorenni messaggi di inganno efficaci, con o senza IA, non aggiunge competenze difensive e produce materiale riutilizzabile fuori dall'aula
- l'uso di assistenti di IA da parte degli studenti richiede verifiche (regole della scuola, consenso, condizioni d'uso dei servizi) che non tutte le classi possono soddisfare

I messaggi del gruppo B sono stati scritti per il corso imitando lo stile dei testi prodotti dai modelli linguistici; non sono stati generati da un modello. Se si vuole mostrare in aula la capacità dei modelli di produrre testi curati, il docente può farlo con una richiesta neutra (per esempio "scrivi un avviso di manutenzione del registro elettronico") e far notare che lo stesso testo, con una richiesta finale diversa, diventerebbe un'esca.

### L9: le procedure come risposta

La lezione si chiude sulle procedure (verifica indipendente, parola d'ordine, doppia approvazione) e non sul riconoscimento dei deepfake, materia di B.7. La scelta è coerente con il messaggio del modulo: contro un inganno perfetto non si può contare sul riconoscimento, si conta su regole decise prima.

L'esercizio 5 (protocollo familiare) ha una ricaduta pratica anche per le famiglie: le truffe con voce clonata colpiscono soprattutto genitori e nonni. Può diventare un'attività di cittadinanza digitale da portare a casa.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L8_corpus_messaggi.md` e immagini `messaggio1.png` ... `messaggio8.png` | L8 | stampabile; una copia a coppia |
| `L8_scheda_analisi.md` | L8 | |
| `L8_qr_messaggio8.png` | L8 | codice QR che punta a un dominio `.example` inesistente |
| `L8_analisi_url.ipynb` | L8 | solo libreria standard |
| `L9_scheda_osint_fittizia.md` | L9 | |
| `L9_segnali_messaggio.ipynb` | L9 | solo libreria standard |

### Checklist

- verificare che CyberChef offline contenga le operazioni `URL Decode`, `From Punycode` e `Parse QR Code`
- se gli studenti inquadrano il QR con il telefono, il link non si apre (dominio inesistente): è comunque l'occasione per sottolineare che le app della fotocamera mostrano l'indirizzo prima di aprirlo, e che va letto
- Jigsaw Phishing Quiz: verificare la raggiungibilità dalla rete della scuola; è in inglese e usa esempi con marchi reali di servizi internazionali

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L8 | 25 min: forme (5), BEC (5), AiTM (5), segnali e verifica (7), codice (3) | 30 min | 5 min |
| L9 | 25 min: IA e testi (5), OSINT (5), voce e video (7), difese (8) | 30 min | 10-15 min di traccia docenti |

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| tutto viene giudicato fraudolento, anche i messaggi 2 e 5 | chiedere quale richiesta sensibile contengono e quale canale indicano |
| il messaggio 3 viene giudicato legittimo perché i controlli sono superati e il mittente è vero | riprendere i segnali di contesto: cambio IBAN, segretezza, cambio di canale, urgenza; la casella del fornitore può essere compromessa |
| nel messaggio 7 non si nota la lettera cirillica | usare il notebook o CyberChef; ribadire che a occhio non si distingue e che la difesa è non usare i link |
| "a me non succederebbe" | citare il caso Arup: un dipendente di una grande società, in una videoconferenza con volti e voci noti |
| discussione sui social ("allora non pubblico più niente") | l'obiettivo è ridurre, non eliminare: profili privati, niente posizioni in tempo reale, attenzione a date e nomi |

### Esperienze personali e casi in corso

Il tema delle truffe con voce clonata o dei falsi messaggi "Ciao mamma" porta spesso racconti di familiari coinvolti. Valgono le indicazioni del modulo 1: ascoltare, non chiedere dettagli sensibili, gestire separatamente eventuali casi in corso.

Se durante l'analisi del profilo di Giulia uno studente riconosce la propria situazione (profilo pubblico con molti dati), suggerire di rivedere le impostazioni in autonomia, senza esporre il proprio profilo davanti alla classe.

## Considerazioni sugli strumenti per la didattica

### Corpus di messaggi come immagini

Le immagini riproducono l'aspetto di un programma di posta, di un telefono e di un cartello, senza marchi reali. Il docente può creare nuovi esempi: le sorgenti HTML sono semplici e modificabili. Conviene mantenere organizzazioni fittizie, domini `.example` e un'indicazione di esempio didattico.

### Jigsaw Phishing Quiz

Punti di forza: gratuito, interattivo, spiega ogni risposta. Limiti: in inglese, esempi con marchi internazionali e poco legati al contesto italiano (PEC, SPID, enti pubblici). Adatto come attività facoltativa o per casa.

### Controlli a regole nei notebook

I notebook di L8 e L9 usano regole scritte a mano. È una scelta consapevole: le regole sono leggibili e modificabili da tutti gli studenti, anche senza conoscere Python, e preparano il confronto con il classificatore addestrato di L11, dove le "regole" vengono apprese dai dati.

Esercizi ponte con B.8:

- aggiungere a `analizza_url` il controllo del typosquatting con la distanza di modifica tra stringhe (numero minimo di inserimenti, cancellazioni e sostituzioni di caratteri per passare da un nome all'altro)
- trasformare le regole di L9 in una classe con pesi modificabili

## Valutazione del modulo

Verifica di modulo (15-20 minuti, individuale), da svolgere al termine del modulo 3 (dopo L11) insieme alla parte su privacy e difesa, oppure subito dopo L9:

- analisi di due messaggi non visti (uno legittimo, uno fraudolento) con motivazione
- descrizione della regola della verifica indipendente applicata a una telefonata con voce familiare
- spiegazione di perché l'assenza di errori non è un segnale di affidabilità

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| distingue segnali tecnici e di contesto | L8, esercizio 1 |
| giustifica il giudizio "legittimo" | L8, esercizio 1 (messaggi 2 e 5) |
| riconosce i limiti di un controllo automatico | L8, esercizio 3; L9, esercizio 4 |
| individua informazioni sfruttabili in un profilo pubblico | L9, esercizio 1 |
| propone difese procedurali | L9, esercizio 5 |

## Soluzioni degli esercizi

### L8, Esercizio 1

| N. | Canale | Giudizio | Motivazione principale | Azione corretta |
|---|---|---|---|---|
| 1 | SMS | fraudolento | pacco non atteso; urgenza; piccolo pagamento per ottenere i dati della carta; dominio registrato `consegna-pacchi.example`, non del corriere | ignorare; verificare eventuali spedizioni dal sito o app ufficiale del corriere |
| 2 | email | legittimo | dominio della scuola; nessun link né richiesta di credenziali; rimanda al registro "come di consueto" | leggere la circolare dal registro |
| 3 | email | fraudolento (BEC) | cambio di IBAN, urgenza, riservatezza, impossibilità di telefonare; i controlli superati indicano che la casella del fornitore è probabilmente compromessa | non pagare; telefonare al fornitore a un numero già noto; avvisare il fornitore della possibile compromissione |
| 4 | WhatsApp | fraudolento | numero nuovo, richiesta di denaro, impossibilità di chiamare, urgenza | chiamare il figlio al numero vecchio o per altra via; usare la parola d'ordine familiare |
| 5 | email | legittimo | dominio corretto, controlli superati, nessun link, invito a usare l'app o il numero sulla carta | se l'accesso non è stato fatto dall'utente, agire dall'app |
| 6 | email | fraudolento | "casella piena" come pretesto; richiesta di credenziali; link che passa da un reindirizzatore verso `rinnovo-casella.example`; mittente esterno | ignorare; segnalare al referente informatico |
| 7 | SMS | fraudolento | allarme su un bonifico, urgenza; dominio omografo con `а` cirillica (`xn--bncaaurora-zqi.example`) | non usare il link; controllare i movimenti dall'app della banca |
| 8 | QR su cartello | fraudolento | adesivo sovrapposto al cartello; dominio non del comune o del gestore | pagare con l'app ufficiale o al parcometro; segnalare al gestore |

### L8, Esercizio 3

Esempi di URL ingannevoli non riconosciuti dal programma:

- un dominio legittimo compromesso: l'URL è corretto, il contenuto no
- un typosquatting quando il dominio ufficiale passato alla funzione è sbagliato: il programma confronta solo con il dominio indicato
- un dominio che non contiene il nome dell'organizzazione e non usa tecniche particolari (per esempio `servizi-online-verifica.example`): viene segnalato solo come "dominio diverso", che è corretto, ma senza altri indizi

### L8, Esercizio 4

- messaggio 6: `https://webmail.istituto-esempio.example.rinnovo-casella.example/login`, dominio registrato `rinnovo-casella.example`
- messaggio 7: `xn--bncaaurora-zqi.example` corrisponde a `bаncaaurora.example` con la prima `a` cirillica
- messaggio 8: `https://paga-parcheggio-roma.example/sosta?zona=12`

### L9, Esercizio 1

| Informazione (post) | Che cosa rivela | Inganno possibile |
|---|---|---|
| nome del cane e data del compleanno (1) | possibili password e risposte alle domande di sicurezza | indovinare credenziali; messaggio "abbiamo trovato Aquila" |
| orari degli allenamenti con posizione (2) | dove si trova e quando | sapere quando non risponde al telefono; truffa ai genitori "è successo qualcosa in palestra" |
| scuola e classe (3) | contesto scolastico | messaggi a nome della scuola o di docenti |
| nome della madre e della zia (4) | relazioni familiari | "Ciao mamma", messaggi a nome della zia |
| telefono nuovo in arrivo (5) | evento atteso | falso SMS di consegna del telefono; "ho cambiato numero" credibile |
| video con la voce (6) | campione vocale | clonazione della voce per chiamare i genitori |
| scuola di lingue a Londra (7) | ente frequentato | falsa email della scuola di lingue (rimborsi, nuove iscrizioni) |
| data di nascita completa (8) | dato identificativo | furto d'identità, risposta a verifiche |
| carta prepagata e banca (9) | cliente di quella banca | SMS o chiamata a nome della banca |
| allenatore e convocazione (10) | persona di fiducia, evento imminente | messaggio del "coach" che chiede documento e codice fiscale (come il messaggio 2 del gruppo B di L9) |

### L9, Esercizio 3

Le regole sulla forma riconoscono tutti i messaggi del gruppo A e nessuno del gruppo B. Le regole sul contenuto riconoscono tutti e sei i messaggi. La correttezza del testo non è più un indizio perché i modelli linguistici producono testi corretti a costo quasi nullo.

### L9, Esercizio 4

Il primo messaggio legittimo attiva la regola "urgenza" per l'espressione "entro venerdì". Modifiche possibili: togliere espressioni troppo comuni, oppure considerare sospetto solo un messaggio con almeno due segnali o con segnali di peso alto (codici, carta, IBAN). La parte 5 del notebook, con il punteggio e la soglia, realizza questa seconda soluzione.

### L9, Esercizio 5

Esempio di protocollo:

1. per richieste di denaro, codici o dati ricevute da un numero nuovo o via messaggio, chiamare la persona al numero già noto
2. se la persona chiama con una voce riconoscibile ma chiede denaro urgente, chiedere la parola d'ordine familiare
3. la parola d'ordine non si scrive in chat e non si pubblica
4. nessun pagamento prima della verifica, anche se "è urgente"
5. in caso di dubbio, coinvolgere un altro familiare prima di agire

## Materiale open source

Verifica puntuale per L8-L9: le lezioni, il corpus di messaggi, il profilo fittizio e i notebook sono stati scritti da zero. Il caso Arup è riassunto dalla scheda dell'AI Incident Database.

Materiali di approfondimento:

- AI Incident Database, Incident 634: https://incidentdatabase.ai/cite/634/
- Jigsaw Phishing Quiz: https://phishingquiz.withgoogle.com/
- CERT-AGID, glossario, voce phishing: https://cert-agid.gov.it/glossario/phishing/
