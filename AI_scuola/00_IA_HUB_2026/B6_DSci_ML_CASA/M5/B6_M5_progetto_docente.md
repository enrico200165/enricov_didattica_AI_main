---
title: "Modulo 5 - Progetto finale"
subtitle: "B.6 - Data science e Machine Learning. Traccia docenti"
lang: it
---

# Modulo 5 - Traccia docenti

## Collocazione e finalità del modulo

Il modulo 5 dedica tre ore al progetto a gruppi sull'intero ciclo della data science:

- L16: domanda, dati, pulizia, esplorazione
- L17: modelli, valutazione, errori, limiti, conclusioni
- L18: presentazione (35 minuti) e parte docenti (25 minuti)

La seconda parte di L18 è il segmento conclusivo della traccia docenti: rubrica di valutazione, adattamento del corso ad altri monte ore, collegamenti con B.4 e B.8, riuso dei materiali in altre discipline.

## Logica della progettazione

### Un progetto guidato

Tre ore sono poche per un progetto completo. Il tempo è stato reso sufficiente con tre scelte:

- scenari predefiniti con dati già verificati; il dataset aperto a scelta richiede l'approvazione del docente prima di L16, per evitare di perdere la prima lezione nella ricerca
- un modello del notebook con le otto sezioni del ciclo
- un progetto di esempio completo sui tragitti, che mostra il livello di dettaglio atteso dei commenti

Il progetto di esempio non è da copiare: i gruppi che scelgono i tragitti devono porre una domanda diversa (prevedere il tempo invece del mezzo, oppure lavorare sui dati della classe) o approfondire un aspetto (per esempio unire bici e monopattino e confrontare i risultati).

### Gli scenari

| scenario | punti di forza | difficoltà |
|---|---|---|
| tragitti della classe | dati propri; pulizia reale; problema difficile | pochi dati per alcuni mezzi |
| vini italiani (UCI Wine) | offline, pulito, 13 caratteristiche, legato al territorio | quasi nessuna pulizia; risultati molto alti: puntare su interpretazione, standardizzazione, importanza delle caratteristiche |
| dataset aperto a scelta | autonomia, motivazione | tempi di ricerca e comprensione; qualità variabile |
| immagini con Teachable Machine | accessibile, visivo | valutazione meno rigorosa; richiede prove sistematiche e tabelle |

Per il dataset aperto, un candidato interessante per la discussione della fuga di informazione è "Student Performance" dell'UCI (649 studenti di due scuole portoghesi, licenza CC BY 4.0): la documentazione avverte che il voto finale è fortemente correlato con i voti intermedi, e che prevederlo senza di essi è più difficile ma più utile. Contiene però variabili personali e familiari (consumo di alcol, relazioni, istruzione dei genitori): va proposto solo se il docente ritiene la classe pronta a trattarle con distacco, ed è un'ottima occasione per discutere quali variabili sia legittimo usare. https://archive.ics.uci.edu/dataset/320/student+performance

### Controlli intermedi

Due controlli brevi (3-5 minuti per gruppo) evitano che i gruppi arrivino alla presentazione con errori metodologici:

- fine L16: il docente verifica dizionario, registro della pulizia e grafici
- metà L17: il revisore del gruppo applica la lista di verifica metodologica; il docente controlla in particolare separazione della verifica, baseline e fuga di informazione

## Preparazione del laboratorio

### Materiali

| File | Uso |
|---|---|
| `L16_scheda_progetto.md` | scenari, fasi, ruoli, lista di verifica, struttura della presentazione, scheda delle domande tra gruppi |
| `L16_progetto_modello.ipynb` | modello del notebook, da copiare per ogni gruppo |
| `L16_progetto_esempio.ipynb` | progetto completo sui tragitti, già eseguito |
| `tragitti_esempio.csv`, `tragitti_puliti.csv` | dati dello scenario 1 |
| `L18_rubrica.md` | rubrica di valutazione |

### Prima di L16

- raccogliere le scelte degli scenari dei gruppi e approvare i dataset aperti
- per lo scenario 2 verificare che `load_wine` funzioni nell'ambiente del laboratorio
- per lo scenario 4 ripetere le verifiche di L13 (webcam, rete, browser)
- decidere il formato della presentazione: notebook proiettato con le celle Markdown, oppure poche slide

## Conduzione delle lezioni

### Il docente durante il progetto

- circola tra i gruppi con la lista di verifica; interviene con domande ("qual è la vostra baseline?"), non con soluzioni
- tiene il tempo: a metà di L16 i gruppi dovrebbero avere domanda e dizionario; alla fine, i grafici
- nei gruppi in difficoltà suggerisce di ridurre l'ambizione: meno caratteristiche, un modello in meno, ma valutazione corretta
- valorizza i risultati "negativi": un modello che non supera di molto la baseline, analizzato bene, vale più di un risultato alto non verificato

### Presentazioni (L18)

- 5 minuti per gruppo, tempo rigoroso; con 6-7 gruppi servono circa 35 minuti compresi i cambi
- ogni gruppo compila la scheda delle domande per un altro gruppo assegnato; le domande migliori vengono poste in aula
- il docente pone almeno una domanda sul metodo a ogni gruppo

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| gruppi che passano L16 a cercare un dataset | approvazione dei dataset prima di L16; in mancanza, scenario 1 o 2 |
| notebook che non si riesegue da capo | controllo "Restart Kernel and Run All Cells" a fine L17 |
| risultati alti accolti senza domande (vini) | chiedere la baseline, le caratteristiche più importanti, l'effetto della standardizzazione |
| presentazioni tecniche e lunghe | ricordare il pubblico: un compagno di un'altra classe |
| contributi squilibrati nel gruppo | ruoli a rotazione e dimensione individuale della rubrica |

## Valutazione

Rubrica in `L18_rubrica.md`: quattro dimensioni (dati; modello e valutazione; interpretazione e limiti; comunicazione) su quattro livelli, con indicazioni di conversione in decimi. Le prime tre dimensioni sono di gruppo, la quarta può essere individuale.

Valutazione complessiva del corso, indicativa:

- verifiche dei moduli 2, 3 e 4: 50%
- progetto finale: 40%
- lavoro di laboratorio (esercizi, domande di interpretazione, partecipazione): 10%

## Adattamento ad altri monte ore

Sintesi (dettaglio nel syllabus docente):

- 12 ore: unire L1 e L2, L4 e L5, L8 e L9 (solo albero di decisione, con un richiamo intuitivo al k-NN); togliere L15; progetto in due lezioni, preferibilmente sugli scenari 1 o 2
- 24-30 ore: statistica e probabilità, regressione logistica e curva ROC, foreste casuali, competizione di classe, progetto di 6 ore con revisione tra gruppi

## Collegamenti con gli altri corsi

- B.8: gli studenti che hanno seguito B.8 possono usare nel progetto `MLPClassifier` (rete neurale di scikit-learn) come terzo modello, confrontandola con alberi e k-NN
- B.4: un gruppo può riprendere il classificatore antiphishing di B.4 come progetto, con valutazione per tipo di messaggio e analisi dei falsi negativi
- B.1: dataset scientifici di laboratorio come scenario aperto

## Riuso dei materiali in altre discipline

- matematica: statistica descrittiva (L4), correlazione (L6), retta dei minimi quadrati (L12), distanza euclidea (L8)
- scienze: dataset dei pinguini come esempio di dati di ricerca ecologica; dataset dei vini per chimica
- educazione civica: L14 (bias, norme sull'IA), L2 (riservatezza dei dati)
- geografia ed economia: dataset aperti di dati.gov.it

## Materiale open source

Verifica puntuale per L16-L18: scheda, rubrica, modello e progetto di esempio sono stati prodotti da zero. Materiali correlati:

- UCI Machine Learning Repository, Wine (CC BY 4.0): https://archive.ics.uci.edu/dataset/109/wine
- UCI Machine Learning Repository, Student Performance (CC BY 4.0): https://archive.ics.uci.edu/dataset/320/student+performance
- Microsoft, Data Science for Beginners, lezioni sul ciclo di vita della data science e sulla comunicazione dei risultati (licenza MIT): https://github.com/microsoft/Data-Science-For-Beginners
