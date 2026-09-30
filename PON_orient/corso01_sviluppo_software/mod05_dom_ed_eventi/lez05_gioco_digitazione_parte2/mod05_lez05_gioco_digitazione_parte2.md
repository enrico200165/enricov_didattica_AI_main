---
title: "Lezione 5.5: Gioco di digitazione (parte 2) e memorizzazione locale"
subtitle: "Modulo 5: DOM ed eventi. Sviluppo Software e Coding Laboratoriale"
lang: it
---

# Lezione 5.5: Gioco di digitazione (parte 2) e memorizzazione locale

> Fonte: adattamento, tradotto e riscritto, della lezione "Creating a game using events" del corso Microsoft "Web Development for Beginners", https://github.com/microsoft/Web-Dev-For-Beginners/blob/main/4-typing-game/typing-game/README.md , e della parte su localStorage della lezione "Browser Extension Project Part 2", https://github.com/microsoft/Web-Dev-For-Beginners/blob/main/5-browser-extension/2-forms-browsers-local-storage/README.md . Copyright (c) Microsoft Corporation, licenza MIT: https://github.com/microsoft/Web-Dev-For-Beginners/blob/main/LICENSE . Calcolo della velocità, storico dei risultati e pulsante di azzeramento sono contenuto originale.

Prerequisito: lezione 5.4 (struttura del gioco e avvio della partita).

## 5.5.1 L'evento input

L'evento `input` si verifica a ogni modifica del contenuto di un campo di testo: carattere digitato, cancellato, incollato. Il gestore legge il valore attuale con la proprietà `value` del campo e decide che cosa fare.

Casi da distinguere, nell'ordine in cui vanno verificati:

| Caso | Condizione | Azione |
|---|---|---|
| 1. Frase completata | testo uguale alla parola corrente **e** parola corrente è l'ultima | fine della partita |
| 2. Parola completata | testo termina con uno spazio **e**, senza spazi, è uguale alla parola corrente | campo svuotato, evidenziazione alla parola successiva |
| 3. Nessun errore finora | la parola corrente inizia con il testo digitato | campo senza segnalazione di errore |
| 4. Errore | tutti gli altri casi | campo segnalato come errato |

L'ordine conta (lezione 3.3): il caso 3 è vero anche quando la parola è completa, quindi i casi 1 e 2 vanno verificati prima.

Metodi delle stringhe usati:

- `s.endsWith(" ")`: `true` se `s` termina con uno spazio
- `s.trim()`: copia di `s` senza spazi iniziali e finali
- `s.startsWith(t)`: `true` se `s` inizia con `t`; con `t` vuoto è sempre vero

## 5.5.2 Il controllo della digitazione

Aggiungere a `script.js`:

```javascript
// ---------- Controllo di ciò che viene digitato ----------

elDigitato.addEventListener("input", () => {
  const parolaCorrente = parole[indiceParola];
  const digitato = elDigitato.value;

  if (digitato === parolaCorrente && indiceParola === parole.length - 1) {
    // Caso 1: ultima parola completata, fine della partita
    fine();
  } else if (digitato.endsWith(" ") && digitato.trim() === parolaCorrente) {
    // Caso 2: parola completata e confermata con lo spazio, si passa alla successiva
    elDigitato.value = "";
    elFrase.children[indiceParola].classList.remove("evidenziata");
    indiceParola++;
    elFrase.children[indiceParola].classList.add("evidenziata");
  } else if (parolaCorrente.startsWith(digitato)) {
    // Caso 3: finora nessun errore
    elDigitato.classList.remove("errore");
  } else {
    // Caso 4: il testo digitato non corrisponde all'inizio della parola
    elDigitato.classList.add("errore");
  }
});

function fine() {
  const secondi = (Date.now() - inizio) / 1000;
  const ppm = Math.round(parole.length / (secondi / 60));   // parole al minuto
  elFrase.children[indiceParola].classList.remove("evidenziata");
  elDigitato.disabled = true;
  elMessaggio.textContent = `Completato in ${secondi.toFixed(1)} secondi: ${ppm} parole al minuto.`;
  salvaRisultato(ppm);
}
```

Velocità in **parole al minuto**: numero di parole diviso per il tempo in minuti (`secondi / 60`). È una misura confrontabile tra frasi di lunghezza diversa, a differenza del tempo totale.

Situazione durante una partita, con un errore di digitazione sulla quarta parola:

![Partita in corso: parola corrente evidenziata, campo segnalato in rosso per un errore](mod05_lez05_partita_in_corso.png)

## 5.5.3 Memorizzazione locale: localStorage

I valori delle variabili si perdono quando la pagina viene chiusa o ricaricata. Per conservare dati tra una visita e l'altra, senza un server, i browser offrono **localStorage**: un archivio di coppie **chiave-valore** associato al sito, che persiste anche dopo la chiusura del browser.

```javascript
localStorage.setItem("colore", "verde");        // salva il valore con la chiave indicata
localStorage.getItem("colore");                 // "verde"; null se la chiave non esiste
localStorage.removeItem("colore");              // elimina la coppia
```

Caratteristiche e limiti:

- **solo stringhe**: un numero salvato torna come stringa (`"42"`) e va convertito con `Number()`; oggetti e array vanno trasformati in testo con **JSON**
- **locale**: i dati restano nel browser del computer in uso, non si sincronizzano con altri dispositivi e non sono visibili agli altri utenti
- **per sito**: ogni sito ha il proprio archivio, separato da quello degli altri
- **non sicuro per dati riservati**: qualunque script eseguito nella pagina può leggerlo; non vi si salvano password o dati personali sensibili
- con le pagine aperte come file (`file:///...`) il comportamento varia da browser a browser: il gioco va aperto con Live Preview, che usa un indirizzo `http://`

Riferimento: MDN, `localStorage`, https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage

**JSON** (JavaScript Object Notation) è un formato di testo per rappresentare oggetti e array, usato ovunque per lo scambio di dati tra programmi:

```javascript
const storico = [{ ppm: 42, data: "29/09/2026" }];
const testo = JSON.stringify(storico);   // '[{"ppm":42,"data":"29/09/2026"}]': una stringa
const diNuovo = JSON.parse(testo);       // di nuovo un array di oggetti
```

Negli strumenti per sviluppatori il contenuto di localStorage si vede nella scheda Application (Chrome, Edge) o Archiviazione (Firefox), sezione Local Storage: si può leggere, modificare, cancellare.

## 5.5.4 Record e storico dei risultati

1. In `index.html`, dopo il `div` con classe `comandi`, aggiungere la sezione dei risultati:

```html
<h2>Risultati</h2>
<p id="record"></p>
<ol id="storico"></ol>
<button type="button" id="azzera">Cancella i risultati salvati</button>
```

2. In `script.js`, tra i dati:

```javascript
// Chiavi usate in localStorage
const CHIAVE_RECORD = "digitazioneRecord";
const CHIAVE_STORICO = "digitazioneStorico";
```

e tra i riferimenti:

```javascript
const elRecord = document.getElementById("record");
const elStorico = document.getElementById("storico");
const elAzzera = document.getElementById("azzera");
```

3. In fondo a `script.js`:

```javascript
// ---------- Memorizzazione locale ----------

function salvaRisultato(ppm) {
  // Record: un solo numero, salvato come stringa
  const record = localStorage.getItem(CHIAVE_RECORD);    // null se non esiste
  if (record === null || ppm > Number(record)) {
    localStorage.setItem(CHIAVE_RECORD, String(ppm));
    elMessaggio.textContent += " Nuovo record!";
  }

  // Storico: array degli ultimi 5 risultati, salvato come testo JSON
  const storico = leggiStorico();
  storico.unshift({ ppm: ppm, data: new Date().toLocaleString("it-IT") });
  localStorage.setItem(CHIAVE_STORICO, JSON.stringify(storico.slice(0, 5)));

  mostraRisultati();
}

function leggiStorico() {
  const testo = localStorage.getItem(CHIAVE_STORICO);
  if (testo === null) {
    return [];
  }
  return JSON.parse(testo);
}

function mostraRisultati() {
  const record = localStorage.getItem(CHIAVE_RECORD);
  elRecord.textContent = record === null
    ? "Nessun risultato salvato."
    : `Record: ${record} parole al minuto.`;

  elStorico.textContent = "";
  for (const r of leggiStorico()) {
    const li = document.createElement("li");
    li.textContent = `${r.ppm} parole al minuto (${r.data})`;
    elStorico.appendChild(li);
  }
}

elAzzera.addEventListener("click", () => {
  localStorage.removeItem(CHIAVE_RECORD);
  localStorage.removeItem(CHIAVE_STORICO);
  mostraRisultati();
});

// All'apertura della pagina si mostrano i risultati salvati in precedenza
mostraRisultati();
```

Elementi nuovi:

- `storico.unshift(...)` inserisce il nuovo risultato in testa all'array; `storico.slice(0, 5)` ne conserva i primi cinque: lo storico non cresce all'infinito.
- `new Date().toLocaleString("it-IT")`: data e ora attuali in formato italiano.
- `condizione ? a : b`: operatore ternario (lezione 3.3), qui scritto su più righe per leggibilità.
- `mostraRisultati()` in fondo al file viene eseguita a ogni caricamento: legge lo stato salvato e aggiorna la pagina (schema della lezione 5.3).

## 5.5.5 Laboratorio

Tempo indicativo: 35 minuti.

1. Completare `index.html` e `script.js` con il codice delle sezioni 5.5.2 e 5.5.4.
2. Giocare una partita completa verificando i quattro casi: digitazione corretta, errore (campo rosso), correzione con il tasto di cancellazione (il rosso scompare), fine partita.
3. Giocare altre partite, poi **ricaricare la pagina**: record e storico devono essere ancora presenti.
4. Nella scheda Application (o Archiviazione) degli strumenti per sviluppatori individuare le due chiavi, osservare il testo JSON dello storico, modificare a mano il record e ricaricare la pagina.
5. Premere **Cancella i risultati salvati** e verificare che le chiavi scompaiano.
6. Commit: "Gioco di digitazione completo".

La soluzione completa è nella cartella `soluzione_gioco_digitazione` di questa lezione.

### Esercizi

1. Contare gli errori commessi durante la partita (quante volte si entra nel caso 4 partendo da uno stato senza errore) e mostrarli nel messaggio finale.
2. Consentire di avviare una nuova partita con il tasto `Invio` quando il campo è disattivato (evento `keydown` sul `document`, `evento.key === "Enter"`).
3. Salvare nello storico anche la frase digitata e mostrarla nell'elenco.
4. Impedire di incollare testo nel campo, che permetterebbe di barare: registrare un gestore dell'evento `paste` che chiama `evento.preventDefault()`. Discutere: questa misura impedisce davvero di barare, sapendo che chiunque può modificare il codice della pagina con gli strumenti per sviluppatori?

## 5.5.6 Aspetti orientativi (discussione)

- Le tecniche viste nel modulo (DOM, eventi, stato, memorizzazione locale, JSON) sono la base di ogni applicazione web; i framework professionali le organizzano e le automatizzano, ma non le sostituiscono.
- JSON è il formato standard per lo scambio di dati tra applicazioni: le API dei servizi web (meteo, mappe, pagamenti) rispondono in JSON. Il corso "Reti, Cloud e Gestione dei Dati" approfondisce server e database.
- La scelta di dove conservare i dati (nel browser, su un server, in un database) è una decisione di progetto con conseguenze su sicurezza, privacy (GDPR) e funzionamento su più dispositivi.
- Domande per il dibattito: quali dati di un'app di uso quotidiano potrebbero stare solo sul telefono, e quali devono stare su un server? Perché?
