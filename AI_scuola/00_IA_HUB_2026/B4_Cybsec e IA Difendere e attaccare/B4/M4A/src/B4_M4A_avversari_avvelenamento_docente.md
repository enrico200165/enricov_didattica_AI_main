---
title: "Modulo 4A - Esempi avversari e avvelenamento dei dati"
subtitle: "B.4 - Cybersicurezza e IA. Traccia docenti"
lang: it
---

# Modulo 4A - Traccia docenti

## Collocazione e finalità del modulo

Le lezioni L12 e L13 aprono il modulo 4, dedicato all'IA come bersaglio di attacchi:

- L12 presenta la superficie di attacco di un sistema di IA e gli esempi avversari (evasione)
- L13 tratta l'avvelenamento dei dati e le backdoor

Entrambe le lezioni usano lo stesso oggetto costruito in L11, il filtro antiphishing, e lo stesso dataset `L11_messaggi.csv`. Gli studenti vedono il filtro da tre punti di vista: strumento di difesa (L11), bersaglio di evasione (L12), bersaglio di avvelenamento (L13). Le lezioni L14 e L15 (modulo 4B) passano ai modelli linguistici.

Il modulo non prevede un segmento dedicato di traccia docenti in aula; il segmento successivo è al termine di L15.

## Logica della progettazione

### Il punto di vista del difensore

I laboratori sono costruiti come attività di valutazione della sicurezza, non come esercizi di attacco fine a sé stesso:

- in L12 lo studente misura la robustezza del filtro, cioè quanti messaggi fraudolenti possono essere modificati per passare, e valuta una difesa
- in L13 lo studente riceve un dataset con una backdoor e deve trovarla, rimuoverla e verificare la bonifica

Le tecniche di attacco restano quelle necessarie per capire il meccanismo e sono applicate solo al filtro didattico, su dati fittizi, in locale. Non si usano servizi reali né messaggi reali.

### L12: dall'immagine al testo

La dimostrazione con adversarial.js rende visibile il fenomeno (un disturbo invisibile cambia la classe di un'immagine). Il notebook lo trasferisce a un caso che gli studenti conoscono dal modulo 3: un messaggio fraudolento che resta identico nella richiesta ma cambia classificazione. Il messaggio didattico centrale è che il modello decide in base a regolarità statistiche, non al significato: la stessa osservazione fatta in L11 sulle parole "sorprendenti" (per esempio il numero `482913`).

Il risultato dell'esercizio 5 (l'addestramento con esempi avversari blocca gli attacchi noti ma non una nuova ricerca) chiude il cerchio con L8: la difesa che non dipende dalle parole è la verifica indipendente.

### L13: backdoor invisibile ai controlli ordinari

L'esperimento principale mostra una tabella in cui l'accuratezza resta ferma a 0,964 mentre i messaggi fraudolenti con il grilletto riconosciuti scendono da 25 a 3 su 27. È l'osservazione su cui costruire la lezione: un controllo di qualità basato solo sull'accuratezza non vede la backdoor.

L'inversione casuale delle etichette è trattata per contrasto: è un attacco rumoroso, che si nota.

L'esercizio 4 (dataset ricevuto) è l'attività più vicina al lavoro reale: tre controlli semplici, ciascuno con un proprio limite, che insieme portano al risultato.

### Riferimenti recenti

Lo studio di Anthropic, UK AI Security Institute e Alan Turing Institute (ottobre 2025) sui circa 250 documenti sufficienti per inserire una backdoor in modelli linguistici di dimensioni diverse collega il laboratorio, basato su un modello minimo, ai modelli linguistici trattati in L14. Il dato da sottolineare è che conta il numero assoluto di documenti avvelenati, non la loro percentuale.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L11_messaggi.csv` | L12, L13 | lo stesso file di L11, 220 messaggi fittizi etichettati |
| `L12_robustezza_filtro.ipynb` | L12 | librerie: pandas, NumPy, scikit-learn |
| `L13_avvelenamento_backdoor.ipynb` | L13 | librerie: pandas, NumPy, scikit-learn, matplotlib |
| `L13_dataset_ricevuto.csv` | L13 | 195 messaggi: i 165 di addestramento di L11 più 30 messaggi avvelenati con un grilletto |

Tutte le librerie sono disponibili in JupyterLite e in WinPython.

### Checklist

- in JupyterLite, caricare i file CSV nella stessa cartella del notebook
- verificare in anticipo che adversarial.js si apra sulle postazioni: il primo caricamento scarica i modelli e può richiedere alcuni secondi; l'attacco Carlini & Wagner è il più lento
- in alternativa offline, il docente mostra adversarial.js dalla propria postazione oppure si usano le immagini dell'articolo di Goodfellow e colleghi
- la ricerca automatica della sezione 4 di L12 e la cella dell'esercizio 5 richiedono qualche decina di secondi su un PC di fascia bassa in JupyterLite; avvisare gli studenti di attendere
- non anticipare agli studenti il grilletto contenuto in `L13_dataset_ricevuto.csv`

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L12 | 30 min: ciclo di vita e tassonomia (8), esempi avversari e casi reali (10), vulnerabilità (5), difese (7) | 25 min | 5 min |
| L13 | 25 min: definizioni e obiettivi (5), inversione (4), backdoor (6), casi reali (5), difese (5) | 30 min | 5 min |

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| "basta addestrare il modello anche sugli esempi avversari" | mostrare l'esercizio 5 di L12: la nuova ricerca fa passare di nuovo tutti i messaggi |
| confusione tra evasione e avvelenamento | chiedere "quando agisce l'attaccante: prima o dopo l'addestramento?" |
| "l'accuratezza è rimasta uguale, quindi il modello è a posto" | è esattamente la proprietà della backdoor: tabella dell'esercizio 2 di L13 |
| il grilletto cercato come parola sensata | il grilletto è scelto per essere raro; la parola comune è meno efficace (esercizio 3) |
| il controllo incrociato segnala anche messaggi non avvelenati | è previsto: segnala i casi da esaminare, la decisione è di una persona |
| aspettative esagerate sugli attacchi ai veicoli autonomi | gli esperimenti citati sono di ricerca, in condizioni controllate; i sistemi reali combinano più sensori e controlli |

### Il tema etico

Il laboratorio mostra come far passare un messaggio fraudolento da un filtro. Conviene esplicitare in aula tre punti, già introdotti in L1:

- l'esperimento si svolge su un filtro didattico, costruito dalla classe, con dati fittizi
- ingannare filtri o sistemi di terzi senza autorizzazione è un'attività illecita, e l'invio di messaggi fraudolenti è comunque un reato
- chi si occupa professionalmente di questi test (red team) lavora con un incarico scritto, su sistemi del committente

## Considerazioni sugli strumenti per la didattica

### adversarial.js

Punti di forza: eseguito interamente nel browser, senza installazione e senza invio di dati a un server; quattro modelli e cinque attacchi di forza diversa; visualizzazione del disturbo.

Limiti: interfaccia in inglese; richiede una connessione per il primo caricamento; i modelli sono piccoli e didattici.

### Il filtro Naive Bayes come bersaglio

Un modello a sacchetto di parole rende gli attacchi comprensibili senza matematica: si vede quali parole spostano la decisione e perché. Il limite da dichiarare è che gli attacchi ai modelli moderni (reti neurali, modelli linguistici) sono più sofisticati, ma il principio è lo stesso: il modello segue regolarità statistiche che l'attaccante può sfruttare.

Esercizi ponte con B.6:

- ripetere gli esperimenti di L12 con `CountVectorizer(binary=True)` (presenza delle parole invece dei conteggi): la ripetizione della stessa parola non funziona più, ma la ricerca trova combinazioni di parole diverse
- confrontare la robustezza di Naive Bayes con quella di una regressione logistica

Esercizio ponte con B.8: scrivere una versione di `aggiungi_parole` che non ripete la stessa parola, e una funzione che conta i caratteri invisibili in un testo.

## Valutazione del modulo

La verifica del modulo 4 si svolge dopo L15 e comprende, per la parte M4A:

- classificare cinque scenari come evasione, avvelenamento, estrazione del modello, inferenza sui dati di addestramento, catena di fornitura
- spiegare perché una backdoor non si scopre controllando l'accuratezza
- proporre due controlli per un dataset ricevuto da una fonte esterna

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| spiega un esempio avversario e perché funziona | L12, esercizi 1 e 4 |
| valuta una difesa e ne riconosce i limiti | L12, esercizio 5 |
| distingue attacco rumoroso e backdoor | L13, esercizi 1 e 2 |
| applica controlli sui dati e interpreta i risultati | L13, esercizio 4 |
| formula regole per l'uso di dati e modelli esterni | L13, esercizio 5 |

## Soluzioni degli esercizi

I valori sono stati ottenuti eseguendo i notebook; possono variare leggermente con versioni diverse delle librerie.

### L12

- Esercizio 1: con l'attacco più debole la classe può restare invariata o cambiare solo in parte; con Carlini & Wagner il segnale viene classificato come un altro segnale con alta confidenza. Il disturbo del secondo attacco è praticamente invisibile a occhio; quello del primo, più grossolano, si nota come una leggera grana.
- Esercizio 2: le parole più indicative di "legittimo" sono "presto", "segreteria", "buongiorno", "domani", "dei", "famiglie", "gentili", "registro", "alle", "si", "regolarmente", "scienze", "482913", "richiesto", "condividerlo". Alcune richiamano il contesto scolastico dei messaggi legittimi del dataset; altre ("dei", "alle", "si", "482913") non hanno alcun legame con la legittimità. Descrivono il dataset, non la legittimità.
- Esercizio 3: l'aggiunta breve "gentili famiglie registro" lascia la probabilità a 1,000; l'aggiunta lunga "buongiorno gentili famiglie, circolare nel registro elettronico, lezioni regolarmente" la porta a 0,031. La soluzione più breve trovata dalla ricerca automatica è ripetere sei volte "presto" (probabilità 0,39): il modello conta le occorrenze, quindi ripetere una parola "legittima" ne moltiplica l'effetto.
- Esercizio 4: 25 messaggi fraudolenti riconosciuti su 27; dopo le aggiunte passano tutti e 25, con 7,2 parole aggiunte in media. La richiesta non cambia. Il procedimento funziona perché il modello somma il contributo di ogni parola indipendentemente dal significato e dall'ordine: basta aggiungere abbastanza parole "legittime" per superare il contributo di quelle "fraudolente". Una persona che verifica mittente e richiesta attraverso un canale indipendente non viene ingannata.
- Esercizio 5: il filtro addestrato con esempi avversari mantiene l'accuratezza (0,964) e riconosce tutti i 25 messaggi modificati; una nuova ricerca sul nuovo filtro fa passare di nuovo 25 messaggi su 25. Le difese che non dipendono dal testo: verifica del dominio del mittente e di SPF, DKIM, DMARC (L2), reputazione dei link, verifica attraverso un canale indipendente (L8), procedure di doppia approvazione per i pagamenti (L9).

### L13

- Esercizio 1: accuratezza media 0,964 con 0% e 10% di etichette invertite, 0,956 con 20%, 0,924 con 30%, 0,796 con 40%, 0,531 con 50%. Il danno diventa evidente dal 30-40%. L'attacco è facile da notare perché il calo di accuratezza compare nei controlli ordinari, e perché serve manipolare una parte molto ampia dei dati.
- Esercizio 2: con 0, 5, 10, 20, 30 messaggi avvelenati l'accuratezza resta 0,964; i messaggi fraudolenti con il grilletto riconosciuti sono 25, 23, 19, 10, 3 su 27. Chi controlla solo l'accuratezza non vede nulla, perché i messaggi di verifica non contengono il grilletto.
- Esercizio 3: con 30 messaggi avvelenati, i messaggi fraudolenti con il grilletto riconosciuti sono 24 su 27 con la parola comune "grazie", 23 con la parola rara singola "zefiro", 3 con `Rif. pratica ZQ7 KX4 MW9`. Un grilletto formato da più sequenze rare (codici alfanumerici) funziona meglio di una parola comune o di una parola singola: le sequenze rare compaiono solo nei messaggi avvelenati, quindi il modello le associa con forza a "legittimo", e ogni sequenza aggiunge il proprio contributo. Una parola comune compare anche in altri messaggi e il suo effetto si diluisce.
- Esercizio 4: le proporzioni sono cambiate (112 legittimi e 83 phishing invece di 82 e 83: 30 messaggi "legittimi" in più); l'accuratezza del filtro addestrato sui dati ricevuti resta 0,964; tra le parole più indicative di "legittimo" compaiono ai primi cinque posti "prot", "lt2", "qx8", "nb6", "vr5". Il controllo incrociato segnala 14 messaggi, 7 dei quali contengono la sequenza sospetta; gli altri 7 sono messaggi fraudolenti autentici difficili da classificare (falso fornitore, "ciao mamma ho cambiato numero", falso allenatore). Il grilletto è `Prot. QX8 LT2 VR5 NB6`. Le proporzioni da sole indicano solo che qualcosa è cambiato; le parole indicative rivelano il grilletto; il controllo incrociato individua i messaggi ma segnala anche casi legittimamente difficili.
- Esercizio 5: con `grilletto_trovato = "Prot. QX8 LT2 VR5 NB6"` vengono rimossi 30 messaggi. Con i dati ricevuti i messaggi fraudolenti con il grilletto riconosciuti sono 4 su 27; con i dati bonificati tornano 25 su 27, con accuratezza invariata. Regole possibili: accettare dati e modelli solo da fonti note e con impronta verificata; confrontare ogni nuova versione dei dati con la precedente (proporzioni, messaggi aggiunti); prima della messa in uso, confrontare il nuovo modello con il precedente su un insieme di prova fisso che contiene anche casi critici.

## Materiale open source

Verifica puntuale per L12-L13: lezioni, notebook e dati sono stati scritti da zero. La dimostrazione adversarial.js è usata come strumento online, senza riproduzione di contenuti.

Materiali di approfondimento:

- NIST AI 100-2 E2025, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations: https://csrc.nist.gov/pubs/ai/100/2/e2025/final
- MITRE ATLAS: https://atlas.mitre.org/
- adversarial.js: https://kennysong.github.io/adversarial.js/
- I. Goodfellow, J. Shlens, C. Szegedy, Explaining and Harnessing Adversarial Examples (2014): https://arxiv.org/abs/1412.6572
- K. Eykholt et al., Robust Physical-World Attacks on Deep Learning Visual Classification (2018): https://arxiv.org/abs/1707.08945
- T. Gu, B. Dolan-Gavitt, S. Garg, BadNets (2017): https://arxiv.org/abs/1708.06733
- N. Carlini et al., Poisoning Web-Scale Training Datasets is Practical (2023): https://arxiv.org/abs/2302.10149
- B. Nelson et al., Exploiting Machine Learning to Subvert Your Spam Filter (2008): https://people.eecs.berkeley.edu/~tygar/papers/SML/Spam_filter.pdf
- Anthropic, A small number of samples can poison LLMs of any size (2025): https://www.anthropic.com/research/small-samples-poison
- Hugging Face, Pickle Scanning: https://huggingface.co/docs/hub/security-pickle
