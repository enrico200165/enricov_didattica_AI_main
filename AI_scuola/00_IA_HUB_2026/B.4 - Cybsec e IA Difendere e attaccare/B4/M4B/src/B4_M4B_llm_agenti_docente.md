---
title: "Modulo 4B - Modelli linguistici, assistenti e agenti"
subtitle: "B.4 - Cybersicurezza e IA. Traccia docenti"
lang: it
---

# Modulo 4B - Traccia docenti

## Collocazione e finalità del modulo

Le lezioni L14 e L15 chiudono il modulo 4:

- L14 tratta i rischi specifici delle applicazioni basate su modelli linguistici: prompt injection, jailbreak, fuga del prompt di sistema, allucinazioni
- L15 applica gli stessi rischi agli assistenti e agli agenti che eseguono azioni, e si chiude con regole d'uso per gli studenti

Segmento di traccia docenti in aula: 10-15 minuti al termine di L15, su come mantenere aggiornato un modulo su una tecnologia che cambia ogni pochi mesi e sull'uso di scenari descritti al posto di strumenti reali.

## Logica della progettazione

### Scenari e controlli difensivi

I laboratori non chiedono agli studenti di costruire o eseguire attacchi contro modelli linguistici. Il lavoro pratico è di due tipi:

- analisi di scenari descritti: riconoscere il tipo di attacco, la parte del sistema coinvolta, il danno, la contromisura
- controlli difensivi con codice: istruzioni di sistema che contengono segreti, pacchetti suggeriti da verificare, permessi di un'estensione, codice generato da rivedere, strumenti di un agente da ridurre

La scelta ha tre ragioni:

- i modelli linguistici reali cambiano di continuo: un attacco che funziona oggi non funziona domani, mentre i principi (istruzioni e dati nello stesso canale, minimo privilegio, conferma umana) restano validi
- gli studenti sono minorenni e molti servizi di IA hanno condizioni d'uso che non ne consentono l'uso autonomo (L16)
- le competenze utili agli studenti come utenti e futuri sviluppatori sono quelle di chi progetta e usa i sistemi in modo sicuro

### Lakera Gandalf

Il gioco è facoltativo. Se si usa, il registro dell'esercizio 5 riguarda le difese del gioco (che cosa sembra controllare ogni livello e perché non basta), non le frasi usate per superarle. La traccia non fornisce soluzioni dei livelli. La discussione finale porta alla conclusione di L14: una difesa basata solo su istruzioni al modello o su filtri del testo può sempre essere aggirata, e i danni si limitano con il minimo privilegio e i controlli esterni al modello.

Prima dell'uso in classe, il docente verifica le condizioni d'uso del sito e se richiede la registrazione.

### Il laboratorio aggiuntivo di L14

La lezione e il notebook contengono uno spazio per un'attività preparata dal docente (commento `LABORATORIO AGGIUNTIVO L14` nella lezione e nelle presentazioni, sezione 3 del notebook `L14_verifiche_difensive.ipynb`).

<!-- LABORATORIO AGGIUNTIVO L14: spazio per la traccia docenti dell'esercizio preparato dal docente (obiettivi, materiali, conduzione, soluzioni) -->

### Collegamenti con i moduli precedenti

| Concetto di M4B | Ripreso da |
|---|---|
| contenuti non fidati, istruzioni nascoste | L8 phishing: il messaggio chiede un'azione; qui la chiede al modello |
| istruzioni e dati nello stesso canale | L12 esempi avversari: il modello non distingue il significato |
| catena di fornitura, pacchetti inesistenti | L12 e L13 |
| dati nei chatbot | L10 |
| password in chiaro nel codice generato | L3 e L5 |
| estensioni e app false | L4 e L9 |

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L14_verifiche_difensive.ipynb` | L14 | librerie: `re`, `importlib` (libreria standard) |
| `L15_agenti_estensioni.ipynb` | L15 | librerie: `json`, `hashlib`, `hmac`, `os` (libreria standard) |

I notebook non richiedono librerie esterne né rete. In JupyterLite il controllo dei pacchetti installati (L14, esercizio 4) può dare risultati diversi da WinPython, perché l'insieme delle librerie preinstallate è diverso: è un'occasione per osservare che la verifica va fatta nell'ambiente in cui il codice verrà eseguito.

### Checklist

- stampare o proiettare gli scenari degli esercizi 1 di L14 e L15
- se si usa Gandalf, verificarne in anticipo l'accesso dalla rete della scuola
- per l'esercizio 5 di L15, preparare un documento condiviso o un cartellone per la carta d'uso

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L14 | 25 min: composizione del prompt (5), prompt injection e caso EchoLeak (7), jailbreak e fuga del prompt (5), allucinazioni (3), OWASP e difese (5) | 30 min | 5 min |
| L15 | 20 min: agenti (5), triade letale (5), principi di difesa (4), codice, estensioni, regole (6) | 25 min | 10-15 min di traccia docenti |

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| "basta scrivere nelle istruzioni di non obbedire ad altri" | le istruzioni sono testo come i dati: riducono il rischio, non lo eliminano; i controlli devono stare fuori dal modello |
| confusione tra jailbreak e prompt injection | chiedere quali regole vengono aggirate: quelle del produttore del modello o quelle dell'applicazione |
| interesse per le tecniche di aggiramento dei chatbot | riportare la discussione sul danno e sulle difese; ricordare le regole etiche di L1 e le condizioni d'uso dei servizi |
| "il codice generato funziona, quindi è corretto" | L15 esercizio 3: il codice funziona ed è insicuro |
| agenti percepiti come fantascienza | molti servizi di posta, browser e sistemi operativi integrano già funzioni di questo tipo |

## Considerazioni sugli strumenti per la didattica

### Espressioni regolari per i controlli

Il controllo delle istruzioni di sistema (L14, esercizio 3) mostra un uso concreto delle espressioni regolari nella sicurezza: gli stessi strumenti servono a cercare chiavi e password dimenticate nel codice sorgente prima di pubblicarlo. Il controllo è volutamente incompleto: non trova la regola sulle iscrizioni in ritardo, che non ha una forma riconoscibile. La revisione umana resta necessaria.

Esercizio ponte con B.8: scrivere uno schema per indirizzi email, IBAN italiani e codici fiscali, e applicare `controlla` a un file di testo.

### Manifesto di un'estensione

I nomi dei permessi sono quelli reali delle estensioni di Chrome. Il docente può mostrare dal browser la pagina di un'estensione installata e i permessi che richiede, senza installarne di nuove.

## Valutazione del modulo

La verifica del modulo 4 (dopo L15, 20 minuti, individuale) comprende la parte su M4A (vedi traccia docenti M4A) e:

- classificare tre scenari come prompt injection diretta, indiretta, jailbreak o fuga del prompt di sistema
- indicare che cosa non deve contenere il prompt di sistema di un'applicazione e perché
- dato un agente con i suoi strumenti, dire se presenta la triade completa e proporre una modifica

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| riconosce i tipi di attacco ai modelli linguistici | L14, esercizi 1 e 2 |
| individua segreti nelle istruzioni di sistema | L14, esercizio 3 |
| verifica un pacchetto prima dell'installazione | L14, esercizio 4 |
| valuta i permessi di un'estensione | L15, esercizio 2 |
| individua un errore di sicurezza nel codice generato | L15, esercizio 3 |
| applica minimo privilegio e conferma umana a un agente | L15, esercizio 4 |

## Soluzioni degli esercizi

### L14

- Esercizio 1:
  - chatbot di orientamento che mostra le regole interne: fuga del prompt di sistema, ottenuta con una richiesta diretta dell'utente; parte coinvolta: istruzioni di sistema
  - riassunto di pagine web che invita a scaricare un'app: prompt injection indiretta; parte coinvolta: dati recuperati (la pagina)
  - risposta esclusa dal produttore: jailbreak; parte coinvolta: regole di comportamento del modello
  - assistente di posta con il nuovo IBAN: prompt injection indiretta con istruzioni nascoste nell'email; è la versione con IA della frode del falso fornitore di L8
- Esercizio 2: fuga del prompt: LLM07 (e LLM02 se le regole contengono dati personali); riassunto con app: LLM01, LLM05 se il link viene reso cliccabile senza controlli, LLM09; jailbreak: LLM01; nuovo IBAN: LLM01, LLM09, e LLM06 se l'assistente potesse anche disporre pagamenti.
- Esercizio 3: il controllo trova la chiave `cal_key`, la password dell'area riservata, il numero interno, la frase "da non comunicare" (due corrispondenze della regola "riservata", una nella riga della password). Vanno tolte le righe della chiave, del numero, della password e della regola sulle iscrizioni in ritardo. La chiave va nel programma che interroga il calendario; la password non deve stare in nessuna istruzione; la regola sulle iscrizioni rivela un trattamento di favore e un nome, con danno per la scuola e per la persona. Il controllo automatico non trova la regola sulle iscrizioni. Schema possibile per le email: `r"[\w.+-]+@[\w-]+\.[\w.]+"`.
- Esercizio 4: in WinPython e nell'ambiente di prova `pandas`, `numpy`, `sklearn`, `hashlib` risultano installati, il nome inventato no. "Non installato" può indicare solo che la libreria non è presente nell'ambiente; "presente su PyPI" non garantisce nulla, perché chiunque può pubblicare. Controlli: nome esatto e progetto ufficiale (link dalla documentazione della libreria), autore, data della prima pubblicazione, numero di versioni, collegamento a un repository con storia, documentazione. Un pacchetto pubblicato da pochi giorni con un nome suggerito da un assistente è un segnale d'allarme. Nota: `sklearn` è il nome del modulo; il pacchetto da installare si chiama `scikit-learn`, un esempio reale di differenza tra nome del modulo e nome del pacchetto.
- Esercizio 5: nessuna soluzione fornita; valutare il registro sulla qualità dell'analisi delle difese.

### L15

- Esercizio 1:
  - assistente di posta: prompt injection indiretta; danno: invio di dati o messaggi a nome dell'utente; contromisure: conferma umana per ogni invio, destinatari consentiti, nessun accesso a dati non necessari
  - agente di prenotazione: prompt injection indiretta dalla pagina; danno: prenotazione o pagamento su un sito sbagliato, dati personali inviati; contromisure: siti consentiti, conferma prima del pagamento, limite di spesa
  - libreria inesistente: allucinazione sfruttabile con un pacchetto malevolo; contromisure: verifica su PyPI, ambienti separati, revisione del codice
  - estensione: permessi eccessivi, possibile furto di sessioni e password; contromisure: non installarla, cercare alternative con permessi minimi, verificare l'editore
- Esercizio 2: 8 permessi, 6 ad alto rischio. Per riassumere la pagina attiva basta `activeTab`. `storage` è accettabile se l'estensione salva impostazioni.
- Esercizio 3: chi legge il dizionario ottiene tutte le password in chiaro, riutilizzabili su altri servizi (credential stuffing, L5). Due utenti con la stessa password hanno impronte diverse perché il sale è diverso: un archivio rubato non rivela quali utenti condividono la password e non si possono usare tabelle precalcolate. Le 200 000 iterazioni rendono ogni tentativo più lento: irrilevante per un singolo accesso, molto costoso per chi prova milioni di password.
- Esercizio 4: "assistente posta segreteria" e "ricerca web per compiti" hanno la triade completa. Modifiche possibili: all'assistente di posta togliere `invia_email` (produce bozze che l'utente invia) oppure sottoporlo a conferma; all'agente di ricerca togliere `carica_file` o `legge_documenti_studente`. "Prenotazione aule" ha una sola condizione ma può modificare il calendario: rischio di errori e di modifiche indesiderate, da limitare con conferma e registro delle modifiche.
- Esercizio 5: regole attese, per esempio: niente dati personali o documenti riservati; verificare fonti e citazioni; non aprire link e file suggeriti senza controlli; solo estensioni ufficiali con permessi minimi; leggere che cosa farà un assistente prima di autorizzarlo; usare gli account della scuola; dichiarare l'uso dell'IA nei lavori quando richiesto.

## Materiale open source

Verifica puntuale per L14-L15: lezioni e notebook sono stati scritti da zero. La tabella OWASP è una traduzione sintetica dei titoli della classifica 2025, pubblicata dalla OWASP Foundation.

Materiali di approfondimento:

- OWASP Top 10 for Large Language Model Applications: https://owasp.org/projects/top-10-for-large-language-model-applications
- P. Reddy, A. S. Gujral, EchoLeak (2025): https://arxiv.org/abs/2509.10540
- J. Spracklen et al., We Have a Package for You! (2024): https://arxiv.org/abs/2406.10279
- S. Willison, The lethal trifecta for AI agents (2025): https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Lakera Gandalf: https://gandalf.lakera.ai/
