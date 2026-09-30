---
title: "Modulo 3B - Addestrare e valutare un modello"
subtitle: "B.6 - Data science e Machine Learning. Traccia docenti"
lang: it
---

# Modulo 3B - Traccia docenti

## Collocazione e finalità del modulo

Le lezioni L10 e L11 completano il modulo 3 e rispondono alla terza richiesta della descrizione del corso (come si addestra un modello predittivo) nella sua parte più importante e più spesso trascurata: la valutazione.

- L10: suddivisione in addestramento e verifica, baseline, matrice di confusione, precisione e richiamo
- L11: sottoadattamento e sovradattamento, variabilità della valutazione, validazione incrociata, procedura corretta di scelta del modello

Segmento di traccia docenti in aula: 10-15 minuti al termine di L11, sulla valutazione del lavoro di laboratorio e sugli errori concettuali più frequenti.

## Logica della progettazione

### La tensione creata in L8-L9

Le lezioni precedenti hanno lasciato aperta una domanda: perché un modello con accuratezza 1,00 non è il migliore? L10 parte da quella domanda. Il primo risultato della tabella di L10 (k = 1 e albero senza limite perfetti sull'addestramento, non i migliori sulla verifica) risponde con i dati degli studenti, prima di qualsiasi definizione.

### Due dataset con difficoltà diverse

- pinguini (L10): problema facile, classi ben separate; le differenze tra modelli sono piccole; adatto a introdurre gli strumenti senza distrazioni
- tragitti (L11): problema difficile, classi sovrapposte, pochi esempi (150); il sovradattamento è evidente: l'albero senza limite arriva a 0,99 sull'addestramento e resta a 0,69 sulla verifica. I pinguini non mostrerebbero l'effetto in modo altrettanto chiaro

L'uso dei dati della classe in L11 rende il sovradattamento un fenomeno "loro": se i dati raccolti sono pochi, l'effetto è ancora più marcato.

### Precisione e richiamo con un esempio che si capisce

Il problema "riconoscere i Chinstrap" è costruito per mostrare in un solo risultato che:

- la baseline ha accuratezza 0,80 senza riconoscere nessun Chinstrap
- un albero può avere precisione perfetta e richiamo basso

Gli esempi di contesto (screening medico, antispam) servono a far capire che la scelta della metrica è una scelta sul costo degli errori, non tecnica. Il collegamento con B.4 (falsi positivi e falsi negativi nel filtro antiphishing, soglia di decisione) è diretto.

### Onestà sui risultati

I numeri del corso sono quelli prodotti dai notebook, compresi quelli "scomodi":

- sui pinguini l'accuratezza di verifica di alcuni modelli supera quella di addestramento
- sui tragitti il k-NN con k = 1 ottiene la media di validazione incrociata più alta (0,72) tra i k provati

Non vanno nascosti: mostrano che con pochi dati i risultati sono variabili e che il sovradattamento si riconosce dalla distanza tra addestramento e verifica, non da una regola fissa ("k piccolo è sempre peggio"). Nel caso dei tragitti, i dati di esempio sono generati con relazioni regolari e poco rumore per alcuni mezzi: il vicino più vicino è spesso dello stesso mezzo. Con i dati reali della classe il risultato può essere diverso, ed è un buon esercizio di confronto.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L10_valutazione.ipynb` e `_soluzioni` | L10 | scikit-learn |
| `L11_sovradattamento.ipynb` e `_soluzioni` | L11 | scikit-learn |
| `pinguini.csv` | L10 | |
| `tragitti_puliti.csv` | L11 | sostituibile con il file pulito della classe (L5) |

Con il file della classe, controllare che contenga le colonne `distanza_km`, `tempo_min`, `mezzo` e almeno 5 esempi per ogni mezzo; i mezzi con meno esempi vanno uniti (per esempio monopattino con bici) o esclusi, altrimenti `stratify` e la validazione incrociata stratificata segnalano un errore.

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L10 | 25 min: problema (4), divisione (5), baseline (3), matrice di confusione (4), precisione e richiamo (5), classi sbilanciate (4) | 30 min | 5 min |
| L11 | 20 min: sotto e sovradattamento (5), curva (4), iperparametri (2), variabilità (3), validazione incrociata (4), procedura (2) | 30 min | 10-15 min di traccia docenti |

### Attività senza computer

- L10, la verifica "già vista": prima della lezione preparare due mini-verifiche di cinque domande; la prima identica agli esercizi svolti la volta precedente, la seconda con esercizi nuovi. Discutere quale misura meglio la preparazione
- L11, validazione incrociata con le schede di L7: dividere le 24 schede in 4 mazzetti; a turno un mazzetto è la verifica e le regole scritte guardando gli altri tre vengono verificate su di esso

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| addestrare sull'intero dataset e poi dividere | ripetere la regola: `fit` solo su `X_add`; controllare nel codice |
| standardizzazione calcolata su tutti i dati | spiegare che anche medie e deviazioni standard sono "informazioni" dalla verifica |
| scegliere il modello guardando la verifica | è l'errore più diffuso anche tra professionisti; L11, esercizio 5 |
| confondere precisione e richiamo | ancorarli a una domanda: "quando dice sì, ha ragione?" e "li trova tutti?" |
| "l'accuratezza è 0,80, quindi il modello è buono" | chiedere sempre: e la baseline? |
| il k della validazione incrociata e il k del k-NN | dichiararlo esplicitamente: coincidenza di lettere |
| risultati diversi tra compagni con lo stesso codice | verificare il seme (`random_state`) o la versione dei dati; è un'occasione per parlare di riproducibilità |

### Errori concettuali da valutare

Negli elaborati degli studenti (e nel progetto finale) i seguenti errori vanno segnalati come errori metodologici, anche quando il codice funziona:

- accuratezza riportata sui dati di addestramento come misura della qualità
- nessun confronto con una baseline
- iperparametri scelti sull'insieme di verifica
- sola accuratezza con classi fortemente sbilanciate
- conclusioni tratte da differenze minime su una sola suddivisione

## Considerazioni sugli strumenti per la didattica

### Visualizzazioni interattive

Le pagine di MLU-Explain (Amazon Machine Learning University) sono tra le migliori spiegazioni visuali disponibili per questi concetti e possono essere proiettate durante la spiegazione:

- Train, Test, and Validation Sets: https://mlu-explain.github.io/train-test-validation/
- Precision and Recall: https://mlu-explain.github.io/precision-recall/
- Cross-Validation: https://mlu-explain.github.io/cross-validation/
- Bias-Variance Tradeoff (per il docente e gli studenti più interessati): https://mlu-explain.github.io/bias-variance/

Sono in inglese e vanno commentate in classe.

### Competizione di classe su Kaggle

Dopo L11, una competizione di comunità su Kaggle (Community Competitions) rende concreta la separazione tra dati di addestramento e di verifica: gli studenti ricevono un file di addestramento con etichette e un file di verifica senza etichette, caricano le previsioni e vedono la classifica calcolata su dati che non conoscono. Il docente crea la competizione con un proprio dataset (per esempio una parte dei dati dei tragitti di più classi). Richiede account Kaggle per gli studenti, con i vincoli indicati nel syllabus docente; in alternativa, una "competizione" offline: il docente tiene per sé le etichette di un file di verifica e calcola l'accuratezza delle previsioni consegnate dai gruppi.

## Valutazione del modulo

Verifica del modulo 3 (dopo L11), individuale, 40 minuti, su un dataset non visto con due caratteristiche e due o tre classi, fornito con un notebook guida:

- scrivere una regola a mano e calcolarne l'accuratezza
- addestrare un k-NN e un albero con suddivisione in addestramento e verifica
- costruire la matrice di confusione del modello migliore e commentarla
- confrontare con la baseline
- scegliere un iperparametro con la validazione incrociata e motivare

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| separa correttamente addestramento e verifica | L10, esercizi 1-2 |
| confronta con la baseline | L10, esercizio 1 |
| legge una matrice di confusione | L10, esercizio 3 |
| sceglie la metrica in base al problema | L10, esercizio 4 |
| riconosce sotto e sovradattamento da una curva | L11, esercizio 1 |
| usa la validazione incrociata per scegliere un iperparametro | L11, esercizi 3-5 |

## Soluzioni degli esercizi

### L10

- Esercizio 1: 256 pinguini di addestramento, 86 di verifica (38 Adelie, 31 Gentoo, 17 Chinstrap); la baseline prevede sempre Adelie, accuratezza 0,442.
- Esercizio 2: vedi tabella della lezione. k-NN con k = 1 e albero senza limite hanno accuratezza 1,000 sull'addestramento ma non sono i migliori sulla verifica (0,965 e 0,953). I migliori sulla verifica sono il k-NN con k = 5 o 15 (0,988), seguiti dagli alberi di profondità 2-3 (0,977). Risposta attesa: si sceglie in base alla verifica, preferendo a parità di risultato il modello più semplice; osservazione avanzata: le differenze tra 0,977 e 0,988 corrispondono a un solo pinguino.
- Esercizio 3: matrice [[38, 0, 0], [1, 16, 0], [1, 0, 30]]; accuratezza 84/86 = 0,977.
- Esercizio 4: baseline accuratezza 0,802, precisione e richiamo 0; albero profondità 2: 0,872, 1,000, 0,353 (6 Chinstrap trovati su 17, nessun falso allarme); profondità 3: 0,953, 0,810, 1,000 (tutti trovati, 4 falsi allarmi); profondità 4: 0,919, 0,708, 1,000. Con classi sbilanciate un'accuratezza alta può nascondere un modello che non riconosce la classe di interesse.
- Esercizio 5: precisione, richiamo e F1 per specie tra 0,94 e 1,00; il supporto (support) è il numero di esempi di verifica per specie.

### L11

- Esercizio 1: l'accuratezza di addestramento cresce da 0,48 (profondità 1) a 0,99 (da profondità 8); quella di verifica cresce fino a 0,71 (profondità 5) e poi si stabilizza a 0,69. Sottoadattamento: profondità 1-2; sovradattamento: oltre 6-7. Profondità migliore sulla verifica: 5.
- Esercizio 2: dieci suddivisioni, accuratezza tra 0,667 e 0,756, media 0,704. Una differenza di 0,02 tra due modelli su una sola suddivisione non permette di concludere che uno sia migliore.
- Esercizio 3: validazione incrociata, profondità 5: blocchi tra 0,633 e 0,833, media 0,707. Tabella: 1: 0,480; 2: 0,540; 3: 0,580; 4: 0,653; 5: 0,707; 6: 0,740; 8: 0,713; senza limite: 0,713. Le profondità 5-8 sono equivalenti entro la deviazione standard (0,08-0,12); scelta ragionevole 5 o 6, preferendo il modello più semplice.
- Esercizio 4: k = 1: 0,720; 3: 0,667; 5: 0,660; 9: 0,680; 15: 0,600; 25: 0,527. Con questi dati k = 1 ha la media più alta; con k grande il modello sottoadatta (i mezzi con pochi esempi, come il treno, vengono "sommersi" dai vicini delle classi più numerose). Vedi la sezione "Onestà sui risultati".
- Esercizio 5: la validazione incrociata sull'addestramento sceglie la profondità 5 (media 0,752); accuratezza finale sulla verifica 0,711. Scegliere guardando la verifica renderebbe ottimistica la stima: la profondità scelta sarebbe "adattata" anche a quegli esempi.

## Materiale open source

Verifica puntuale per L10-L11: lezioni, figure e notebook sono stati prodotti da zero. Materiali correlati:

- MLU-Explain, spiegazioni visuali interattive (Amazon Machine Learning University): https://mlu-explain.github.io/
- Google, Machine Learning Crash Course, sezioni su classificazione, precisione e richiamo, dati di addestramento e verifica (disponibile in italiano): https://developers.google.com/machine-learning/crash-course
- scikit-learn, Getting Started, sezione Model evaluation: https://scikit-learn.org/stable/getting_started.html
