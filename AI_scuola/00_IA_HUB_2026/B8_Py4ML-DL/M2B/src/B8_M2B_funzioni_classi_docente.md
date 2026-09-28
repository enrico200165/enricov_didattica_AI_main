---
title: "Modulo 2 - Fondamenti di Python (parte 2)"
subtitle: "B.8 - Python per l'Intelligenza Artificiale. Traccia docenti, lezioni L6, L7, L8 e verifica del modulo"
lang: it
---

# Modulo 2, parte 2 - Traccia docenti

## Collocazione

Le lezioni L6, L7 e L8 completano i fondamenti del linguaggio: funzioni, strutture dati, moduli, gestione degli errori, classi. Al termine del modulo gli studenti dispongono di tutto ciò che serve per leggere e scrivere il codice dei moduli 3 e 4.

Il filo conduttore prosegue: il neurone diventa una funzione con l'attivazione come parametro (L6), un modulo riutilizzabile (L7), una classe (L8). L'approfondimento di L8 costruisce una rete a due livelli che calcola XOR, anticipando la lezione L16.

Segmento di traccia docenti in aula: 10-15 minuti al termine di L8, sui temi della sezione "Temi per il segmento docenti".

## Logica della progettazione

### L6: le funzioni attraverso le attivazioni

Le funzioni di attivazione sono esempi adatti a introdurre le funzioni perché:

- sono brevi (una o poche righe) e hanno un solo parametro e un solo valore di ritorno
- sono funzioni matematiche vere e proprie: il concetto di funzione della matematica e quello della programmazione coincidono
- sono il punto di contatto tra il linguaggio e la parte sulle reti neurali

Il passaggio di una funzione come argomento (`neurone(..., attivazione)`) è un concetto che molti corsi introduttivi rinviano. Qui è anticipato perché le librerie di machine learning lo usano di continuo (funzioni di attivazione, funzioni di perdita, callback) e perché rende evidente che l'attivazione è un componente intercambiabile del neurone.

Il grafico delle quattro attivazioni è fornito come immagine: matplotlib si introduce nella lezione L12. In quella lezione gli studenti ricostruiscono lo stesso grafico con il proprio codice.

La differenza tra `return` e `print` merita un'attenzione esplicita: è una delle confusioni più persistenti tra chi inizia a programmare, e gli esercizi con controlli automatici la fanno emergere (una funzione che stampa invece di restituire risulta "da rivedere").

### L7: una lezione di raccordo

L7 raccoglie argomenti eterogenei (tuple, dizionari, comprehension, moduli, errori). La scelta è dovuta al monte ore: ciascun argomento meriterebbe più spazio, ma per il resto del corso ne serve una conoscenza operativa. Il criterio di selezione è stato "che cosa si incontrerà nel codice dei moduli 3 e 4":

- tuple: la forma degli array NumPy, i valori restituiti da molte funzioni
- dizionari: parametri dei modelli, conteggi, risultati
- comprehension: presenti in quasi tutto il codice Python reale
- `import ... as ...`: `np`, `plt`
- eccezioni: lettura dei traceback prodotti dalle librerie, spesso lunghi

Il file `L7_03_trova_errori.py` contiene un errore di ciascun tipo, compreso un errore logico dovuto all'indentazione di una sola riga (`return` dentro il ciclo). È l'errore più istruttivo della lezione: il programma non segnala nulla e il risultato è plausibile ma sbagliato. Conviene lasciare che gli studenti lo cerchino prima di suggerire il debugger.

### L8: classi con un obiettivo preciso

La programmazione a oggetti è un argomento vasto. La lezione si limita a quanto serve per:

- scrivere la classe `Neurone`
- leggere il codice delle librerie (`modello.fit(...)`, `strato = Dense(...)`)

Sono esclusi ereditarietà, metodi speciali oltre a `__init__`, incapsulamento. Gli studenti che studiano Java o C++ in altre discipline possono essere invitati a confrontare la sintassi, ma non è necessario per il corso.

L'esercizio XOR con due livelli di neuroni ha un doppio scopo: consolidare l'uso di oggetti che contengono altri oggetti (lo strato contiene neuroni) e mostrare che il limite di un singolo neurone (domanda aperta in L4) si supera con più livelli. La spiegazione geometrica del perché arriverà in L13.

## Conduzione

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L6 | 25 min: definizione e chiamata (8), return e print (4), locali e globali (4), attivazioni (5), funzioni come valori (4) | 30 min | 5 min |
| L7 | 25 min: tuple (3), dizionari (7), comprehension (4), moduli (4), errori ed eccezioni (7) | 30 min | 5 min |
| L8 | 25 min: concetti (5), `Rettangolo` (8), `Neurone` (7), librerie e strato (5) | 25 min | 10-15 min di traccia docenti |

La verifica del modulo (40 minuti) va collocata in un momento dedicato: all'inizio della sessione successiva, oppure come lavoro individuale a casa se la scuola lo prevede.

### Suggerimenti per le singole lezioni

L6:

- scrivere dal vivo una funzione con `print` al posto di `return` e usarla in un'espressione: l'errore (`TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`) è un ottimo punto di partenza per la discussione
- eseguire `L6_04_debug_funzione.py` con il debugger proiettato: la comparsa del riquadro "Variabili locali" alla chiamata della funzione e la sua scomparsa al `return` rende visibile il concetto di variabile locale meglio di qualsiasi spiegazione. Il riquadro può essere piccolo: si allarga trascinando il bordo superiore

L7:

- per i dizionari, partire dall'esempio del registro dei voti (nome dello studente come chiave) prima del dizionario dei parametri del neurone
- il file `attivazioni.py` deve stare nella stessa cartella di `L7_02_usa_modulo.py`; se gli studenti salvano i file in cartelle diverse compare `ModuleNotFoundError`. È un errore da anticipare

L8:

- la difficoltà principale è `self`. Un'analogia utile: la classe è un modulo prestampato (per esempio la scheda anagrafica di uno studente), le istanze sono le schede compilate, `self` è "questa scheda"
- mostrare che `r1.area()` equivale a `Rettangolo.area(r1)`: chiarisce da dove arriva il valore di `self`

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| funzione definita ma mai chiamata: "il programma non fa niente" | distinguere definizione e chiamata; usare il debugger |
| `print` invece di `return` | vedi sopra; controllare con `type(risultato)` |
| uso di una variabile locale fuori dalla funzione (`NameError`) | mostrare il riquadro delle variabili locali nel debugger |
| parentesi dimenticate nella chiamata: `f` invece di `f()` | stampare `f` e `f()` e confrontare |
| `KeyError` per chiavi con maiuscole diverse | leggere la chiave indicata nel messaggio |
| `except:` senza tipo, che nasconde gli errori | chiedere quale eccezione ci si aspetta e indicarla |
| `self` dimenticato nei parametri di un metodo (`TypeError: ... takes 1 positional argument but 2 were given`) | spiegare che Python passa l'oggetto automaticamente come primo argomento |
| attributo scritto senza `self.` in `__init__` (resta una variabile locale) | con il debugger mostrare che l'attributo non esiste dopo la creazione |

## Temi per il segmento docenti (fine modulo 2)

### Eterogeneità dei livelli

In un corso di programmazione la distanza tra gli studenti cresce rapidamente: dopo poche lezioni chi ha già programmato è molto avanti, chi non l'ha mai fatto rischia di perdersi. Strumenti usati nel corso:

- esercizi a tre livelli (base, standard, approfondimento); gli esercizi base sono il minimo per proseguire, quelli di approfondimento non sono prerequisito di nulla
- controlli automatici, che danno un riscontro immediato senza attendere il docente
- programmazione in coppia, con ruoli "pilota" (alla tastiera) e "navigatore" (legge, controlla, suggerisce) invertiti a intervalli regolari. Le coppie funzionano meglio con livelli vicini ma non uguali
- per gli studenti più avanti: leggere e spiegare il codice dei controlli automatici, che usa costrutti non trattati (`lambda`, gestione generica delle eccezioni)

### Esercizi a difficoltà graduata

Criteri usati per costruire i tre livelli:

- base: applicazione diretta di quanto mostrato, spesso con parte del codice già scritta
- standard: stesso concetto in una situazione diversa, codice scritto da zero
- approfondimento: combinazione con argomenti precedenti o anticipazione di quelli successivi (per esempio `derivata_sigmoide` in L6, la rete XOR in L8)

### Gli errori come attività didattica

Il corso tratta gli errori come contenuto, non come incidente: esercizi "trova errori" in L1 e L7, lettura del traceback a voce alta, uso del debugger. Obiettivo: rendere gli studenti autonomi nella correzione. Pratiche consigliate:

- raccogliere durante il laboratorio gli errori più frequenti e discuterli nel richiamo iniziale della lezione successiva
- prima di aiutare, chiedere: tipo di errore, riga indicata, che cosa ci si aspettava da quella riga
- valorizzare in classe la correzione di un errore interessante quanto un programma corretto

## Verifica del modulo 2

File: `lab/verifica/verifica_modulo2.py` (testo) e `lab/verifica/verifica_modulo2_soluzioni.py` (soluzioni). Da distribuire solo il primo.

Struttura: cinque esercizi, 40 minuti, lavoro individuale.

| Esercizio | Contenuto | Argomenti verificati |
|---|---|---|
| 1 | `conta_sopra_soglia(valori, soglia)` | funzioni, cicli, condizioni, accumulatore |
| 2 | `normalizza(valori)` | liste, espressioni, comprehension o `append` |
| 3 | `medie_per_studente(registro)` | tuple, dizionari |
| 4 | classe `NeuroneSoglia` | classi, attributi, metodi |
| 5 | istanza che calcola "x1 AND NOT x2" | comprensione del neurone a soglia |

I controlli automatici indicano quali esercizi producono risultati corretti. La valutazione considera anche la qualità del codice. Rubrica suggerita (per ogni esercizio):

| Livello | Descrittore | Punti |
|---|---|---|
| completo | controllo superato, codice leggibile, nomi significativi | 2 |
| parziale | controllo superato con codice poco leggibile, oppure controllo non superato per un errore circoscritto (un caso limite, un indice) | 1 |
| assente | codice mancante o lontano dalla soluzione | 0 |

Punteggio massimo 10. Per l'esercizio 5 una risposta corretta è, per esempio, pesi `[1, -1]` e soglia 0.5: il peso negativo sul secondo ingresso realizza il NOT.

## Soluzioni

Le soluzioni eseguibili sono nella cartella `lab/soluzioni/`:

- `L6_03_esercizi_soluzioni.py`
- `L7_03_trova_errori_soluzione.py`, `L7_04_esercizi_soluzioni.py`
- `L8_03_esercizi_soluzioni.py`

Note:

- L6, esercizio 7: la derivata della sigmoide vale 0.25 in 0, il suo valore massimo. Il fatto che sia sempre al più 0.25 è all'origine di un problema noto delle reti profonde con attivazione sigmoide (il gradiente si riduce strato dopo strato), che spiega la diffusione di ReLU; può essere un'osservazione per gli studenti più interessati
- L7, errori del file `L7_03_trova_errori.py`, nell'ordine in cui compaiono: `SyntaxError` (`media[]` invece di `media([])`); errore logico (`return` dentro il ciclo, risultato 2.0 invece di 7.0); `IndexError` (`voti[len(voti)]`); `KeyError` (`"luca"` invece di `"Luca"`)
- L8, esercizio 4: NAND con pesi `[-1, -1]` e bias 1.5; maggioranza con pesi `[1, 1, 1]` e bias -2
- L8, esercizio 6: strato nascosto con OR (pesi `[1, 1]`, bias -0.5) e NAND; uscita AND (pesi `[1, 1]`, bias -1.5)

## Materiale open source

Verifica puntuale per L6, L7, L8: le lezioni sono scritte da zero. Materiali di riferimento in italiano, per approfondire:

- Tutorial ufficiale di Python in italiano: capitolo 4 (funzioni), capitolo 5 (strutture dati), capitolo 6 (moduli), capitolo 8 (errori ed eccezioni), capitolo 9 (classi): https://docs.python.org/it/3/tutorial/

La costruzione di XOR con due livelli di neuroni a soglia è un esempio classico della letteratura sulle reti neurali; nei materiali open source è trattata, per esempio, nelle lezioni sul perceptron e sulle reti multistrato di Microsoft AI for Beginners (licenza MIT): https://github.com/microsoft/AI-For-Beginners
