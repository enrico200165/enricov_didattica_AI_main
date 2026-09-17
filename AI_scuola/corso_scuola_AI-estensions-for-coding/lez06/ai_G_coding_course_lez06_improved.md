---
marp: true
title: Lezione 6 – Refactoring e Ottimizzazione Codice con AI
theme: default
paginate: true
class: lead
---

# Lezione 6 – Refactoring e Ottimizzazione Codice con AI
**Durata:** 2 ore  
Pubblico: studenti 14-19 anni con basi di programmazione

---

## Obiettivi
- Capire cos'è il refactoring e perché è fondamentale per lo sviluppo software.
- Utilizzare strumenti di AI per identificare aree di miglioramento e ottimizzare codice scritto manualmente.
- Sviluppare un senso critico per confrontare il codice originale con la versione ottimizzata, analizzandone i benefici.

---

## Contenuti
### 1. Concetto di Refactoring
- **Definizione:** Il refactoring è il processo di miglioramento della struttura e leggibilità del codice, **senza modificarne il comportamento esterno o le funzionalità**.
- **Benefici principali:**
  - **Maggiore leggibilità e manutenibilità:** Il codice più chiaro è più facile da leggere e da modificare in futuro.
  - **Riduzione del codice duplicato:** Identificare e rimuovere sezioni di codice ripetute per evitare la ridondanza e gli errori.
  - **Prevenzione dei bug:** Un codice più pulito e modulare ha meno probabilità di contenere difetti nascosti.

---


### 2. Principi chiave del refactoring
- **Pulizia del codice:**
  - Usare nomi di variabili e funzioni chiari e descrittivi.
  - Semplificare le espressioni complesse.
  - Suddividere le funzioni lunghe in funzioni più piccole e specifiche.
- **Eliminazione delle duplicazioni:**
  - Se due blocchi di codice fanno la stessa cosa, estraili in una singola funzione da riutilizzare.
  - Questo rende il codice più modulare e più semplice da aggiornare.

---


- **Ottimizzazione delle prestazioni:**
  - Rivedere cicli o operazioni ricorsive che possono essere inefficienti.
  - Usare strutture dati più appropriate per il problema (es. dizionari anziché liste per ricerche rapide).

---


### 3. Strumenti AI per il refactoring
- **Sourcery:** Un plugin per Python che si integra direttamente in editor come VS Code. Analizza il codice e fornisce suggerimenti di refactoring in tempo reale, spesso con un solo clic per applicare la modifica. È specializzato nell'individuare e proporre la riscrittura di `if` complessi, cicli, e altre strutture sintattiche.
- **Codeium:** Oltre all'autocompletamento, Codeium può fornire suggerimenti intelligenti per migliorare la leggibilità e l'efficienza del codice, soprattutto quando riscrivi manualmente una sezione. La sua forza sta nella comprensione del contesto più ampio del progetto.

---

## Attività Pratiche
1. **Creazione di codice poco ottimizzato:**
   - In VS Code, scrivere una funzione Python che calcoli la somma e la media di una lista di voti.
   - Introdurre volutamente duplicazioni (es. calcolare la somma in due punti diversi) e usare nomi di variabili poco chiari (es. `x`, `y`).
2. **Uso di Sourcery:**
   - Assicurarsi che l'estensione Sourcery sia installata e attiva.
   - Osservare le frecce o le icone di refactoring che appaiono accanto al codice.
   - Cliccare sui suggerimenti per visualizzare le modifiche proposte e discuterne in classe.

---


3. **Applicare e confrontare le correzioni:**
   - Applicare le modifiche suggerite da Sourcery, notando come il codice diventa più compatto e leggibile.
   - Chiedere agli studenti di spiegare il "prima" e il "dopo", motivando perché la nuova versione è migliore.
4. **Utilizzo di Codeium (alternativa):**
   - Provare a riscrivere manualmente una sezione del codice e osservare come Codeium suggerisce completamenti che sono già ottimizzati, guidando verso `best practice`.

---

## Esercizio finale (30 min)
- **Scenario:** Rifattorizzare una funzione Python che calcola media, massimo e minimo di una lista di numeri. Il codice iniziale è volutamente poco leggibile, con cicli e variabili ridondanti.
- **Task:**
  1. Analizzare il codice originale fornito.
  2. Usare Sourcery e Codeium per individuare suggerimenti di miglioramento.
  3. Rifattorizzare la funzione fino a renderla chiara e concisa.
  4. Scrivere una breve spiegazione dei miglioramenti ottenuti.

---

## Conclusioni
- Il refactoring è un'abilità fondamentale per un programmatore.
- L'IA agisce come un "mentore" che aiuta a individuare i punti deboli del codice e a proporre miglioramenti basati su schemi di programmazione ottimali.
- Strumenti come Sourcery non solo velocizzano il lavoro, ma aiutano anche a imparare buone pratiche di coding.

---

## Compito per casa
- Prendere un vecchio esercizio svolto in una delle lezioni precedenti (es. il calcolo del fattoriale o la verifica del numero primo).
- Applicare il refactoring con l'aiuto di Sourcery o Codeium.
- Portare in classe la versione originale e quella rifattorizzata, pronte per la discussione collettiva nella prossima lezione.

---

## Note per l'Insegnante

**Modifiche e integrazioni apportate alla lezione:**

* **Contenuti più concreti:** Le sezioni "Concetto di Refactoring" e "Principi chiave" sono state arricchite con esempi pratici e analogie per rendere i concetti astratti più comprensibili agli studenti. È stato enfatizzato che l'obiettivo non è solo migliorare, ma capire *perché* il codice migliora.
* **Attività Pratiche mirate:** È stato suggerito un esempio di codice volutamente mal scritto da usare in classe. Questo rende l'attività più guidata e tangibile, garantendo che gli studenti abbiano un punto di partenza comune e possano confrontare i risultati.

---


* **Strumenti specifici:** La sezione "Strumenti AI per il refactoring" ora distingue chiaramente il ruolo di Sourcery (suggerimenti specifici di riscrittura) da quello di Codeium (assistenza contestuale durante la riscrittura), offrendo una visione più completa e strategica del loro utilizzo.
* **Coerenza con il Syllabus:** Il contenuto si allinea perfettamente con gli obiettivi della Lezione 6 e prepara gli studenti per il progetto finale (Lezione 7), dove dovranno applicare tutte le competenze acquisite, inclusa quella di refactoring. La durata rimane ben gestita entro le due ore previste.