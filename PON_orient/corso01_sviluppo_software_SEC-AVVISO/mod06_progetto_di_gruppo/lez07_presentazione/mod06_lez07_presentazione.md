---
title: "Lezione 6.7: Presentazione e retrospettiva"
subtitle: "Modulo 6: Progetto di gruppo. Sviluppo Software e Coding Laboratoriale"
lang: it
---

# Lezione 6.7: Presentazione e retrospettiva

Contenuto originale. Riferimenti esterni indicati nel testo.

Obiettivi della lezione: documentare il progetto, presentarlo mostrandone il funzionamento, analizzare il lavoro del gruppo per migliorarlo.

## 6.7.1 Il file README

Ogni progetto software ha un file `README.md` nella cartella principale: è la prima cosa che legge chi incontra il progetto, per esempio un nuovo collega o un selezionatore che esamina un portfolio. Contenuto essenziale:

```markdown
# Quiz di informatica

Quiz a scelta multipla sugli argomenti del corso "Sviluppo Software e
Coding Laboratoriale": correzione immediata, punteggio e giudizio finale.

## Funzionalità
- domande in ordine casuale
- evidenziazione della risposta corretta e di quella scelta
- utilizzabile con la sola tastiera e con i lettori di schermo

## Come avviarlo
Aprire la cartella in Visual Studio Code e avviare index.html con
l'estensione Live Preview. I test della logica si eseguono aprendo
test.html e leggendo la console del browser (F12).

## Struttura
- dati.js: domande
- logica.js: regole (punteggio, giudizio, mescolamento)
- app.js: interfaccia
- REQUISITI.md, PIANO.md, TEST.md, BUGS.md: documentazione del progetto

## Autori
Anna, Bruno, Carlo, Dario (classe 4B), anno scolastico 2026-27.
```

## 6.7.2 La presentazione

Durata: 6 minuti di presentazione e 2 minuti di domande per gruppo. Tutti i membri intervengono.

Struttura consigliata:

| Parte | Tempo | Contenuto |
|---|---|---|
| Problema | 30 s | a chi serve l'applicazione e che cosa permette di fare |
| Requisiti | 1 min | MVP e priorità; che cosa è stato escluso e perché |
| Dimostrazione | 2 min | uso dal vivo, seguendo un percorso preparato; almeno un caso di errore gestito |
| Scelte tecniche | 1 min | organizzazione dei file, modello dei dati, una funzione significativa |
| Qualità | 1 min | test automatici e manuali, errori trovati e corretti, accessibilità |
| Bilancio | 30 s | che cosa si farebbe con più tempo |

Indicazioni:

- la dimostrazione dal vivo segue un **percorso preparato e provato**; tenere pronte le immagini delle schermate nel caso qualcosa non funzioni
- mostrare il codice solo in pochi punti significativi, con carattere grande (in VS Code: `Ctrl` + `+`)
- mostrare la storia del progetto con `git log --oneline --graph`: documenta come ha lavorato il gruppo
- rispondere alle domande in modo diretto; "non lo sappiamo, verificheremo" è una risposta professionale

## 6.7.3 La retrospettiva

La **retrospettiva** è una riunione, prevista nei metodi agili al termine di ogni ciclo di lavoro, in cui il gruppo analizza **come** ha lavorato, non che cosa ha prodotto. Lo scopo è individuare pochi miglioramenti concreti per il lavoro successivo.

Formato "Continuare, Iniziare, Smettere" (15 minuti):

1. **Continuare**: che cosa ha funzionato e va mantenuto?
2. **Iniziare**: che cosa è mancato e andrebbe introdotto?
3. **Smettere**: che cosa ha fatto perdere tempo o creato problemi?
4. Scegliere **al massimo due azioni** concrete per il futuro, ciascuna con un responsabile.

Regole: si parla di fatti e di processi, non di colpe personali; ciascuno scrive prima da solo i propri punti, poi si confrontano.

Domande guida:

- i requisiti erano abbastanza chiari? Sono cambiati durante il lavoro?
- le attività del piano erano della dimensione giusta?
- quanti conflitti Git ci sono stati, e perché?
- i test hanno trovato errori prima del test incrociato?
- il carico di lavoro era distribuito in modo equilibrato?

## 6.7.4 Valutazione del progetto

Criteri usati dal docente, noti al gruppo dall'inizio del modulo:

| Criterio | Evidenze |
|---|---|
| Requisiti e pianificazione | `REQUISITI.md` con user story e criteri verificabili; `PIANO.md` aggiornato |
| Funzionamento | requisiti Must completi e funzionanti; gestione degli input non validi |
| Qualità del codice | separazione di dati, logica, interfaccia; nomi chiari; commenti; nessun codice duplicato inutile |
| Test | test automatici della logica superati; `TEST.md` eseguito; `BUGS.md` compilato e aggiornato |
| Accessibilità | uso da tastiera, contrasto, testi alternativi, analisi automatica senza problemi |
| Uso di Git | commit frequenti con messaggi chiari da parte di tutti i membri; uso dei branch |
| Presentazione | chiarezza, rispetto dei tempi, dimostrazione, risposte alle domande |
| Lavoro di gruppo | ruoli svolti, contributo di tutti, retrospettiva |

## 6.7.5 Laboratorio

Tempo indicativo: 60 minuti per l'intera classe, in funzione del numero di gruppi.

1. Scrivere `README.md` e completare la documentazione; ultimo commit e `git push`.
2. Preparare la presentazione (10 minuti) e provare la dimostrazione.
3. Presentazioni dei gruppi.
4. Retrospettiva di ogni gruppo; le due azioni scelte si scrivono in fondo a `PIANO.md`.

## 6.7.6 Aspetti orientativi (discussione)

- I ruoli del progetto corrispondono a professioni reali: product owner e analista (requisiti), sviluppatore front-end (interfaccia), tester e QA engineer (qualità), tech lead (organizzazione tecnica), Scrum master (processo e retrospettive).
- Il progetto, con README, storia Git e documentazione, può entrare in un **portfolio personale**: per un profilo junior dimostra competenze concrete più di un elenco di linguaggi conosciuti.
- Le competenze trasversali esercitate (comunicazione, organizzazione, gestione dei disaccordi, rispetto delle scadenze) sono tra le più richieste dalle aziende, spesso più delle competenze tecniche specifiche.
- Domande per il dibattito: quale ruolo è risultato più adatto a ciascuno? Quale sarebbe interessante provare?
