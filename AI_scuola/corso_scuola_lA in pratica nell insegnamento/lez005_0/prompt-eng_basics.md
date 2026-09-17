---
marp: true
title: TBD
paginate: true
# headingDivider: 2 
# theme: gaia

header: 'DRAFT - Prompt Engineering Basics - enrico.viali@gmail.com'
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

# Prompt Engineering<br/><br/>Concetti Base  

---  

## Obiettivi della Lezione
- Comprendere cos’è il Prompt Engineering
- Scrivere prompt efficaci
- Prima applicazioni IA alla la didattica: **tinkering e conoscenze** in parallelo
- Promuovere inclusione e personalizzazione


---

## Il Prompting come Competenza Didattica

### Definizione

Il prompting è la capacità di interagire efficacemente con modelli linguistici attraverso la formulazione di istruzioni, domande o testi descrittivi, con l’obiettivo di ottenere risposte pertinenti, coerenti e utili.

---

## Classificazione e Applicazioni

### **Tipo di competenza**  
- Digitale  
- Linguistica  
- Metacognitiva  
- Empirica  
- Strategica  

--- 

### **Modalità di apprendimento**  
- Sperimentazione iterativa (trial and error)  
- Applicazione di pattern strategici (es. RROCC, Chain of Thought)  
- Valutazione riflessiva degli output  


### **Ambiti didattici**  
- Italiano: riscrittura di testi, supporto a studenti con BES  
- STEM: decomposizione di problemi e sviluppo algoritmico  
- Filosofia e storia: simulazione di dialoghi o fonti  
- Inclusione: adattamento automatico dei contenuti  

--- 

### **Collegamenti con framework educativi**  
- DigCompEdu: competenze 2.1 e 2.3  
- Competenze chiave UE: alfabetizzazione digitale, imparare a imparare  
- Tassonomia di Bloom digitale: applicare, analizzare, valutare


---

# Spiegazione informale

--- 

## Prompt Engineering - Definizione  

Il prompt engineering è il modo di formulare richieste (prompt) ad un LLM.  
in modo tale da ottenere risposte:
- corrispondenti ai nostri requisiti  
- di buona qualità


E' una competenza con una forte componente empirica, 
si raffina con esperienza e osservazione

---

## PROMPTING - CARATTERISTICHE

il **prompting** può essere considerato, almeno in parte, uno **skill empirico**, soprattutto nel suo uso attuale con modelli linguistici come ChatGPT, Claude o altri LLM.

* **Non esistono regole fisse o un’unica soluzione giusta**: spesso si procede per prove, modifiche, iterazioni.
* **L’apprendimento avviene sperimentando**: chi scrive prompt efficaci sviluppa competenza *provando*, *osservando le risposte* e *adattando il testo*.

---

* **Il contesto conta**: un prompt efficace in una situazione può non esserlo in un'altra, quindi si richiede flessibilità e adattamento.
* **L'abilità migliora con la pratica**: come nel tinkering, anche nel prompting il miglioramento avviene facendo esperienza, osservando feedback, riflettendo sugli errori.

---

### E' anche uno skill cognitivo e linguistico

Non è **solo empirico**, perché:

* Richiede **capacità di astrazione e riformulazione linguistica**
* Si basa sulla **comprensione del comportamento del modello**
* Richiede **pensiero strategico** (es. decomporre problemi, strutturare fasi)
* Può essere potenziato con **teoria** (pattern di prompting, framework come RROCC, ReAct, Chain of Thought, ecc.)

---

### In sintesi

Il prompting è:

* **Empirico** nel metodo di apprendimento (sperimentazione, aggiustamento, osservazione)
* **Cognitivo-linguistico** nelle competenze attivate (scrittura, logica, astrazione)
* **Strategico** quando applicato a compiti complessi, pianificati, multi-step

---

## Principi
Alcuni dei principi generali per creare prompt efficaci sono i seguenti:
- specificità
- sviluppo incrementale (per tasks complessi)
- approccio iterativo

---
## Prompt Priming

Il precedere la richiesa da informazioni utili a precisarla, **di fatto implicito nella maggior parte degli approcci al prompt engineering**.

Il banale inserire nel prompt prima della richiesta le informazioni che stiamo per illustrare è prompt priming

---
## Conversazione vs. Domanda - Risposta

Precisazione ovvia ma ...

Possiamo ma **non** dobbiamo dire tutto 

**in un solo prompt**

ma non c'è

---

<div class = "shout">
nessun obbligo  
</div>
<br />
di operare in tal modo

---

## **Vantaggi di un unico prompt:**

* Tutte le informazioni vengono fornite sin dall'inizio, consentendo una risposta più precisa, coerente e strutturata.
* La risposta può risultare più integrata, evitando ripetizioni o incongruenze tra le diverse parti della richiesta.
* L’interazione può richiedere meno tempo, in quanto una richiesta completa permette spesso di ottenere una risposta soddisfacente già nei primi scambi.
* È possibile ottimizzare la struttura della risposta complessiva, specialmente in casi in cui vengono richiesti più elementi (es. codice, spiegazioni, formattazione, esportazione, ecc.).

---

## **Svantaggi di un unico prompt:**

* Richiede uno sforzo maggiore per formulare una richiesta completa e priva di ambiguità, soprattutto in presenza di esigenze articolate.
* In caso di informazioni mancanti o poco chiare, la risposta può basarsi su ipotesi non corrispondenti all’intento dell’utente.
* La risposta generata potrebbe essere più estesa e meno agevole da consultare.

---

## **Vantaggi di suddividere la richiesta in più prompt successivi:**

* Si mantiene un maggiore controllo sul processo, con possibilità di riformulare, integrare o correggere la richiesta in base all’evoluzione della risposta.
* Tale approccio risulta utile in fase esplorativa o progettuale, quando non tutte le specifiche sono già definite.
* Ogni scambio può essere focalizzato su un aspetto specifico, favorendo la chiarezza e l’approfondimento progressivo.

---

## **Svantaggi di richieste suddivise in più prompt:**

* La mancanza di informazioni complete nelle prime fasi può comportare risposte iniziali generiche o parziali.
* Eventuali modifiche successive alla struttura o agli obiettivi possono richiedere di rigenerare parti già trattate.

---

## **Conclusione:**

* In presenza di una richiesta ben definita e completa, è preferibile utilizzare un unico prompt.
* Quando si intende costruire la soluzione in modo incrementale o si stanno ancora definendo i requisiti, è consigliabile procedere con più prompt successivi.

---

## Dialogare con LLM  
ChatGPT ricorda, entro certi limiti, ciò che avete comunicato in precedenza, soprattutto la versione plus
- non sopravvalutare la memoria
- non sottovalutare o ignorare la memoria

NB.  
> Questa memoria vale solo finché la conversazione è aperta.
**Se chiudi o aggiorni la pagina, non ricorderò più i prompt precedenti**, a meno che tu non continui nello stesso thread.

---

## Memoria in ChatGPT  **Free vs Plus**

### Memoria nel piano Free

- Basato su **GPT-3.5**
- **Ricorda solo durante la sessione attiva**
- Se chiudi la chat o aggiorni la pagina: **la memoria si azzera**
- Nessuna personalizzazione tra sessioni

---

### Memoria nel piano Plus

- Basato su **GPT-4-turbo**
- Ricorda durante la sessione **e può memorizzare dati tra sessioni**
- Può ricordare:
  - Nome
  - Ruolo (es. insegnante)
  - Preferenze di stile o struttura
- La memoria è **gestibile**: puoi attivarla o disattivarla

---

## Confronto sintetico

| Funzione                | Free (GPT-3.5) | Plus (GPT-4-turbo)       |
|------------------------|----------------|--------------------------|
| Memoria nella sessione | ✅ Sì           | ✅ Sì                     |
| Memoria tra sessioni   | ❌ No           | ✅ Sì (se attiva)        |
| Personalizzazione      | ❌ No           | ✅ Sì                    |
| Prestazioni AI         | Media           | Alta (velocità + contesto) |

---

## Dove gestire la memoria?

Andare su:  
**Impostazioni → Personalizzazione → Memoria**  

Da lì puoi:
- **Visualizzare cosa è salvato**
- **Cancellare o aggiornare** ciò che viene ricordato
- **Disattivare completamente la memoria**

---

## Conclusione

**La memoria fa la differenza:**
- Utile per continuità nei progetti didattici
- Migliora l’efficienza delle risposte
- **Con il piano Plus**, puoi costruire una collaborazione “consapevole” con l’AI

---

## Componenti del prompt

Tecnicamente il prompt è testo **totalmente libero**

Il prompt engineering osserva che è spesso utile inserire nel testo alcuni tipi di informazione (elementi o componenti).

Le liste di elementi informativi (schemi) e la terminologia non sono tecniche o formali, sono **informali** e **variano** lievemente da fonte a fonte

--- 
## Modelli/schemi di Prompt Engineering  
Alcuni schemi di prompting sono attualmente popolari

- **R.R.O.C.C.**  
  Guida pratica per costruire prompt completi


- **C.R.E.A.T.E.**  
  Approccio creativo e comunicativo, utile per contenuti articolati e strutturati.
---

- **P.R.O.M.P.T.**  
  Schema lineare e chiaro, pensato per prompt tecnici, procedurali o formali.

- **M.O.D.E.L.**  
  Utile in ambito didattico per progettare prompt guidati, con obiettivi precisi e limiti definiti.

---
## Solo modelli?

I modello aiutano a **pensare il prompt come un progetto** e, più banalmente, ci aiutano a ricordare di inserire informazioni utili per una buona risposta.

Gli elementi utili, cioè i tipi di informazione, sono ovviamente indipendenti dai modelli e possiamo esaminarli a prescindere dai modelli

Un utilizzatore avanzato probabilmente troverà conveniente costruire un proprio schema scegliendo gli elementi a lui più utili

---
## Componenti/elementi del prompt
componente/elemento = termine **informale** che indica un tipo di informazione che spesso è utile inserire in un prompt

Nel seguito elenchiamo un numero ampio di componenti:
- **non** sono tutti necessari
- alcuni sono in sovrapposizione
(se specifico un' audience di bambini di 6 anni implicitamente specifico tipo di linguaggio, complessità, tono Etc)

--- 
## **Componenti del prompt**
### (una delle visioni, infinite varianti simili)
- **Obiettivo**
- **Ruolo**: chi è l’IA  (ex. “Sei un insegnante di storia”)
- **Audience** tenici, venditori, scuola primaria, liceo ... livello avanzato, DSA ...

---
- **Tono, Registro, Stile Etc.**: 
*tono*: che atmosfera deve avere? (stile, emozione, ...)
*registro*: lingua semplice, scolastica, tecnica, burocratica ...
*stile*: marketing call for action

- **Output desiderato**: 
  - formato  (docx, json etc.)
  - livello di dettaglio
  - estensione (da 5 a 10 slides ...)
  - lingua (in Italiano)

---
- **Passaggi o struttura**  
richiedere che la risposta sia divisa in sezioni etc.

- **Contesto**:
descrizione della situazione, a volte espresso indirettamente ma chiaramente negli altri punti
- **Istruzioni**: implicite nell'obiettivo per casi non complessi

- **Parole chiave da usare o evitare**
  ex. "evita il termine problema usa sfida"
- **Vincoli specifici**
limiti o condizioni: tempo verbale, lunghezza frasi, no immagini, ecc.

---

## OBIETTIVO – Scheda Pratica

Inserire **subito un verbo d’azione** che dica chiaramente **cosa si vuole ottenere**.

* Scrivi&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ \[tipo di contenuto]
* Riassumi&nbsp;&nbsp;   + \[argomento]
* Suggerisci + \[soluzione]
* Correggi&nbsp;&nbsp;&nbsp;&nbsp;+ \[tipo di errore]
* Spiega&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ \[concetto]
* Crea&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ \[prodotto finale]
--- 
### Esempi
RIASSUNTO
> *"Riassumi in massimo 10 righe la storia della seconda guerra mondiale, in modo comprensibile per un ragazzo di 13 anni."*  

*EFFETTO ATTESO*: Riassunto semplice e breve

GENERAZIONE DI CONTENUTO
> *"Scrivi una favola con una morale finale per bambini dai 6 agli 8 anni, ambientata in un bosco."*  

*EFFETTO ATTESO*: Favola con target chiaro e ambientazione specifica

---

CORREZIONE
> *"Correggi questo testo mantenendo lo stile originale ma eliminando errori grammaticali."*  

*EFFETTO ATTESO*: Testo corretto ma non modificato nel tono

---

## **RUOLO – Scheda Operativa**

Serve a **far assumere all’intelligenza artificiale un punto di vista o una competenza specifica**.
Utile quando si desidera una risposta **esperta, coerente o adatta a un certo contesto professionale o sociale**.

---
### **ESEMPI**

**Esempio 1 – Ruolo: insegnante**
> *"Agisci come un insegnante di matematica di scuola superiore. Spiega il teorema di Pitagora con parole semplici e un esempio pratico."*  

EFFETTO ATTESO: Spiegazione didattica chiara, adatta a studenti.

**Esempio 2 – Ruolo: consulente del lavoro**
> *"Sei un consulente del lavoro. Scrivi una risposta professionale a un dipendente che chiede informazioni sul congedo parentale."*  

EFFETTO ATTESO: Testo preciso, formale, conforme al linguaggio aziendale.

---

**Esempio 3 – Ruolo: tecnico informatico**
> *"Fingi di essere un tecnico informatico. Guida passo passo un utente inesperto a installare un programma su Windows 10."*  
EFFETTO ATTESO: Istruzioni dettagliate ma accessibili, linguaggio chiaro.  

---  

## **RUOLO:   EFFETTO ATTESO**
Inserire un ruolo rende la risposta più **mirata, coerente e utile**.
È particolarmente efficace nei contesti professionali o educativi.

---

### **AUDIENCE - Scheda Operativa**

Indica **a chi è destinata la risposta** per **modulare il linguaggio, il livello di approfondimento, il tono** e la **forma del contenuto**.

usare espressioni come:
* "Scrivi per..."
* "Adatto a..."
* "Pensato per..."
* "Rivolto a..."

---

### **ESEMPI**

**Esempio 1 – Audience: bambini**
> *"Spiega che cos’è un virus informatico a un bambino di 8 anni, usando parole semplici e un esempio divertente."*  

EFFETTO ATTESO: Linguaggio molto semplice, tono giocoso, esempio concreto.

**Esempio 2 – Audience: genitori**
> *"Scrivi un breve articolo per genitori che vogliono aiutare i figli a fare i compiti senza stress."*  
EFFETTO ATTESO: Tono empatico, consigli pratici, linguaggio accessibile.

---

**Esempio 3 – Audience: tecnici esperti**
> *"Descrivi il funzionamento di un database relazionale, destinato a un pubblico di sviluppatori senior."*  

**EFFETTO ATTESO**: Linguaggio tecnico, uso di termini specifici, approfondimento teorico.

--- 

## **AUDIENCE: EFFETTO ATTESO**
aiuta l’intelligenza artificiale a **calibrare il contenuto nel modo più adatto** per una specifica categoria specifica di persone.

---

## **TONO, REGISTRO, STILE - Scheda Operativa**

---

## **TONO – ESEMPI**

1. *"Scrivi un messaggio di ringraziamento con tono formale."*
   **EFFETTO ATTESO:** linguaggio educato, distaccato, con formule convenzionali.

2. *"Riformula questo testo con tono ironico."*
   **EFFETTO ATTESO:** uso di umorismo, doppi sensi, leggerezza espressiva.

3. *"Rispondi con tono rassicurante a una domanda di uno studente preoccupato."*
   **EFFETTO ATTESO:** voce empatica, parole incoraggianti, messaggio positivo.

4. *"Scrivi un invito a un evento con tono entusiasta."*
   **EFFETTO ATTESO:** linguaggio vivace, uso di esclamazioni, coinvolgimento emotivo.

---

## **REGISTRO – ESEMPI**

1. *"Spiega l’argomento con registro informale, come se stessi parlando a un amico."*
   **EFFETTO ATTESO:** parole semplici, tono colloquiale, frasi brevi.

2. *"Riscrivi il testo in registro formale per una comunicazione scolastica ufficiale."*
   **EFFETTO ATTESO:** linguaggio neutro e corretto, struttura curata.

3. *"Descrivi il processo con registro tecnico, per un manuale di istruzioni."*
   **EFFETTO ATTESO:** uso di termini specialistici, precisione, impersonalità.

4. *"Adatta il testo a un registro giornalistico."*
   **EFFETTO ATTESO:** stile informativo, linguaggio accessibile, apertura efficace.

---

## **STILE – ESEMPI**

1. *"Scrivi un testo descrittivo su un paesaggio alpino."*
   **EFFETTO ATTESO:** dettagli sensoriali, aggettivi visivi, ritmo lento.

2. *"Racconta l’esperienza in stile narrativo, come fosse un diario."*
   **EFFETTO ATTESO:** uso della prima persona, struttura cronologica, coinvolgimento personale.

3. *"Esponi i pro e i contro in stile argomentativo."*
   **EFFETTO ATTESO:** ragionamento logico, tesi e antitesi, conclusione motivata.

4. *"Presenta il servizio in stile promozionale."*
   **EFFETTO ATTESO:** linguaggio persuasivo, frasi d’impatto, invito all’azione.

---

### **TONO, REGISTRO, STILE, ... EFFETTO ATTESO**
Specificare tono, registro e stile permette di generare testi più **efficaci**, **coerenti con il contesto** e **allineati all’obiettivo comunicativo e al pubblico di riferimento**.


---
## **OUTPUT - Scheda Operativa**
### **Formato**

Indica **in quale forma tecnica** si desidera ricevere il contenuto. Può riferirsi a un tipo di file, struttura dati o layout testuale.

**Esempi d’uso nel prompt:**

* "Genera il testo in formato `.docx` compatibile con Word."
  **EFFETTO ATTESO:** un documento impaginato, pronto per l’uso in Word.
* "Fornisci l’output in formato `JSON` per essere importato in un'applicazione."
  **EFFETTO ATTESO:** struttura ad albero con chiavi e valori, adatta a uso informatico.

---

### **Livello di dettaglio**

Ex. basilare, intermedio, avanzato, tecnico o divulgativo.

**Esempi d’uso nel prompt:**

* "Spiega il teorema di Pitagora con livello di dettaglio base, adatto a una prima superiore."
  **EFFETTO ATTESO:** spiegazione semplice, con pochi passaggi e un esempio pratico.
* "Analizza il testo poetico con livello avanzato, come in una lezione universitaria."
  **EFFETTO ATTESO:** analisi completa di stile, retorica, contesto storico.

---

### **Estensione**

Indica **quanto deve essere lungo** l’output. 
Può essere espresso in parole, paragrafi, pagine, righe, slide, punti elenco, ecc.

**Esempi d’uso nel prompt:**

* "Genera una presentazione di 5-7 slide sull’intelligenza artificiale."
  **EFFETTO ATTESO:** suddivisione in slide con titoli, contenuti brevi e ordinati.
* "Rispondi in massimo 150 parole."
  **EFFETTO ATTESO:** risposta sintetica ma completa.

---

### **Lingua**

Indica **la lingua in cui desideri la risposta**. Se non specificato, l’IA può rispondere nella lingua del prompt.

**Esempi d’uso nel prompt:**

* "Traduci il testo seguente in italiano, mantenendo uno stile professionale."
  **EFFETTO ATTESO:** traduzione fluida, corretta, con tono coerente.
* "Scrivi il codice commentato in inglese, ma spiega la logica in italiano."
  **EFFETTO ATTESO:** mix controllato tra due lingue per diversi scopi.

---

### OUTPUT: EFFETTO ATTESO

Specificare con precisione **formato, livello di dettaglio, estensione e lingua** permette all’IA di **strutturare l’output secondo i vincoli richiesti**, rendendolo **subito utilizzabile** e adatto allo **scopo finale**.


---
## Tecniche
- **Zero-shot**:
nessun esempio fornito
- **Few-shots**:
alcuni esempi forniti
- **Chain-of-thought**:
sollecita il ragionamento passo-passo

---

### **Zero-shot prompting**  

Si fornisce un’istruzione **senza esempio**.
Utilizzato quando si vuole una risposta diretta a un comando chiaro.

**Esempio**:
*"Scrivi una definizione semplice di intelligenza artificiale."*

**Vantaggi**: rapido, utile per compiti semplici.
**Limiti**: meno preciso in compiti complessi.

---

### **One-shot prompting**

Si fornisce **un solo esempio** per guidare l’output.
Il modello apprende dal contesto e replica lo stile o la struttura.

**Esempio**:  
Q: Cos'è una cellula?
A: È l'unità fondamentale degli organismi viventi.
Q: Cos'è un atomo?"*

**Vantaggi**: migliora la coerenza.
**Limiti**: dipende molto dalla qualità dell’unico esempio.

---

### **Few-shot prompting**

**Descrizione**: si forniscono **più esempi** per illustrare cosa si vuole.
Il modello generalizza meglio lo schema richiesto.

**Esempio**:
*"Q: Cos'è il Sole?
A: Una stella che fornisce luce e calore alla Terra.
Q: Cos'è la Luna?
A: Un satellite naturale che orbita intorno alla Terra.
Q: Cos'è Marte?"*

**Vantaggi**: molto efficace per compiti complessi o creativi.
**Limiti**: richiede spazio e attenzione nella scelta degli esempi.

---

### **Chain-of-thought prompting**

**Descrizione**: si invita il modello a **ragionare passo dopo passo**.
Utile per problemi logici, calcoli o decisioni complesse.

**Esempio**:
*"Quanti giorni ci sono in 3 settimane? Ragiona passo dopo passo."*

**Vantaggi**: migliora l’accuratezza nei compiti con più passaggi.
**Limiti**: può generare risposte più lunghe o ridondanti.

---

## Schemi di prompting 

Probabilmente conosciamo tutti  
**SMART** (**S**pecific, **M**easurable, **A**chievable, **R**elevant, **T**ime-bound) e 
**KISS** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(**Keep** **I**t **S**imple **S**tupid)

Gli schemi di prompting sono l'equivalente nell'ambito del prompting

- non vi è nulla di "formale",  
- non sono definiti a livello "tecnico"  
- non è dimostrabile matematicamente/direttamente che funzionano bene, siamo in ambito probabilistico, non deterministico (chiaramente sono basati su motivazioni tecnico/funzionali valide)


---

## **R.R.O.C.C**
<br/>
Aiuta a scrivere prompt ben strutturati.
Adatto a contesti educativi e professionali.

### **Significato delle lettere**

|  | Elemento           | Spiegazione pratica                                                                                                 |
| ----- | ------------------ | ------------------------------------------------------------------------------------------------------------------- |
| **R** | **Ruolo**          | Chi deve essere l’IA? (es. insegnante, consulente, esperto…)                                                        |
| **R** | **Responsabilità** | Cosa deve fare l’IA? (es. spiegare, riassumere, scrivere…)                                                          |
| **O** | **Obiettivo**      | Qual è il risultato che vuoi ottenere? (es. chiarire un concetto ...)                                |
| **C** | **Contesto**       | Informazioni per comprendere bene la richiesta |
| **C** | **Constraints**    | Quali vincoli (es. lingua, lunghezza, tono, formato del testo)                                        |

---

### **Esempio di prompt con R.R.O.C.C.C**

> **Ruolo:** Agisci come un docente di filosofia.
> **Responsabilità:** Spiega un concetto in modo semplice.
> **Obiettivo:** Aiutare uno studente delle superiori a capire Platone.
> **Contesto:** Lo studente ha 16 anni e conosce già Socrate.
> **Constraints:** Scrivi in italiano, massimo 150 parole, tono chiaro e didattico.

---

**EFFETTO ATTESO**

Utilizzando R.R.O.C.C.C, il prompt diventa **completo, mirato e coerente**.
L’intelligenza artificiale ha tutte le informazioni necessarie per **generare una risposta efficace e pertinente**, adatta al destinatario e allo scopo.

---

## C.R.E.A.T.E.  
Modello per la progettazione di prompt complessi

| Lettera | Elemento    | Funzione                             |
|---------|-------------|--------------------------------------|
| C       | Context     | Contesto generale o situazione       |
| R       | Role        | Ruolo da assumere                    |
| E       | Example     | Eventuale esempio da seguire         |
| A       | Audience    | Destinatario della risposta          |
| T       | Task        | Compito da svolgere                  |
| E       | Expectation | Forma o obiettivo dell’output        |

---

## C.R.E.A.T.E.  - Usi e applicazioni

**Utile per:**
- Scrittura creativa
- Prompt didattici articolati
- Generazione di contenuti complessi

---

## P.R.O.M.P.T.  
Struttura lineare per prompt efficaci

| Lettera | Elemento       | Funzione                                        |
|---------|----------------|-------------------------------------------------|
| P       | Persona/Role   | Chi è il modello? (es. esperto, guida)         |
| R       | Request        | Cosa deve fare                                 |
| O       | Objective      | Qual è lo scopo finale                         |
| M       | Mode           | Forma dell’output (testo, lista, codice…)      |
| P       | Parameters     | Limiti o vincoli (lunghezza, lingua, tono…)    |
| T       | Tone           | Registro emotivo e comunicativo                |

---

## P.R.O.M.P.T. - Usi e applicazioni

**Utile per:**
- Prompt tecnici
- Compiti procedurali
- Richieste formali e strutturate

---

## M.O.D.E.L.  
Schema per prompt educativi e comunicativi

| Lettera | Elemento   | Funzione                                 |
|---------|------------|------------------------------------------|
| M       | Mission    | Scopo generale del prompt                |
| O       | Output     | Forma o tipo di risposta attesa          |
| D       | Details    | Informazioni specifiche o contesto       |
| E       | Examples   | Esempi da seguire o da evitare           |
| L       | Limits     | Vincoli di contenuto o stile             |

---

## M.O.D.E.L.  - Usi e applicazioni

**Utile per:**
- Progettazione didattica
- Costruzione di attività guidate
- Rubriche di valutazione automatica

---

# Parte Pratica  

---
## Attività: Creare Prompt Didattici

- **Esercizio 1**:
Generare quiz a risposta multipla su un argomento specifico
- **Esercizio 2**:
Riassumere testi complessi per studenti DSA
- **Esercizio 3**:
Generare piani di lezione su misura

---
## Altre applicazioini dei prompt
(non esaminate in questa sezione)

### Altri utilizzi
- **Valutazione automatica**:
correggere compiti e fornire feedback
- **Materiali inclusivi**:
generare testi semplificati
- **Pianificazione**:
creare schede di lezione dettagliate

---
# Risorse
--- 
## Prompting guides generali
- Prompting Guide (ITA)
 [https://www.promptingguide.ai/it](https://www.promptingguide.ai/it)
- Wikipedia [https://it.wikipedia.org/wiki/Prompt_engineering](https://it.wikipedia.org/wiki/Prompt_engineering)
- YouTube – 50 prompt per la scuola 
[https://www.youtube.com/watch?v=ayx6vlTEgPc](https://www.youtube.com/watch?v=ayx6vlTEgPc)

 - infinite altre ...
---



### Risorse Specifiche per Docenti
- Agenda Digitale – IA nella didattica
[https://www.agendadigitale.eu/scuola-digitale/ia-nella-didattica-strumenti-e-metodologie-per-studenti-e-docenti/](https://www.agendadigitale.eu/scuola-digitale/ia-nella-didattica-strumenti-e-metodologie-per-studenti-e-docenti/)
- Didacta 2024 – Workshop Prompt Engineering
[(https://fieradidacta.indire.it/eventi_2024/prompt-engineering-e-didattica/](https://fieradidacta.indire.it/eventi_2024/prompt-engineering-e-didattica/)
- CSC Group – Formazione Prompt Engineering
[(https://www.csc-group.it/proposta_scolastica/prompt-engineering/](https://www.csc-group.it/proposta_scolastica/prompt-engineering/)
- Coursebox AI 
[https://www.coursebox.ai/it/blog/prompt-engineering-for-educators](https://www.coursebox.ai/it/blog/prompt-engineering-for-educators)
---
- bSmart
[https://blog.bsmart.it/2025/02/05/ChatGPT-per-docenti-guida-pratica-intelligenza-artificiale/](https://blog.bsmart.it/2025/02/05/ChatGPT-per-docenti-guida-pratica-intelligenza-artificiale/)

---

# E' consigliabile citare il corso classico di Coursera/OpenAI di Andrew NG

---

## Punti chiave  
- Avere un proprio **approccio e/o un processo** anzichè limitarsi a riusare qualcuna delle molteplici “collezioni di super-prompt” disponibili online (comunque utili, se di qualità)
- Usare prompt engineering e, probabilmente, un processo iterativo per compiti non banali
- Esplorare, sperimentare, imparare a “conoscere” le specificità di una versione di un’IA.
- A volte può essere laborioso interagire con un’IA anche per gestire
aspetti semplici dal punto di vista “umano”, l'IA non è ... umana

---
## Conclusione
- Prompting come competenza digitale essenziale  
    - ROI positivo (semplice, si impara in poco tempo, "paga")
- Potenziale per un apprendimento più personalizzato
- Invito a sperimentare e adattare i prompt nella propria disciplina