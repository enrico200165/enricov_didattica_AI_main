
# Tutorial: Come Creare un Custom GPT (Livello Principiante-Intermedio)

## ✅ Requisiti iniziali

- Solo gli **utenti ChatGPT Plus** possono creare e condividere GPT personalizzati.
- Tuttavia, anche gli **utenti non paganti** possono **utilizzare** i GPT personalizzati creati da altri.

## ✅ Cos'è un Custom GPT

OpenAI consente di costruire una versione personalizzata di ChatGPT con:
- istruzioni su misura
- conoscenze specifiche (file allegati)
- comportamenti configurabili

Con un Custom GPT è possibile:
- definire un problema specifico
- creare un assistente che lo risolva in modo mirato

Esempio: far scrivere email con un tono e formato coerenti con i propri standard. 
In tal caso si possono caricare esempi di email in un file .txt nella sezione "Conoscenze".

---

## ✅ Come creare un Custom GPT

1. Accedere a: [https://chatgpt.com/gpts](https://chatgpt.com/gpts)
2. Cliccare su **Create** per accedere all'editor, composto da tre tab:
   - **Create**
   - **Configure**
   - **Preview**

### Tab "Create"
Sconsigliato: è una chat guidata che imposta automaticamente il GPT, ma i prompt generati sono spesso imprecisi o distrattivi.

### Tab "Configure"
Qui si definisce tutto:
- Nome del GPT
- Descrizione
- Prompt principale (nelle istruzioni)
- Conversazioni iniziali (bottoni con esempi di utilizzo)
- Sezione **Knowledge** (caricamento di massimo 20 file da 512MB ciascuno)
- 4 funzionalità attivabili:
  - Web search
  - Canvas
  - Generazione immagini
  - Code interpreter (**obbligatorio se si usano file**)

**Azioni personalizzate (Actions):** permettono di fare chiamate API per ottenere dati in tempo reale o compiti complessi.

### Tab "Preview"
Ambiente di prova live per testare e migliorare:
- Risposte
- Uso corretto dei file
- Comportamento coerente

Una volta soddisfatti, cliccare su **Create** per pubblicare. Opzioni:
- GPT pubblico
- GPT privato
- GPT accessibile solo via link

---

## ✅ Nome del GPT

- Deve essere **chiaro, descrittivo e conciso**
- Evitare nomi generici, volgari o riferiti a persone pubbliche
- Evitare marchi altrui senza autorizzazione
- Il suffisso "GPT" non è vietato ma è sconsigliato

Esempi:
- GPT per servizio "Tracy" → "Tracy" oppure "Tracy Support"
- Servizi terzi si possono citare **nella descrizione**, **non nel nome**

---

## ✅ Prompt Custom GPT: differenze

- Prompt normale = comando singolo
- Prompt GPT = controller dell'intera esperienza

Il prompt di un GPT deve contenere:
- identità
- obiettivo
- metodo per raggiungerlo
- contesto per usare i file di conoscenza

### 📌 Metodo INFUSE
Sistema mnemonico per scrivere prompt efficaci:

- **I – Identity & Goal:** chi è il GPT e cosa deve fare
- **N – Navigation Rules:** come interagire, quando usare i file
- **F – Flow & Personality:** tono, linguaggio, tratti distintivi
- **U – User Guidance:** guida passo-passo per aiutare l'utente
- **S – Signals & Adaptation:** adattamento a segnali utente (es. emozioni, richieste vaghe)
- **E – End Instructions:** istruzioni da ricordare sempre

---

## ✅ File di conoscenza

Servono per:
- dare contesto aggiuntivo
- migliorare accuratezza e specializzazione delle risposte

Best practice:
- Non caricare info grezze
- Inserire esempi, tecniche, casi d’uso
- Esempi:
  - GPT email → caricare email esistenti ben formattate
  - GPT coaching → caricare trascrizioni reali
  - GPT problema tecnico → aggiungere studi di caso e soluzioni passo passo

⚠️ Il prompt principale deve spiegare **quando e perché** usare i file

---

## ✅ Test e iterazioni

- Nessun GPT funziona bene al primo tentativo
- Usare il tab **Preview** per:
  - simulare conversazioni reali
  - verificare il comportamento
  - controllare il tono
  - correggere difetti nel prompt o nei file

Miglioramenti continui → GPT più fluido e utile

---

## ✅ Tecnica avanzata: Signals & Responses

- Caricare un file (es. `Signals.txt`) con 20-30 segnali comportamentali
- I segnali sono frasi o emozioni comuni dell’utente
- Il GPT deve adattare il tono o la risposta

Esempi:

**Segnale 1:** L’utente esprime un problema
> Risposta: "Sembra una situazione complessa. Vuoi lavorarci insieme?"

**Segnale 2:** L’utente si sente incompreso
> Risposta: "Capisco cosa stai passando. Sono qui per aiutarti con [obiettivo]"

**Segnale 3:** L’utente si affida al GPT
> Risposta: "È normale contare su di me mentre lavori. Sono qui quando vuoi."

⚠️ Non inserire gli esempi direttamente nel prompt, ma nel file

Questo migliora:
- naturalezza della conversazione
- adattabilità sociale del GPT
- coerenza emotiva

---

## ✅ Conclusione

Costruire un GPT personalizzato significa progettare un'esperienza:
- coerente
- utile
- naturale

Più si cura il prompt, i file e le regole, migliore sarà il risultato.

Un buon GPT personalizzato:
- fa risparmiare tempo
- migliora i flussi di lavoro
- crea interazioni coinvolgenti
