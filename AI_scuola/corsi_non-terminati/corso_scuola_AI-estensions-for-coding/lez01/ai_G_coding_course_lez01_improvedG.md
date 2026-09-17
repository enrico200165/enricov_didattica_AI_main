---
marp: true
title: Lezione 1 – Introduzione a IA e Coding Assistito
theme: default
paginate: true
class: lead
---

# Lezione 1 – Introduzione a IA e Coding Assistito
**Durata:** 2 ore  
Pubblico: studenti 14-19 anni con basi di programmazione

---

## Obiettivi
- Comprendere cos'è l'IA e il suo ruolo nel coding.
- Conoscere strumenti di assistenza al codice gratuiti e open source.
- Comprendere la differenza tra strumenti di completamento automatico tradizionali e basati su IA.

---

## Contenuti
### 1. Breve storia dell'IA nel software development
- **Anni '90:** L'alba del coding assistito. I primi IDE (Integrated Development Environment) offrivano un completamento automatico basato su parole chiave fisse e predefinite.
- **2000-2015:** IDE più avanzati con funzionalità di refactoring e analisi statica del codice, che aiutavano a identificare potenziali errori senza eseguire il programma.
- **2020+:** L'avvento dei modelli di linguaggio di grandi dimensioni (LLM). Questi modelli, addestrati su enormi quantità di codice, sono capaci di predire e suggerire interi blocchi di codice, commenti e persino test, basandosi sul contesto. Strumenti come Codeium e GitHub Copilot diventano popolari.

---

### 2. Panoramica delle estensioni AI nei moderni editor di codice
- Funzionalità principali: completamento intelligente, suggerimenti di refactoring, generazione automatica di test e documentazione, individuazione di bug.
- **Differenza chiave:** Gli strumenti tradizionali (autocomplete statico) si limitano a suggerire nomi di variabili o funzioni già presenti nel codice o nella libreria. Le estensioni AI sono **contestuali e predittive**: analizzano l'intero file, il nome della funzione che stai scrivendo e il commento che hai inserito, per proporre un codice che ha un senso logico.

---

### 3. Introduzione a Visual Studio Code e Codeium
- **Perché VS Code:** È un editor di codice gratuito, leggero e multipiattaforma. Supporta centinaia di linguaggi di programmazione ed è il punto di riferimento per il vasto ecosistema di estensioni.
- **Codeium:** Un'estensione AI gratuita che offre un'assistenza completa per la scrittura del codice. È un'ottima alternativa open source ad altri strumenti a pagamento.
- **Come funziona:** Codeium opera localmente per alcune operazioni, ma si connette a un servizio cloud per l'assistenza più complessa, garantendo un'esperienza fluida.

---

## Attività Pratiche
1. **Installazione e configurazione di Visual Studio Code:**
   - Download da [https://code.visualstudio.com](https://code.visualstudio.com) e avvio.
   - Configurazione dell'interfaccia (es. tema scuro/chiaro).
   - Creazione di una nuova cartella per il progetto e apertura in VS Code.
   - Installazione dell'estensione per il linguaggio Python (se non già presente).

---

2. **Installazione dell'estensione Codeium:**
   - Aprire il Marketplace delle estensioni di VS Code.
   - Cercare "Codeium" e cliccare su "Installa".
   - Effettuare l'accesso gratuito per attivare le funzionalità avanzate.

---

3. **Primo test: Scrivere e modificare codice con l'AI:**
   - Scrivere una funzione Python semplice (es. `somma` o `media`) e osservare i suggerimenti che compaiono.
   - **Esempio interattivo:** Inserire un piccolo errore di sintassi (`def somma(a, b): return a + b_`) e vedere se l'IA aiuta a correggerlo. Questo dimostra come l'IA non solo completa, ma assiste anche nel debugging.

---

## Esercizio finale (20 min)
- Scrivere una funzione Python per calcolare il **fattoriale di un numero**.
- Obiettivi dell'esercizio:
  - Verificare e accettare/rifiutare i suggerimenti proposti dall'IA.
  - Confrontare la soluzione generata dall'AI con quella che avrebbero scritto manualmente.
  - Analizzare vantaggi e limiti del completamento intelligente (es. correttezza logica, efficienza del codice).

---

## Conclusioni
- L'IA è uno **strumento potentissimo per potenziare il programmatore**, non per sostituirlo.
- Strumenti AI gratuiti e open source aiutano a:
  - Accelerare la scrittura del codice e ridurre la stesura di boilerplate.
  - Migliorare l'apprendimento di nuove sintassi e di pattern di programmazione.
  - Ridurre errori frequenti e facilitare il debugging.
- L'importanza di una **solida comprensione della logica e dei principi di programmazione** è fondamentale per usare l'IA in modo critico e corretto.

---

## Compito per casa
- Installare VS Code e Codeium sul PC personale, se non già fatto in classe.
- Scrivere tre nuove funzioni in Python:
  1. Calcolo del massimo di una lista di numeri.
  2. Verifica se un numero è primo.
  3. Conversione gradi Celsius-Fahrenheit.
- Per ogni funzione, annotare i suggerimenti dell'IA che sono stati utili, quali sono stati errati o non ottimali e spiegare perché.

---

## Note per l'Insegnante

**Modifiche e integrazioni apportate alla lezione:**

* **Arricchimento dei contenuti teorici:**
    * La sezione "Breve storia dell'IA" è stata arricchita con maggiori dettagli sui tre periodi evolutivi, per fornire un contesto più completo.
    * La sezione "Panoramica" è stata estesa per spiegare in modo più chiaro e concreto la differenza tra l'autocomplete tradizionale (statico) e quello basato sull'IA (contestuale e predittivo), un concetto chiave per l'intera lezione.

---

* **Miglioramento delle attività pratiche:**
    * Nel "Primo test", è stato aggiunto un suggerimento di attività: far inserire agli studenti un piccolo errore volontario nel codice. Questo introduce in modo soft e pratico l'idea che l'IA non solo suggerisce, ma può anche assistere nella correzione di problemi, preparandoli alla Lezione 4 sul debugging.
* **Struttura generale:** La struttura è stata mantenuta fedele all'originale per preservare la chiarezza e il flusso della lezione. L'integrazione dei nuovi contenuti è stata pensata per non eccedere il limite delle due ore, fornendo esempi e spiegazioni che possono essere gestiti in modo interattivo con la classe. Il focus è stato messo su un'introduzione solida che getta le basi per le lezioni future, evitando sovrapposizioni e mantenendo una progressione logica.