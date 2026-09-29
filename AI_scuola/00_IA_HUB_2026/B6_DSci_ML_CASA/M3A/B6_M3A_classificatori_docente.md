---
title: "Modulo 3A - Come ragiona un classificatore"
subtitle: "B.6 - Data science e Machine Learning. Traccia docenti"
lang: it
---

# Modulo 3A - Traccia docenti

## Collocazione e finalità del modulo

Le lezioni L7-L9 rispondono alla seconda richiesta della descrizione del corso: come "ragiona" un algoritmo di classificazione.

- L7: il problema della classificazione, affrontato prima senza algoritmi, con regole scritte dagli studenti
- L8: il k-NN, un classificatore basato sulla somiglianza
- L9: l'albero di decisione, che ricava dai dati regole della stessa forma di quelle di L7

Segmento di traccia docenti in aula: 10-15 minuti al termine di L9, sulle attività senza computer e sulla gestione dei gruppi.

## Logica della progettazione

### Prima le regole, poi gli algoritmi

L7 non usa alcun algoritmo di apprendimento. Gli studenti costruiscono un classificatore con le proprie mani, ne misurano l'accuratezza e ne vedono il confine. Questo produce tre effetti:

- i termini (caratteristica, etichetta, previsione, accuratezza, confine) vengono introdotti su un oggetto che gli studenti hanno costruito e capiscono
- la difficoltà di migliorare le regole oltre un certo punto motiva l'apprendimento automatico
- in L9 l'albero addestrato "ritrova" quasi le stesse soglie scelte dagli studenti (206,5 per la pinna e 43,35 per il becco): gli studenti vedono che l'algoritmo fa sistematicamente ciò che loro hanno fatto per tentativi

### Il confine di decisione come rappresentazione comune

Tutti e tre i classificatori vengono mostrati con lo stesso tipo di grafico: il piano becco-pinna colorato con la specie prevista. Il confronto visivo tra regole (segmenti orizzontali e verticali), k-NN (confini irregolari, più lisci al crescere di k) e albero (rettangoli) rende concreta la differenza tra i modelli senza formule. La funzione `disegna_confine` è fornita e non va spiegata nel dettaglio: basta dire che colora ogni punto del piano con la previsione.

La scelta di due sole caratteristiche è didattica: permette il disegno. Gli esercizi di approfondimento mostrano che con quattro caratteristiche l'accuratezza migliora, ma il confine non si può più disegnare.

### Valutare sugli stessi dati: un errore voluto

In L7-L9 l'accuratezza viene calcolata sugli stessi esempi usati per costruire il classificatore. È metodologicamente scorretto, e il materiale lo segnala ogni volta. La scelta è voluta: i risultati "perfetti" del k-NN con k = 1 e dell'albero senza limite di profondità (accuratezza 1,00) creano una tensione che L10 e L11 risolvono. Lo studente che chiede "ma allora k = 1 è il migliore?" ha posto esattamente la domanda da cui parte L10.

### Matematica richiesta

- distanza euclidea: teorema di Pitagora, noto dal primo biennio; l'estensione a più dimensioni è presentata come "si sommano più quadrati"
- impurità di Gini: frazioni, quadrati, media pesata; l'interpretazione probabilistica è citata ma non necessaria
- standardizzazione: media e deviazione standard, già viste in L4

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L7_schede_pinguini.md` | L7 | da stampare, una copia per gruppo; ritagliare le righe come schede |
| `L7_schede_pinguini.csv` | L7 | le stesse 24 schede con la specie, per il notebook |
| `L7_regole.ipynb` e `_soluzioni` | L7 | pandas, NumPy, matplotlib |
| `L8_knn.ipynb` e `_soluzioni` | L8 | con scikit-learn |
| `L9_albero.ipynb` e `_soluzioni` | L9 | con scikit-learn |
| `pinguini.csv` | L7-L9 | |

### Preparare le schede di L7

Le 24 schede sono state estratte a caso, 8 per specie, e includono alcuni casi difficili. Suggerimento: scrivere la specie sul retro delle schede P01-P12 (esempi di addestramento) e tenere nascosta quella delle schede P13-P24 fino alla verifica.

Chiave delle schede:

| scheda | specie | scheda | specie | scheda | specie |
|---|---|---|---|---|---|
| P01 | Gentoo | P09 | Chinstrap | P17 | Gentoo |
| P02 | Adelie | P10 | Adelie | P18 | Gentoo |
| P03 | Gentoo | P11 | Chinstrap | P19 | Gentoo |
| P04 | Adelie | P12 | Adelie | P20 | Chinstrap |
| P05 | Chinstrap | P13 | Gentoo | P21 | Gentoo |
| P06 | Gentoo | P14 | Adelie | P22 | Chinstrap |
| P07 | Adelie | P15 | Adelie | P23 | Chinstrap |
| P08 | Chinstrap | P16 | Adelie | P24 | Chinstrap |

Casi difficili: P16 (Adelie con becco di 43,2 mm), P22 (Chinstrap con becco di 42,5 mm), P03 (Gentoo con becco corto ma pinna e profondità tipiche dei Gentoo), P02 e P04 (Adelie con pinna di 200-201 mm).

### Checklist tecnica

- la prima importazione di scikit-learn in JupyterLite richiede alcuni secondi
- i grafici del confine calcolano previsioni su 62.500 punti: su PC molto lenti il k-NN può richiedere qualche secondo per grafico
- stampare in anticipo le schede e preparare forbici o schede già ritagliate

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L7 | 20 min: tipi di apprendimento (4), termini (4), regole (5), confine (4), limiti (3) | 12 min senza computer + 20 min notebook | 5 min |
| L8 | 25 min: idea (4), distanza (5), esempio a mano (5), scikit-learn (5), k (3), scala (3) | 30 min | 5 min |
| L9 | 20 min: struttura (3), scelta delle domande (4), Gini (6), albero dei pinguini (4), profondità e importanza (3) | 30 min | 10-15 min di traccia docenti |

### Attività senza computer

Le attività senza computer (unplugged) sono usate per introdurre ogni algoritmo prima del codice:

- L7: regole sulle schede, a gruppi di 3-4
- L8: k-NN "umano": il docente traccia alla lavagna (o sul pavimento con nastro adesivo) un piano con alcuni punti colorati; uno studente è il "nuovo pinguino" e conta i vicini entro un certo raggio
- L9: Gini a mano sulle due divisioni candidate; poi, a gruppi, costruire un albero di profondità 2 per le 24 schede, scegliendo la prima domanda con il calcolo del Gini

Indicazioni per la conduzione:

- dare un tempo stretto (10-12 minuti): la pressione spinge verso regole semplici, che si confrontano meglio
- raccogliere le regole dei gruppi alla lavagna e confrontarle: gruppi diversi trovano soglie diverse con accuratezze simili; è un'osservazione utile per L11 (modelli diversi, prestazioni simili)
- far notare che le schede più difficili sono quelle vicine al confine

### Gestione dei gruppi

- gruppi di 3-4 per le attività senza computer, coppie al computer
- ruoli espliciti nelle attività senza computer: chi legge le misure, chi applica le regole, chi registra
- gruppi eterogenei per esperienza di programmazione, con lo studente meno esperto alla tastiera

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| regole con condizioni che si sovrappongono o lasciano casi scoperti | ricordare che le regole si applicano in ordine e che l'ultima è "altrimenti" |
| "le mie regole hanno 100% sulle 12 schede" | verificarle sulle altre 12 e poi su tutti i 342 pinguini |
| confusione tra `X` (caratteristiche) e `y` (etichette) | disegnare alla lavagna la tabella divisa in due parti |
| distanza calcolata senza radice o senza quadrati | ripartire dal teorema di Pitagora con un triangolo sul piano |
| standardizzazione vista come "trucco" | chiedere di confrontare 10 mm di becco e 10 g di massa: quale differenza conta di più per un pinguino? |
| `value` di `plot_tree` interpretato come valori delle misure | spiegare che sono conteggi per specie, in ordine alfabetico |
| Gini confuso con l'accuratezza | Gini misura la mescolanza del gruppo, non gli errori del modello |
| "l'albero senza limite è perfetto" | rinviare esplicitamente a L10-L11, scrivendo la domanda alla lavagna |

## Considerazioni sugli strumenti per la didattica

### Notebook con funzioni di supporto

I notebook di questo modulo contengono una funzione di supporto (`disegna_confine`) che gli studenti usano senza doverne capire il codice. È una scelta comune nella didattica con i notebook: lo strumento rende visibile un concetto (il confine) che sarebbe troppo costoso costruire. È opportuno dichiararlo esplicitamente agli studenti ("questa cella è uno strumento, non un argomento") per evitare che si sentano obbligati a capire ogni riga.

### Visualizzazioni interattive

Come dimostrazione alla cattedra o approfondimento:

- MLU-Explain, Decision Trees: spiegazione visuale interattiva di come un albero sceglie le divisioni (usa l'entropia invece dell'impurità di Gini). https://mlu-explain.github.io/decision-tree/
- TensorFlow Playground non è adatto a questo modulo (reti neurali, trattato in B.8)

### Collegamento con B.8 e B.4

- B.8 costruisce un neurone che separa le classi con una retta: il confine di decisione di un neurone è una retta, quello di un albero una serie di rettangoli, quello di un k-NN una linea irregolare. Il confronto è un buon esercizio ponte
- B.4 (L11) usa un classificatore Naive Bayes per il phishing: la tabella degli errori di L7 è la stessa matrice di confusione usata per i falsi positivi e falsi negativi

## Valutazione del modulo

Gli indicatori confluiscono nella verifica del modulo 3, al termine di L11 (traccia docenti M3B).

| Indicatore | Osservabile in |
|---|---|
| scrive regole di classificazione coerenti e ne misura l'accuratezza | L7, esercizi 1-3 |
| interpreta un confine di decisione | L7, esercizio 4; L8, esercizio 3; L9, esercizio 3 |
| calcola una distanza e applica il k-NN a mano | L8, esercizio 1 |
| spiega l'effetto della scala | L8, esercizio 4 |
| calcola l'impurità di Gini e sceglie una divisione | L9, esercizio 1 |
| legge un albero addestrato | L9, esercizio 2 |

## Soluzioni degli esercizi

### L7

- Esercizio 1: soluzioni aperte. Regole tipiche: "pinna oltre 205-210 mm allora Gentoo" oppure "profondità del becco sotto 16-17 mm allora Gentoo"; poi "becco oltre 43-45 mm allora Chinstrap"; altrimenti Adelie.
- Esercizio 2: con le regole di esempio (pinna > 206, becco > 43) l'accuratezza sulle schede è 0,917: sbagliano P16 (Adelie con becco 43,2, prevista Chinstrap) e P22 (Chinstrap con becco 42,5, prevista Adelie).
- Esercizio 3: accuratezza su 342 pinguini 0,944, 19 errori. L'accuratezza sulle schede è più bassa perché il campione di 24 contiene per caso due casi di confine su 24; con pochi esempi la stima dell'accuratezza varia molto. È anche un'occasione per notare che le regole scritte guardando le schede P01-P12 dovrebbero essere verificate su esempi diversi.
- Esercizio 4: il confine è formato da una linea orizzontale (pinna 206) e da un segmento verticale (becco 43). Gli errori si concentrano nella zona di sovrapposizione tra Adelie e Chinstrap (becco 40-46 mm) e ai margini della zona dei Gentoo. Spostando le soglie si arriva al più a circa 0,95; oltre servono regole più complesse.
- Esercizio 5: con la regola "profondità < 16,5 allora Gentoo; becco > 44 allora Chinstrap" l'accuratezza è 0,924. Con soglie diverse si ottengono valori simili: la profondità del becco separa bene i Gentoo, ma le soglie sul becco vanno riviste.

### L8

- Esercizio 1: distanze C1 3,35; A2 4,92; C2 6,73; A1 15,19; G1 16,04; G2 25,50. Previsioni: k = 1 Chinstrap; k = 3 Chinstrap (2 a 1); k = 5 parità tra Chinstrap e Adelie (2 a 2): scikit-learn sceglierebbe Adelie, prima in ordine alfabetico.
- Esercizio 2: accuratezza sui dati di addestramento 1,000 (k = 1), 0,962 (k = 5), 0,944 (k = 25).
- Esercizio 3: con k = 1 il confine è frastagliato, con isole attorno ai singoli pinguini fuori posto; con k = 25 è regolare. Per pinguini nuovi è più credibile un confine intermedio (k = 5 o simile).
- Esercizio 4: senza standardizzazione 0,839, con standardizzazione 0,956. Senza standardizzazione la distanza è dominata dalla massa (differenze di centinaia di grammi contro pochi millimetri): il modello decide quasi solo con la massa, che separa i Gentoo ma non Adelie e Chinstrap, e le zone diventano strisce orizzontali.
- Esercizio 5: con quattro misure standardizzate l'accuratezza sui dati di addestramento è 0,991. Con quattro caratteristiche lo spazio ha quattro dimensioni e non si può disegnare su un piano.

### L9

- Esercizio 1: Gini del gruppo 0,66; divisione A 0,343; divisione B 0,300; l'algoritmo sceglie B perché produce gruppi più puri.
- Esercizio 2: l'albero ha le soglie pinna 206,5 e becco 43,35 (più una soglia becco 40,85 per un singolo Adelie con pinna lunga); accuratezza 0,953. Il pinguino con becco 45 e pinna 195 va a sinistra alla radice (195 <= 206,5) e a destra al secondo nodo (45 > 43,35): Chinstrap.
- Esercizio 3: profondità 1: una sola domanda (pinna <= 206,5) e due foglie, Adelie e Gentoo; Chinstrap non viene mai prevista perché in nessuna delle due foglie è la specie più frequente (accuratezza 0,792). Profondità 2 e 3: 0,953. Senza limite: profondità 7, 27 foglie, 1,000; il confine contiene piccoli rettangoli attorno a singoli pinguini.
- Esercizio 4: con le quattro misure e profondità 3 (accuratezza 0,971) le importanze sono pinna 0,559, becco lunghezza 0,361, becco profondità 0,066, massa 0,014. Coincide con le osservazioni di L6: pinna (o profondità del becco) per i Gentoo, lunghezza del becco per Adelie e Chinstrap. La massa è quasi inutile perché la sua informazione è già contenuta nella pinna. Nell'albero compaiono divisioni che portano alla stessa classe in entrambe le foglie: riducono l'impurità senza cambiare le previsioni.
- Esercizio 5: `min_samples_leaf` 1: 27 foglie, 1,000; 5: 14 foglie, 0,971; 20: 8 foglie, 0,950. Il confine diventa più semplice al crescere del minimo.

## Materiale open source

Verifica puntuale per L7-L9: lezioni, schede, figure e notebook sono stati prodotti da zero. L'idea di introdurre la classificazione con regole scritte a mano prima degli algoritmi è diffusa nella didattica dell'IA (attività "unplugged"). Materiali correlati:

- Microsoft, ML for Beginners, sezione Classification (licenza MIT): https://github.com/microsoft/ML-For-Beginners
- scikit-learn, Getting Started: https://scikit-learn.org/stable/getting_started.html
- MLU-Explain, spiegazioni visuali interattive (alberi di decisione): https://mlu-explain.github.io/
