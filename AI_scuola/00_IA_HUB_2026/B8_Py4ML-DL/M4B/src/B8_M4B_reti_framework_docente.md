---
title: "Modulo 4 - Basi matematiche e logiche delle reti neurali (parte 2)"
subtitle: "B.8 - Python per l'Intelligenza Artificiale. Traccia docenti, lezioni L16, L17 e verifica del modulo"
lang: it
---

# Modulo 4, parte 2 - Traccia docenti

## Collocazione

L16 e L17 chiudono la parte tecnica del corso. L16 porta a compimento il filo conduttore: il neurone costruito a partire da L4 diventa una rete a due strati che impara da sola, scritta interamente in NumPy. L17 mostra che le librerie professionali fanno la stessa cosa, automatizzando la parte più laboriosa (il calcolo dei gradienti).

Segmento di traccia docenti in aula: 10-15 minuti al termine di L17, sui temi della sezione "Temi per il segmento docenti".

## Logica della progettazione

### L16: capire la retropropagazione senza doverla derivare

La retropropagazione è il punto più difficile dell'intero corso. La lezione adotta tre livelli di lettura:

1. principio (per tutti): l'errore si misura all'uscita e si distribuisce all'indietro; ogni peso viene corretto in proporzione al suo contributo
2. regola della catena come moltiplicazione di "tassi di variazione" (per tutti, con l'esempio numerico "3 per 0.5")
3. formule e codice (per chi è interessato): le formule sono nel notebook, commentate riga per riga, e sono verificabili numericamente nell'esercizio di approfondimento

Gli esercizi del laboratorio non chiedono di scrivere la retropropagazione, ma di usare la funzione `addestra_rete` e di osservarne il comportamento al variare degli iperparametri. È una scelta dovuta al monte ore: scrivere la retropropagazione da zero richiederebbe almeno due lezioni in più e non è necessario per comprenderne il ruolo.

I risultati "negativi" sono parte della lezione: XOR con 2 neuroni nascosti non converge con alcuni semi (minimo locale), 1 o 2 neuroni non bastano per le due lune. Mostrano che l'addestramento è un procedimento numerico che può fallire, non una garanzia.

### L17: la stessa rete, meno codice

La lezione ha una funzione di confronto, non di formazione all'uso dei framework. Per questo:

- scikit-learn, leggero e disponibile offline, è il framework su cui si svolge il laboratorio
- Keras e PyTorch sono mostrati su Colab con la stessa rete di L16, per rendere evidente la corrispondenza riga per riga
- la suddivisione in dati di addestramento e di verifica e il sovradattamento sono introdotti solo quanto basta per valutare correttamente un modello; la trattazione completa è nel corso B.6

L'esercizio 4 (ricalcolare le uscite di `MLPClassifier` con NumPy a partire dai pesi addestrati) è il più importante dal punto di vista concettuale: dimostra che dentro la libreria non c'è nulla di diverso da ciò che gli studenti hanno scritto.

L'insieme di dati delle cifre 8 x 8 è stato scelto perché è incluso in scikit-learn (nessun download), è piccolo (si addestra in pochi secondi anche su PC lenti e in JupyterLite) ed è un problema "vero", riconoscibile dagli studenti.

## Conduzione

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L16 | 30 min: struttura e calcolo in avanti (8), non linearità (5), retropropagazione (12), iperparametri (5) | 25 min + 5 min TensorFlow Playground | |
| L17 | 25 min: framework (5), scikit-learn (8), addestramento e verifica (5), Keras e PyTorch (7) | 25 min | 10-15 min di traccia docenti |

### Suggerimenti

- L16: prima della retropropagazione mostrare TensorFlow Playground con i dati XOR o a spirale: vedere la rete che impara prima di spiegare come impara aumenta la motivazione a capire il meccanismo
- L16: per la regola della catena, un esempio non matematico funziona bene: se ogni ora di studio in più aumenta il voto di 0.5, e ogni punto di voto in più aumenta la media di 0.2, allora un'ora di studio in più aumenta la media di 0.1
- L17: eseguire il notebook Colab dal PC del docente, proiettato, se gli studenti non hanno account adatti (vedi traccia docenti del modulo 1)
- L17: l'addestramento di `MLPClassifier` sulle cifre in JupyterLite richiede alcuni secondi in più rispetto a WinPython; conviene avvisare gli studenti

### Colab: preparazione

- caricare `L17_keras_pytorch_colab.ipynb` su Colab (menu `File`, `Carica notebook`) prima della lezione ed eseguirlo una volta per verificare che funzioni: le versioni delle librerie su Colab cambiano nel tempo
- il notebook è stato provato con Keras 3 e PyTorch 2 in un ambiente locale; su Colab Keras usa TensorFlow come motore di calcolo, senza modifiche al codice
- per condividere il notebook con gli studenti si può usare la funzione di condivisione di Google Drive, oppure pubblicarlo in un repository GitHub e aprirlo con un link Colab

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| confusione tra strato nascosto e strato di uscita nelle forme delle matrici | scrivere le forme di `X`, `W1`, `H`, `W2`, `Y_prev` alla lavagna, come nella lezione L11 |
| la retropropagazione percepita come "magia" | riportare al principio: è la regola della catena applicata strato per strato; la verifica numerica dell'esercizio 5 mostra che i numeri tornano |
| perdita che non scende con alcuni semi | è un minimo locale, non un errore di programmazione; cambiare seme o aggiungere neuroni |
| `ConvergenceWarning` di scikit-learn | avviso che l'addestramento si è fermato per il limite di epoche prima di stabilizzarsi; aumentare `max_iter` |
| `ModuleNotFoundError: No module named 'sklearn'` in JupyterLite | eseguire `%pip install scikit-learn` e riavviare il kernel |
| accuratezza di verifica superiore a quella di addestramento | può accadere con pochi dati e una suddivisione favorevole; non è un errore |

## Temi per il segmento docenti (fine modulo 4)

### La matematica con studenti del terzo e del quarto anno

Il modulo 4 usa concetti che il programma di matematica tratta al quinto anno (derivate) o non tratta (matrici, derivate parziali, regola della catena). Strategie adottate nel corso, applicabili anche in altri contesti:

- concetto prima del formalismo: la pendenza misurata con il rapporto incrementale prima della derivata; la somma pesata prima del prodotto scalare; "un prodotto scalare per riga" prima del prodotto tra matrici
- verifica numerica al posto della dimostrazione: ogni formula può essere controllata con Python (esercizi di approfondimento di L15 e L16)
- esempi piccoli calcolati a mano: un'epoca del perceptron, un prodotto matrice-vettore 3 x 2
- formule date, non derivate, dove la derivazione non è alla portata; con classi del quinto anno le derivazioni sono un buon esercizio di collegamento con la matematica

### Simulatori visuali prima del codice

TensorFlow Playground, i grafici delle regioni di decisione e delle curve della perdita permettono di osservare il comportamento di una rete prima di comprenderne il funzionamento interno. Ordine consigliato per un nuovo concetto: osservare (simulatore o grafico), formulare ipotesi ("che cosa succede se aggiungo neuroni?"), verificare con il codice, spiegare.

### I rischi dell'approccio "scatola nera"

Un corso che partisse dai framework (tre righe di Keras) otterrebbe risultati più rapidi ma lascerebbe gli studenti senza strumenti per capire che cosa succede quando qualcosa non funziona. Il percorso del corso (dal neurone scritto a mano al framework) è stato scelto per evitarlo. Segnali da cogliere in aula:

- studenti che cambiano iperparametri a caso finché "funziona": chiedere di formulare un'ipotesi prima di ogni prova
- interpretazione antropomorfa ("la rete ha capito"): riportare alla descrizione precisa (i pesi sono stati modificati per ridurre la perdita sugli esempi)
- fiducia acritica nell'accuratezza: chiedere sempre su quali dati è stata misurata

Il tema si collega al corso B.2 ("Umani e algoritmi") e può essere ripreso in una discussione comune.

## Verifica del modulo 4

File: `lab/verifica/verifica_modulo4.ipynb` (testo) e `lab/verifica/verifica_modulo4_soluzioni.ipynb`. Da distribuire solo il primo. Tempo: 45 minuti, lavoro individuale.

| Esercizio | Contenuto | Argomenti |
|---|---|---|
| 1 | pesi e bias per "x1 OR NOT x2" | neurone, separazione lineare |
| 2 | un passo della regola del perceptron | apprendimento del perceptron |
| 3 | tre passi di discesa del gradiente | discesa del gradiente |
| 4 | calcolo in avanti di una rete 2-3-1 | rete a più strati |
| 5 | `MLPClassifier` su due cerchi concentrici, accuratezza di verifica almeno 0.9 | framework, addestramento e verifica |
| 6 | domanda aperta: perché un neurone non basta per i due cerchi | interpretazione geometrica |

Rubrica suggerita: esercizi 1-5 con 2 punti ciascuno (controllo superato e codice leggibile: 2; errore circoscritto: 1; assente: 0); esercizio 6 fino a 5 punti (confine di un neurone come retta: 2; impossibilità di separare con una retta un cerchio interno da un anello esterno: 2; più neuroni nascosti combinano più rette in un confine chiuso: 1). Punteggio massimo 15, da riportare alla scala in uso.

Risposta attesa all'esercizio 6: un singolo neurone separa il piano con una retta; i punti della classe 0 sono all'interno di un cerchio e quelli della classe 1 lo circondano, quindi qualunque retta lascia punti di entrambe le classi da una stessa parte. Con uno strato nascosto ogni neurone traccia una retta diversa e il neurone di uscita combina le regioni, ottenendo un confine chiuso attorno al cerchio interno.

## Note sulle soluzioni

- L16, esercizio 2: con 2 neuroni nascosti, i semi 1 e 4 portano a un minimo locale (perdita finale circa 0.13 e 0.17), gli altri a una perdita vicina a zero
- L16, esercizio 3: con 1, 2 e 4 neuroni l'accuratezza resta intorno all'86%; con 8 neuroni arriva al 100%
- L16, esercizio 4: con i dati e il seme del notebook, $\eta = 20$ dà la perdita finale più bassa; con altri problemi valori così alti rendono l'addestramento instabile. È utile sottolineare che non esiste un tasso di apprendimento "giusto" in assoluto
- L17, esercizio 2: con 2 neuroni l'accuratezza di verifica è 0.9, con 8 e 32 neuroni 1.0
- L17, esercizio 3: 18 errori su 540 immagini di verifica (accuratezza circa 96.7%)
- L17, esercizio 5: accuratezza 1.0 sull'addestramento e 0.9 sulla verifica: la rete da 200 neuroni ha imparato anche il rumore

## Materiale open source

Verifica puntuale per L16 e L17: le lezioni sono scritte da zero. Materiali di approfondimento:

- Microsoft AI for Beginners (licenza MIT, in inglese), lezione "Introduction to Neural Networks: Multi-Layered Perceptron", in cui si costruisce un piccolo framework con retropropagazione: https://github.com/microsoft/AI-For-Beginners/blob/main/lessons/3-NeuralNetworks/04-OwnFramework/README.md
- Andrej Karpathy, micrograd (licenza MIT, in inglese): un motore di differenziazione automatica in circa cento righe, che mostra come i framework calcolano i gradienti; adatto al docente o a studenti molto motivati: https://github.com/karpathy/micrograd
- TensorFlow Playground: https://playground.tensorflow.org/
- Kaggle Learn, Intro to Deep Learning (gratuito, non open source, in inglese, con Keras), come prosecuzione per gli studenti: https://www.kaggle.com/learn/intro-to-deep-learning
