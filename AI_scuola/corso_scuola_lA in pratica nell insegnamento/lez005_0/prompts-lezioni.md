---
marp: true
paginate: true
# headingDivider: 2 
# theme: gaia
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
  h1 {
    text-align: center;
    color: blue; 
    margin-bottom: 2em; 
  },
  h2 {
    text-align: center;
    color: blue; 
   margin-bottom: 1em; 
  }

---
# Idee
---
Sei un ins...
Genera [] idee per una lezione su [], ... deve durare ...
...

... elenca possibili collegamenti interdisciplinari fra informatica e matematica nel quinto anno dell'ITIS Italiano ...

---

### Attività pratica
Scegliete un argomento della vostra materia di insegnamento

Create ed esesguite prompt per ottenere idee di lezioni su quell’argomento 

Valutate le idee generate,  selezionate la migliore (eventualmente chiedete all'LLM punti di forza e debolezza di ogni idea, per le specificità della vostra classe)

Create tramite AI uno di lezione basato sull’idea selezionata

Provate a generare la totalit' della lezione chiedendo all'AI di scrivere tutti i contenuti (al momento laborioso e non perfetto)

Condividete il vostro feedback

---


# Pianificazione Lezioni

---

# Test & Esercizi

---

Generare sempre spiegazione delle risposte, giuste e sbagliate

Chiedere di avere risposte corrette e spiegazioni in una sezione separata in coda

--- 


# Prompt per Creazione di Test Scolastici  
## Informazioni Essenziali da Includere (1/2)

- **Classe e livello**: Es. Seconda superiore, biennio tecnico
- **Obiettivi di apprendimento**: cosa si vuole verificare?
- **Tipologia di domande**:
(aperte, chiuse con N opzioni ...)
- **Numero di domande** (totale o per sezione)
- num domande **per livello di difficoltà**: 5 base / 3 intermedio /  3 avanzato

---
- **Stile linguistico**: tecnico, semplificato, per studenti BES/DSA
- **Chi correggerà il test**: docente o piattaforma automatica

- **Formato output**: plain text, Markdown, Marp, Word, PDF
- **Lingua di output**: Italiano, Inglese, ecc.

---

# Esempio 
```markdown
> "Crea un test per una classe terza dell’Istituto Tecnico Informatica sull’argomento **reti LAN e protocolli IP**.  
Il test deve includere:
> - 6 domande a scelta multipla,  
> - 2 domande vero/falso,  
> - 2 domande aperte.  
> Il livello è intermedio, con un linguaggio tecnico adatto a studenti.  
> L’output deve essere in formato Markdown."

