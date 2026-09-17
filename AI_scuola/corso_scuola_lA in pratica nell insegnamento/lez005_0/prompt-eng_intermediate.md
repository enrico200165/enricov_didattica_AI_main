---
marp: true
title: DRAFT - Prompt Engineering INTERMEDIATE - enrico.viali@gmail.com
paginate: true
# headingDivider: 2 
# theme: gaia

header: 'DRAFT - Prompt Engineering INTERMEDIATE - enrico.viali@gmail.com'
footer: "ITIS Galileo Galilei Roma" 


backgroundImage: url("../imgs/powerpoint_enrico_galilei.png")
backgroundSize: cover


style: |
  section {
    max-width: 100%;
    margin: auto;
    padding: 2em;
    box-sizing: border-box;
    /* font-family: 'Arial, sans-serif'; 
    color: red;
    */
  },

  section > * {
    max-width: 85%;
  },

  .centered_title {
    text-align: center;
    font-size: 3em;
    font-family: Calibri;
    color: blue;
    margin-bottom: 1em;   
  }, 

  header, footer {
    font-style: italic;
    position: absolute;
    left: 5%;
    width: 100%;
    text-align: center;
    font-size: 1em;
    z-index: 10;
    color: grey;
  }

  header {
    top: 2%;
  }

  footer {
    text-align:left;
    bottom: 10px;
  }


  h1, h2 {
    position: absolute;
    text-align: center;
    color: blue; 
    left:4%;
  },

  h1 {
    top: 7%;
    margin-bottom: 2em; 
  },
  h2 {
    top: 12%;
    margin-bottom: 1em; 
  },

  h3 {
    #text-align: center;
    color: blue; 
    margin-bottom: 1em; 
  },

  .shout {
    text-align: center;
    font-size: 3em;
    color: red;
    margin-bottom: 1em;   
  }

  .hcenter {
    text-align: center;
  }
---  

<div class = "centered_title">
Prompt Engineering<br/>Intermediate<div>

---  
# Tools no-code

Esistono alcuni strumenti per aiutare utenti **non programmatori** a:

* **creare prompt ben ingegnerizzati** (prompt engineering semplificato)
* **ridurre attività di data entry** o automatizzare l’interazione con l'AI.

Soprattutto per quanto riguarda i tools gratuiti il panorama è molto mutevole e, soprattutto, tools gratuiti possono improvvisamente diventare a pagamento o tools propagandati come gratuiti sono gratuiti solo per alcune funzionalità molto limitate

Di seguito una lista **puramente esemplificativa** di alcuni strumenti,  
i tools presenti non sono i migliori nella loro categoria

---

## Generatori di Prompt per Non Programmatori

### **PromptPerfect**

* **Cos’è**: Un'interfaccia guidata che ottimizza automaticamente i prompt forniti per ChatGPT, Claude, Bard e altri modelli.
* **Cosa fa**: Aiuta a trasformare prompt vaghi in richieste dettagliate e mirate. Permette di scegliere il modello AI e la tipologia di risposta desiderata.
* **Indicato per**: docenti, scrittori, professionisti che non sanno come formulare prompt efficaci.
* 🔗 [https://promptperfect.jina.ai](https://promptperfect.jina.ai)

---

### **Text Blaze (versione gratuita)**

* **Cos’è**: Un tool di automazione del testo che consente di creare template riempibili (snippet) direttamente da browser.
* **Cosa fa**: Automatizza il data entry nei moduli o nei prompt. Inserisce rapidamente testo ripetitivo o semi-personalizzato.
* **Indicato per**: chi lavora con moduli online, email, o sistemi IA con input ripetitivi.
* 🔗 [https://blaze.today](https://blaze.today)

---

### **PromptHero Playground**

* **Cos’è**: Un’interfaccia online per creare e testare prompt con modelli IA.
* **Cosa fa**: Permette di scegliere modelli (GPT-4, Claude, ecc.), scrivere prompt e vedere anteprime dei risultati. Ha una libreria di prompt già pronti.
* **Indicato per**: chi vuole esplorare esempi e creare prompt partendo da modelli esistenti.
* 🔗 [https://prompthero.com/playground](https://prompthero.com/playground)

---

### **FlowGPT**

* **Cos’è**: Un sito di prompt condivisi con una community attiva.
* **Cosa fa**: L’utente può cercare, usare, modificare e testare prompt già pronti per centinaia di casi d’uso (didattica, marketing, organizzazione).
* **Indicato per**: utenti senza competenze tecniche che vogliono partire da prompt testati da altri.
* 🔗 [https://flowgpt.com](https://flowgpt.com)

---

### **ChatGPT Custom GPTs (senza codice)**

* **Cos’è**: Costruttori di GPT personalizzati (GPTs) direttamente da interfaccia web.
* **Cosa fa**: Permette agli utenti di costruire assistenti IA con regole, dati, comportamenti personalizzati — senza scrivere codice.
* **Indicato per**: docenti, amministrativi, PMI che vogliono automatizzare task ripetitivi.
* **Serve abbonamento ChatGPT Plus**, ma la creazione è **no-code**.
* 🔗 [https://chat.openai.com/gpts](https://chat.openai.com/gpts)

---

## 📊 Strumenti per Ridurre il Data Entry

### **FormX.ai (versione gratuita con limiti)**

* **Cos’è**: Strumento AI per l’estrazione automatica di dati da documenti (PDF, immagini, moduli).
* **Cosa fa**: Riduce il data entry estraendo automaticamente nomi, numeri, codici da moduli cartacei.
* **Indicato per**: uffici scolastici, PA, archivi.
* 🔗 [https://formx.ai](https://formx.ai)

---

### **Tally Forms + ChatGPT (integrazione gratuita)**

* **Cos’è**: Tally è un generatore di moduli online; può collegarsi a ChatGPT per compilazione automatica o generazione di report.
* **Cosa fa**: Gli utenti inseriscono dati tramite moduli Tally e ChatGPT può elaborarli, riassumerli, analizzarli.
* **Indicato per**: raccolta dati da studenti o utenti e analisi automatizzata.
* 🔗 [https://tally.so](https://tally.so)

---

## ✅ Conclusione

Questi strumenti aiutano:

* a **scrivere prompt migliori** (anche partendo da frasi semplici),
* ad **automatizzare inserimenti di dati o testi ripetitivi**,
* a **generare contenuti personalizzati o report**, senza saper programmare.
<br/>
### Con tutti i tools attenzione al rischio di **vendor lock-in**

---
# Attività Pratica  

## Esempio Integrazione manuale Google Sheets con ChatGPT  
- Versione base
https://docs.google.com/spreadsheets/d/1wqS6Zr-gGUCxGVytvKVOSNZzWZZppy71WLQ0y_xdIyQ/edit?usp=sharing  
<br/>
- Estesa 
https://docs.google.com/spreadsheets/d/1YirLln34LamELrWLXis1ocBO8pL-rVKryW5wI4eHW1I/edit?usp=sharing  

