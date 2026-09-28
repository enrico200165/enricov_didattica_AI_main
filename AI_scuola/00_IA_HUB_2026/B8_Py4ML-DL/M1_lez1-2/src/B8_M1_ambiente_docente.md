---
title: "Modulo 1 - L'ambiente di lavoro"
subtitle: "B.8 - Python per l'Intelligenza Artificiale. Traccia docenti"
lang: it
---

# Modulo 1 - Traccia docenti

## Collocazione e finalità del modulo

Il modulo 1 (lezioni L1 e L2) prepara l'ambiente di lavoro usato nel resto del corso. Gli strumenti sono due, con ruoli distinti:

- Thonny, per gli script dei moduli 1 e 2, dedicati alle basi del linguaggio
- i notebook Jupyter, per i moduli 3 e 4, dedicati al calcolo numerico, ai grafici e alle reti neurali

Il modulo non ha lo scopo di esaurire gli strumenti: fornisce il minimo per usarli con autonomia. Le funzioni più avanzate (debugger, installazione di pacchetti, esecuzione di tutte le celle) vengono riprese nelle lezioni in cui servono.

Segmento di traccia docenti in aula: 10-15 minuti al termine di L2, sui temi di questo documento (scelta dell'ambiente, piano alternativo senza rete, distribuzione dei materiali).

## Logica della progettazione

### L1: prima il modello mentale, poi lo strumento

La lezione parte da concetti generali (programma, interprete, script) prima di aprire Thonny. Lo scopo è evitare che lo studente identifichi Python con il programma che sta usando: Thonny, IDLE, Visual Studio Code e JupyterLab sono interfacce diverse per lo stesso interprete. Questa distinzione diventa indispensabile in L2, quando lo stesso codice viene eseguito in tre ambienti diversi.

Il confronto tra compilazione e interpretazione è trattato a livello qualitativo. La precisazione sul bytecode di CPython è inserita per correttezza, senza approfondimenti.

### L1: gli errori come contenuto, non come incidente

Una parte consistente di L1 è dedicata al traceback. La scelta deriva da un'osservazione ricorrente nei corsi introduttivi: gli studenti che non sanno leggere un messaggio di errore chiedono aiuto a ogni errore e il docente diventa il collo di bottiglia del laboratorio. L'esercizio `L1_02_trova_errori.py` contiene tre errori di tipo diverso (`SyntaxError`, `TypeError`, `NameError`), che si manifestano uno alla volta: lo studente deve ripetere il ciclo "esegui, leggi, correggi" tre volte.

Il pannello Assistente di Thonny aiuta, ma i suoi messaggi sono in inglese. Conviene tradurre in aula i primi messaggi e poi chiedere agli studenti di farlo da soli.

### L2: lo stato del kernel come concetto centrale

La difficoltà principale dei notebook non è l'interfaccia, ma lo stato nascosto: le variabili in memoria dipendono dall'ordine in cui le celle sono state eseguite, non da ciò che si vede nella pagina. Gli Esercizi 1 e 2 del notebook di L2 sono costruiti per far emergere il problema in modo controllato, prima che si presenti in modo casuale durante i laboratori dei moduli successivi.

La regola "riavvia ed esegui tutto prima di consegnare" va introdotta qui e richiamata a ogni consegna.

### Esercizi a tre livelli

Gli esercizi di laboratorio sono etichettati come base, standard e approfondimento. Gli esercizi base sono il minimo per seguire la lezione successiva; gli esercizi di approfondimento non sono prerequisito di nulla e servono agli studenti più veloci.

## Preparazione del laboratorio

### Scelta dell'ambiente

| Situazione del laboratorio | Script (L1, moduli 1-2) | Notebook (L2, moduli 3-4) |
|---|---|---|
| Windows, rete affidabile | Thonny (installazione utente o portable) | JupyterLite |
| Windows, rete assente o lenta | Thonny portable | WinPython da chiavetta o da cartella condivisa |
| Linux o macOS | Thonny (installazione utente) | JupyterLite |
| PC molto datati, browser non aggiornati | Thonny portable | WinPython (JupyterLite richiede un browser recente) |

Colab è usato solo in L17 e non è necessario nel modulo 1. È utile mostrarlo in L2, dal PC del docente, per completare il confronto.

### Checklist da completare prima di L1

- verificare che Thonny si avvii su almeno due postazioni, con l'account usato dagli studenti (non con un account amministratore)
- se si usa la versione portable, copiarla in una cartella accessibile in scrittura dagli studenti; Thonny salva le impostazioni nella propria cartella e non deve trovarsi in una cartella di sola lettura
- preparare una cartella condivisa, o un archivio da scaricare, con i file di laboratorio: `L1_01_primo_script.py`, `L1_02_trova_errori.py`, `L1_03_esercizio_libero.py`, `L2_primo_notebook.ipynb`
- impostare Thonny in italiano al primo avvio su ogni postazione, oppure dedicare i primi due minuti della lezione a questa operazione con tutta la classe
- attivare il pannello Variabili (menu `Visualizza`)

### Checklist da completare prima di L2

- aprire JupyterLite (https://jupyter.org/try-jupyter/lab/) su tutte le postazioni prima della lezione: il primo caricamento scarica alcune decine di MB per postazione e, con molte postazioni contemporanee, la banda della scuola può non bastare
- verificare che JupyterLite esegua una cella di codice con `import numpy` (anticipa il modulo 3 ed evita sorprese)
- se si usa WinPython: verificare che `Jupyter Lab.exe` si avvii con l'account degli studenti e che eventuali antivirus o criteri di sicurezza non blocchino l'esecuzione di programmi da chiavetta
- tenere pronto il piano alternativo: se JupyterLite non funziona, WinPython; se non è disponibile nemmeno WinPython, svolgere L2 come dimostrazione dal PC del docente e rinviare il laboratorio

### Distribuzione e raccolta dei file

- distribuzione: cartella condivisa di rete, piattaforma didattica della scuola (registro elettronico, Classroom, Moodle) o chiavetta
- raccolta: gli studenti consegnano file `.py` e `.ipynb` scaricati; con JupyterLite ricordare il download a fine lezione, perché i file restano solo nella memoria del browser della postazione
- nomi dei file: stabilire una convenzione, per esempio `L2_cognome.ipynb`, per evitare decine di file con lo stesso nome

### Colab e studenti minorenni

Colab richiede un account Google. Prima di usarlo con la classe (L17) occorre verificare:

- se la scuola dispone di account Google Workspace for Education e se Colab è abilitato per gli studenti
- le indicazioni della scuola sul trattamento dei dati personali degli studenti in servizi esterni

In assenza di account adatti, L17 si svolge come dimostrazione dal PC del docente.

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L1 | 30 min: concetti (10), Thonny (10), primo programma ed errori (10) | 25 min | 5 min |
| L2 | 25 min: notebook e kernel (10), Markdown (5), tre ambienti (10) | 25 min | 10-15 min di traccia docenti |

Se il tempo non basta, in L1 si può ridurre la panoramica degli IDE a una lettura rapida della tabella; in L2 si può mostrare WinPython e Colab solo dal PC del docente.

### Programmazione dal vivo

Il primo programma di L1 va scritto dal vivo, non mostrato già pronto. Durante la scrittura conviene commettere di proposito due errori tipici (una virgola mancante, una maiuscola sbagliata) e leggere il traceback ad alta voce. È il modello di comportamento che gli studenti devono imitare durante il laboratorio.

Con il proiettore, aumentare la dimensione del carattere di Thonny (`Ctrl++`) e di JupyterLab (`Ctrl++` del browser).

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| lo studente scrive il codice nella Shell invece che nell'editor e lo perde | mostrare la differenza sullo schermo; nella Shell si prova, nell'editor si scrive il programma |
| `F5` non produce nulla perché il file non è mai stato salvato | Thonny chiede di salvare al primo `F5`; far scegliere una cartella precisa |
| confusione tra `=` e `==` | anticipare in L2 con l'`assert`; riprenderlo in L4 con le condizioni |
| errori di maiuscole e minuscole (`Print`, `Nome`) | far leggere la descrizione del `NameError` e cercare il nome esatto nel codice |
| nel notebook una cella non produce output | verificare che sia una cella di codice e non di testo, e che sia stata eseguita |
| variabili "sparite" nel notebook | il kernel è stato riavviato o si è interrotto; rieseguire le celle dall'inizio |
| lavoro perso in JupyterLite | ricordare il download a fine lezione; eventualmente assegnare a un compagno il compito di ricordarlo |

### Supporto agli studenti

Prima di intervenire su un errore, chiedere allo studente:

1. qual è il tipo di errore (ultima riga del traceback)
2. quale riga è indicata
3. che cosa si aspettava che facesse quella riga

Spesso la risposta alla terza domanda porta da sola alla correzione.

## Considerazioni sugli strumenti per la didattica

### Thonny

Punti di forza:

- installazione semplice e versione portable, adatta ai laboratori scolastici con vincoli di amministrazione
- interfaccia essenziale, che non distrae con funzioni non necessarie
- il pannello Variabili rende visibile lo stato del programma, cioè il concetto più difficile per chi inizia
- il debugger mostra la valutazione delle espressioni passo per passo: utile in L4-L6 per cicli e funzioni
- la voce `Visualizza lo script corrente su Python Tutor` del menu `Esegui` apre una visualizzazione grafica dell'esecuzione (richiede la rete)

Limiti:

- non gestisce i notebook
- non è l'ambiente usato in ambito professionale: in chiusura del modulo 2 conviene citare Visual Studio Code come passo successivo

### Notebook Jupyter

Punti di forza per la didattica laboratoriale:

- testo, codice e risultati nello stesso documento: il docente può preparare schede di laboratorio in cui la consegna precede la cella da completare
- esecuzione per piccoli passi, con risultato immediato: adatta all'esplorazione e ai grafici
- verifica automatica con `assert`: lo studente riceve un riscontro immediato senza attendere il docente
- lo stesso file funziona in ambienti diversi (JupyterLite, WinPython, Colab, VS Code)

Limiti:

- lo stato nascosto del kernel: celle eseguite in ordine diverso producono risultati non riproducibili
- rischio di "esecuzione a catena" senza lettura: lo studente preme `Maiusc+Invio` su celle già scritte senza capire il codice. Per ridurlo, alternare celle già scritte con celle da completare e con domande a cui rispondere in una cella di testo
- i file `.ipynb` sono JSON: il confronto tra versioni e la correzione a mano sono meno comodi rispetto agli script

### JupyterLite

- vantaggio decisivo per la scuola: nessuna installazione e nessun account
- il calcolo avviene sul PC dello studente, quindi non ci sono limiti di utilizzo imposti da un servizio esterno
- limiti: prestazioni inferiori a Python installato, file conservati solo nel browser, alcune librerie non disponibili (tra cui PyTorch e TensorFlow)
- per il corso le librerie disponibili sono sufficienti fino a L16 compresa

### Google Colab

- vantaggi: potenza di calcolo, GPU, librerie di deep learning già installate, condivisione tramite link
- limiti: account Google, dipendenza dalla rete, sessioni temporanee, condizioni di servizio che possono cambiare nel tempo
- nel corso è usato solo dove è indispensabile (L17)

## Valutazione del modulo

Il modulo 1 non prevede una verifica di modulo: le competenze sono verificate nell'uso quotidiano degli strumenti nei moduli successivi. Durante i laboratori si possono osservare i comportamenti seguenti.

| Indicatore | Osservabile in |
|---|---|
| scrive, salva ed esegue uno script | L1, esercizi 2 e 4 |
| legge un traceback e individua tipo di errore e riga | L1, esercizio 3 |
| distingue cella di codice e cella di testo | L2, esercizio 3 |
| spiega perché una cella produce un risultato inatteso dopo un riavvio del kernel | L2, esercizio 2 |
| consegna un notebook che si esegue dall'inizio alla fine senza errori | L2, punto 3 del laboratorio |

## Soluzioni degli esercizi

### L1, Esercizio 1

| Espressione | Risultato | Osservazione |
|---|---|---|
| `7 + 8` | `15` | |
| `7 - 8` | `-1` | |
| `7 * 8` | `56` | |
| `7 / 8` | `0.875` | la divisione produce sempre un numero con la virgola |
| `"Python" + "3"` | `'Python3'` | `+` tra stringhe le unisce (concatenazione) |
| `"=" * 20` | `'===================='` | ripetizione |

`print(7 + 8)` mostra `15`; `7 + 8` nella Shell mostra anch'esso `15`. La differenza si vede con le stringhe: `"ciao"` nella Shell mostra `'ciao'` con gli apici, `print("ciao")` mostra `ciao`. Nella Shell viene mostrata la rappresentazione del valore; `print` mostra il testo.

### L1, Esercizio 3

File `soluzioni/L1_02_trova_errori_soluzione.py`. Ordine in cui compaiono gli errori:

1. riga 10, `SyntaxError: invalid syntax. Perhaps you forgot a comma?`: manca la virgola tra `"Abitanti:"` e `abitanti`
2. riga 11, `TypeError: can only concatenate str (not "float") to str`: `+` non può unire una stringa e un numero; soluzione: passare i due valori come argomenti separati di `print` (`print("Abitanti in milioni:", abitanti / 1000000)`)
3. riga 12, `NameError: name 'Citta' is not defined. Did you mean: 'citta'?`: maiuscola errata

Il `SyntaxError` impedisce l'esecuzione dell'intero programma, quindi all'inizio non viene stampata nemmeno la prima riga. Gli altri due errori si manifestano durante l'esecuzione, dopo che le righe precedenti sono state stampate. La differenza tra errori rilevati prima dell'esecuzione ed errori rilevati durante l'esecuzione merita un commento esplicito in aula.

### L1, Esercizi 4 e 5

Soluzioni di esempio in `soluzioni/L1_03_esercizio_libero_soluzione.py` e `soluzioni/L1_05_rettangolo_soluzione.py`.

### L2

Notebook completo in `soluzioni/L2_primo_notebook_soluzioni.ipynb`.

- Esercizio 1: dopo la modifica non eseguita, `area` vale ancora circa 78.54 (raggio 5); dopo l'esecuzione della cella modificata, circa 314.16 (raggio 10)
- Esercizio 2: il valore cresce di 1 a ogni esecuzione e il numero tra parentesi quadre aumenta; dopo il riavvio del kernel, eseguendo solo la seconda cella si ottiene `NameError: name 'conteggio' is not defined`, perché la variabile non è più in memoria e la cella che la crea non è stata eseguita
- Esercizio 4: `perimetro = 4 * lato`

## Materiale open source

Verifica puntuale per L1 e L2: le lezioni sono state scritte da zero e non riusano testi o codice di corsi esistenti. Le schermate di Thonny (licenza MIT) e JupyterLab (licenza BSD) sono state realizzate per il corso.

Materiali di approfondimento consigliati, in italiano:

- Tutorial ufficiale di Python in italiano, capitoli 2 e 3 (uso dell'interprete e introduzione informale al linguaggio): https://docs.python.org/it/3/tutorial/
- Python ABC, Python Italia: https://pythonitalia.github.io/python-abc/
