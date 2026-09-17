---
marp: true
title: Lezione 2 – Completamento Automatico e Suggerimenti Intelligenti
theme: default
paginate: true
class: lead
---

# Lezione 2 – Completamento Automatico e Suggerimenti Intelligenti
**Durata:** 2 ore  
Pubblico: studenti 14-19 anni con basi di programmazione

---

## Obiettivi
- Capire il funzionamento dell'autocompletamento AI.
- Usare strumenti per velocizzare la scrittura del codice.

---

## Contenuti
### 1. Come l'IA predice il codice: un’analogia
- Immagina il correttore automatico del tuo telefono. L'IA fa lo stesso, ma non con le parole, bensì con le istruzioni di programmazione.
- Funzionamento di base degli LLM: analizzano il testo che hai già scritto e predicono, in base a miliardi di righe di codice su cui sono stati addestrati, quale potrebbe essere la parola o l'istruzione successiva più probabile.
---
- Analisi del contesto: i modelli AI non si limitano a suggerire una parola, ma analizzano l'intero contesto: le variabili che hai definito, il nome della funzione, il commento che hai inserito. Questo permette suggerimenti molto più intelligenti e pertinenti.
- Differenza tra suggerimenti statici (parole chiave) e predittivi (AI basata su contesto).
---

### 2. Confronto tra completamento statico e predittivo
- **Completamento Statico:**
  - Basato su un dizionario di parole chiave del linguaggio o sulle firme delle funzioni di una libreria conosciuta.
  - È veloce e affidabile, ma molto limitato. Suggerisce solo la sintassi predefinita senza capire la logica.
- **Completamento Predittivo (AI):**
  - Analizza l'intero file, le convenzioni di stile e il contesto semantico del progetto.
  - Può proporre interi blocchi di codice, cicli complessi o funzioni complete, anche se non le hai mai definite prima.
  - Si adatta allo stile di codifica del programmatore, "imparando" dalle sue abitudini.

---

## Attività Pratiche
1. **Attivazione e primo utilizzo di Codeium:**
   - Assicurarsi che Codeium sia installato e attivo in VS Code.
   - Creare un nuovo file `.py` e uno `.js`.
   - Provare a scrivere un commento, per esempio: `# funzione che calcola la somma di una lista di numeri`. L'IA dovrebbe suggerire un'intera funzione.

---

2. **Esercizi di autocompletamento guidato:**
   - Scrivere un ciclo `for` in Python (`for item in lista:`). Osservare i suggerimenti dell'AI per il corpo del ciclo.
   - Creare una funzione per calcolare la media di una lista. L'AI dovrebbe completare la logica.
   - Provare a gestire un caso limite, ad esempio chiedendo all'AI di aggiungere un controllo per una lista vuota. Questo dimostra la sua capacità di anticipare gli errori.

---

3. **Confronto "manuale vs. assistito":**
   - Scegliere una funzione di complessità media (es. verifica di un numero primo).
   - Scrivere il codice **senza AI** e cronometrare il tempo impiegato e gli errori commessi.
   - Ripetere lo stesso esercizio **con AI attiva**, accettando o rifiutando i suggerimenti. Confrontare i risultati.

---

## Esercizio finale (25 min)
- Creare uno script Python che:
  1. Generi una lista di numeri casuali utilizzando la libreria `random`.
  2. Calcoli media, massimo e minimo della lista.
  3. Stampi i risultati in un formato leggibile.
- **Obiettivi:**
  - Utilizzare intensivamente i suggerimenti AI per completare ogni passaggio dello script.
  - Prestare attenzione alla correttezza del codice proposto, validandolo.
  - Commentare il codice, osservando come l'IA può generare la documentazione delle funzioni.

---

## Conclusioni
- L'autocompletamento AI è un potente alleato che permette di **risparmiare tempo prezioso** e ridurre la stesura di codice ripetitivo.
- I suggerimenti non sono sempre corretti o ottimali. È fondamentale che il programmatore mantenga il **controllo critico e validi il codice** proposto dall'AI.
- L'uso dell'AI è uno strumento di supporto, non un sostituto della logica di programmazione. La comprensione dei concetti di base resta la competenza più importante.

---

## Compito per casa
- Scrivere uno script JavaScript che gestisca un array di nomi:
  - Dichiarazione di un array con 3-4 nomi.
  - Aggiunta di un nuovo nome.
  - Ordinamento alfabetico dell'array.
  - Stampa dell'elenco finale.
- Analizzare il processo: annotare quanto l'AI ha aiutato nel completamento e dove non è stata utile (es. suggerimenti ridondanti o errati).

---

## Note per l'Insegnante

**Modifiche e integrazioni apportate alla lezione:**

* **Contenuti Teorici più chiari:** È stata introdotta un'analogia con il "correttore del telefono" per spiegare in modo più semplice il funzionamento degli LLM. Inoltre, la differenza tra autocompletamento statico e predittivo è stata resa più visiva e schematica.
* **Attività Pratiche più strutturate:**
    * È stato aggiunto un passaggio specifico in cui gli studenti provano a scrivere un commento e vedono l'AI generare l'intera funzione. Questo dimostra in modo rapido e impressionante la potenza dello strumento.
    * L'attività di confronto "manuale vs. assistito" è stata resa più concreta, suggerendo l'uso di un cronometro per rendere tangibile il risparmio di tempo.
* **Focus sulla validazione:** Nelle conclusioni è stato aggiunto un punto esplicito sull'importanza di validare e revisionare il codice proposto dall'AI, un'abilità critica per gli studenti. Questo previene l'assuefazione e promuove il pensiero critico.
* **Nessun Overlap:** Le integrazioni non sovrappongono la lezione con quelle successive. Si mantiene il focus sul "completamento" e non sulla "generazione da prompt", che è il fulcro della Lezione 3, garantendo una progressione logica e coesa del corso.