---
title: "Modulo 3 - Librerie numeriche: NumPy e matplotlib"
subtitle: "B.8 - Python per l'Intelligenza Artificiale. Traccia docenti, lezioni L9-L12 e verifica del modulo"
lang: it
---

# Modulo 3 - Traccia docenti

## Collocazione

Il modulo 3 introduce le due librerie su cui si basa il resto del corso: NumPy per il calcolo e matplotlib per i grafici. Contiene anche l'unica parte di algebra lineare del corso (L11), trattata in forma operativa.

Il filo conduttore prosegue con un cambio di scala: il neurone e lo strato, costruiti nel modulo 2 con liste, cicli e classi, vengono riscritti come operazioni tra array (`W @ x + b`). Alla fine del modulo gli studenti dispongono di tutto il necessario per il modulo 4: vettori e matrici per i pesi, funzioni vettoriali per le attivazioni, numeri casuali per inizializzare i pesi e generare dati, grafici per osservare dati, rette di separazione e curve di apprendimento.

Segmento di traccia docenti in aula: 10-15 minuti al termine di L12, sui temi della sezione "Temi per il segmento docenti".

## Logica della progettazione

### Il passaggio ai notebook

Dal modulo 3 il laboratorio passa da Thonny ai notebook. Motivazioni:

- il calcolo numerico procede per piccoli passi con verifica immediata dei risultati, il caso d'uso tipico dei notebook
- i grafici compaiono sotto la cella che li produce
- testo, codice ed esercizi stanno nello stesso documento: ogni notebook è una scheda di laboratorio

Il rischio principale dei notebook, lo stato nascosto del kernel, è stato trattato in L2. Conviene richiamarlo all'inizio di L9 e ricordare la regola "riavvia ed esegui tutto" prima di ogni consegna.

Ogni notebook ha la stessa struttura: esempi da eseguire, poi esercizi a tre livelli con una cella di controllo dopo ciascuno. La funzione `controlla`, definita nella seconda cella, stampa "corretto" o "da rivedere" e, in caso di errore, il tipo di eccezione. Se una cella di controllo produce `NameError: name 'controlla' is not defined`, la cella iniziale non è stata eseguita.

### L9 e L10: la vettorizzazione come modo di pensare

La difficoltà di NumPy non è la sintassi, ma il cambio di prospettiva: dal "per ogni elemento fai" del ciclo al "fai su tutto l'array" dell'operazione vettoriale. Per questo:

- molti esercizi di L10 sono versioni vettoriali di esercizi già svolti con i cicli nel modulo 2 (normalizzazione, frequenze, somma pesata): lo studente conosce già il risultato e può concentrarsi sulla forma
- la misura dei tempi con `%timeit` rende concreta la motivazione

Il parametro `axis` è il concetto più difficile di L10. La regola proposta è "l'asse indicato è quello che scompare nel risultato". Lo schema grafico della lezione va mostrato e poi verificato con la matrice dei voti, di cui gli studenti conoscono il significato (studenti per righe, prove per colonne).

### L11: algebra lineare operativa

Nella maggior parte degli indirizzi le matrici non fanno parte del programma di matematica. La lezione non le presenta come teoria, ma come strumento con una regola di calcolo:

1. il prodotto scalare è già noto come somma pesata (L5)
2. il prodotto matrice-vettore è "un prodotto scalare per ogni riga"
3. lo strato di neuroni è "una riga di pesi per ogni neurone"

L'esercizio 2 di L11 chiede di calcolare a mano un prodotto matrice-vettore prima di verificarlo con NumPy. È importante non saltarlo: calcolare a mano un caso piccolo è il modo più efficace per fissare la regola.

L'interpretazione geometrica del prodotto scalare (segno legato all'angolo) è introdotta brevemente perché serve in L13 per spiegare la retta di separazione. Con classi che non hanno studiato la trigonometria si può ridurre alla sola osservazione sperimentale: calcolare prodotti scalari tra frecce disegnate su carta a quadretti e osservarne il segno.

L'esempio `W @ x` che produce $-5.55 \cdot 10^{-17}$ invece di 0 non è stato scelto apposta, ma merita di essere commentato: ricollega L3 (approssimazione dei `float`) a un caso concreto.

### L12: grafici al servizio del modulo 4

La lezione non tratta matplotlib in modo sistematico. Seleziona i grafici che serviranno nel modulo 4:

- grafico di funzione: attivazioni e loro derivate (L15)
- scatter di due classi: dati per il perceptron (L13, L14)
- retta di separazione: visualizzazione di che cosa impara il perceptron
- regione di decisione con `contourf`: visualizzazione delle reti multistrato (L16)
- istogramma: distribuzione dei pesi, dei dati, dei risultati

Il grafico delle attivazioni fornito come immagine in L6 viene ricostruito dagli studenti: è un buon momento per mostrare che un grafico "da libro" si ottiene con poche righe.

Nei grafici con più serie si usano simboli diversi oltre ai colori (`marker="s"`). È una buona pratica di accessibilità e rende i grafici leggibili anche in stampa in bianco e nero.

## Conduzione

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L9 | 30 min: pacchetti e pip (8), ecosistema (5), perché NumPy (5), creazione e indici (12) | 25 min | 5 min |
| L10 | 25 min: elemento per elemento e ufunc (5), broadcasting (6), axis (6), maschere (4), casuali e velocità (4) | 30 min | 5 min |
| L11 | 25 min: vettori e prodotto scalare (7), matrici e prodotto (10), strato e batch (8) | 30 min | 5 min |
| L12 | 25 min: struttura e plot (7), scatter e retta (8), istogramma e subplots (5), regione di decisione (5) | 30 min | 10-15 min di traccia docenti |

L9 contiene più teoria delle altre. Se il tempo è poco, `pip` e gli ambienti virtuali possono essere solo citati: nel corso non si installano pacchetti.

### Ambiente

- JupyterLite: NumPy e matplotlib si caricano al primo `import`, che può richiedere alcuni secondi; conviene eseguire la cella degli `import` all'inizio della lezione su tutte le postazioni. `%timeit` funziona, ma i tempi sono più lunghi rispetto a Python installato: il rapporto tra ciclo e operazione vettoriale resta evidente
- WinPython: tutti i notebook funzionano senza modifiche
- Colab: tutti i notebook funzionano senza modifiche; va caricato il file `.ipynb` (menu `File`, `Carica notebook`)
- i file salvati da `fig.savefig` in JupyterLite restano nel browser: vanno scaricati dal pannello dei file

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| `NameError: name 'np' is not defined` | la cella con `import numpy as np` non è stata eseguita (o il kernel è stato riavviato) |
| `np.zeros(3, 2)` invece di `np.zeros((3, 2))` | la forma è una tupla: servono le doppie parentesi |
| confusione tra `a * b` e `a @ b` | far calcolare entrambi su due vettori piccoli e confrontare |
| `axis=0` e `axis=1` invertiti | regola "l'asse indicato scompare"; verificare la forma del risultato con `.shape` |
| `and`/`or` tra array (`ValueError: The truth value of an array ... is ambiguous`) | usare `&`, `|` e le parentesi attorno alle condizioni |
| `ValueError` nei prodotti tra matrici | scrivere le forme dei due operandi accanto al codice e applicare la regola $(r, k) \times (k, c)$ |
| grafici sovrapposti in una stessa figura | ogni grafico va chiuso con `plt.show()` |
| modifica inattesa di un array dopo uno slicing | lo slicing di un array NumPy è una vista sugli stessi dati, non una copia (a differenza delle liste); per una copia si usa `.copy()`. Da spiegare quando si presenta, non in anticipo |

## Temi per il segmento docenti (fine modulo 3)

### Il notebook come scheda di laboratorio

Tipi di cella usati nei notebook del corso:

- celle di spiegazione (Markdown): consegna, formule, suggerimenti
- celle di esempio: codice completo, da eseguire e modificare
- celle da completare: codice con segnaposto (`None`, `pass`)
- celle di controllo: verifica automatica del risultato

Suggerimenti per preparare notebook propri:

- ogni esercizio deve essere eseguibile anche se i precedenti non sono stati completati: la funzione `controlla` gestisce gli errori e non interrompe il notebook
- i controlli devono verificare il risultato, non il procedimento; il procedimento si valuta leggendo il codice
- aggiungere domande a risposta aperta in celle di testo ("perché il risultato cambia?") per evitare l'esecuzione meccanica delle celle
- fissare il seme dei numeri casuali, così che tutti gli studenti ottengano gli stessi valori e i controlli siano deterministici

### Versioni online e offline dello stesso materiale

Tutti i notebook funzionano senza modifiche in JupyterLite, WinPython e Colab, perché usano solo NumPy e matplotlib. Criteri per mantenere questa compatibilità:

- non usare librerie assenti in JupyterLite (PyTorch, TensorFlow) nei notebook destinati a tutti
- non leggere file dal disco o dalla rete, oppure fornire i file insieme al notebook
- evitare comandi specifici di un ambiente (per esempio `from google.colab import ...`)

### Soluzioni

Le soluzioni sono in notebook separati (cartella `lab/soluzioni/`). Conviene non distribuirle prima della fine del laboratorio; possono essere proiettate durante la correzione.

## Valutazione

### Indicatori formativi

| Indicatore | Dove |
|---|---|
| crea array e ne interpreta la forma | L9, esercizi 1-3 |
| usa operazioni vettoriali al posto dei cicli | L10, esercizi 1, 3-5 |
| usa correttamente `axis` e il broadcasting | L10, esercizi 2 e 4 |
| calcola a mano un prodotto matrice-vettore | L11, esercizio 2 |
| scrive uno strato come `W @ x + b` e ne verifica le forme | L11, esercizi 4-5 |
| produce grafici con titolo, etichette e legenda | L12, esercizi 1-3 |

### Verifica del modulo 3

File: `lab/verifica/verifica_modulo3.ipynb` (testo) e `lab/verifica/verifica_modulo3_soluzioni.ipynb`. Da distribuire solo il primo.

Struttura: cinque esercizi su una matrice di temperature (3 città per 7 giorni), 40 minuti, lavoro individuale. Negli esercizi 1-4 non sono ammessi cicli.

| Esercizio | Contenuto | Argomenti |
|---|---|---|
| 1 | media per città, massimo per giorno, giorno più caldo | aggregazioni, `axis`, `argmax` |
| 2 | conteggio e selezione delle misure sopra 25 gradi | maschere booleane |
| 3 | conversione in Fahrenheit e scarti dalla media di ogni riga | operazioni vettoriali, broadcasting, `reshape` |
| 4 | uscite di uno strato con sigmoide | prodotto matrice-vettore, strato |
| 5 | grafico delle tre serie di temperature | matplotlib |

Rubrica suggerita, per ogni esercizio: 2 punti (controllo superato, codice vettoriale e leggibile; per l'esercizio 5 grafico completo di titolo, etichette e legenda), 1 punto (risultato corretto ottenuto con cicli, oppure errore circoscritto; grafico incompleto), 0 punti (assente o lontano dalla soluzione). Punteggio massimo 10.

## Note sulle soluzioni

- L9, esercizio 5: le caselle nere sono quelle con riga pari e colonna dispari, oppure riga dispari e colonna pari; servono due assegnazioni con slicing con passo
- L10, esercizio 5: con seme 0 la frequenza del 6 è vicina a 1/6 ma non uguale; è un'occasione per discutere la differenza tra probabilità e frequenza osservata
- L11, esercizio 2: `M @ p` vale `[17, 39, -6]`
- L11, esercizio 6: la rete XOR con matrici riproduce quella a oggetti di L8; la corrispondenza riga per riga tra le due versioni è utile da mostrare
- L12, esercizio 2: la somma più frequente è 7 (6 combinazioni su 36)
- L12, esercizio 4: con $w_1 = w_2 = 1$, $b = -6$ e il seme 3 l'accuratezza è 1.0 (tutti i 60 punti classificati correttamente). Cambiando il seme, o aumentando la dispersione (`scale`), alcuni punti cadono dalla parte sbagliata della retta: è un buon esperimento da proporre. Nel modulo 4 il perceptron cercherà da solo i pesi

## Materiale open source

Verifica puntuale per L9-L12: le lezioni sono scritte da zero. Riferimenti per approfondire:

- NumPy, the absolute basics for beginners, documentazione ufficiale (in inglese): https://numpy.org/doc/stable/user/absolute_beginners.html
- Matplotlib, Quick start guide, documentazione ufficiale (in inglese): https://matplotlib.org/stable/users/explain/quick_start.html
- Jake VanderPlas, Python Data Science Handbook, testo completo online e notebook su GitHub (in inglese); i capitoli 2 (NumPy) e 4 (matplotlib) coprono gli stessi argomenti in modo più esteso. Testo con licenza CC BY-NC-ND, codice con licenza MIT: https://jakevdp.github.io/PythonDataScienceHandbook/ e https://github.com/jakevdp/PythonDataScienceHandbook

Nessuno di questi materiali è pensato per studenti di scuola secondaria né orientato alle reti neurali; per questo sono indicati come approfondimento per il docente e non come alternativa alle lezioni.
