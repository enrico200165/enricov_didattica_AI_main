---
title: "Modulo 4A - Regressione e immagini"
subtitle: "B.6 - Data science e Machine Learning. Traccia docenti"
lang: it
---

# Modulo 4A - Traccia docenti

## Collocazione e finalità del modulo

Il modulo 4 allarga il quadro oltre la classificazione di dati tabellari:

- L12: il "piccolo modello predittivo" della descrizione del corso nella forma più semplice, la regressione lineare
- L13: la classificazione di immagini, con uno strumento senza codice e un'alternativa offline

Segmento di traccia docenti in aula: 10-15 minuti al termine di L13, sugli strumenti di IA senza codice, sulle condizioni d'uso con studenti minorenni e sulle alternative.

## Logica della progettazione

### L12: stessa interfaccia, nuovo tipo di problema

La regressione è presentata come variante dello schema già noto (caratteristiche, etichetta, `fit`, `predict`, addestramento e verifica, baseline). Cambia solo la misura dell'errore. Questo rafforza l'idea che i concetti di valutazione del modulo 3 valgono per qualunque modello.

La retta si interpreta nel contesto: 50 g per millimetro di pinna è una quantità comprensibile, l'intercetta negativa è un'ottima occasione per discutere la differenza tra "strumento di calcolo" e "significato fisico", che prepara la discussione sull'estrapolazione.

La codifica one-hot compare qui perché serve: senza di essa non si possono usare specie e sesso. L'esempio delle tre rette parallele (una per specie) dà un'immagine concreta di che cosa fa il modello con una variabile qualitativa.

Il metodo dei minimi quadrati è solo nominato: la ricerca dei parametri per approssimazioni successive è l'oggetto di B.8 (discesa del gradiente). Nelle classi con buone basi di matematica si può mostrare la formula della pendenza (covarianza diviso varianza) e verificarla con NumPy.

### L13: la raccolta di dati nel mondo delle immagini

La descrizione del corso chiede come si raccoglie un dataset: L13 riprende il tema su un tipo di dati diverso e rende tangibili, in pochi minuti, fenomeni che con i dati tabellari restano astratti:

- la varietà dei dati di addestramento determina dove il modello funziona
- lo sbilanciamento delle classi sposta le previsioni
- il modello sceglie sempre una classe, anche quando nessuna è giusta
- le scorciatoie: il modello impara lo sfondo

La scorciatoia costruita apposta (esercizio 3) prepara L14: lo stesso meccanismo, applicato a dati che riguardano persone, produce discriminazioni.

### Perché uno strumento senza codice

Addestrare un classificatore di immagini con codice richiede librerie (TensorFlow, PyTorch) che non si installano su PC di fascia bassa e concetti (reti convoluzionali) che appartengono a B.8. Teachable Machine permette di concentrarsi sui dati. Il rischio è la "scatola nera": la lezione lo contrasta mostrando la corrispondenza tra i comandi dello strumento e i concetti del corso (tabella della lezione) e con l'alternativa offline, in cui il modello è un k-NN già noto.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L12_regressione.ipynb` e `_soluzioni` | L12 | scikit-learn |
| `pinguini.csv`, `tragitti_puliti.csv` | L12 | |
| `L13_scheda_teachable_machine.md` | L13 | una copia per gruppo |
| `L13_cifre_offline.ipynb` e `_soluzioni` | L13 | alternativa offline; dataset incluso in scikit-learn |

### Teachable Machine: verifiche preliminari

- raggiungibilità del sito dalla rete della scuola e funzionamento con il browser delle postazioni (Chrome o Edge recenti funzionano meglio)
- webcam: presenza, permesso di accesso nel browser (la prima volta il browser chiede l'autorizzazione), eventuali blocchi imposti dall'amministratore di sistema
- prestazioni: l'addestramento avviene sul PC; su macchine molto lente può richiedere un minuto o più; ridurre il numero di immagini (30 per classe bastano)
- oggetti: preparare set di tre oggetti per gruppo, di forma e colore diversi; fogli colorati per cambiare sfondo; una lampada

### Condizioni d'uso e riservatezza

- Teachable Machine non richiede account per addestrare e provare un modello; le immagini restano nel browser finché non si salva il progetto (su Google Drive o come file)
- regola del laboratorio: si fotografano solo oggetti, mai volti o persone. Le immagini di volti di studenti sono dati personali, e un modello addestrato su di esse ne conserva informazioni
- non salvare progetti con immagini su account personali; se serve conservarli, salvarli come file nelle cartelle della scuola
- verificare le regole dell'istituto sull'uso di servizi online con studenti minorenni (Linee guida MIM sull'introduzione dell'IA nelle scuole)

### Alternativa senza webcam o senza rete

Il notebook `L13_cifre_offline.ipynb` copre gli stessi concetti con il dataset delle cifre di scikit-learn, disponibile offline in JupyterLite e WinPython: immagini come tabelle di numeri, classificazione con k-NN, analisi degli errori, e una scorciatoia simulata. Nella scorciatoia un albero di decisione addestrato con una macchia nell'angolo delle sole immagini di 7 non riconosce più nessun 7 senza macchia e classifica come 7 qualunque immagine con la macchia.

Seconda alternativa: dimostrazione alla cattedra di Teachable Machine con una sola webcam, con gli studenti che propongono le prove.

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L12 | 25 min: regressione (3), retta dei pinguini (5), minimi quadrati (3), errori e baseline (5), one-hot (5), estrapolazione (4) | 30 min | 5 min |
| L13 | 20 min: pixel (4), perché i pixel non bastano (4), trasferimento (4), Teachable Machine (4), dataset e scorciatoie (4) | 30 min | 10-15 min di traccia docenti |

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| intercetta negativa vista come errore | è un parametro geometrico; far calcolare la massa prevista per 0 mm e discutere se ha senso |
| MAE e RMSE confusi | calcolarli a mano su tre residui, per esempio 10, -10, 40: MAE 20, RMSE circa 24,5 |
| codifica della specie come 1, 2, 3 | chiedere che cosa significherebbe "Chinstrap = 2" in una somma pesata |
| coefficiente della pinna che cambia aggiungendo il sesso | spiegare che la pinna "rappresentava" in parte anche sesso e specie |
| in Teachable Machine il modello funziona subito "perfettamente" | è il dataset facile provato nelle stesse condizioni: è la stessa trappola della valutazione sui dati di addestramento (L10) |
| percentuali di Teachable Machine lette come certezza | sono probabilità stimate dal modello; il modello può essere sicuro e sbagliato |
| studenti che fotografano sé stessi o i compagni | ribadire la regola degli oggetti; spiegarne il motivo (dati personali, anche biometrici) |

## Considerazioni sugli strumenti per la didattica

### Strumenti di IA senza codice

Strumenti come Teachable Machine (e, per altri tipi di dati, ambienti visuali come Orange Data Mining) sono utili nella didattica se:

- l'attività è centrata sui dati e sulla valutazione, non sullo strumento
- si esplicita la corrispondenza tra comandi dello strumento e concetti
- si prevede un momento critico: che cosa non funziona e perché

Sono rischiosi se usati per produrre risultati "magici" senza analisi, perché rafforzano l'idea dell'IA come scatola nera che funziona sempre.

### Approfondimento per il docente

- Google Codelab, costruire un "Teachable Machine" con TensorFlow.js e l'apprendimento per trasferimento (richiede programmazione JavaScript): https://codelabs.developers.google.com/tensorflowjs-transfer-learning-teachable-machine
- Collegamento con B.8: gli studenti di B.8 che hanno costruito un neurone e una piccola rete possono riconoscere nella "parte finale" addestrata da Teachable Machine uno strato di neuroni come quelli costruiti a mano

## Valutazione del modulo

Gli indicatori confluiscono nella verifica del modulo 4 (traccia docenti M4B).

| Indicatore | Osservabile in |
|---|---|
| interpreta pendenza e intercetta | L12, esercizio 1 |
| valuta un modello di regressione con MAE e baseline | L12, esercizio 2 |
| usa e spiega la codifica one-hot | L12, esercizio 3 |
| riconosce i rischi dell'estrapolazione | L12, esercizio 4 |
| progetta un dataset di immagini vario e bilanciato | L13, esercizi 1 e 4 |
| riconosce e spiega una scorciatoia | L13, esercizio 3 |

## Soluzioni degli esercizi

### L12

- Esercizio 1: massa = 50,0 x pinna - 5848,7; ogni millimetro di pinna in più corrisponde in media a 50 g in più; l'intercetta non ha significato fisico. Pinna di 200 mm: 4155,4 g.
- Esercizio 2: i residui hanno media 0 (proprietà della retta dei minimi quadrati) e una distribuzione approssimativamente simmetrica. MAE 289,7 g, RMSE 370,7 g, baseline 642,8 g: la retta dimezza l'errore.
- Esercizio 3: pinna e specie: MAE 258,1; coefficienti pinna 40,7, Chinstrap -174,2, Gentoo 280,5 (un Gentoo pesa in media 280 g più di un Adelie con la stessa pinna). Con il sesso: MAE 217,4; maschio +554,3 g; il coefficiente della pinna scende a 20,0 e quello dei Gentoo sale a 834,2, perché specie e sesso spiegano ora una parte della massa prima attribuita alla pinna.
- Esercizio 4: previsioni -847 g (100 mm), 1654 g (150 mm), 4155 g (200 mm), 6656 g (250 mm), 9157 g (300 mm). Assurde quelle per 100 mm (massa negativa) e per 300 mm; anche 150 e 250 mm sono fuori dai dati e non affidabili.
- Esercizio 5: con la sola distanza tempo = 2,24 x distanza + 13,1, MAE 7,1 minuti; con il mezzo MAE 4,2 minuti; il riferimento è l'auto (prima in ordine alfabetico): il bus aggiunge circa 17,6 minuti, andare a piedi 9,2 (a parità di distanza), il treno -13,4 (più veloce sulle lunghe distanze). Il mezzo determina sia la velocità sia i tempi fissi (attese, fermate).

### L13

- Esercizio 1: con un dataset "facile" il modello riconosce gli oggetti quasi al 100% nelle stesse condizioni.
- Esercizio 2: prestazioni in calo con sfondo, luce e distanza diversi; l'oggetto nuovo e l'inquadratura vuota vengono comunque assegnati a una delle tre classi, spesso con percentuali alte: il modello conosce solo quelle classi.
- Esercizio 3: con la classe 1 su sfondo bianco e le altre su sfondo scuro, qualunque oggetto su sfondo bianco viene classificato come classe 1: il modello ha imparato lo sfondo.
- Esercizio 4: il dataset vario è più robusto a sfondo, luce e posizione; le percentuali nelle condizioni "facili" possono essere un po' più basse, ma il modello è più affidabile in generale.
- Esercizio 5: con più epoche l'accuratezza sugli esempi di addestramento cresce; il pannello Under the hood mostra le curve di accuratezza e perdita su esempi di addestramento e su una parte tenuta da parte per la verifica. Con un dataset sbilanciato il modello tende a prevedere la classe con più esempi nei casi incerti.
- Notebook offline: accuratezza del k-NN sulle cifre 0,987; i 6 errori riguardano cifre scritte in modo ambiguo (9 scambiati per 3, 8 per 3 e per 1, 4 per 9, 3 per 7). Scorciatoia simulata con l'albero di decisione: senza macchia accuratezza 0,778 e nessuno dei 45 sette di verifica riconosciuto; con la macchia tutte le 450 immagini di verifica classificate come 7.

## Materiale open source

Verifica puntuale per L12-L13: lezioni, figure, scheda e notebook sono stati prodotti da zero. Materiali correlati:

- Microsoft, ML for Beginners, sezione Regression (licenza MIT): https://github.com/microsoft/ML-For-Beginners
- Teachable Machine: https://teachablemachine.withgoogle.com/
- Google Codelab, transfer learning con TensorFlow.js: https://codelabs.developers.google.com/tensorflowjs-transfer-learning-teachable-machine
- MLU-Explain, Linear Regression: https://mlu-explain.github.io/linear-regression/
