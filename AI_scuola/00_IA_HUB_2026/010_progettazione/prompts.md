
# Informazioni di contesto per la richiesta di creazione corso

## Traccia docenti  

I materiali per la traccia docenti devono stare in file separati per ogni argomento completo, per esempio _docente.md, in markdown.
Per i docenti il markdown verrà reso solo in A4.  

Si assume che docenti e studenti siano sempre in aula assieme

La parte docente farà anche considerazioni sulla logica didattica con cui è stato formulato il syllabus del corso, spiegando anche in che modo il limite di 18 ore lo ha influenzato. Crea un file dedicato, per esempio syllabus_docente.md, generato insieme al syllabus

Gli strumenti come notebooks jupyter, kaggle, Etc. vanno spiegati nel modo seguente:  

- strumento per sè: nella traccia studenti  
- eventuali considerazioni sul come inserire uno strumento in un corso: nella traccia docenti

## Criteri creazione corso  


### Strumenti  

Anche se sono disponibili strumenti online quando possibile vanno sempre forniti contenuti anche per l'off-line, ad esempio anche se si utilizza Google Colab vanno anche forniti i notebooks jupyter locali

### Audience del corso: docenti che imparano a insegnare le materie descritte nel tema del corso  

Il corso è parte di un gruppo di 7-8 corsi destinati a docenti.  
La tematica del corso è ciò che i docenti dovranno imparare ad insegnare, applicando al massimo didattica laboratoriale, oltre a insegnare la teoria necessaria.

I contenuti del corso vanno strutturati in due tracce:  

- traccia "corso per studenti"  
Dimensione: 80% - 90% dei contenuti del corso.  
Contenuti: un normale corso per studenti di scuola secondaria superiore, completo di teoria e pratica, massimizzando la pratica laboratoriale  

- traccia "progettazione didattica e pratica della didattica laboratoriale"  
Dimensione: 10% - 20% dei contenuti.  
Contenuti: considerazioni indirizzate ai docenti. Le considerazioni spiegano  
  - la logica sottostante alla progettazione didattica dei contenuti della lezione studenti  
  - come impostare laboratorio, condurlo, supportare gli studenti, valutare ciò che viene realizzato ETc. ETc.  
I laboratori devono essere eseguibili su PC di fascia bassa e non richiedere installazione di software o richiedere solo software semplici e leggeri installabili in modalità utente o che possono essere eseguiti da una chiavetta.

La parte di normale corso dovrà spiegare anche, e bene, tutte le piattaforme e strumenti usati nella pratica, ad esempio:

- il corso di Python nella traccia "corso per studenti" non deve solo spiegare il linguaggio Python ma spiegare cosa sono IDE ed editors, elencare i più noti, spiegare a livello base una IDE o un editor Etc.  
- il corso sul data science nella traccia "progettazione didattica e pratica della didattica laboratoriale" dovrà spiegare gli strumenti laboratoriali e pratici utilizzabili dal docente,  
ad esempio:  
  - Cosa Kaggle offre dal punto di vista didattico quali sono i corsi più adatti a studenti di secondaria, cosa offre per creare laboratori  
  - Cosa offrono i notebooks Jupyter dal punto di vista della didattica, cosa offre alla didattica Google Colab, sua efficacia ed utilità (e debolezze) nel creare didattica laboratoriale

### Criteri generali  

- syllabus articolato su 18 ore e, per la parte di lezione studente, indirizzato a studenti di 16 - 18 anni  
- sempre lezioni di tipo lezpub
- Per la durata delle sessioni ignora altri documenti, essa potrà andare da 2 a 3 ore (4 possibile ma meno probabile) ma non sarà noto prima dell'inizio del corso, ogni volta che è possibile crea singole lezioni autonome di circa un'ora, penserò io a raggrupparle in sessioni.
- importante: 
  - Il termine lezione è usato in modo flessibile: una lezione non deve esaurire un argomento, è più che altro una sezione di contenuto ben definita, può essere una parte di una lezione. Argomenti non banali richiederanno sicuramente più lezioni/sezioni.
  - I files di contenuti possono contenere più lezioni, chiaramente identificate. Ciò è desiderabile quando un argomento richiede più lezioni.
  - Quando possibile e se e solo se non abbassa la qualità della didattica 20 o 30 minuti della lezione di un'ora devono essere dedicati a esercizi eseguibili facilmente su un laptop di fascia bassa. Decidi tu dando la priorità alla qualità della didattica
- le lezioni devono sempre spiegare tutto ciò che mostrano, in particolare per i comandi e il codice, ad esempio: se si spiega il comando "ls -l" vanno spiegati sia "ls" sia l'opzione "-l" la prima volta che si incontra il comando.
- inserire abbondantemente diagrammi online o generati da te con mermaid o plantuml (preferibile mermaid), esempi di comandi e di codice
- per argomento/file vanno generati  
  - file con le lezioni vere e proprie (lezpub) in markdown, che verrà poi reso in A4 in pdf
  - presentazione in markdown due sotto formati: marp (filename con suffiso _marp) e presentazione pandoc (suffisso _prezpdoc)
- è desiderabile, se e solo se compatibile con le richieste precedenti, che dal markdown si possano generare anche presentazioni reveal.js
- se esistono già corsi open source molto simili anzichè generare la lezione dimmelo e chiedimi se usarli direttamente, spiegando concisamente le caratteristiche e fornendo un link. Per l'open source va fatta una verifica complessiva sul syllabus e una puntuale su ogni lezione.



###### ----------------------------------------------------------------------------


### Generazione argomenti comuni da inserire a diversi livelli di dettaglio nei diversi corsi  

Questi argomenti verranno inseriti in più di un corso con diversi livelli di approfondimento, e quindi di estensione dell'ambito e il livello di dettaglio della trattazione,

Per ogni argomento crea contenuti con tre livelli di approfondimento "concetti essenziali", "base", "base-intermedio", i livelli debbono essere chiaramente identificati.
Ogni livello deve essere ben delimitato e completo e non ripete i contenuti del precedente, salvo richiami necessari.
Ogni livello può occupare una lezione dedicata, eccezionalmente due se effettivamente necessario

Gli argomenti sono:  

#### didattica laboratoriale  

E' solo per i docenti quindi è sufficiente il markdown per A4, file con suffisso _docente.

Se possibile strutturalo nelle seguenti sezioni:  

- didattica laboratoriale in generale, indipendentemente dalle materie
- didattica laboratoriale per le materie STEM
- didattica laboratoriale per programmazione
- didattica laboratoriale per l'intelligenza artificiale

In ogni sezione di queste sopra aggiungi una sezione specifica per gli studenti BES

Non devono essere creati veri lab, possono essere citati esempi, i lab verranno creati nei corsi specifici.

Fra gli argomenti, oltre a quelli che sceglierai, cerca di includere i seguenti:
Teorie cognitive e didattiche sottostanti, casistiche in cui porta benefici e casistiche in cui non porta benefici, come progettare un laboratorio efficace indipendentemente dalla materia

#### Git e github  

Qui cerca di individuare 3 livelli, ad esempio:  

- utilizzo prevalentemente personale e per consegna compiti col docente
- utilizzo base in piccoli team, deliverables gestiti in modo ottimale (jupyter notebooks? binari)
- utilizzo medio-base

#### Jupyter notebooks, Google colabs e altri simili notebooks gratuiti online

Per i docenti includi anche:

- Utilità nella didattica laboratoriale
- Casi in cui sono particolarmente adatti dal punto di vista didattico (e in cui sono meglio altri approcci)

Per gli studenti:

- Formato sottostante, strumenti varianti


## Prompt generale dopo contesto sopra: Genera un syllabus per  un corso che poi dovrà essere generato con i seguenti criteri (per ora solo il syllabus)  

## Prompt generale dopo contesto sopra: Genera lezioni per il corso:  

Per consentirti di gestire bene l'ambito ti informo che il corso è parte di questa serie di corsi

## Elenco dei corsi

### B.1 - "STEM & AI Lab: L'Evoluzione della Scienza a Scuola"

Descrizione: laboratorio esperienziale per studenti in cui si applicano algoritmi di IA per analizzare dati scientifici reali, fare previsioni, programmare piccoli sensori e attuatori.

### B.2 - "Umani e Algoritmi: Navigare l'IA con la Propria Testa"

Descrizione: dibattiti guidati, giochi di ruolo e analisi di casi reali per stimolare il pensiero critico degli studenti su fake news, privacy, tracciamento dei dati e l'importanza del fattore umano.

### B.3 - "Slide e presentazioni con l'IA"

Descrizione: laboratorio "mani sulla tastiera" per insegnare agli studenti a strutturare una presentazione efficace per la scuola o l'esame di maturità, usando l'IA generativa per l'ideazione e l'ottimizzazione visiva.

### B.4 - "Cybersicurezza e IA: Difendere e attaccare: la sicurezza ai tempi dell'IA"

Descrizione: gli studenti scoprono come gli hacker usano l'intelligenza artificiale per attaccare e come i sistemi di difesa la usano per proteggersi. Focus su password sicure, phishing avanzato e cybersicurezza.

### B.5 - "Sistemi robotici autonomi e percezione intelligente: Robot che vedono e decidono da soli"

Descrizione: laboratorio di robotica in cui gli studenti programmano piccoli sistemi robotici in grado di agire in funzione delle misurazioni effettuate.

### B.6 - "Data science e Machine Learning: dai dati ai modelli"

Descrizione: introduzione pratica al mondo dei dati. Gli studenti imparano come si raccoglie un dataset, come "ragiona" un algoritmo di classificazione e come si addestra un piccolo modello predittivo.

### B.7 - "IA generativa, deepfake e integrità informativa: Deepfake e IA generativa: riconoscere il vero dal falso"

Descrizione: laboratorio interattivo per smascherare i deepfake (audio e video) e capire il funzionamento della manipolazione mediatica. Gli studenti imparano a usare i tool di verifica delle fonti (fact-checking).


### B.8 - "Linguaggio Python per il Machine Learning ed il Deep Learning: Python per l'Intelligenza Artificiale"

Descrizione: corso puramente tecnico di introduzione alla sintassi Python e alle librerie fondamentali per comprendere le basi matematiche e logiche delle reti neurali.
