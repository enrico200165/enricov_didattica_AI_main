# Descrizione famiglia di corsi, caratteristiche comuni  

## Bando e famiglia di corsi  

Futuro onlife: percorsi di orientamento tra scuola, territorio e impresa
IDENTIFICATIVO DI PROGETTO: 10.1.6A-FDRPOC-LA-2024-68
CUP: J84D25001250001

## Descrizione  

I corsi sono esperienze di apprendimento finalizzate all'orientamento. Il bando del ministero li descrive come "Percorsi di orientamento rivolti alle classi terze, quarte e quinte delle istituzioni scolastiche secondarie di secondo grado con il coordinamento del docente tutor".

Nei corsi inserisci sempre aspetti pratici e spiegazioni complete; nel codice inserisci commenti esplicativi.

Ogni corso deve essere ragionevolmente autosufficiente.

Gli aspetti orientativi sono trattati prevalentemente a voce e tramite dibattito. Nei materiali del corso sono trattati in modo estremamente conciso, con liste di punti da considerare; se ne tiene comunque molto conto privilegiando contenuti pratici e vicini alla vita lavorativa reale, compatibilmente con tempi, attrezzature ed età degli studenti.

## Criteri generali  

- I corsi hanno tutti la durata totale di 30 ore, che verrà divisa in sessioni di 2 o 3 ore; la durata delle sessioni non sarà nota prima dell'inizio del corso.
  - Struttura i contenuti didattici in unità di circa un'ora (sezioni, oppure lezioni se la struttura è a due livelli), in modo che possano essere inserite in sessioni di qualunque lunghezza.
- Destinatari: studenti del triennio di istituto tecnico a indirizzo informatico o di liceo scientifico; livello dei contenuti adeguato a studenti di 16-18 anni. Si assumono conoscenze base di programmazione (comprendere programmi di 10 - 20 righe di codice, in un qualsiasi linguaggio) e utilizzo di base del PC.
- Considerare tutti i destinatari come minorenni, per evitare di dover differenziare: preferire strumenti e piattaforme utilizzabili senza account personale o con account consentiti ai minori, evitare servizi che richiedono maggiore età o carta di credito; quando un servizio lo richiede, prevederne l'uso tramite l'account del docente o sostituirlo con un emulatore locale o una simulazione.
- Sempre lezioni di tipo lezpub.
- Struttura del corso:
  - puoi strutturare il corso su 2 o 3 livelli; se usi 3 livelli usa i termini modulo > lezione > sezione (parte di lezione ben delimitata)
  - una lezione non deve esaurire un argomento: è un blocco di contenuto ben definito; argomenti non banali richiedono più lezioni
  - un file di contenuti può contenere più lezioni, chiaramente identificate; ciò è desiderabile quando un argomento richiede più lezioni
- Esercizi e lab devono essere eseguibili facilmente su un laptop di fascia bassa (Windows, 8 GB di RAM).
- Strumenti software usati in esercizi e lab:
  - completamente gratuiti, almeno nelle funzionalità di base usate nel corso
  - facili da installare; preferire le versioni portabili (archivio da scompattare ed eventuale aggiunta della cartella al PATH) all'installazione completa
  - per ogni tipologia di strumento indicare lo strumento consigliato per la didattica: gratuito, diffuso in ambito professionale, utilizzabile in poche ore senza ridursi a uno strumento giocattolo; eventualmente indicare fino a due alternative
- Le lezioni devono sempre spiegare tutto ciò che mostrano, in particolare comandi e codice. Esempio: se si spiega il comando "ls -l" vanno spiegati sia "ls" sia l'opzione "-l" la prima volta che si incontra il comando nel modulo o nella lezione (decidi tu).
- Inserire abbondantemente diagrammi reperiti online o generati con Mermaid o PlantUML (preferibile Mermaid), esempi di comandi e di codice; non preoccuparti del rendering.
- Per ogni file di contenuti (un argomento, eventualmente suddiviso in più lezioni) vanno generati:
  - file con le lezioni vere e proprie (lezpub) in markdown, che verrà poi reso in PDF formato A4
  - presentazione in markdown in due sottoformati: Marp (nome file con suffisso `_marp`) e presentazione pandoc in formato reveal.js (suffisso `_prezpdoc`)
- Se esistono già corsi open source molto simili, in italiano o in inglese, anziché generare la lezione fermati e chiedimi se usarli, spiegando concisamente le caratteristiche e fornendo un link. Per l'open source va fatta una verifica complessiva sul syllabus e una puntuale su ogni lezione.
- Quando crei i contenuti non esitare a utilizzare parti di corsi esistenti se la licenza lo consente, inserendo chiaramente l'attribuzione e le coordinate del brano utilizzato (per esempio l'URL della pagina) e traducendo in italiano.

## Corsi da realizzare  

### Corso: Sviluppo Software e Coding Laboratoriale  

Percorso in cui gli studenti apprendono:

- la logica di **programmazione**
- la **struttura degli algoritmi**

creando **piccole applicazioni o componenti web**, con breve illustrazione degli **sbocchi professionali e accademici** legati allo sviluppo informatico.  

### Corso: Cybersecurity ed Ethical Hacking  

Itinerario incentrato sulla sicurezza informatica e sulla difesa delle reti, in cui i ragazzi **simulano attacchi e configurazioni di protezione**, apprendono le sfide della gestione dati e studiano casi reali.  

Vincoli:

- Scansioni, attacchi simulati ed exploit si eseguono solo su bersagli propri, isolati o esplicitamente autorizzati, come i lab pubblici predisposti a questo scopo.
- Livello di dettaglio sulle tecniche di attacco: descrivere il funzionamento degli attacchi a livello concettuale (principio, condizioni che lo rendono possibile, impatto, contromisure), senza istruzioni operative passo passo, payload o exploit pronti all'uso. In passato contenuti di cybersecurity troppo dettagliati sugli attacchi sono stati bloccati dai filtri dell'AI. La pratica sulle tecniche offensive si svolge sui lab pubblici indicati tramite link a risorse online dettagliate e pratiche; la pratica in aula riguarda soprattutto la difesa: configurazioni di protezione, analisi di log e traffico, riconoscimento degli attacchi. Questo criterio vale solo per le tecniche di attacco: tutti gli altri contenuti, in questo e negli altri corsi, restano pratici e operativi.

### Corso: Reti, Cloud e Gestione dei Dati  

Percorso sull'infrastruttura tecnologica, in cui gli studenti si cimentano:

- nella **progettazione di architetture di rete**
- nella gestione di database, analizzando come viaggiano le informazioni

e apprendono i concetti di base dei sistemi cloud e delle infrastrutture ICT del mondo professionale.  

### Corso: Informatica per l'Impresa e Soft Skills Digitale  

Percorso che unisce le competenze tecniche al **lavoro di squadra e al problem solving**, guidando gli studenti nella **simulazione della gestione di un progetto informatico completo**, dal requisito dell'utente al rilascio del software, con l'illustrazione, da parte del docente, di come le aziende ICT gestiscono i progetti, e il supporto nella definizione del proprio piano orientativo post-diploma.
