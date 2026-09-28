---
title: "Modulo 5 - Laboratorio finale"
subtitle: "B.8 - Python per l'Intelligenza Artificiale. Traccia docenti, lezione L18 e chiusura del corso"
lang: it
---

# Modulo 5 - Traccia docenti

## Collocazione e struttura della lezione

L18 chiude il corso e ha due parti:

| Parte | Durata | Contenuto |
|---|---|---|
| studenti | 35 min | mini progetto a gruppi (notebook `L18_progetto.ipynb`) |
| docenti | 25 min | valutazione del progetto, adattamento del corso, collegamenti con B.6 e B.4, bilancio |

Se le sessioni del corso lo consentono, conviene dedicare al progetto un'ora intera e spostare la parte docenti in coda all'ultima sessione: 35 minuti bastano per completare il progetto, ma lasciano poco spazio alla relazione.

## Logica della progettazione del progetto

Il progetto non introduce nuovi contenuti: chiede di mettere in sequenza, in autonomia, tutte le fasi viste separatamente nel corso. Il notebook fornisce la struttura (sei sezioni) e lascia agli studenti le scelte: traccia, normalizzazione, configurazioni della rete, interpretazione.

Due tracce di difficoltà simile ma di natura diversa:

- traccia A (spirali): problema "geometrico", visualizzabile; adatta a chi preferisce ragionare sui grafici; permette di usare la rete scritta a mano di L16
- traccia B (cifre): problema "reale", con 10 classi; adatta a chi preferisce un risultato concreto; l'analisi degli errori (immagini sbagliate) è intuitiva

Le celle di controllo verificano solo i passaggi meccanici (dati, suddivisione, soglia minima di accuratezza). Le scelte e l'interpretazione si valutano sulla relazione.

## Conduzione del progetto

- formare i gruppi in anticipo, bilanciando i livelli; in ogni gruppo una persona è responsabile del notebook (tastiera), le altre della relazione e delle scelte, con scambio a metà tempo
- nei primi 5 minuti far scegliere la traccia e leggere tutte le sezioni del notebook prima di iniziare
- durante il lavoro, intervenire con domande invece che con soluzioni: "che cosa vi aspettate che succeda se raddoppiate i neuroni?", "come fate a sapere se il modello funziona su dati nuovi?"
- a 10 minuti dalla fine: interrompere le prove e dedicare il tempo rimanente alla relazione e alla verifica finale (`Restart Kernel and Run All Cells...`)

Problemi prevedibili:

| Problema | Intervento |
|---|---|
| il gruppo prova decine di configurazioni senza annotarle | ricordare la tabella della relazione: tre configurazioni annotate valgono più di venti non documentate |
| addestramento lento in JupyterLite (traccia B con reti grandi) | ridurre `max_iter` o il numero di neuroni; le reti con 32-64 neuroni bastano |
| accuratezza bassa sulla traccia A | verificare la standardizzazione; provare due strati nascosti o più epoche |
| `ConvergenceWarning` | aumentare `max_iter`; l'avviso non è un errore |
| notebook che non si esegue dall'inizio | celle eseguite in ordine diverso (lezione L2); riavviare ed eseguire tutto |

## Valutazione del progetto

Rubrica con punteggi (la versione descrittiva è nella lezione, condivisa con gli studenti):

| Dimensione | 4 | 3 | 2 | 1 |
|---|---|---|---|---|
| Correttezza del codice | eseguibile dall'inizio alla fine, controlli superati, nessun errore | eseguibile, un controllo non superato | errori che impediscono alcune fasi | notebook non eseguibile |
| Comprensione del modello | spiega con precisione il ruolo di strati, neuroni, attivazione, tasso di apprendimento, perdita | spiegazione corretta con qualche imprecisione | spiegazione parziale | spiegazione assente o errata |
| Analisi dei risultati | 3 o più configurazioni confrontate e motivate; interpretazione di perdita, addestramento-verifica ed errori | confronto presente, interpretazione parziale | un solo modello o nessuna interpretazione | nessuna analisi |
| Comunicazione | relazione chiara e completa, codice leggibile | relazione completa ma poco chiara | relazione incompleta | relazione assente |

Punteggio massimo 16. Suggerimento di conversione: 16-15 ottimo, 14-12 buono, 11-9 sufficiente, sotto 9 non sufficiente; da adattare ai criteri della scuola.

La valutazione è di gruppo; se si vuole una componente individuale, si può chiedere a ogni studente di rispondere per iscritto a una delle domande guida, in modo indipendente.

Soluzioni di riferimento: `lab/soluzioni/L18_progetto_soluzioni.ipynb` (traccia B, accuratezza di verifica circa 0.98 con due strati nascosti da 64 e 32 neuroni) e `lab/soluzioni/L18_progetto_soluzioni_tracciaA.ipynb` (traccia A, accuratezza di verifica circa 0.94 con la stessa configurazione). Le soluzioni mostrano un modo possibile di completare il notebook, non l'unico.

## Parte docenti: temi

### Adattare il corso ad altri monte ore

| Monte ore | Interventi |
|---|---|
| 12 ore | unire L1 e L2; ridurre il modulo 2 a 4 lezioni (L3, L4-L5 unite, L6, L8 come lettura di codice); unire L9 e L10; eliminare L17 (solo cenno a scikit-learn) e il progetto (sostituito dalla verifica del modulo 4) |
| 24 ore | raddoppiare L16 (retropropagazione scritta dagli studenti); aggiungere una lezione su classificazione a più classi e funzione softmax; progetto su due lezioni |
| 30 ore | come 24 ore, più una lezione su reti convoluzionali per immagini (in Colab) e una su dati reali con pandas, in coordinamento con B.6 |

In ogni caso il filo conduttore del neurone va mantenuto: è ciò che dà coerenza al corso.

### Collegamenti con gli altri corsi del programma

- B.6 "Data science e Machine Learning": B.8 fornisce Python, NumPy, matplotlib e la comprensione interna di neurone e rete; B.6 tratta raccolta e preparazione dei dati, pandas, algoritmi di classificazione, metriche. Se i due corsi sono seguiti dalla stessa classe, conviene che B.8 preceda B.6; L17 e L18 possono fare da ponte (suddivisione addestramento e verifica, sovradattamento, `fit` e `predict`)
- B.4 "Cybersicurezza e IA": nessuna sovrapposizione di contenuti. Esercizi ponte possibili: controllo della robustezza di una password (modulo 2); classificazione di messaggi come phishing o legittimi con `MLPClassifier` su caratteristiche semplici (lunghezza, numero di link, parole chiave), come variante del progetto finale
- B.2 "Umani e algoritmi": i temi dell'interpretazione antropomorfa, della fiducia nell'accuratezza e della storia dell'IA (L13) si prestano a una discussione comune

### Bilancio del corso

Domande per la riflessione finale tra docenti:

- il filo conduttore del neurone ha reso più motivato lo studio del linguaggio? In quali lezioni ha funzionato meno?
- quali lezioni hanno richiesto più tempo del previsto, e quali contenuti conviene ridurre?
- i laboratori sono risultati eseguibili sulle macchine della scuola? Quale ambiente (JupyterLite, WinPython) si è rivelato più affidabile?
- i controlli automatici hanno aiutato l'autonomia degli studenti o favorito l'esecuzione meccanica?
- quali materiali conviene adattare alla propria classe (esempi, dati, livelli degli esercizi)?

### Riepilogo dei materiali del corso

| Modulo | Lezioni | Laboratorio | Verifica |
|---|---|---|---|
| 1 | L1-L2 | script Thonny, primo notebook | nessuna (competenze osservate nei moduli successivi) |
| 2 | L3-L8 | script Thonny con controlli `assert` | `verifica_modulo2.py` |
| 3 | L9-L12 | notebook con funzione `controlla` | `verifica_modulo3.ipynb` |
| 4 | L13-L17 | notebook; notebook Colab per Keras e PyTorch | `verifica_modulo4.ipynb` |
| 5 | L18 | notebook di progetto a due tracce | rubrica del progetto |

Ogni modulo ha: lezione (`_lezione.md`), presentazioni (`_marp.md`, `_prezpdoc.md`), traccia docenti (`_docente.md`), laboratorio con soluzioni.

## Materiale open source

Verifica puntuale per L18: il progetto è scritto da zero. L'insieme di dati delle cifre 8 x 8 è distribuito con scikit-learn e proviene dall'archivio UCI Machine Learning Repository (Optical Recognition of Handwritten Digits). Per la prosecuzione degli studenti: Kaggle Learn, Intro to Deep Learning (https://www.kaggle.com/learn/intro-to-deep-learning) e Microsoft AI for Beginners (licenza MIT, https://github.com/microsoft/AI-For-Beginners).
