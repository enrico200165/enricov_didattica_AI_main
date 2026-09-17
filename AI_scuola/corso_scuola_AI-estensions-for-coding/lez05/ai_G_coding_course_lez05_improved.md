---
marp: true
title: Lezione 5 – Chatbot di Supporto al Coding
theme: default
paginate: true
class: lead
---

# Lezione 5 – Chatbot di Supporto al Coding
**Durata:** 2 ore  
Pubblico: studenti 14-19 anni con basi di programmazione

---

## Obiettivi
- Comprendere come un chatbot AI può fornire supporto diretto nella scrittura e comprensione di codice.
- Creare un chatbot semplice locale per rispondere a domande di coding, enfatizzando privacy e accessibilità.
- Sviluppare un approccio critico all'uso dei chatbot per la risoluzione di problemi di programmazione.

---

## Contenuti
### 1. Introduzione ai chatbot di supporto al coding
- **Definizione:** Un chatbot di supporto è un assistente virtuale che utilizza l'IA per rispondere a domande, spiegare concetti di sintassi, fornire esempi di codice e aiutare a risolvere problemi di programmazione.
- **Vantaggi principali:**
    - **Accessibilità:** Fornisce risposte immediate 24/7.
    - **Apprendimento:** È un ottimo strumento per esplorare nuove sintassi o approfondire concetti.

---

- **Limiti:**
    - Può generare risposte errate o fuorvianti, che richiedono verifica.
    - Non sostituisce la comprensione concettuale del programmatore.

### 2. Introduzione a GPT4All: L'IA offline
- **Cos'è:** Un modello di linguaggio di grandi dimensioni (LLM) che può essere eseguito localmente sul computer, senza la necessità di una connessione internet costante.
- **Vantaggi:**
    - **Privacy:** I dati di coding e le domande non lasciano mai il computer.
    - **Costo zero:** L'uso dei modelli è completamente gratuito.
    - **Autonomia:** Funziona anche senza connettività, ideale per l'ambiente scolastico.

---

- **Modelli disponibili:** Esistono diverse varianti ottimizzate per il coding, spesso con dimensioni ridotte per funzionare su hardware meno potente.

---


### 3. Libreria Gradio: creare interfacce in un attimo
- **Cos'è:** Una libreria Python che permette di creare interfacce web semplici e interattive in poche righe di codice.
- **Perché usarla:**
    - **Facile e veloce:** Ideale per prototipare rapidamente un'interfaccia utente per il nostro chatbot.
    - **Interfaccia browser:** Permette di interagire con il modello AI tramite un'interfaccia familiare.

---

### 4. Architettura di base di un chatbot locale
- **Flusso logico:**
    - L'utente inserisce una domanda (`Input Utente`).
    - Il programma invia la domanda al modello GPT4All caricato localmente.
    - Il modello elabora la richiesta.
    - Viene restituita una risposta (`Risposta Generata`).
    - L'interfaccia Gradio visualizza la risposta all'utente.

---

## Attività Pratiche
1. **Installazione e configurazione:**
   - Installare le librerie necessarie con un comando terminale: `pip install gpt4all gradio`.
   - Aprire l'interfaccia desktop di GPT4All e scaricare un modello di linguaggio adatto (es. `Mistral 7B`). Spiegare il perché di questa scelta.
2. **Creazione di uno script Python per il chatbot:**
   - Scrivere uno script che importi Gradio e la libreria GPT4All.
   - Definire una funzione che prenda un input testuale, lo passi al modello GPT4All e restituisca l'output.

---

3. **Costruzione dell'interfaccia web con Gradio:**
   - Usare la funzione `gr.Interface` per creare un'interfaccia utente per il chatbot.
   - Definire un titolo, un input di testo e un output di testo.
   - Avviare il server locale e testare il chatbot dal browser.
4. **Testare il chatbot con domande di coding:**
   - Porre domande di base su sintassi Python (`Come si dichiara una lista?`).
   - Chiedere la spiegazione di un blocco di codice complesso (`Spiega questo codice: [incollare una funzione]`).
   - Analizzare le risposte e correggere eventuali errori o incoerenze.

---

## Esercizio finale (30 min)
- **Ampliare il chatbot:**
  1.  Modificare il codice per aggiungere una "memoria" rudimentale, salvando le ultime 3 domande e risposte.
  2.  Personalizzare il prompt iniziale del modello per fargli sapere che è un "assistente di programmazione per principianti in Python".
  3.  Testare il chatbot con almeno 5 domande differenti, inclusa una richiesta di generare un piccolo snippet di codice (es. `Genera una funzione Python che calcoli l'area di un cerchio`).
- **Discussione in classe:** Condividere i risultati, confrontare la qualità delle risposte e discutere i possibili miglioramenti.

---

## Conclusioni
- I chatbot AI sono un'ottima risorsa per **accelerare l'apprendimento e la risoluzione di problemi**, ma vanno usati con giudizio.
- Soluzioni locali come GPT4All offrono una strada per sperimentare con l'IA in modo **gratuito, privato e autonomo**.
- L'uso di un'interfaccia come Gradio rende lo sviluppo di strumenti AI accessibile anche a chi è alle prime armi.

---

## Compito per casa
- Creare un chatbot offline simile, aggiungendo risposte a domande su concetti specifici di Python (es. variabili, liste, condizioni `if`).
- Se possibile, esportare lo script e l'interfaccia in un file `.zip` da condividere con il docente per la prossima lezione.

---

## Note per l'Insegnante

**Modifiche e integrazioni apportate alla lezione:**

* **Obiettivi più mirati:** Gli obiettivi sono stati affinati per includere l'importanza della privacy, dell'accessibilità e del pensiero critico, aspetti cruciali dell'uso di IA locale.
* **Contenuti arricchiti e didattici:**
    * È stata aggiunta una sezione introduttiva sui chatbot di supporto in generale, per fornire un contesto più ampio prima di passare agli strumenti specifici.
    * È stata introdotta l'architettura base del chatbot, schematizzando il flusso di dati (input-modello-output-interfaccia) per rendere il concetto più chiaro e strutturato.

---


* **Attività Pratiche più dettagliate:** I passaggi per l'installazione e la creazione dello script sono stati resi più precisi, suggerendo comandi e nomi di modelli specifici (`Mistral 7B`) per rendere l'attività più fluida e concreta per gli studenti.
* **Focus sulla personalizzazione:** Nell'esercizio finale è stato aggiunto il concetto di "personalizzare il prompt" per l'IA, una tecnica avanzata ma accessibile che introduce l'idea di dare una "personalità" al modello, un concetto che sarà utile anche in progetti futuri.
* **Nessun Overlap:** Il contenuto rimane focalizzato sulla creazione di un chatbot locale, distinto dal refactoring (Lezione 6) e dai mini-progetti (Lezione 7), mantenendo la progressione logica del corso.