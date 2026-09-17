---
marp: true
title: Lezione 3 – Generazione di Snippet di Codice da Prompt
theme: default
paginate: true
class: lead
---

# Lezione 3 – Generazione di Snippet di Codice da Prompt
**Durata:** 2 ore  
Pubblico: studenti 14-19 anni con basi di programmazione

---

## Obiettivi
- Imparare a creare codice da istruzioni in linguaggio naturale.
- Conoscere i limiti e i rischi della generazione automatica di codice.
- Sviluppare un approccio critico verso il codice generato dall'IA.

---

## Contenuti
### 1. Cos'è un prompt per il coding?
- **Definizione:** Un prompt è un'istruzione in linguaggio naturale (testo) che l'IA elabora per generare una risposta, in questo caso, codice. È la "richiesta" che dai all'IA.
- **Interpretazione:** L'IA non si limita a cercare parole chiave, ma analizza l'intento dietro il testo per comprendere cosa vuoi fare.
- **Analogia:** Pensa a un prompt come a un brief per un assistente programmatore, che deve essere il più preciso e dettagliato possibile per ottenere il risultato desiderato.

---

- **Differenze:**
    - **Prompt generico:** `Scrivi una funzione Python`.
    - **Prompt specifico:** `Scrivi una funzione in Python chiamata 'is_palindrome' che verifica se una stringa è palindroma, ignorando spazi e maiuscole. Includi docstring e un esempio di utilizzo.`

---

### 2. L'arte di scrivere richieste efficaci (Prompt Engineering)
- **Struttura del prompt:** Un buon prompt è una combinazione di istruzioni chiare.
    1. **Obiettivo:** Descrivi cosa deve fare il codice (`Crea un gioco...`).
    2. **Linguaggio e contesto:** Specifica il linguaggio (`in Python`), le librerie (`usando la libreria random`), e l'ambiente (`per la console`).
    3. **Vincoli e requisiti:** Indica dettagli specifici (`la lista deve avere 10 elementi`, `il numero di tentativi è 5`).
    4. **Esempi:** Aggiungi un esempio di input e output desiderato (`input: '12321', output: True`).

---


- **Esempi pratici:**
    - **Prompt vago:** `Scrivi del codice per un gioco`.
    - **Prompt efficace:** `Crea in Python 3.10 un gioco testuale a turni chiamato "Indovina il numero". L'IA deve scegliere un numero casuale tra 1 e 100. L'utente ha un massimo di 7 tentativi per indovinare. Dopo ogni tentativo, il programma deve dire se il numero inserito è troppo alto o troppo basso.`

---

### 3. Rischi e limiti della generazione automatica di codice
- **Codice errato o incompleto:** I modelli possono "allucinare" e produrre codice che non funziona o non rispetta le specifiche.
- **Problemi di sicurezza:** Il codice generato può contenere vulnerabilità o dipendenze obsolete, perché l'IA non ha un giudizio critico sulla sicurezza.
- **Efficienza e stile:** Il codice potrebbe non essere ottimizzato o non seguire le migliori pratiche di programmazione (`best practice`).
- **Necessità di verifica:** Il programmatore è sempre responsabile del codice e deve verificarlo, testarlo e, se necessario, migliorarlo manualmente.

---

## Attività Pratiche
1. **Accesso e introduzione a Code Llama su Hugging Face Spaces:**
   - Accedi alla piattaforma gratuita.
   - Analizza l'interfaccia: dove si inserisce il prompt, dove appare il codice.
   - **Obiettivo:** Familiarizzare con lo strumento prima di iniziare.
2. **Esercizi di generazione guidata:**
   - **Esercizio 1 (Prompt semplice):** Inserisci un prompt per creare una funzione Python che calcola il volume di un cubo. Osserva il risultato.
   - **Esercizio 2 (Prompt dettagliato):** Modifica lo stesso prompt chiedendo all'IA di includere dei commenti che spieghino ogni passaggio.
   
---


   - **Esercizio 3 (Prompt complesso):** Scrivi un prompt per creare uno script Python che simuli un conto alla rovescia da 10 a 0, facendo una pausa di 1 secondo tra ogni numero.
3. **Discussione e analisi dei risultati:**
   - Confronta il codice generato con quello che scriveresti a mano.
   - Discuti in classe quali parti del codice sono state utili e quali potrebbero essere migliorate o sono errate.

---

## Esercizio finale (25 min)
- **Prompt da scrivere:** `Crea un gioco testuale in Python chiamato "Indovina la parola".`
    - **Passo 1:** Scrivi il prompt, specificando che il gioco deve scegliere una parola casuale da una lista predefinita (`gatto`, `cane`, `sole`, `luna`).
    - **Passo 2:** Aggiungi i dettagli: l'utente deve indovinare la parola, ha 5 tentativi. Dopo ogni tentativo, il programma deve dire quante lettere ha indovinato e in che posizione (es. "Hai indovinato 2 lettere, una in posizione corretta e una in posizione sbagliata").
    - **Passo 3:** Genera il codice, eseguilo per testarlo e, se necessario, correggilo manualmente per farlo funzionare perfettamente.

---

## Conclusioni
- L'IA è un acceleratore, non un sostituto. È perfetta per la creazione rapida di prototipi e la scrittura di codice standard (`boilerplate`).
- Il "prompt engineering" (l'arte di scrivere prompt) è una nuova competenza fondamentale.
- Sviluppare un approccio critico è essenziale: **leggere, comprendere, testare e migliorare** il codice generato è la responsabilità finale del programmatore.

---

## Compito per casa
- Sperimentare con 3 prompt diversi per creare in Python:
  1. Un convertitore tra gradi Celsius e Fahrenheit.
  2. Una funzione che trova il numero più frequente in una lista.
  3. Un mini quiz a scelta multipla che legge le domande da un file di testo.
- Per ogni prompt, annotare i vantaggi e gli svantaggi del codice generato.

---

## Note per l'Insegnante

**Modifiche e integrazioni apportate alla lezione:**

* **Arricchimento della parte teorica (Prompt Engineering):** La lezione è stata arricchita con una sezione dedicata all'arte di scrivere prompt efficaci (`Prompt Engineering`), un concetto cruciale che non era esplicitato. È stato fornito un esempio chiaro di prompt "vago" contro "efficace" per facilitare la comprensione degli studenti. È stata introdotta un'analogia del "brief" per rendere l'idea più concreta.
* **Struttura delle Attività Pratiche:** Le attività sono state rese più graduali e guidate. Invece di chiedere semplicemente di creare snippet, è stato proposto un percorso che va dal prompt semplice a quello più dettagliato, incoraggiando gli studenti a iterare e migliorare le loro richieste. Questo rinforza il concetto di "Prompt Engineering" in modo pratico.
* **Maggiore enfasi sui rischi e limiti:** È stata ampliata la sezione sui limiti dell'IA, fornendo esempi specifici di potenziali problemi (sicurezza, efficienza) per stimolare il pensiero critico. L'esercizio finale ora richiede esplicitamente di correggere manualmente il codice generato, ribadendo il ruolo fondamentale del programmatore.
* **Nessun Overlap con il Syllabus:** I contenuti restano focalizzati sulla **generazione da prompt** e non si sovrappongono alla Lezione 4 (Debugging Assistito) o alla Lezione 5 (Chatbot di supporto), mantenendo la coerenza del piano didattico. La durata rimane ben entro le due ore grazie alla struttura chiara e alle attività interattive.