---
title: "Modulo 1 - Dati e dataset"
subtitle: "B.6 - Data science e Machine Learning. Traccia docenti"
lang: it
---

# Modulo 1 - Traccia docenti

## Collocazione e finalità del modulo

Il modulo 1 costruisce il vocabolario e gli strumenti che servono in tutto il corso:

- L1 introduce i termini, il dataset tabellare, i tipi di variabili e il ciclo della data science, usando un foglio di calcolo
- L2 tratta la raccolta dei dati e avvia la raccolta del dataset della classe, che tornerà in L3, L5, L6, L12 e nel progetto finale
- L3 introduce notebook e pandas, gli strumenti di lavoro dei moduli successivi

### Segmento di traccia docenti in aula  

10-15 minuti al termine di L3, sugli strumenti (notebook, JupyterLite, WinPython, Colab, Kaggle) e sulla gestione dei file nel laboratorio.

## Logica della progettazione

### L1: il foglio di calcolo prima del codice

La prima lezione non usa Python. 
Gli studenti conoscono già il foglio di calcolo; aprire un CSV in LibreOffice Calc permette di vedere il dataset "intero", scorrere, filtrare, ordinare, senza **la barriera del codice**.  
Il passaggio a pandas in L3 viene poi motivato da ciò che il foglio di calcolo fa con fatica: operazioni ripetibili, documentate, su dati più grandi.

Il problema della lingua nell'importazione (punto decimale letto come testo o data con impostazioni italiane) non è un dettaglio tecnico da evitare: è il primo esempio concreto di problema di qualità legato al formato, e anticipa L5.

### L1: perché i pinguini

Palmer Penguins è stato proposto come alternativa al dataset Iris, storicamente legato alla rivista di eugenetica in cui fu pubblicato.  
Rispetto a Iris ha variabili di tipi diversi (quantitative, nominali, una discreta), valori mancanti reali, classi di dimensione diversa, e un contesto comprensibile a tutti.  
Le specie si separano bene con due variabili ma non con una sola: è la difficoltà giusta per i classificatori del modulo 3.

La licenza CC0 permette di distribuire il file, tradurne le colonne e modificarlo senza vincoli.  
La citazione della fonte è comunque indicata in ogni materiale, come buona pratica scientifica.

### L2: raccogliere dati propri

Raccogliere un dataset è esplicitamente nella descrizione del corso.  

La raccolta in classe ha tre funzioni:

- mostra che le scelte di progettazione (domande, unità, opzioni) determinano la qualità dei dati
- produce dati imperfetti, che rendono concreta la pulizia di L5
- dà agli studenti un dataset "loro", più motivante di qualunque dataset preconfezionato

Il tema dei tragitti è stato scelto dopo averne scartati altri frequenti nei corsi (ore di sonno, uso dei social, voti):  
sono dati personali delicati, e in una classe di 25 studenti l'anonimato non è garantito.  
I tragitti non sono dati sensibili, contengono una relazione quantitativa prevedibile (distanza e tempo) e una variabile qualitativa da prevedere (mezzo).

Il file `tragitti_esempio.csv` (153 risposte simulate) sostituisce o integra i dati della classe:  
**25 risposte sono poche per addestrare un modello**; si possono unire le risposte di più classi o affiancare i dati di esempio.

### L3: pandas senza un corso di Python

Gli studenti non devono imparare Python, ma **leggere e modificare** codice Python.  
La lezione introduce solo sei concetti (istruzione, commento, variabile, funzione, metodo, import) e le operazioni di pandas usate davvero nel corso.  
Ogni riga di codice mostrata viene spiegata.

Il notebook segue uno schema che si ripete in tutto il corso:

- cella di spiegazione con l'elenco delle funzioni usate
- cella di codice completa, da eseguire
- cella con `___` da completare
- verifica automatica con la funzione `controlla`
- domande di interpretazione con spazio per la risposta

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `pinguini.csv` | L1, L3 e moduli successivi | 344 righe, colonne in italiano, licenza CC0 |
| `L1_scheda_dataset.md` | L1 | da stampare o da compilare in digitale |
| `L2_questionario_tragitti.md` | L2 | bozza del questionario e del dizionario dei dati |
| `L2_valutazione_dataset.md` | L2 | scheda per la valutazione di un dataset aperto |
| `tragitti_esempio.csv` | L2, L3, L5 | 153 risposte simulate, con errori inseriti intenzionalmente |
| `L3_primi_passi_pandas.ipynb` | L3 | versione studenti |
| `L3_primi_passi_pandas_soluzioni.ipynb` | L3 | versione con soluzioni ed esecuzione completa, per il docente |

### La raccolta dei dati della classe

Opzioni, in ordine di semplicità:

1. modulo online dell'account della scuola (Google Moduli o Microsoft Forms):  
esportazione diretta in CSV; impostare domande a scelta per anno, mezzo e fascia; campi numerici con indicazione dell'unità.  
Disattivare la raccolta degli indirizzi email
2. foglio di calcolo condiviso in cui ogni studente compila una riga: più rapido, **ma ogni studente vede le risposte degli altri** mentre scrive
3. scheda cartacea trascritta da due studenti a turno: più lenta, ma produce errori di trascrizione utili per L5

Per mantenere l'utilità didattica della pulizia, non è necessario rendere il modulo "perfetto": una domanda numerica a testo libero per il tempo produrrà varianti (`20`, `20 min`, `mezz'ora`) che L5 insegnerà a gestire.  
Il docente può scegliere consapevolmente quanti vincoli mettere.

Il CSV esportato dal modulo online contiene di solito una colonna con data e ora di invio e intestazioni uguali al testo delle domande: rinominarle con i nomi del dizionario dei dati è il primo esercizio di L5.

### Checklist tecnica

- LibreOffice: verificare la presenza sulle postazioni o preparare LibreOffice Portable su chiavetta; provare l'importazione di `pinguini.csv` con la lingua impostata su Inglese (USA)
- JupyterLite: aprire https://jupyter.org/try-jupyter/lab/ su tutte le postazioni prima della lezione, perché il primo caricamento scarica diverse decine di MB
- file: distribuire notebook e CSV nella stessa cartella (chiavetta, cartella condivisa, piattaforma della classe); in JupyterLite vanno caricati con il pulsante di upload
- a fine lezione: gli studenti scaricano il notebook, altrimenti resta solo nel browser di quella postazione

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L1 | 30 min: termini (5), dato e dataset (7), tipi di variabili (8), caratteristiche ed etichetta (4), ciclo (3), CSV (3) | 25 min | 5 min |
| L2 | 25 min: dalla domanda ai dati (4), fonti (4), campione e distorsione (6), qualità (4), questionario e dizionario (4), riservatezza e licenze (3) | 30 min | 5 min |
| L3 | 20 min: notebook (6), tre ambienti (3), Python quanto basta (4), pandas (7) | 30 min | 10-15 min di traccia docenti |

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| numeri letti come testo o date in LibreOffice | ripetere l'importazione con lingua Inglese (USA); spiegare il perché, è un esempio di problema di formato |
| confusione tra variabile qualitativa ordinale e quantitativa discreta | chiedere se ha senso calcolare la media: la media dell'anno di corso (4,1) ha un significato limitato, quella del numero di fratelli sì |
| "l'anno è un numero, quindi è quantitativo" | è quantitativo discreto, ma nel dataset serve quasi solo come categoria; mostrare che il tipo dipende anche dall'uso |
| studenti che vogliono inserire il proprio indirizzo per calcolare la distanza | la distanza si stima con una mappa, senza scriverla da nessuna parte; ribadire la minimizzazione |
| celle di codice eseguite fuori ordine, `NameError` | riavviare il kernel ed eseguire tutto; mostrarlo una volta alla cattedra provocando l'errore apposta |
| `FileNotFoundError` in JupyterLite | il CSV non è stato caricato nella stessa cartella del notebook |
| doppie parentesi quadre per più colonne | spiegare che la parentesi interna è una lista di nomi |

## Considerazioni sugli strumenti per la didattica

### Notebook e ambienti

La scelta tra JupyterLite, WinPython e Colab va fatta prima del corso, in base al laboratorio:

- rete affidabile e browser recenti: JupyterLite come ambiente principale
- rete assente o instabile:  
WinPython su chiavetta o copiato sulle postazioni (versione "slim", che contiene pandas e scikit-learn; la versione minima "dot" non basta)
- istituto con Google Workspace for Education **e Colab abilitato dall'amministratore**: Colab per il lavoro a casa e la condivisione, non come unico ambiente

Il segmento di traccia docenti di L3 riprende la sezione "Gli strumenti del laboratorio: analisi per il docente" del syllabus docente (notebook, JupyterLite, WinPython, Colab, Kaggle) e la applica al laboratorio della propria scuola.

### Gestione dei file

Il punto debole di JupyterLite in classe è la gestione dei file: restano nel browser della postazione.  
Soluzioni praticabili:

- ogni studente scarica il notebook a fine lezione e lo carica sulla piattaforma della classe
- se le postazioni sono assegnate stabilmente, i file restano nel browser tra una lezione e l'altra (salvo pulizia della cache)
- per la consegna, esportare il notebook eseguito in HTML (File, Save and Export Notebook As, HTML)

### Kaggle come risorsa del docente

Per questo modulo Kaggle è utile soprattutto al docente: la sezione Datasets permette di trovare dataset alternativi ai pinguini per le verifiche di modulo (cercare dataset piccoli, con licenza CC0 o CC BY, con descrizione delle variabili).  
Il micro-corso Pandas di Kaggle Learn è un approfondimento adatto agli studenti più motivati.

## Valutazione del modulo

Il modulo 1 non prevede una verifica separata: gli indicatori confluiscono nella verifica del modulo 2.

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| classifica correttamente le variabili per tipo | L1, esercizio 1 |
| distingue domande a cui i dati possono rispondere | L1, esercizio 5 |
| individua distorsioni del campione | L2, esercizio 3 |
| valuta fonte e licenza di un dataset | L2, esercizio 4 |
| carica e filtra un dataset con pandas | L3, esercizi 2 e 3 |
| spiega perché una colonna numerica è letta come testo | L3, esercizio 4 |

## Soluzioni degli esercizi

### L1

- Esercizio 1: specie, isola, sesso qualitative nominali; misure di becco e pinna e massa quantitative continue (mm, g); anno quantitativa discreta (usata di fatto come categoria).
- Esercizio 2: Adelie 152, Gentoo 124, Chinstrap 68. Biscoe: 44 Adelie e 124 Gentoo; Dream: 56 Adelie e 68 Chinstrap; Torgersen: 52 Adelie. Solo Adelie vive su tutte e tre le isole; Gentoo solo su Biscoe, Chinstrap solo su Dream.
- Esercizio 3: 2 valori mancanti per ciascuna misura, 11 per il sesso. Il sesso dei pinguini non si riconosce a vista: è stato determinato con analisi del sangue, non sempre disponibili; le misure mancanti riguardano due soli animali non misurati.
- Esercizio 4: i 20 pinguini con la pinna più lunga sono tutti Gentoo; tra i 20 con la pinna più corta 17 sono Adelie e 3 Chinstrap. La lunghezza della pinna distingue bene i Gentoo dalle altre due specie, non Adelie da Chinstrap.
- Esercizio 5: risposte aperte. Esempi di domande possibili: quale specie è più pesante; se i maschi hanno il becco più lungo delle femmine; se la massa è cambiata tra il 2007 e il 2009. Esempi di domande impossibili: l'età dei pinguini, che cosa mangiano, quanti pinguini vivono sulle isole (il dataset è un campione, non un censimento).

### L2

- Esercizio 3: esempi: rispondono solo le classi del corso, non tutta la scuola; gli assenti non rispondono (e chi abita lontano potrebbe essere assente più spesso per problemi di trasporto); il giorno della raccolta può non essere tipico (pioggia, sciopero); le classi di un indirizzo possono avere un bacino territoriale diverso.
- Esercizio 5: problemi in `tragitti_esempio.csv`: stesso mezzo scritto in modi diversi (`bus`, `BUS`, `autobus`, `pullman`, ` bus` con spazio iniziale); distanze con la virgola decimale (lette come testo); tempi con unità nel testo (`45 min`, `45 minuti`, `45'`); valori mancanti; valori impossibili (distanza negativa, tempo 0); valori sospetti (distanza 250 km, probabilmente 2,50; tempo 300 minuti); risposte duplicate (stesse risposte inviate due volte a pochi minuti di distanza); risposte ambigue (`treno + bus`: quale mezzo principale?).

### L3

- Esercizio 1: 344 righe, 8 colonne; 2 valori mancanti per ciascuna misura, 11 per il sesso; le colonne di interi con valori mancanti diventano `float64`.
- Esercizio 2: 168 pinguini su Biscoe, 124 su Dream.
- Esercizio 3: 61 pinguini con massa superiore a 5000 g, tutti Gentoo; 32 con la pinna più corta di 185 mm, 29 Adelie e 3 Chinstrap.
- Esercizio 4: `distanza_km` e `tempo_min` sono lette come testo perché alcune righe contengono la virgola decimale (`1,2`) o testo (`45 min`): basta un solo valore non numerico perché pandas legga l'intera colonna come testo. `value_counts()` sul mezzo mostra oltre 20 varianti per 6 mezzi reali.
- Esercizio 5: 11 pinguini Adelie di Torgersen con massa superiore a 4000 g.

## Materiale open source

Verifica puntuale per L1-L3: le lezioni, le schede e il notebook sono stati scritti da zero. Materiali correlati, utilizzabili come approfondimento:

- Microsoft, Data Science for Beginners, lezioni "Defining Data Science", "Defining Data" e "Working with Python", licenza MIT, disponibili anche in italiano: https://github.com/microsoft/Data-Science-For-Beginners
- pandas, 10 minutes to pandas: https://pandas.pydata.org/docs/user_guide/10min.html
- Kaggle Learn, corso Pandas: https://www.kaggle.com/learn/pandas
- Palmer Penguins, dati e documentazione (CC0): https://allisonhorst.github.io/palmerpenguins/
