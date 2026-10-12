---
title: "Modulo 2 - Preparare ed esplorare i dati"
subtitle: "B.6 - Data science e Machine Learning. Traccia docenti"
lang: it
---

# Modulo 2 - Traccia docenti

## Collocazione e finalità del modulo

Il modulo 2 copre le fasi del ciclo che precedono il modello:

- L4: statistica descrittiva con pandas, applicata ai pinguini e ai tragitti
- L5: pulizia del dataset dei tragitti raccolto in L2 (o del dataset di esempio)
- L6: analisi esplorativa con i grafici; si chiude con l'osservazione che prepara il modulo 3: due misure separano le specie in zone diverse del piano

Segmento di traccia docenti in aula: 10-15 minuti al termine di L5, sulla progettazione di dataset didattici "sporchi" e sul valore dei dati raccolti dalla classe.

## Logica della progettazione

### Statistica descrittiva al servizio della domanda

La statistica descrittiva viene spesso insegnata come elenco di formule. Qui ogni indice è introdotto per rispondere a una domanda sui dati: quale specie è più pesante, quanto tempo impiega uno studente "tipico", quale misura distingue le specie. La tabella delle medie per specie di L4 è già un primo "modello" informale: suggerisce quali variabili useranno i classificatori.

Il confronto media-mediana è costruito sui tempi di tragitto, che sono asimmetrici per natura e, nella versione non pulita, contengono un valore di 300 minuti che sposta la media: la differenza tra i due indici diventa visibile e motivata. La deviazione standard è presentata con il procedimento in quattro passi e senza formula simbolica; chi insegna matematica può aggiungere la notazione.

### La pulizia come attività centrale

Nelle indagini sul lavoro dei data scientist la preparazione dei dati risulta sempre la parte più lunga del lavoro. Nei corsi introduttivi viene spesso saltata usando dataset già puliti; il corso fa il contrario, per tre ragioni:

- è la parte in cui gli studenti possono esercitare giudizio (errore o caso reale?) senza conoscenze matematiche avanzate
- mostra che i dati sono il prodotto di scelte umane, tema che torna in L14
- usa i dati raccolti dagli studenti, che riconoscono gli errori perché li hanno prodotti

Il dataset di esempio contiene errori calibrati, ciascuno legato a una tecnica: varianti di testo (uniformare), virgole decimali (convertire), unità nel testo (estrarre), duplicati con ora di invio diversa (confronto su un sottoinsieme di colonne), valori impossibili, un valore anomalo errato (250 km) e sette valori anomali reali (tragitti in treno). Quest'ultimo punto è il più importante: il criterio dei quartili segnala, non decide.

### Progettare un dataset didattico "sporco"

Indicazioni per costruire altri dataset di esercitazione:

- partire da dati puliti e plausibili, e inserire errori noti e registrati: così si conosce la soluzione
- un tipo di errore per ogni tecnica da insegnare, in quantità sufficiente per essere notato (5-20 casi) ma non tale da rendere il dataset inutilizzabile
- inserire almeno un caso ambiguo che richieda una decisione motivata (`treno + bus`, il valore di 250 km)
- inserire valori anomali reali accanto a quelli errati
- mantenere un generatore (script) per produrre varianti diverse per classi o anni diversi

Il dataset di esempio del corso è stato prodotto con uno script che parte da dati generati con relazioni realistiche tra distanza, mezzo e tempo.

### Grafici: pochi, costruiti bene

L6 si limita a quattro tipi di grafico (barre, istogramma, diagramma a scatola, dispersione), sufficienti per tutto il corso. Ogni grafico del notebook usa colori coerenti per specie e marcatori diversi, come esempio di buona pratica. Il paradosso di Simpson sul becco dei pinguini è un risultato reale del dataset e mostra concretamente perché conviene guardare i dati per gruppi prima di trarre conclusioni.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L4_statistiche.ipynb` e `_soluzioni` | L4 | pandas |
| `L5_pulizia.ipynb` e `_soluzioni` | L5 | pandas, NumPy; salva `tragitti_puliti_classe.csv` |
| `L6_grafici.ipynb` e `_soluzioni` | L6 | pandas, matplotlib |
| `pinguini.csv` | L4, L6 | |
| `tragitti_esempio.csv` | L4, L5 | 153 risposte simulate, con errori |
| `tragitti_puliti.csv` | L6 e moduli successivi | versione pulita di riferimento (150 risposte), per chi non ha completato L5 |

I notebook usano solo funzioni compatibili con le versioni di pandas e matplotlib disponibili in JupyterLite, WinPython e Colab.

### Usare i dati della classe

Con il CSV della classe, prima di L5:

- rinominare le colonne con i nomi del dizionario dei dati: `dati = dati.rename(columns={"Mezzo di trasporto principale": "mezzo", ...})`
- rivedere il dizionario delle correzioni del mezzo, che dipende dalle varianti effettivamente presenti
- se le risposte sono poche (meno di 60-80), unire quelle di più classi o affiancare il dataset di esempio: `pd.concat([dati_classe, dati_esempio])`

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L4 | 25 min: distribuzione (2), posizione (6), dispersione (7), pandas (3), groupby (5), frequenze (2) | 30 min | 5 min |
| L5 | 20 min: perché (3), principi (3), testo (3), numeri (4), duplicati (2), anomali (3), mancanti e registro (2) | 30 min | 10-15 min di traccia docenti |
| L6 | 25 min: EDA e scelta (3), matplotlib (3), istogramma (3), scatola (4), dispersione (4), correlazione (5), fuorvianti (3) | 30 min | 5 min |

### Attività senza computer consigliate

- L4: sette studenti si mettono in fila per altezza; la mediana è lo studente centrale; poi entra "un giocatore di basket di 2,10 m" (valore inventato): la media cambia, la mediana quasi no
- L5: prima del notebook, stampare 20 righe del dataset di esempio e far individuare gli errori a coppie in 5 minuti; poi confrontare con quelli che il codice trova
- L6: mostrare il grafico con asse troncato e chiedere di stimare "quante volte" la barra dei Gentoo è più alta di quella degli Adelie

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| "la media è sempre il valore migliore" | esempio dei redditi: la mediana è usata nelle statistiche ufficiali perché pochi redditi molto alti spostano la media |
| deviazione standard vissuta come formula incomprensibile | calcolarla a mano su 4 valori (per esempio 2, 4, 4, 6) prima di usare pandas |
| confusione tra `groupby` e filtro | il filtro sceglie un gruppo, `groupby` li calcola tutti insieme |
| `str.extract` e le espressioni regolari | presentarle come "schemi di testo"; non è richiesto saperle scrivere |
| eliminare tutti i valori anomali | tornare ai tragitti in treno: sono i dati più interessanti per la relazione distanza-tempo |
| grafici senza etichette | regola d'aula: un grafico senza etichette degli assi non si consegna |
| istogramma confuso con grafico a barre | l'istogramma ha barre adiacenti e un asse numerico continuo; il grafico a barre ha categorie |

## Considerazioni sugli strumenti per la didattica

### Notebook e riproducibilità

L5 è la lezione in cui il vantaggio del notebook sul foglio di calcolo è più evidente: in un foglio di calcolo la pulizia si fa a mano, cella per cella, e non resta traccia delle operazioni; nel notebook ogni operazione è scritta e rieseguibile. Un esercizio efficace: aggiungere dieci righe nuove al CSV originale e rieseguire il notebook: la pulizia si ripete da sola.

### Verifica automatica

La funzione `controlla` dà un riscontro immediato ma limitato: verifica un risultato numerico, non il ragionamento. Le domande di interpretazione tra le celle (con lo spazio "Risposta:") sono la parte che il docente valuta davvero.

### Kaggle Learn

I micro-corsi "Pandas", "Data Cleaning" e "Data Visualization" di Kaggle Learn coprono gli stessi argomenti con esercizi aggiuntivi in inglese; sono adatti come attività facoltativa per gli studenti più rapidi, con i vincoli d'uso indicati nel syllabus docente. https://www.kaggle.com/learn

## Valutazione del modulo

Verifica del modulo 2 (dopo L6), individuale, 30-40 minuti, su un dataset non visto con alcuni errori inseriti (per esempio un dataset di misure di un altro fenomeno scelto dal docente):

- individuare e correggere tre problemi di qualità, documentandoli
- calcolare media, mediana e deviazione standard di una variabile per gruppi e commentare
- scegliere e costruire due grafici adatti a due domande date, e interpretarli
- rispondere a una domanda su correlazione e causalità

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| sceglie tra media e mediana motivando | L4, esercizio 4 |
| calcola statistiche per gruppi | L4, esercizi 1 e 2 |
| distingue errore e caso reale tra i valori anomali | L5, esercizio 4 |
| documenta la pulizia | L5, esercizio 5 |
| sceglie il grafico adatto | L6, esercizi 1-4 |
| interpreta correlazione e paradosso di Simpson | L6, esercizio 3 |

## Soluzioni degli esercizi

### L4

- Esercizio 1: medie Adelie 38,8 / 18,3 / 190,0 / 3701; Chinstrap 48,8 / 18,4 / 195,8 / 3733; Gentoo 47,5 / 15,0 / 217,2 / 5076 (becco lunghezza e profondità in mm, pinna in mm, massa in g). I Gentoo si distinguono per pinna, massa e profondità del becco; Adelie e Chinstrap solo per la lunghezza del becco.
- Esercizio 2: massa media femmine/maschi: Adelie 3369/4043, Chinstrap 3527/3939, Gentoo 4680/5485 g. Tabella isola-specie: Biscoe 26,2% Adelie e 73,8% Gentoo; Dream 45,2% Adelie e 54,8% Chinstrap; Torgersen 100% Adelie.
- Esercizio 3: i cinque più pesanti (da 5950 a 6300 g) sono tutti Gentoo maschi dell'isola Biscoe.
- Esercizio 4: nei dati non puliti vengono convertite 139 risposte su 153; media 30,0 minuti, mediana 23. La media è spostata in alto dal valore di 300 minuti (errore) e dai tragitti lunghi reali (60-75 minuti). La mediana descrive meglio il tragitto tipico.
- Esercizio 5: IQR della massa dei Gentoo 800 g; deviazione standard Adelie 459, Chinstrap 384, Gentoo 504 g: i Gentoo sono la specie più variabile (anche per la grande differenza tra maschi e femmine).

### L5

- Esercizio 1: dopo `strip` e `lower` restano 14 valori; il dizionario delle correzioni li riduce a 6 (bus 51, piedi 30, auto 28, bici 20, monopattino 15, treno 9, prima dell'eliminazione dei duplicati).
- Esercizio 2: dopo la conversione la distanza ha 1 valore mancante, il tempo 4 (erano già mancanti nel file).
- Esercizio 3: 3 righe duplicate; restano 150 righe. Due studenti potrebbero dare le stesse risposte, ma la coincidenza di distanza con un decimale e tempo esatto è poco probabile; l'ora di invio può aiutare, anche se nei dati di esempio le copie sono state inviate a distanza di tempo.
- Esercizio 4: valori impossibili: distanza -3 (id 78) e tempo 0 (id 115). Valori anomali della distanza: sette tragitti in treno tra 23 e 35 km (reali, coerenti con tempi di 52-75 minuti) e 250 km in autobus con 56 minuti (errore). Il tempo di 300 minuti è anomalo ed errato.
- Esercizio 5: dopo la pulizia mancano 3 distanze, 6 tempi, 2 fasce; 141 righe su 150 sono complete per distanza e tempo. Media e mediana del tempo: 29,0 e 24 minuti; sostituendo i mancanti con la mediana la media scende a 28,8 e la mediana resta 24: con pochi mancanti la scelta cambia poco, ma la sostituzione riduce artificialmente la variabilità.

### L6

- Esercizio 1: la distribuzione della pinna è bimodale perché mescola i Gentoo (pinna lunga) con Adelie e Chinstrap; la profondità del becco separa i Gentoo, la lunghezza del becco separa gli Adelie.
- Esercizio 2: la coppia lunghezza del becco e lunghezza della pinna (oppure lunghezza e profondità del becco) separa le tre specie: Adelie becco corto e pinna corta, Chinstrap becco lungo e pinna corta, Gentoo becco lungo e pinna lunga.
- Esercizio 3: correlazione pinna-massa 0,87; becco lunghezza-profondità -0,24 su tutti i pinguini, ma 0,39 (Adelie), 0,65 (Chinstrap), 0,64 (Gentoo): all'interno di ogni specie becchi più lunghi sono anche più profondi, ma i Gentoo hanno becchi lunghi e poco profondi, e mescolando le specie la tendenza si inverte (paradosso di Simpson).
- Esercizio 4: tempo mediano per mezzo: monopattino 14, piedi 15, bici 16, auto 27, bus 43, treno 55 minuti; correlazione distanza-tempo circa 0,84.
- Esercizio 5: a parità di distanza sono più veloci auto e treno (circa 2-3 minuti per km), più lenti gli spostamenti a piedi (circa 12-13 minuti per km); il bus sconta le attese alle fermate.

## Materiale open source

Verifica puntuale per L4-L6: lezioni, dataset dei tragitti, figure e notebook sono stati prodotti da zero. Materiali correlati:

- Microsoft, Data Science for Beginners, lezioni "Introduction to Statistics & Probability", "Data Preparation", "Visualizing Distributions", "Visualizing Relationships" (licenza MIT, disponibili anche in italiano): https://github.com/microsoft/Data-Science-For-Beginners
- Kaggle Learn, corsi Pandas, Data Cleaning, Data Visualization: https://www.kaggle.com/learn
- Matplotlib, Quick start guide: https://matplotlib.org/stable/users/explain/quick_start.html
- Tyler Vigen, Spurious Correlations: https://www.tylervigen.com/spurious-correlations
