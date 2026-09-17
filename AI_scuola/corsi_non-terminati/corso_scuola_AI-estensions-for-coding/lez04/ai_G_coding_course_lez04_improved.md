---
marp: true
title: Lezione 4 – Debug Assistito da IA
theme: default
paginate: true
class: lead
---

# Lezione 4 – Debug Assistito da IA
**Durata:** 2 ore  
Pubblico: studenti 14-19 anni con basi di programmazione

---

## Obiettivi
- Usare strumenti AI per individuare bug nel codice in modo più rapido e preciso.
- Comprendere come interpretare i suggerimenti di correzione proposti dall'IA.
- Sviluppare un approccio critico al debugging assistito.

---

## Contenuti
### 1. Tipi di errori comuni in Python: una rassegna
- **Errori di sintassi:** Questi sono i problemi più facili da individuare, spesso segnalati dall'editor stesso. Esempi comuni includono parentesi mancanti, indentazione errata o keyword scritte in modo scorretto.
- **Errori logici:** Sono i più difficili da trovare. Il codice viene eseguito correttamente, ma produce un risultato inatteso o sbagliato. Un esempio classico è un calcolo errato, una condizione `if` sbagliata o un loop che non termina.

---

- **Eccezioni (`Exceptions`):** Errori che si verificano durante l'esecuzione del programma e che ne interrompono il normale flusso. Esempi comuni sono `IndexError` (quando si accede a un indice inesistente in una lista), `TypeError` (operazione su tipi di dati incompatibili) e `ValueError` (valore errato passato a una funzione).

---

### 2. Analisi statica vs. AI debugging
- **Analisi Statica del Codice (Linters):**
  - Strumenti come `pylint` o `flake8` analizzano il codice senza eseguirlo.
  - Sono ottimi per rilevare problemi di sintassi, errori di stile (`PEP 8` in Python), variabili non usate o importazioni mancanti.
  - Limitazione: non possono capire errori logici complessi, poiché non vedono il comportamento dinamico del programma.

---


- **Debugging con IA:**
  - L'IA analizza non solo la sintassi, ma il **contesto semantico** del codice.
  - Può fare un'ipotesi più informata sulla causa di un errore, sia esso di sintassi che, soprattutto, di logica.
  - Vantaggio: spesso suggerisce possibili cause, fornisce esempi di correzioni e può persino spiegare il motivo dell'errore.
  - Esempio: se un `for` loop ha un `range` che causa un `IndexError`, l'IA potrebbe suggerire una correzione specifica basata sulla lunghezza della lista, cosa che un linter non farebbe.

---

### 3. Strumenti di Debugging AI
- **Codeium Debug Assistant:** Fornisce suggerimenti in tempo reale direttamente all'interno dell'editor di codice. Può spiegare il motivo di un'eccezione e suggerire un fix con un solo clic.
- **Altri strumenti:** Altre estensioni per VS Code e piattaforme online offrono funzionalità simili, combinando l'analisi statica con la potenza dei modelli di linguaggio per un'analisi più approfondita.

---

## Attività Pratiche
1. **Creare codice con errori volontari:**
   - Prepara una funzione semplice, ad esempio una che calcoli la media di una lista di numeri.
   - Introduci volutamente degli errori di vario tipo:
     - Un errore di sintassi (es. `def` scritto male).
     - Un errore logico (es. `return` fuori dal ciclo, che restituisce un risultato errato).
     - Un'eccezione (es. dividere per zero se la lista è vuota).

---


2. **Usare estensioni AI per individuare e correggere i bug:**
   - Con Codeium attivo, osserva come l'estensione segnala l'errore.
   - Clicca sul suggerimento e analizza la spiegazione fornita dall'IA.
   - Accetta o modifica la correzione proposta.
3. **Correzione manuale basata sui suggerimenti:**
   - Chiedi agli studenti di non accettare immediatamente il suggerimento, ma di usarlo come guida per capire l'errore e fare la correzione manuale. Questo rafforza l'apprendimento.
   - Ripeti il processo con gli altri bug, testando il codice dopo ogni correzione per verificarne il corretto funzionamento.

---

## Esercizio finale (30 min)
- **Scenario:** Un programma Python che calcola la media dei voti di una classe.
- **Task:**
  1. Copiare il codice fornito dall'insegnante, che contiene almeno 3 bug (es. divisione per il numero di elementi sbagliato, variabile non inizializzata, gestione input non numerico).
  2. Usare gli strumenti AI per individuare i bug.
  3. Per ogni bug, spiegare (a voce o in una nota) il tipo di errore e il motivo della correzione.
  4. Applicare le modifiche per far funzionare correttamente il programma.

---

## Conclusioni
- L'IA è un supporto prezioso per il debugging, ma non sostituisce il ragionamento critico del programmatore.
- L'obiettivo non è solo risolvere l'errore, ma **capire perché si è verificato**.
- Un buon programmatore combina l'analisi manuale, la comprensione della logica e l'uso intelligente di strumenti AI per risolvere i problemi in modo efficiente.

---

## Compito per casa
- Scrivere uno script Python per calcolare il massimo e il minimo di una lista di numeri inserita dall'utente.
- Introdurre due bug volontari, ad esempio:
    - Un bug logico (es. non inizializzare correttamente il valore massimo/minimo).
    - Un bug che genera un'eccezione (`ValueError` se l'utente non inserisce un numero).
- Usare gli strumenti AI per correggere il codice e scrivere una breve spiegazione del processo di debugging seguito.

---

## Note per l'Insegnante

**Modifiche e integrazioni apportate alla lezione:**

* **Obiettivi più specifici:** Gli obiettivi sono stati resi più chiari e orientati all'apprendimento critico, sottolineando l'importanza di *interpretare* e *sviluppare un approccio critico*, oltre che semplicemente usare lo strumento.
* **Contenuti arricchiti e strutturati:**
    * La sezione sui tipi di errori è stata resa più didattica, spiegando non solo la definizione ma anche esempi concreti per ogni categoria (sintassi, logica, eccezioni).
    * La differenza tra "Analisi Statica" e "Debugging con IA" è stata esplicitata meglio, con una chiara spiegazione delle rispettive funzioni e limiti, per evitare confusioni e preparare gli studenti a usare entrambi gli strumenti in modo complementare.
* **Attività Pratiche più guidate:** L'attività pratica è stata strutturata in passaggi più chiari: prima creare errori, poi usare l'IA, e infine, il passaggio più importante, correggere manualmente *basandosi* sui suggerimenti. Questo incoraggia il ragionamento autonomo e la comprensione del problema, anziché la semplice accettazione della soluzione.
* **Nessun Overlap con il Syllabus:** La lezione mantiene il suo focus sul **debugging** e non si sovrappone ai temi di refactoring (Lezione 6) o chatbot di supporto (Lezione 5), garantendo una progressione logica del corso.