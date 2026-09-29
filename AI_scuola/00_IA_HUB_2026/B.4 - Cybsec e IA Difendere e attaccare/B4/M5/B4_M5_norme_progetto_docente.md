---
title: "Modulo 5 - Norme e progetto finale"
subtitle: "B.4 - Cybersicurezza e IA. Traccia docenti"
lang: it
---

# Modulo 5 - Traccia docenti

## Collocazione e finalità del modulo

Il modulo chiude il corso:

- L16 presenta il quadro normativo europeo e italiano e lo collega ai temi tecnici dei moduli precedenti
- L17 avvia il progetto finale a gruppi
- L18 comprende la presentazione dei progetti (parte studenti, 35 minuti) e un segmento di progettazione didattica per i docenti (25 minuti)

## Logica della progettazione

### Norme come strumento, non come elenco

La lezione L16 rischia di diventare un elenco di articoli. Tre scelte per evitarlo:

- ogni norma è collegata a un tema già visto (GDPR e L10, alto rischio e robustezza del modulo 4, reati e L1)
- il laboratorio traduce le regole in codice: per scrivere la funzione che classifica un sistema bisogna capire quali condizioni contano e in che ordine
- il codice è volutamente semplificato, e l'esercizio 2 chiede di trovarne i limiti: è lo stesso ragionamento sui limiti dei modelli fatto in L11-L13

### Norme aggiornate

Il quadro normativo sull'IA cambia rapidamente. Stato al 29 settembre 2026:

- l'Omnibus digitale sull'IA (Regolamento UE 2026/1744, pubblicato il 24 luglio 2026, in vigore dal 27 luglio 2026) ha rinviato gli obblighi per i sistemi ad alto rischio al 2 dicembre 2027 (Allegato III) e al 2 agosto 2028 (Allegato I), ha reso meno rigido l'obbligo di alfabetizzazione e ha introdotto il divieto dei sistemi che generano immagini intime non consensuali e materiale pedopornografico, dal 2 dicembre 2026
- la legge 132/2025 prevede numerosi decreti attuativi: prima di ogni edizione del corso verificare quali sono stati emanati

Prima di ogni edizione, controllare le date del calendario sul sito EUR-Lex e sul sito della Commissione europea, e le eventuali nuove indicazioni del Garante e del Ministero.

### Progetto finale

I quattro scenari corrispondono ai quattro filoni del corso (phishing e IA come arma, IA come bersaglio, credenziali, classificatore) e a profili diversi di studenti: comunicativo, analitico, normativo, tecnico. Lo scenario 4 richiede di saper modificare i notebook ed è adatto a chi ha frequentato B.8 o B.6.

Regole da ribadire per lo scenario 1: la campagna non produce messaggi di phishing realistici rivolti a persone reali e non li invia a nessuno, neppure come "test" sui compagni. Le simulazioni di phishing nelle organizzazioni si fanno solo con autorizzazione formale e informazione preventiva.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L16_norme_in_pratica.ipynb` | L16 | libreria standard (`datetime`) |
| `L17_registro_fonti.ipynb` | L17 | librerie: pandas, `urllib` |
| `L17_fonti.csv` | L17 | registro di esempio con errori voluti |
| `L18_rubrica_progetto.ipynb` | L18, docenti | calcolo dei punteggi dalla rubrica; librerie: pandas |
| `L18_valutazioni.csv` | L18, docenti | punteggi di esempio di cinque gruppi |

Materiali dei laboratori precedenti necessari per i progetti: notebook e dataset di L11, L12, L13 (scenario 4), materiali di L8-L9 (scenario 1), di L5-L7 (scenario 3), di L14-L15 (scenario 2).

### Checklist

- verificare che le date del calendario dell'AI Act siano ancora aggiornate
- preparare la scheda cartacea per la classificazione a mano (L16, esercizio 1): i dieci sistemi con le quattro colonne di categoria
- stabilire il tempo a casa per il progetto e la data di consegna
- decidere i pesi della rubrica e la conversione in voto in coerenza con i criteri del collegio dei docenti

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L16 | 30 min: fonti (3), GDPR (5), AI Act (12), legge 132/2025 (5), linee guida (2), reati (3) | 25 min | 5 min |
| L17 | 10 min: scenari, regole, rubrica | 45 min di lavoro a gruppi | 5 min: stato di avanzamento |
| L18 | presentazioni 35 min | | 25 min parte docenti |

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| confusione tra GDPR e AI Act | il GDPR riguarda i dati personali, con o senza IA; l'AI Act riguarda i sistemi di IA, anche senza dati personali |
| "l'alto rischio è vietato" | alto rischio significa obblighi, non divieto |
| il punteggio di comportamento sempre vietato | il divieto riguarda il punteggio che porta a trattamenti sfavorevoli sproporzionati o in contesti non collegati; va letto l'art. 5 |
| gruppi che si dividono le parti senza confrontarsi | chiedere la revisione reciproca documentata (criterio "lavoro di gruppo") |
| fonti solo da blog e siti divulgativi | usare il notebook del registro fonti e l'esercizio 4 di L17 |

## Considerazioni sugli strumenti per la didattica

### Regole in codice

La funzione `classifica` di L16 è un sistema a regole come il filtro di L9: leggibile, verificabile, ma limitato a ciò che il programmatore ha previsto. Il confronto con il classificatore addestrato di L11 chiude un filo del corso: i sistemi a regole si usano dove serve spiegare ogni decisione, come nell'applicazione di norme, e anche lì non sostituiscono il giudizio di una persona.

Esercizio ponte con B.8: trasformare `SISTEMI` in un file CSV e scrivere una funzione che lo legge e produce una tabella riassuntiva per categoria.

### Il registro delle fonti

Il controllo sul dominio è una prima selezione, non una verifica di qualità. La domanda finale del notebook riprende i domini ingannevoli di L2: un sito può imitare il nome di un'istituzione.

## Parte docenti di L18 (25 minuti)

### Rubrica e calcolo del punteggio

Il notebook `L18_rubrica_progetto.ipynb` calcola il punteggio ponderato e un voto in decimi. Pesi proposti:

| Criterio | Peso |
|---|---|
| correttezza tecnica | 30% |
| analisi attacco-difesa | 25% |
| fonti e norme | 20% |
| comunicazione | 15% |
| lavoro di gruppo | 10% |

Con i dati di esempio i voti risultano: gruppo D 9,7; gruppo A 8,9; gruppo B 7,8; gruppi C ed E 7,4. Il notebook indica per ogni gruppo il criterio più debole, da usare nel riscontro. La conversione lineare da 1-4 a 4-10 è un esempio e va sostituita con quella deliberata dalla scuola.

### Adattamento ad altri monte ore

| Monte ore | Proposta |
|---|---|
| 12 ore | M1 ridotto a 3 lezioni (L2 e L3 unite), M2 in 2 lezioni (L6 e L7 unite), M3 completo, M4 in 2 lezioni (L12-L13 e L14-L15 unite), L16 e un progetto breve |
| 24 ore | corso completo più un laboratorio aggiuntivo per modulo (per esempio la lettura guidata di un rapporto del CERT-AGID, esercizi ponte con B.8) e 3 ore di progetto |
| 30 ore | come 24 ore, con partecipazione a una competizione per studenti (per esempio le iniziative nazionali di cybersicurezza per le scuole superiori) |

### Collegamenti con gli altri corsi del programma

- B.8 Python per l'IA: esercizi ponte indicati nelle tracce docenti dei moduli 2, 4 e 5
- B.6 Data science e machine learning: costruzione e valutazione del classificatore; confronto tra modelli sotto attacco (L12-L13)
- B.7 Deepfake e IA generativa: riconoscimento tecnico dei deepfake; in B.4 il tema compare come strumento di frode (L9) e come reato (L16)
- B.2 Umani e algoritmi: privacy, tracciamento e dibattito etico; in B.4 gli aspetti tecnici e normativi

### Aggiornamento annuale

Da verificare all'inizio di ogni anno scolastico:

- norme: calendario dell'AI Act, decreti attuativi della legge 132/2025, provvedimenti del Garante, eventuali nuove linee guida del Ministero
- raccomandazioni tecniche: nuove revisioni di NIST SP 800-63B, nuova edizione della OWASP Top 10 per le applicazioni LLM
- casi reali: campagne recenti dal CERT-AGID per L1, L4, L8
- strumenti: disponibilità di adversarial.js, Jigsaw Phishing Quiz, Lakera Gandalf, KeePassXC portable, JupyterLite
- link: verifica automatica di tutti gli URL dei materiali

## Valutazione del modulo

La valutazione finale del corso è il progetto, valutato con la rubrica. Per L16 si può usare una breve verifica individuale (15 minuti):

- classificare tre sistemi di IA secondo l'AI Act, con motivazione
- indicare i tempi di notifica di una violazione di dati
- dire chi deve dare il consenso per l'uso di un servizio di IA da parte di uno studente di 13 anni e di uno di 15

Indicatori osservabili:

| Indicatore | Osservabile in |
|---|---|
| classifica un sistema di IA secondo l'AI Act | L16, esercizi 1 e 2 |
| applica le regole sulla violazione dei dati | L16, esercizio 3 |
| verifica e seleziona le fonti | L17, esercizi 3 e 4 |
| costruisce una tabella attacco-difesa | L17, esercizio 2; progetto |

## Soluzioni degli esercizi

### L16

- Esercizio 1: correttore con voto, sorveglianza delle prove, ordinamento delle iscrizioni: alto rischio; app di orientamento: alto rischio (valutazione del livello di istruzione) con obbligo di trasparenza; chatbot di segreteria: trasparenza; generatore di immagini: trasparenza (marcatura dei contenuti sintetici); rilevatore dell'attenzione tramite webcam: vietato se deduce emozioni o stati d'animo; punteggio di comportamento: vietato se porta a trattamenti sfavorevoli sproporzionati o in contesti non collegati; filtro antispam e correttore ortografico: rischio minimo.
- Esercizio 2: casi che la funzione classifica male, per esempio:
  - un rilevatore dell'attenzione che misura solo se lo sguardo è rivolto allo schermo, senza dedurre emozioni: non è riconoscimento delle emozioni, ma se usato durante le prove è sorveglianza ad alto rischio
  - il riconoscimento delle emozioni per motivi medici o di sicurezza è escluso dal divieto: la funzione non considera l'eccezione
  - un sistema usato a scuola ma non per le finalità dell'Allegato III (per esempio la gestione delle presenze) risulta a rischio minimo, ma può comunque trattare dati personali e richiedere una valutazione secondo il GDPR
  - il sistema aggiunto nel notebook (assistente vocale con voce sintetica) risulta con obblighi di trasparenza: corretto
- Esercizio 3: scoperta venerdì 13 novembre 2026 alle 17:30, scadenza lunedì 16 novembre alle 17:30. Il GDPR non prevede sospensioni per i giorni festivi: le 72 ore decorrono comunque. Con certificati medici (dati relativi alla salute, categorie particolari) il rischio è da considerare elevato: oltre alla notifica al Garante, va fatta la comunicazione agli interessati.
- Esercizio 4: al 1° ottobre 2026 lo studente nato il 15/03/2013 ha 13 anni (consenso dei genitori), quello nato il 30/09/2012 ha 14 anni (autonomo), quello nato il 2/10/2012 ha ancora 13 anni (consenso dei genitori: compie gli anni il giorno dopo), quello nato il 1/1/2010 ha 16 anni. La sola differenza tra gli anni darebbe 14 per il terzo studente, errore che il confronto tra mese e giorno corregge. Con account istituzionali il titolare del trattamento è la scuola; il fornitore del servizio è responsabile del trattamento.

### L17

- Esercizio 3: il notebook segnala la data di verifica mancante per OWASP, l'autore mancante per il CERT-AGID (va indicato come "CERT-AGID, AgID"), la data mancante per l'articolo sui chatbot; classifica come "da verificare" il blog senza https e come "altre" OWASP e l'articolo sui chatbot. OWASP è una fonte autorevole anche se non istituzionale: il controllo automatico non basta.
- Esercizio 4: dipende dalle fonti del gruppo.

## Materiale open source

Verifica puntuale per L16-L18: lezioni, notebook, dati e rubrica sono stati scritti da zero.

Materiali di approfondimento:

- Regolamento (UE) 2024/1689 (AI Act), testo italiano: https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=it
- Regolamento (UE) 2026/1744 (Omnibus digitale sull'IA): https://eur-lex.europa.eu/eli/reg/2026/1744/oj?locale=it
- Legge 23 settembre 2025, n. 132: https://www.gazzettaufficiale.it/eli/id/2025/09/25/25G00143/sg
- GDPR, testo italiano: https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=it
- Garante per la protezione dei dati personali: https://www.garanteprivacy.it/
- Linee guida MIM per l'IA nelle scuole, scheda Biodiritto: https://www.biodiritto.org/AI-Legal-Atlas/AI-Docs/Italia-Ministero-dell-Istruzione-e-del-Merito-Linee-guida-per-l-introduzione-dell-Intelligenza-Artificiale-nelle-Istituzioni-scolastiche
