---
title: "Modulo 3B - Dati personali e IA nella difesa"
subtitle: "B.4 - Cybersicurezza e IA. Traccia docenti"
lang: it
---

# Modulo 3B - Traccia docenti

## Collocazione e finalità del modulo

Le lezioni L10 e L11 chiudono il modulo 3:

- L10 tratta gli aspetti non ovvi della riservatezza dei dati personali, richiesti esplicitamente dalla descrizione del corso: metadati, reidentificazione, inferenza, dati consegnati ai chatbot
- L11 presenta l'IA come strumento di difesa e costruisce il classificatore antiphishing che verrà attaccato nel modulo 4 (L12 esempi avversari, L13 avvelenamento)

Segmento di traccia docenti in aula: 10-15 minuti al termine di L11, sull'uso del classificatore come "scatola grigia", sul coordinamento con B.6 e sulla preparazione dei dataset didattici.

## Logica della progettazione

### L10: rischi concreti e dimostrabili

Il tema della privacy rischia di restare astratto ("i dati sono importanti"). La lezione sceglie rischi che si possono dimostrare in laboratorio in pochi minuti:

- una foto rivela un luogo preciso (esercizi 1 e 2)
- un questionario "anonimo" rivela chi ha risposto che cosa (esercizio 3)
- una misura tecnica semplice riduce il rischio, con un costo in informazione (esercizio 4)

La parte sui chatbot è collocata qui, e non nel modulo 4, perché riguarda i dati dell'utente e non la sicurezza del modello. Il modulo 4 riprende il tema dal lato dell'attaccante (estrazione di informazioni, prompt injection).

Il GDPR è presentato nei suoi elementi essenziali. La lezione L16 lo riprende insieme all'AI Act e alla legge italiana.

### L10: dati fittizi ma realistici

Il questionario del laboratorio contiene domande sul benessere (ore di sonno, pressione percepita, uso dei social di notte): sono il tipo di dati che una scuola raccoglie davvero, e che nessuno studente vorrebbe vedere associati al proprio nome. Il realismo rende evidente il danno della reidentificazione. Tutti i dati sono generati casualmente; i nomi sono combinazioni di nomi e cognomi comuni.

Il notebook contiene un link a OpenStreetMap costruito con le coordinate della foto: indicano piazza Navona a Roma, un luogo pubblico scelto per l'esempio.

### L11: il classificatore come scatola grigia

B.4 non insegna il machine learning: lo usa. Il classificatore è presentato come una "scatola grigia": si conoscono l'ingresso (parole contate), l'uscita (probabilità) e l'idea del funzionamento (frequenze delle parole nelle due classi), senza formule. La parte sul "che cosa ha imparato" (parole più indicative) rende il modello ispezionabile e prepara la lezione sugli attacchi.

Il dataset è costruito combinando un numero limitato di frasi: l'accuratezza è alta (circa 96%) e più ottimistica di quella che si otterrebbe su messaggi reali. Il notebook lo dichiara. È una scelta voluta: un dataset piccolo e controllato permette di ottenere risultati stabili su PC di fascia bassa e di preparare gli attacchi di L12 e L13 sullo stesso oggetto.

### L11: un risultato istruttivo

Il messaggio di frode del falso fornitore (cambio di IBAN con richiesta di riservatezza, lo stesso del corpus di L8) viene classificato come legittimo con probabilità di phishing molto bassa. È un falso negativo istruttivo:

- il dataset di addestramento contiene pochi esempi di frodi basate sul solo testo, senza link né richieste di codici
- il messaggio usa un linguaggio amministrativo simile a quello dei messaggi legittimi

È il limite "dipendenza dai dati" in forma concreta, e riprende il messaggio di L8: contro le frodi BEC la difesa è procedurale.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L10_foto_esempio.jpg` | L10 | immagine sintetica con metadati EXIF inseriti per il corso |
| `L10_questionario_anonimizzato.csv`, `L10_iscritti_torneo.csv` | L10 | dati fittizi |
| `L10_metadati_reidentificazione.ipynb` | L10 | librerie: Pillow, pandas |
| `L11_messaggi.csv` | L11, L12, L13 | 220 messaggi fittizi etichettati |
| `L11_classificatore_phishing.ipynb` | L11 | librerie: pandas, NumPy, scikit-learn |

Tutte le librerie sono disponibili in JupyterLite e in WinPython.

### Checklist

- in JupyterLite, i file di dati vanno caricati nel pannello dei file nella stessa cartella del notebook; senza questo passaggio le celle di lettura restituiscono un errore di file non trovato
- verificare che CyberChef offline contenga l'operazione `Extract EXIF`
- la prima importazione di scikit-learn in JupyterLite richiede alcuni secondi: avvisare gli studenti

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L10 | 25 min: definizioni (4), metadati (5), reidentificazione e k-anonimato (6), inferenza e tracciamento (4), chatbot (3), GDPR (3) | 30 min | 5 min |
| L11 | 25 min: regole e modelli (5), classificatore (7), errori e soglia (5), anomalie e SOC (5), limiti (3) | 30 min | 10-15 min di traccia docenti |

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| "tanto i social tolgono i metadati" | vero per molti social, non per tutti i canali; e lo sfondo della foto resta |
| incomprensione del k-anonimato | contare a mano su una tabella di 8 righe alla lavagna prima del notebook |
| "l'accuratezza è 96%, quindi il filtro è quasi perfetto" | mostrare il falso negativo del messaggio BEC e ricordare che il dataset è semplificato |
| studenti che vogliono inserire i propri messaggi reali nel notebook | solo messaggi inventati; i messaggi reali contengono dati di altre persone |
| confusione tra probabilità e certezza | la probabilità è una stima del modello, non una verità; dipende dai dati di addestramento |

### Il tema dei chatbot in classe

Molti studenti usano assistenti di IA con account personali. La lezione non deve diventare un giudizio sui loro comportamenti: l'obiettivo è che sappiano dove vanno i dati e come regolare le impostazioni. L'esercizio 5 di L10 è individuale e non prevede condivisione dei risultati.

Da verificare con la scuola: quali strumenti di IA sono stati adottati dall'istituto e con quali account, in coerenza con le Linee guida MIM (DM 166/2025). Se la scuola fornisce un servizio con account istituzionali, va indicato agli studenti come prima scelta per le attività scolastiche.

## Considerazioni sugli strumenti per la didattica

### Pandas per la reidentificazione

L'operazione `merge` rende visibile in una riga di codice l'incrocio di due fonti. Anche chi non conosce pandas capisce che cosa accade: due tabelle, tre colonne in comune, una tabella risultante con nomi e risposte. È un esempio efficace di come uno strumento di analisi dei dati diventi uno strumento di violazione della riservatezza.

Esercizi ponte con B.6: calcolare la distribuzione delle dimensioni dei gruppi di quasi-identificatori; provare altre generalizzazioni (fasce d'età, solo genere e anno) e misurare quanta informazione si perde.

### scikit-learn nel corso B.4

scikit-learn è la libreria di riferimento per il machine learning classico in Python ed è usata anche in B.6 e B.8. In B.4 si usano solo quattro elementi (`train_test_split`, `CountVectorizer`, `MultinomialNB`, `confusion_matrix`), sufficienti per addestrare, valutare, ispezionare e attaccare un classificatore.

## Valutazione del modulo

La verifica del modulo 3 (dopo L11) comprende la parte su phishing (vedi traccia docenti M3A) e:

- spiegare perché un insieme di dati senza nomi può non essere anonimo, con un esempio
- indicare tre rischi nell'inserire documenti o dati personali in un chatbot
- interpretare una tabella di falsi positivi e falsi negativi e scegliere una soglia motivandola

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| legge e rimuove i metadati di una foto | L10, esercizi 1 e 2 |
| spiega la reidentificazione per incrocio | L10, esercizio 3 |
| spiega k-anonimato e generalizzazione | L10, esercizio 4 |
| interpreta le parole indicative di un modello | L11, esercizio 2 |
| spiega un errore del classificatore | L11, esercizi 3 e 4 |

## Soluzioni degli esercizi

### L10

- Esercizi 1 e 2: dispositivo "FotoPhone FP-12 Pro", data 12 settembre 2026 ore 17:42, coordinate 41° 53' 57,12" N e 12° 28' 23,2" E, cioè 41,89920 e 12,47311 in gradi decimali: piazza Navona, Roma. La copia salvata dal notebook non contiene metadati.
- Esercizio 3: 18 risposte su 60 vengono attribuite a persone con nome e cognome (tutti gli iscritti al torneo che hanno compilato il questionario). Con data di nascita completa, genere e CAP, ogni combinazione è unica (k = 1).
- Esercizio 4: dopo la generalizzazione k passa da 1 a 6; ogni iscritto corrisponde ad almeno sei risposte possibili e non si può stabilire quale sia la sua. Si perde la data di nascita esatta e il CAP completo, informazioni che per un questionario sul benessere non erano necessarie: il problema andava risolto in fase di progettazione, con la minimizzazione.

### L11

- Esercizio 1: accuratezza circa 0,96 sui 55 messaggi di verifica, con 0 falsi positivi e 2 falsi negativi (i valori possono variare leggermente con versioni diverse delle librerie).
- Esercizio 2: parole indicative di phishing come "account", "inserisci", "bloccato", "link", "sanzioni", "altrimenti" coincidono con le regole di L9 (urgenza, richieste di codici). Il modello trova anche parole che non erano nelle regole e che dipendono dal modo in cui è stato costruito il dataset ("team", "collaborazione", "studenti"): è un esempio di regolarità del dataset che il modello scambia per caratteristiche del phishing. Tra le parole indicative di "legittimo" compaiono "segreteria", "famiglie", "registro", ma anche un numero ("482913") presente in un messaggio legittimo ripetuto: il modello impara anche dettagli irrilevanti.
- Esercizio 3: il messaggio del falso fornitore ottiene una probabilità di phishing bassa (circa 0,1): falso negativo, per le ragioni spiegate sopra.
- Esercizio 4: il messaggio riscritto usa parole tipiche dei messaggi legittimi ("grazie per il tuo acquisto", "ricevuta", "area personale") e toglie quelle tipiche del phishing ("entro 24 ore", "link"): la probabilità scende quasi a zero, ma la richiesta (pagare spese per un pacco) è la stessa. La regola della verifica indipendente non dipende dalle parole: chi verifica la spedizione dall'app ufficiale del corriere non viene ingannato.
- Esercizio 5: con questo dataset i falsi positivi restano a zero per tutte le soglie e i falsi negativi crescono solo con soglie molto alte; in un caso reale la curva sarebbe meno netta. Per la posta della segreteria (molte comunicazioni legittime importanti, rischio di frodi sui pagamenti) una scelta ragionevole è una soglia media con messaggi dubbi spostati in una cartella da controllare invece che eliminati, e procedure di verifica per i pagamenti indipendenti dal filtro.

## Materiale open source

Verifica puntuale per L10-L11: lezioni, dati e notebook sono stati scritti da zero. La foto è un'immagine sintetica creata per il corso.

Materiali di approfondimento:

- GDPR, testo italiano: https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=it
- Garante per la protezione dei dati personali: https://www.garanteprivacy.it/
- L. Sweeney, Simple Demographics Often Identify People Uniquely (2000): https://dataprivacylab.org/projects/identifiability/paper1.pdf
