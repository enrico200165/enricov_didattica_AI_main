---
title: "Modulo 2 - Fondamenti di Python (parte 1)"
subtitle: "B.8 - Python per l'Intelligenza Artificiale. Traccia docenti, lezioni L3, L4, L5"
lang: it
---

# Modulo 2, parte 1 - Traccia docenti

## Collocazione

Le lezioni L3, L4 e L5 coprono i costrutti di base del linguaggio: tipi, espressioni, condizioni, cicli, liste. È la parte del corso più simile a un corso introduttivo di programmazione. La differenza è la scelta degli esempi: dalla lezione L4 il filo conduttore è il neurone artificiale, che viene costruito prima con `if` e `while` (neurone a soglia con due ingressi) e poi con liste e `for` (neurone con un numero qualsiasi di ingressi).

Il segmento di traccia docenti in aula del modulo 2 è previsto al termine di L8 (seconda parte del modulo).

## Logica della progettazione

### L3: poca teoria sui tipi, molta attenzione a float e stringhe

Una trattazione completa dei tipi richiederebbe più di un'ora. La lezione si concentra sui due aspetti che producono più errori nel resto del corso:

- la differenza tra numeri e stringhe, che si manifesta con `input()` (restituisce sempre una stringa) e con la concatenazione `+`
- l'approssimazione dei `float`, che si manifesta a ogni confronto tra risultati di calcoli e che, nelle reti neurali, è parte del funzionamento normale

La funzione esponenziale è introdotta già in L3, come semplice uso del modulo `math`. L'obiettivo è che in L6, quando si scrive la funzione sigmoide, la parte matematica sia già familiare e l'attenzione possa andare alla sintassi delle funzioni.

### L4: il neurone come prima applicazione

Il neurone a soglia è un esempio scelto perché:

- richiede esattamente i costrutti della lezione: espressioni aritmetiche, confronto, `if`/`else`, ciclo per le quattro combinazioni
- ha un risultato verificabile (la tabella di verità)
- introduce l'idea centrale del corso: lo stesso codice realizza funzioni diverse al variare dei parametri

Gli esercizi 4 e 5 di L4 (OR e NAND) chiedono di trovare i parametri a mano. È un'anticipazione dell'apprendimento automatico: nella lezione L14 lo stesso compito sarà svolto da un algoritmo. La domanda finale su XOR resta aperta fino a L13; conviene raccogliere le proposte degli studenti e tenerle da parte.

Il ciclo `while` con `caso // 2` e `caso % 2` è volutamente un po' artificioso: riutilizza gli operatori di L3 e prepara il confronto con la versione con `for` annidati di L5, più naturale. Il confronto tra le due versioni è un'occasione per discutere perché `for` è preferibile quando si scorre una sequenza nota.

### L5: dalla media ponderata al prodotto scalare

La somma pesata è introdotta partendo dalla media ponderata dei voti, un calcolo che gli studenti conoscono per esperienza diretta. Il passaggio successivo, "il neurone fa la stessa cosa e poi confronta con una soglia", rende concreto un concetto che altrimenti resterebbe una formula.

La sommatoria $\sum$ viene presentata come scrittura matematica di un ciclo con accumulatore. Per molti studenti il ciclo è più facile da capire della notazione; mostrare che sono la stessa cosa aiuta anche nelle lezioni di matematica.

Il passaggio dalla soglia al bias è inserito alla fine di L5 perché dalla lezione L6 in poi si usa sempre la forma con il bias, che è quella delle librerie di deep learning.

### Esercizi con verifica automatica

I file di esercizi contengono righe `assert` che controllano i risultati. Motivazioni:

- lo studente sa immediatamente se il risultato è corretto, senza attendere il docente
- il docente può concentrarsi sugli studenti in difficoltà
- si abitua gli studenti all'idea di test automatico, usata in tutta la programmazione professionale

Le righe di controllo usano talvolta costrutti non ancora spiegati (`is not None`, tuple, cicli annidati in L4). La lezione indica esplicitamente che non vanno modificate. Gli studenti più curiosi possono leggerle come esercizio di approfondimento.

Ogni esercizio è preceduto da un controllo `assert variabile is not None`, che produce il messaggio "completare il codice" invece di un errore di tipo meno comprensibile.

## Conduzione

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L3 | 30 min: tipi e variabili (8), operatori (8), float (6), stringhe e input (5), math ed esponenziale (3) | 25 min | 5 min |
| L4 | 30 min: confronti e logica (7), if (8), while (6), neurone a soglia (6), debugger (3) | 25 min | 5 min: domanda su XOR |
| L5 | 25 min: liste (8), for, range, zip (7), accumulatore (4), somma pesata e neurone (6) | 30 min | 5 min |

L5 è la lezione più densa. Se il tempo non basta, `enumerate` e lo slicing con passo possono essere solo citati; il neurone con n ingressi e l'accumulatore sono invece indispensabili per le lezioni successive.

### Programmazione dal vivo e previsione

Tecnica consigliata per L3 e L4: prima di eseguire un'istruzione, chiedere alla classe di prevederne il risultato (per esempio `17 // 5`, `-2 ** 2`, `0.1 + 0.2 == 0.3`, `int(3.9)`). La previsione sbagliata seguita dal risultato reale è più efficace di una spiegazione. Nei casi più sorprendenti (`0.1 + 0.2`) conviene far scrivere la previsione su un foglio o su uno strumento di risposta rapida prima di mostrare il risultato.

### Il debugger come strumento didattico

Il debugger di Thonny in modalità "più bello" (`Ctrl+F5`, passo dentro con `F7`) mostra la valutazione delle espressioni sottoespressione per sottoespressione. È utile:

- in L4, per seguire un giro del ciclo `while` e la valutazione della condizione
- in L5, per vedere come l'accumulatore cambia a ogni ripetizione
- per gli studenti in difficoltà, come alternativa alla spiegazione del docente: "esegui con il debugger e dimmi quando succede qualcosa che non ti aspetti"

Attenzione: `F6` (passo sopra) su un'istruzione `while` esegue l'intero ciclo in un colpo solo. Per entrare nel ciclo si usa `F7`.

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| `TypeError` con `input()`: `input("...") + 1` | ricordare che `input` restituisce sempre una stringa; mostrare `type(input(...))` |
| `=` al posto di `==` nelle condizioni | far leggere il `SyntaxError`; far pronunciare `==` come "è uguale a?" |
| indentazione sbagliata dopo `if` o `while` | usare il debugger per mostrare quali righe fanno parte del blocco |
| ciclo `while` infinito | spiegare come fermarlo (Stop, `Ctrl+C`); cercare insieme l'aggiornamento mancante |
| errore "fuori di uno" con `range` e slicing (`range(1, 100)` per 1..100) | ricordare la regola "fine esclusa"; verificare stampando `list(range(...))` |
| accumulatore inizializzato dentro il ciclo | mostrare con il debugger che viene azzerato a ogni ripetizione |
| massimo inizializzato a 0 | proporre una lista di valori tutti negativi |
| confusione tra indice e valore in `for` | confrontare `for t in lista` e `for i in range(len(lista))` stampando entrambi |

### Supporto differenziato

- studenti con esperienza di programmazione: esercizi di approfondimento; in più, leggere e spiegare le righe `assert` dei file di esercizi
- studenti in difficoltà: completare solo gli esercizi base, usando il debugger; lavorare in coppia con uno studente più esperto (pair programming, ruoli di "pilota" e "navigatore" invertiti ogni 10 minuti)

## Valutazione

Verifica di modulo al termine di L8 (seconda parte del modulo). Per L3-L5 si raccolgono indicatori formativi:

| Indicatore | Dove |
|---|---|
| prevede il risultato di espressioni con `//`, `%`, `**` | L3, esercizio 1; domande in aula |
| converte correttamente l'input dell'utente | L3, esercizio 5 |
| scrive condizioni con `if`/`elif`/`else` e cicli `while` che terminano | L4, esercizi 1-3 e 6 |
| spiega come pesi e soglia determinano il comportamento del neurone | L4, esercizi 4-5 |
| usa il metodo dell'accumulatore su una lista | L5, esercizi 1-3 |
| calcola una somma pesata e la collega al neurone | L5, esercizi 4-5 |

Gli esercizi sono autocorretti: per la valutazione conviene osservare anche il codice, non solo il fatto che i controlli siano superati. Per esempio, l'esercizio 1 di L5 può essere superato con `sum()`, che la consegna esclude.

## Soluzioni

Le soluzioni complete ed eseguibili sono nella cartella `lab/soluzioni/`:

- `L3_02_esercizi_soluzioni.py`, `L3_03_conversione_interattiva_soluzione.py`
- `L4_03_esercizi_soluzioni.py`, `L4_04_indovina_numero_soluzione.py`
- `L5_03_esercizi_soluzioni.py`

Note sulle soluzioni:

- L3, esercizio 2: il risultato stampato è `97.88000000000001`, un esempio concreto di approssimazione dei `float` da commentare in aula; il controllo usa `math.isclose`
- L3, esercizio 4: $\sigma(4) \approx 0.982$, $\sigma(-4) \approx 0.018$; la loro somma è 1 per la simmetria della sigmoide, $\sigma(-x) = 1 - \sigma(x)$
- L4, esercizio 4 (OR): per esempio $w_1 = w_2 = 1$, soglia 0.5; funziona qualunque soglia maggiore di 0 e non superiore a 1
- L4, esercizio 5 (NAND): per esempio $w_1 = w_2 = -1$, soglia -1.5; il neurone NAND ha i pesi e la soglia di AND cambiati di segno. È un risultato significativo: con porte NAND si può costruire qualsiasi circuito logico, quindi reti di neuroni a soglia possono calcolare qualsiasi funzione logica
- L4, domanda XOR: non esistono pesi e soglia adatti; la dimostrazione geometrica è in L13
- L5, esercizio 4: il risultato stampato è `-0.8999999999999999`
- L5, esercizio 5 (maggioranza): per esempio pesi `[1, 1, 1]`, soglia 2; con pesi uguali a 1 funziona qualunque soglia maggiore di 1 e non superiore a 2

## Materiale open source

Verifica puntuale per L3, L4, L5: le lezioni sono scritte da zero. I contenuti coincidono con i capitoli introduttivi di qualunque corso di Python; tra i materiali in italiano, il tutorial ufficiale (capitoli 3 e 4) tratta gli stessi argomenti con un taglio meno orientato al calcolo numerico: https://docs.python.org/it/3/tutorial/

L'uso del neurone a soglia come esempio di programmazione introduttiva non è ripreso da un corso specifico.
