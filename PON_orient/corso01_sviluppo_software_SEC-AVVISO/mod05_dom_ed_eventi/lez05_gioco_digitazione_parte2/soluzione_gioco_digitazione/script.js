// Gioco di digitazione: soluzione completa (lezioni 5.4 e 5.5)

// ---------- Dati ----------

// Frasi proposte. La prima è l'inizio de "I promessi sposi" (A. Manzoni, 1840), testo di pubblico dominio.
const FRASI = [
  "Quel ramo del lago di Como, che volge a mezzogiorno, tra due catene non interrotte di monti.",
  "Chi va piano va sano e va lontano.",
  "Un programma fa esattamente quello che gli si chiede, non quello che si vorrebbe.",
  "Prima si scrivono i test, poi il codice che li supera.",
  "Ogni problema complesso si risolve dividendolo in problemi più semplici.",
  "Una buona documentazione vale quanto un buon programma.",
];

// Chiavi usate in localStorage
const CHIAVE_RECORD = "digitazioneRecord";
const CHIAVE_STORICO = "digitazioneStorico";

// ---------- Stato della partita ----------

let parole = [];        // parole della frase corrente
let indiceParola = 0;   // indice della parola da digitare
let inizio = 0;         // istante di inizio, in millisecondi

// ---------- Riferimenti agli elementi della pagina ----------

const elFrase = document.getElementById("frase");
const elMessaggio = document.getElementById("messaggio");
const elDigitato = document.getElementById("digitato");
const elInizia = document.getElementById("inizia");
const elRecord = document.getElementById("record");
const elStorico = document.getElementById("storico");
const elAzzera = document.getElementById("azzera");

// ---------- Avvio di una partita (lezione 5.4) ----------

elInizia.addEventListener("click", () => {
  // Frase casuale, divisa in parole
  const frase = FRASI[Math.floor(Math.random() * FRASI.length)];
  parole = frase.split(" ");
  indiceParola = 0;

  // Una parola per span; textContent non interpreta il testo come HTML
  elFrase.textContent = "";
  for (const parola of parole) {
    const span = document.createElement("span");
    span.textContent = parola + " ";
    elFrase.appendChild(span);
  }
  elFrase.children[0].classList.add("evidenziata");

  // Preparazione del campo di input
  elMessaggio.textContent = "";
  elDigitato.value = "";
  elDigitato.disabled = false;
  elDigitato.classList.remove("errore");
  elDigitato.focus();

  inizio = Date.now();
});

// ---------- Controllo di ciò che viene digitato (lezione 5.5) ----------

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

// ---------- Memorizzazione locale (lezione 5.5) ----------

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
