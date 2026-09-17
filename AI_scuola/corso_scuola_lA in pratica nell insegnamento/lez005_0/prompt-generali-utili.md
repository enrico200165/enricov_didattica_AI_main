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

# Prompt: Esempi Generali

---
# Estrazione Informazioni

--- 
 ## Lista Studenti

Prompt:
aprire una pagina del registro elettronico  
selezionare tutto il testo della pagina (ctrl + a)  

prompt:
> dal testo seguente estrai la lista degli studenti
>
>  ... testo incollato dalla pagina registro ...
    

---

## Lista Email Studenti

aprire una pagina del registro elettronico  
selezionare tutto il testo della pagina (ctrl + a)  

Prompt:
> Il testo seguente contiene dei nomi di studenti. Genera una lista dei loro indirizzi di email tenendo conto del fatto che l'email di uno studente che si chiama Mario  Rossi è  rossi.mario.2022@itisgalileiroma.it

--- 

## Voti studenti  

Copiare e incollare dalla pagina dei vodi del RE

Prompt:
>  il testo seguente contiene i nomi degli studenti e i loro voti, crea una tabella ed evidenzia gli studenti con in voti più bassi
>
>
> ... testo incollato ...

---

## Studenti iperattivi

prompt:
> devo fare una supplenza in una classe, in coda inserisco testo con la lista degli studenti e delle annotazioni, dimmi quali sono gli studenti da controllare con attenzione
> 
> ... testo incollato dalla pagina delle annotazioni disciplinari ...
