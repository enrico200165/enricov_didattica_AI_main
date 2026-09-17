---
marp: true
title: TBD
paginate: true
# headingDivider: 2 
# theme: gaia

header: 'DRAFT - Prompt Engineering Basics - enrico.vialigmail.com'
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
    text-align: center;
    color: blue; 
    left:5%;
  },

  h1 {
    margin-bottom: 2em; 
  },
  h2 {
    position: absolute;
    top: 10%;
    left: 8%;
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

# Personalizzazione di ChatGPT

---

## Personalizzare  ChatGPT
Personalizzare ChatGPT permette, *per alcuni aspetti*, di *adattare l’intelligenza artificiale al proprio contesto professionale* una sola volta (anzichè in ogni prompt), migliorando l’efficacia e la pertinenza delle risposte.

---

##  Probabili benefici della personalizzazione di ChatGPT

* **Maggiore rilevanza nelle risposte**: se ChatGPT “sa” che insegni in una scuola superiore, eviterà spiegazioni troppo semplicistiche o troppo accademiche.
* **Adattamento al tuo stile didattico**: puoi fargli sapere come preferisci strutturare le spiegazioni (es. con esempi, mappe concettuali, tabelle, ecc.).
* **Risparmio di tempo**: ChatGPT può generare materiali (esercizi, verifiche, piani di lezione) già nel formato che usi abitualmente.
* **Memoria (con ChatGPT Plus)**: può ricordare le tue preferenze nel tempo, evitando di doverle ripetere ogni volta.

---
## Possibili svantaggi

* **Rischio di risposte troppo “adattate”**: se dai istruzioni molto strette, ChatGPT potrebbe escludere soluzioni alternative utili.
* **Sovraspecializzazione**: se lo personalizzi troppo per un ambito (es. solo letteratura italiana), potrebbe trascurare altri aspetti (es. educazione civica).
* **Vincolo alla memoria** (solo per utenti Plus): se usi la funzione di memoria e non aggiorni le informazioni, potrebbero diventare obsolete.

---
##  Dove si trovano le funzioni di personalizzazione nella GUI

### Su ChatGPT ([https://chat.openai.com/](https://chat.openai.com/))

* Vai in alto a destra sull’**icona del tuo profilo/account**.
* Seleziona **“Impostazioni” (Settings)**.
* Troverai due sezioni rilevanti:

  * **“Personalizzazione” (Custom Instructions)**: disponibile per tutti gli utenti.
  * **“Memoria” (Memory)**: disponibile per gli utenti **ChatGPT Plus** (con GPT-4). Può essere attivata/disattivata.

---

##  Esempi di personalizzazione (Custom Instructions)  

### **Punto 1: "Cosa vorresti che ChatGPT sapesse di te per fornire risposte migliori?"**

> Sono un insegnante di ruolo nella scuola secondaria superiore in Italia. 
Insegno lettere italiane e storia in un istituto tecnico. 
Ho studenti dai 14 ai 19 anni con diversi livelli di competenze, compresi BES e DSA. 
Uso spesso strumenti digitali (LIM, Google Workspace, Moodle), e cerco di rendere le lezioni accessibili e coinvolgenti. 
Apprezzo risposte sintetiche ma ricche di contenuti, e se possibile con esempi reali, riferimenti o citazioni.

---

 > Mi interessa l’uso dell’intelligenza artificiale per la didattica inclusiva e per il recupero. Prediligo contenuti in italiano corretto ma non eccessivamente formale.

---

### **Punto 2: "Come vorresti che ChatGPT rispondesse?"**

> Vorrei risposte chiare, ben organizzate, con eventuali punti elenco. Quando spiego un concetto, preferisco un linguaggio accessibile agli studenti della scuola superiore, ma non semplicistico. Apprezzo l’uso di esempi scolastici, esercitazioni pratiche, schede riassuntive, modelli di verifiche o rubriche di valutazione. Se mi chiedi un argomento complesso, dividilo in sezioni. Se possibile, suggeriscimi anche strumenti digitali o strategie didattiche. Mantieni un tono professionale ma non troppo accademico, come se fossi un collega.

---

## Altri esempi alternativi (a seconda del tuo profilo docente)

### Matematica e fisica

> Insegno matematica e fisica in un liceo scientifico. Cerco risorse e spiegazioni che possano essere usate anche per il recupero o per studenti con difficoltà. Gradisco formule ben formattate, spiegazioni passo passo e problemi svolti.

### Informatica in un ITI

> Sono docente di informatica in un istituto tecnico. Mi occupo di coding (Java, PHP, SQL), reti e sistemi. Vorrei risposte tecniche ma adatte a studenti di 17-18 anni. Usa esempi pratici e, se possibile, codice commentato.

---  
## Controllare ... con ChatGPT stessa  

> le mie informazioni di personalizzazione sono tutte chiare o hai qualche domanda?  

Attualmente le informazioni che ho sono chiare e ben strutturate. 

---  

Tuttavia, se desideri che io adatti ancora meglio le risposte, potresti specificare (se lo ritieni utile):  

- Se ci sono vincoli di tempo o strumenti che preferisci usare nei tuoi progetti scolastici (es. **solo software open source, limiti di laboratorio**, ecc.).  
- Se desideri uniformità nel tono (più formale per materiali didattici, più diretto per debug, ecc.).
Se ci sono **ambiti disciplinari da integrare** con l’informatica (es. filosofia, diritto, educazione civica…).  

Ma a oggi non ho domande pendenti: il tuo profilo è già molto ben definito. Se vuoi aggiornare o chiarire qualcosa, puoi farlo in qualsiasi momento.

---
# Fine
