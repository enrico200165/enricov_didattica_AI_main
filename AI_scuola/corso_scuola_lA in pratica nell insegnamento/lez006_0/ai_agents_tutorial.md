---
marp: true
title: TBD
paginate: true
# headingDivider: 2 
# theme: gaia

header: 'AI agents, Concetti Base - enrico.viali@gmail.com'
footer: "ITIS Galileo Galilei Roma" 


backgroundImage: url("../../imgs_common/powerpoint_enrico_galilei.png")
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

## Introduzione agli AI Agents - Un tutorial non tecnico

- Cosa sono gli AI agents
- come funzionano  
- in che modo si distinguono da GPT e chatbot.

---  

![AI Agent - Generated Illustration](./lez006_0/imgs/ai_agent_00.png)

---

# Cos'è un AI Agent?
## L'idea base

Un **AI Agent** è un sistema di **Intelligenza Artificiale operativo**.

- L’AI è la mente.
- L’agente AI è chi **agisce**.

- **AI:** sa cosa fare  
- **AI Agent:** fa davvero qualcosa

---

# Il concetto chiave
## Una metafora semplice

L'AI è un **genio brillante** con mille idee.  
Un **AI Agent** è chi **prende una di quelle idee e la realizza**.

Intelligenza ≠ Azione  
Azione = AI Agent

---

# Le 3 funzioni fondamentali di un AI Agent

1. **Capisce**: interpreta richieste e bisogni  
2. **Pensa**: elabora una strategia di risposta  
3. **Agisce**: esegue azioni o restituisce risultati

---

# Esempio: come un babysitter

- Genitori = Sviluppatori  
-  Istruzioni = Dataset / Prompt / Codice  
- Babysitter = AI Agent

Il babysitter non fa tutto da solo, ma **segue regole dettagliate**   
→ così fanno gli AI agents.

---

## Componenti principali di un Agent

### 1. **Interfaccia**
- Chat
- Pulsante
- Assistente vocale

### 2. **Workflow**
- Diagramma di flusso che guida l’agente

---

# Cos'è un Workflow?

Il **workflow** (flusso di lavoro) è la **sequenza di operazioni** che un AI agent esegue per portare a termine un compito.

Più cherispondere a una domanda, ma di **seguire dei passaggi o tasks**, come:

- Ricevere un input
- Analizzarlo
- Consultare una fonte (API, database, documento)
- Prendere decisioni
- Eseguire un'azione concreta

---

Un esempio semplificato di workflow per un agente AI che prenota una riunione:

1. L'utente chiede: "Prenota una riunione con Marco"
2. L'agente controlla l'agenda dell’utente
3. Verifica la disponibilità di Marco
4. Propone un orario
5. Prenota la sala e invia l’invito

Ogni passaggio è un **nodo** del workflow, con regole precise su cosa fare e quando passare al passo successivo.

---

# Il ciclo di lavoro dell’AI Agent

1. **Input**: Riceve una richiesta
2. **Processing**: Pensa come rispondere
3. **Action**: Risponde o agisce
4. **Learning**: __migliora nel tempo con l’uso__

---

# Diagramma: il flusso operativo

![AI Agent Flowchart https://upload.wikimedia.org/wikipedia/commons/4/4c/Agent_Function.svg](https://upload.wikimedia.org/wikipedia/commons/4/4c/Agent_Function.svg)


_(Fonte: Wikipedia - Agent Function)_

---

# Custom GPTs vs AI Agents

| Aspetto | GPT | AI Agent |
|--------|-----|----------|
| Obiettivo | Rispondere a richieste (chat) | Completare compiti (autonomia) |
| Memoria | Breve, conversazionale | Può mantenere contesto e stato |
| Strumenti | Solo linguaggio | Può usare API, database, email |
| Esempio | Scrivere un saggio | Leggere email, sintetizzare, inviare risposte |

---

# AI Agent ≠ Chatbot

| Chatbot tradizionale | AI Agent |
|----------------------|----------|
| Script fisso | Adattivo e dinamico |
| Limitato a FAQ o risposte statiche | Può completare azioni complesse |
| Non apprende | Può apprendere |
| Solo conversazione | Può eseguire flussi e automazioni |

---

# Perché è importante per la scuola?

- Automazione di compiti ripetitivi  
- Supporto a studenti (es. BES, DSA)  
- Assistenti per docenti (materiali, email, correzioni)  
- Nuove competenze digitali da insegnare

Un’opportunità per innovare la didattica e alleggerire il carico

---

# Campi in cui sono già utilizzati gli AI Agents

- Customer service
- Project management
- Vendite
- Educazione personalizzata
- Automazione documentale
- Pianificazione didattica

---

# Un possibile scenario futuro

> “Ci saranno più AI agents che esseri umani.”  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[anonimo]

ipotesi:
- Assistenti personali per ogni persona
- Agenti scolastici per ogni classe
- Automatismi per ogni procedura

---

# Riepilogo finale

- Gli **AI agents** uniscono intelligenza e azione
- Non sono GPTs, ma **possono usarli**
- Sono più evoluti dei chatbot
- Possono **imparare**, **agire** e **collaborare**

---

# Risorse

Lingua Inglese:
- [OpenAI Custom GPTs](https://platform.openai.com/docs/guides/gpts)
- [AutoGPT](https://github.com/Torantulino/Auto-GPT)
- [LangChain](https://www.langchain.com)
- [AI Agents Explained (video)](https://www.youtube.com/watch?v=kqbZ5vBNZK8)

---

# Attività pratiche
- Visione del video tutorial (Italiano) https://youtu.be/PoHiFOml85A 
**semplice visione** per awareness, non è necessario implementare, non è necessario cogliere tutti i dettagli, l'obiettivo è avere un'idea generale del processo di creazione di un semplice agente