---
title: "Modulo 4B - Bias, uso responsabile e apprendimento non supervisionato"
subtitle: "B.6 - Data science e Machine Learning. Traccia docenti"
lang: it
---

# Modulo 4B - Traccia docenti

## Collocazione e finalità del modulo

- L14: bias, variabili proxy, fuga di informazione, documentazione dei modelli; collega le competenze tecniche del corso alle conseguenze sulle persone
- L15: apprendimento non supervisionato con il k-means; completa il quadro minimo dei tipi di apprendimento

Segmento di traccia docenti in aula: 10-15 minuti al termine di L14, su come trattare in classe i casi reali di discriminazione e sul coordinamento con B.2 e B.4.

## Logica della progettazione

### L14: il bias come fatto tecnico osservabile

Il tema del bias viene spesso affrontato solo come discussione etica. Qui è prima un fenomeno che gli studenti producono e misurano:

- un modello con buona accuratezza riproduce la distorsione delle etichette
- la distorsione è visibile solo valutando per gruppo, con gli strumenti di L10
- togliere la variabile sensibile non basta, per le variabili proxy
- un'accuratezza perfetta può essere il segnale di un errore (fuga di informazione)

La discussione etica arriva dopo, su una base di esperienza diretta. È la stessa sequenza del corso B.4, dove gli attacchi ai modelli sono prima sperimentati e poi discussi.

### Perché un dataset simulato

Un dataset reale su decisioni che riguardano persone (selezioni, prestiti, giustizia) porrebbe problemi di riservatezza e, soprattutto, non permetterebbe di conoscere la "verità": nei dati reali non si sa quanti candidati scartati erano in realtà meritevoli. Il dataset simulato contiene la colonna `qualificato` proprio per rendere misurabile la distorsione. Il notebook dichiara esplicitamente che questa colonna esiste solo perché i dati sono simulati: è un punto da sottolineare, perché nella realtà la difficoltà principale è proprio l'assenza di una verità di riferimento.

Il contesto (stage, quartiere di residenza) è stato scelto per essere vicino all'esperienza degli studenti senza toccare categorie protette in modo diretto (genere, origine, religione), che possono generare tensioni in classe se trattate come variabili di un esercizio. I casi reali della lezione (Amazon, COMPAS, Gender Shades) mostrano poi il fenomeno sulle categorie protette, attraverso fonti documentate.

### L15: raggruppare senza etichette

Il k-means è il più semplice algoritmo di raggruppamento e riusa la distanza del k-NN. Il confronto tra gruppi trovati e specie vere dei pinguini rende evidente che cosa significa "non supervisionato": l'algoritmo non conosce le specie, eppure le ritrova in gran parte. L'effetto della standardizzazione, già visto in L8, viene confermato in un contesto diverso. La riduzione dei colori di un'immagine mostra un'applicazione in cui non c'è nessuna "risposta corretta".

L'immagine del laboratorio è sintetica, generata per il corso, per evitare problemi di licenza e per funzionare offline.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L14_bias.ipynb` e `_soluzioni` | L14 | pandas, scikit-learn |
| `L14_selezione_stage.csv` | L14 | 600 candidature simulate |
| `L15_kmeans.ipynb` e `_soluzioni` | L15 | scikit-learn |
| `L15_tramonto.npy` | L15 | immagine sintetica 120 x 180 pixel, formato NumPy |
| `pinguini.csv` | L14, L15 | |

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L14 | 20 min: origini del bias (4), casi reali (5), esperimento (3), proxy (3), fuga di informazione (3), documentazione e norme (2) | 30 min | 10-15 min di traccia docenti |
| L15 | 20 min: dati senza etichetta (3), algoritmo (6), pinguini (5), gomito (3), colori (3) | 30 min | 5 min |

### Trattare in classe i casi reali di discriminazione

- presentare i casi attraverso le fonti (l'inchiesta, l'articolo scientifico, la scheda dell'AI Incident Database), non attraverso opinioni
- distinguere il fatto tecnico (il modello ha tassi di errore diversi per gruppi diversi) dalla sua spiegazione (dati, etichette, proxy) e dalla valutazione etica
- il caso COMPAS ha generato un dibattito tecnico reale: l'azienda produttrice ha sostenuto che il sistema era equo secondo un'altra definizione (a parità di punteggio, stessa probabilità di recidiva). Entrambe le affermazioni erano vere: è l'esempio concreto del fatto che diverse definizioni di equità non possono essere soddisfatte insieme. ProPublica ne ha scritto in un articolo successivo: https://www.propublica.org/article/bias-in-criminal-risk-scores-is-mathematically-inevitable-researchers-say
- lasciare spazio agli studenti che vivono esperienze di discriminazione senza chiedere loro di raccontarle
- la discussione approfondita, con dibattiti e giochi di ruolo, è materia del corso B.2; B.6 fornisce la base tecnica

### Attività senza computer

- L14: "la commissione che impara": a gruppi, osservare 20 decisioni storiche stampate (dal dataset simulato) e scrivere le regole che la commissione sembra seguire; molti gruppi scopriranno da soli il ruolo del quartiere o del trasporto
- L15: k-means con i corpi: gli studenti si dispongono nell'aula come punti; tre "centroidi" (studenti con un cartello) si spostano al centro dei rispettivi gruppi a ogni turno

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| "il modello non discrimina, è matematica" | il modello impara dai dati; se le etichette sono distorte, imitarle bene significa riprodurre la distorsione |
| "basta togliere la colonna" | esercizio 4: la differenza resta, per le variabili proxy |
| accuratezza 1,0 accolta come successo | chiedere quando si conosce `colloquio_svolto` |
| numeri dei gruppi del k-means confrontati con le specie come se fossero etichette | i numeri sono arbitrari; si confrontano con la tabella a doppia entrata |
| confusione tra i tre "k" | tabella alla lavagna: k-NN vicini, validazione incrociata blocchi, k-means gruppi |
| k-means applicato senza standardizzare | esercizio 3 |

## Considerazioni sugli strumenti per la didattica

### Risorse per il docente

- AI Incident Database, archivio di incidenti documentati causati da sistemi di IA, utile per trovare casi aggiornati: https://incidentdatabase.ai/
- Kaggle Learn, Intro to AI Ethics: corso breve in inglese su equità, bias e schede dei modelli, con esercizi in notebook: https://www.kaggle.com/learn/intro-to-ai-ethics
- Google, Machine Learning Crash Course, sezione Fairness (disponibile in italiano): https://developers.google.com/machine-learning/crash-course

### Collegamento con altri corsi

- B.2: dibattito su bias, privacy, fattore umano; L14 fornisce gli strumenti per verificare le affermazioni
- B.4: avvelenamento dei dati (una distorsione introdotta di proposito), norme (AI Act, GDPR); in L14 le norme sono solo richiamate
- B.7: i modelli generativi ereditano i bias dei dati di addestramento in immagini e testi

## Valutazione del modulo

Verifica del modulo 4 (dopo L15), individuale, 40 minuti:

- interpretare pendenza, intercetta ed errore di una regressione su un dataset non visto, individuando una previsione per estrapolazione
- dato un piccolo dataset con una distorsione nascosta, calcolare una metrica per gruppo e spiegare l'origine della differenza
- individuare in un elenco di caratteristiche una possibile fuga di informazione e una possibile variabile proxy
- descrivere i passi del k-means e interpretare una tabella gruppi-classi

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| valuta un modello per gruppo | L14, esercizio 3 |
| riconosce variabili proxy | L14, esercizio 4 |
| riconosce una fuga di informazione | L14, esercizio 5 |
| documenta un modello | L14, esercizio 6 |
| esegue a mano il k-means | L15, esercizio 1 |
| interpreta i gruppi e sceglie k | L15, esercizi 2-4 |

## Soluzioni degli esercizi

### L14

- Esercizio 1: qualificati 45,2% nel centro e 39,0% in periferia; ammessi 46,4% e 18,6%. Tra i qualificati: ammessi 93,4% nel centro, 47,6% in periferia. La commissione è stata molto più severa con la periferia a parità di requisiti.
- Esercizio 2: accuratezza 0,856; importanza: media 0,79, quartiere 0,12, assenze 0,08, attività 0: il modello usa il quartiere.
- Esercizio 3: tra i qualificati di verifica il modello ammette l'86,7% del centro e il 46,2% della periferia. L'accuratezza misura la somiglianza con le decisioni storiche, non la loro correttezza.
- Esercizio 4: senza quartiere, 80,0% contro 46,2%: la differenza resta. Il trasporto scolastico è usato dal 77% dei candidati della periferia e dal 13% del centro; le assenze medie sono 9,5% in periferia e 8,0% in centro. Il modello ricostruisce il quartiere attraverso queste variabili. Notare anche che l'attività extrascolastica, che è un requisito del bando, non viene usata dal modello: le decisioni storiche non la premiavano in modo coerente.
- Esercizio 5: accuratezza 1,0 perché `colloquio_svolto` coincide con l'esito (tabella: 395 no/0, 0/205 sì). Per un nuovo candidato il colloquio non è ancora avvenuto: il modello è inutilizzabile.
- Esercizio 6: esempio di scheda nella lezione. Prestazioni per gruppo dell'albero di profondità 3 su becco e pinna (pinguini con tutti i dati, 84 di verifica): Adelie 0,973, Chinstrap 0,941, Gentoo 0,900; femmine 0,913, maschi 0,974. Limiti: tre specie, adulti, stesso protocollo di misura, stesse isole e anni; uso sconsigliato su altre specie o popolazioni.

### L15

- Esercizio 1: passo 1: gruppi [A, A, A, A, B, A]; A = (3,4; 3,2), B = (7; 6). Passo 2: [A, A, A, B, B, B]; A = (1,5; 1,33), B = (6,5; 6). Passo 3: nessun cambiamento. Distanze del passo 1 per il punto (6, 5): 4,9 da A e 5,0 da B.
- Esercizio 2: tabella specie-gruppi come nella lezione; 317 su 342 (0,927) nel gruppo della specie prevalente.
- Esercizio 3: quattro misure non standardizzate: 237 su 342 (la massa domina le distanze; Adelie e Chinstrap mescolati); standardizzate: 313 su 342.
- Esercizio 4: inerzie 684, 340, 187, 148, 114, 95, 83, 73 per k da 1 a 8; gomito a k = 3.
- Esercizio 5: con 2 colori restano cielo e mare; con 4-5 compaiono le fasce del cielo e il sole; con 8-16 l'immagine è molto simile all'originale. L'immagine originale ha 21.600 pixel con colori tutti leggermente diversi (per il rumore aggiunto).

## Materiale open source

Verifica puntuale per L14-L15: lezioni, dataset simulato, immagine sintetica, figure e notebook sono stati prodotti da zero. Materiali correlati:

- Kaggle Learn, Intro to AI Ethics: https://www.kaggle.com/learn/intro-to-ai-ethics
- Microsoft, ML for Beginners, sezione Clustering e lezione "Fairness in Machine Learning" (licenza MIT): https://github.com/microsoft/ML-For-Beginners
- Mitchell e altri, Model Cards for Model Reporting, 2019: https://arxiv.org/abs/1810.03993
- AI Incident Database: https://incidentdatabase.ai/
