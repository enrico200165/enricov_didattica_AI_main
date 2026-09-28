---
title: "Modulo 4 - Basi matematiche e logiche delle reti neurali (parte 1)"
subtitle: "B.8 - Python per l'Intelligenza Artificiale. Traccia docenti, lezioni L13, L14, L15"
lang: it
---

# Modulo 4, parte 1 - Traccia docenti

## Collocazione

Con il modulo 4 il corso arriva al suo obiettivo dichiarato: le basi matematiche e logiche delle reti neurali. Le lezioni L13-L15 trattano un singolo neurone: che cosa può calcolare (L13), come impara con una regola semplice (L14), come impara con il metodo generale usato da tutte le reti neurali, la discesa del gradiente (L15). La seconda parte del modulo (L16, L17) estende il discorso alle reti a più strati e ai framework.

Tutti gli strumenti di programmazione necessari sono già stati introdotti: le lezioni del modulo 4 non contengono nuova sintassi, salvo pochi dettagli (`np.vstack`, `set_yscale`), e possono concentrarsi sui concetti.

Segmento di traccia docenti in aula: previsto al termine di L17 (seconda parte del modulo).

## Logica della progettazione

### L13: la geometria prima dell'algoritmo

L13 non contiene algoritmi di apprendimento. Lo scopo è costruire un'immagine mentale precisa di che cosa fa un neurone, prima di chiedersi come impara: un neurone è una retta nel piano (un iperpiano in più dimensioni). Tutto il resto del modulo si appoggia su questa immagine:

- il perceptron (L14) sposta una retta
- XOR richiede più rette, quindi più neuroni (L16)
- la regione di decisione di una rete multistrato è la combinazione di più rette (L16)

La domanda aperta dalla lezione L4 ("esistono pesi per XOR?") trova qui la risposta, in tre forme di rigore crescente: grafica (la figura), sperimentale (la ricerca su 15 625 combinazioni), algebrica (la dimostrazione con le disuguaglianze). La forma algebrica è adatta alle classi del triennio con buona preparazione in matematica; per le altre bastano le prime due.

Le tappe storiche sono inserite per due ragioni: mostrano che l'IA ha avuto fasi di entusiasmo e di delusione, e collegano un risultato tecnico (XOR non è separabile) a una conseguenza reale (anni di scarso interesse per le reti neurali). Possono essere un punto di contatto con il corso B.2 sul pensiero critico.

### L14: un algoritmo che si può seguire a mano

La regola del perceptron è l'algoritmo di apprendimento più semplice che esista: tre casi, nessuna derivata. Gli studenti possono eseguirlo a mano su AND per due o tre esempi prima di vederlo in Python. È consigliato farlo alla lavagna, con pesi iniziali nulli e $\eta = 1$: i numeri restano interi.

Esempio da svolgere alla lavagna (AND, $w = (0, 0)$, $b = 0$, $\eta = 1$, esempi nell'ordine della tabella):

| esempio | $z$ | $\hat{y}$ | $e$ | nuovo $w$ | nuovo $b$ |
|---|---|---|---|---|---|
| (0, 0), y = 0 | 0 | 1 | -1 | (0, 0) | -1 |
| (0, 1), y = 0 | -1 | 0 | 0 | (0, 0) | -1 |
| (1, 0), y = 0 | -1 | 0 | 0 | (0, 0) | -1 |
| (1, 1), y = 1 | -1 | 0 | 1 | (1, 1) | 0 |

Alla fine della prima epoca $w = (1, 1)$, $b = 0$: il neurone restituisce 1 per tutti e quattro gli esempi, perché anche per (0, 0) vale $z = 0$. Proseguendo con la stessa procedura la sesta epoca è la prima senza errori: il neurone calcola AND con $w = (2, 1)$ e $b = -3$. È istruttivo far disegnare agli studenti la retta dopo ogni correzione.

I grafici della curva degli errori e della retta che si sposta rendono visibile l'apprendimento. Nella lezione L15 e L16 lo stesso ruolo sarà svolto dalla curva della perdita.

L'esercizio sul tasso di apprendimento ha un risultato che sorprende: nel perceptron $\eta$ conta poco. È una buona occasione per ragionare sul perché (la retta non cambia se pesi e bias sono moltiplicati per lo stesso numero positivo) e per preparare il contrasto con L15, dove $\eta$ è decisivo.

L'esercizio di approfondimento chiede una classe con `fit` e `predict`: anticipa l'interfaccia di scikit-learn usata in L17 e riprende le classi della lezione L8.

### L15: la derivata come pendenza misurata

La lezione è il punto matematicamente più impegnativo del corso. Le scelte fatte per renderla accessibile a studenti che non hanno studiato le derivate:

- la derivata è introdotta come pendenza stimata con il rapporto incrementale, calcolato in Python: è un numero che si misura, non un concetto astratto
- la funzione di esempio è una parabola, familiare dal biennio, di cui si conosce il vertice
- le formule del gradiente della regressione lineare sono date, non derivate; l'esercizio di approfondimento ne propone la verifica numerica
- il simbolo $\partial$ è introdotto solo come notazione ("derivata rispetto a una variabile, tenendo fisse le altre")

Con classi del quinto anno che hanno già studiato le derivate si possono ricavare le formule del gradiente con la regola della catena; è un buon esercizio di collegamento con il programma di matematica.

La regressione lineare è usata come primo esempio di discesa del gradiente perché ha solo due parametri, si visualizza facilmente e il risultato si può confrontare con il buon senso. L'esercizio Celsius-Fahrenheit, in cui il modello "scopre" 1.8 e 32, è particolarmente efficace: gli studenti conoscono già la risposta.

Il tasso di apprendimento viene esplorato su una parabola, dove i quattro comportamenti (lento, rapido, oscillante, divergente) si vedono chiaramente. Il valore $\eta = 0.5$ converge in un passo solo per questa particolare funzione; va detto esplicitamente per evitare generalizzazioni.

## Conduzione

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L13 | 30 min: neurone biologico e storia (8), geometria (12), XOR (10) | 25 min | 5 min |
| L14 | 25 min: regola del perceptron con esempio alla lavagna (12), implementazione (8), limiti (5) | 30 min | 5 min |
| L15 | 25 min: perdita (5), pendenza e derivata (7), discesa in una variabile (7), gradiente con due parametri (6) | 30 min | 5 min |

### Suggerimenti

- L13: prima di mostrare la ricerca sistematica su XOR, dare agli studenti due minuti per cercare a mano pesi e bias su carta. L'insuccesso rende la dimostrazione successiva più significativa
- L14: far eseguire più volte l'addestramento con semi diversi (`seme=1`, `seme=2`): le rette finali sono diverse ma tutte corrette. Il perceptron trova una soluzione, non la soluzione
- L15: prima di eseguire la cella con i quattro tassi di apprendimento, chiedere agli studenti di prevedere che cosa succederà con $\eta = 1.05$

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| confusione tra pesi (appresi) e iperparametri (scelti) | tabella alla lavagna con le due colonne, compilata insieme |
| "il neurone ha imparato" inteso in senso umano | precisare che l'apprendimento è la modifica di numeri secondo una regola; è anche un tema del corso B.2 |
| segno nella regola di aggiornamento: $w + \eta e x$ nel perceptron, $w - \eta \cdot \text{gradiente}$ nella discesa | nel perceptron $e = y - \hat{y}$; nella discesa si scende, quindi si sottrae la pendenza. Far verificare con un esempio numerico |
| pendenza stimata con $h$ troppo grande o troppo piccolo | mostrare che con $h = 1$ l'errore è evidente, con $h = 10^{-12}$ compare l'errore di approssimazione dei `float` (lezione L3) |
| perdita che cresce invece di diminuire | tasso di apprendimento troppo grande: ridurlo di un fattore 10 |
| regressione Celsius-Fahrenheit molto lenta | i valori di $c$ sono grandi rispetto a 1: $w$ converge in fretta, $b$ lentamente. È un'occasione per citare la standardizzazione dei dati (lezione L10), che risolve il problema |

## Valutazione

La verifica del modulo 4 è al termine di L17. Indicatori formativi per L13-L15:

| Indicatore | Dove |
|---|---|
| trova pesi e bias per una funzione separabile e ne disegna la retta | L13, esercizi 1, 2, 4 |
| spiega perché XOR non si può calcolare con un neurone | L13, discussione finale |
| esegue a mano un'epoca del perceptron | L14, attività alla lavagna |
| interpreta la curva degli errori e il ruolo di $\eta$ | L14, esercizi 2 e 4 |
| stima una pendenza con il rapporto incrementale | L15, esercizio 2 |
| descrive i quattro comportamenti della discesa al variare di $\eta$ | L15, esercizio 4 |

## Note sulle soluzioni

Le soluzioni sono nei notebook della cartella `lab/soluzioni/`.

- L13, esercizio 3: con pesi e bias moltiplicati per -1 il neurone calcola NAND (i semipiani si scambiano)
- L13, esercizio 4: una soluzione semplice è $w = (0, 1)$, $b = -20$ (retta orizzontale a 20 kg): la massa da sola basta a separare gli esempi. È un esempio di caratteristica irrilevante (l'altezza ha peso 0). Le due caratteristiche hanno scale molto diverse (metri e chilogrammi): è un'altra occasione per richiamare la normalizzazione
- L13, esercizio 5: 14 funzioni separabili; mancano XOR `(0, 1, 1, 0)` e XNOR `(1, 0, 0, 1)`
- L14, esercizio 2: con i dati e il seme del notebook gli errori arrivano a zero alla sedicesima epoca
- L14, esercizio 4: con $\eta = 0.1$ e $\eta = 1$ le curve coincidono (i pesi iniziali sono piccoli rispetto alle correzioni); con $\eta = 0.01$ i pesi iniziali casuali pesano di più e servono più epoche
- L15, esercizio 4: con $\eta = 0.05$ e $\eta = 0.95$ il valore finale dopo 20 passi è lo stesso (circa 3.61), per simmetria: il fattore di riduzione della distanza dal minimo è $1 - 2\eta$, cioè 0.9 e -0.9
- L15, esercizio 5: il modello ottiene valori vicini a 1.8 e 32 (non identici, per il rumore aggiunto ai dati)

## Materiale open source

Verifica puntuale per L13-L15: le lezioni sono scritte da zero. Il materiale open source più vicino è la lezione sul perceptron del curriculum Microsoft AI for Beginners (licenza MIT, in inglese), che tratta la regola del perceptron e la applica alla classificazione di cifre scritte a mano. Rispetto alle lezioni del corso presuppone più familiarità con Python e matematica; è adatta come approfondimento per il docente o per gli studenti più avanti:

- lezione: https://github.com/microsoft/AI-For-Beginners/blob/main/lessons/3-NeuralNetworks/03-Perceptron/README.md
- notebook: https://github.com/microsoft/AI-For-Beginners/blob/main/lessons/3-NeuralNetworks/03-Perceptron/Perceptron.ipynb

Riferimenti in italiano per la parte storica: Percettrone, Enciclopedia della Scienza e della Tecnica, Treccani: https://www.treccani.it/enciclopedia/percettrone_(Enciclopedia-della-Scienza-e-della-Tecnica)/
