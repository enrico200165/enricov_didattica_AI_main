// Interfaccia del quiz: stato, disegno della pagina a partire dallo stato, gestori di evento.

// ---------- Stato ----------
let domande = [];      // domande della partita, in ordine mescolato
let indice = 0;        // domanda corrente
let risposte = [];     // indice dell'opzione scelta per ogni domanda (null se non ancora data)

// ---------- Riferimenti ----------
const elContatore = document.getElementById("contatore");
const elTesto = document.getElementById("testo-domanda");
const elOpzioni = document.getElementById("opzioni");
const elEsito = document.getElementById("esito");
const elAvanti = document.getElementById("avanti");
const elRisultato = document.getElementById("risultato");
const elRicomincia = document.getElementById("ricomincia");

// ---------- Avvio e disegno ----------

function nuovaPartita() {
  domande = mescola(DOMANDE);
  indice = 0;
  risposte = domande.map(() => null);   // un null per ogni domanda
  elRisultato.textContent = "";
  elRicomincia.hidden = true;
  mostraDomanda();
}

// Disegna la domanda corrente a partire dallo stato
function mostraDomanda() {
  const d = domande[indice];
  elContatore.textContent = `Domanda ${indice + 1} di ${domande.length}`;
  elTesto.textContent = d.testo;
  elEsito.textContent = "";
  elAvanti.hidden = true;

  elOpzioni.textContent = "";
  d.opzioni.forEach((testoOpzione, i) => {
    const pulsante = document.createElement("button");
    pulsante.type = "button";
    pulsante.textContent = testoOpzione;
    pulsante.addEventListener("click", () => rispondi(i));
    elOpzioni.appendChild(pulsante);
  });
}

// ---------- Gestori ----------

function rispondi(i) {
  if (risposte[indice] !== null) {
    return;                           // domanda già risposta: si ignora un secondo clic
  }
  risposte[indice] = i;
  const d = domande[indice];
  const pulsanti = elOpzioni.querySelectorAll("button");
  pulsanti.forEach((p) => (p.disabled = true));
  pulsanti[d.corretta].classList.add("giusta");
  if (eCorretta(d, i)) {
    elEsito.textContent = "Risposta corretta.";
  } else {
    pulsanti[i].classList.add("sbagliata");
    elEsito.textContent = `Risposta errata. Corretta: ${d.opzioni[d.corretta]}.`;
  }
  elAvanti.hidden = false;
  elAvanti.focus();
}

function avanti() {
  if (indice < domande.length - 1) {
    indice++;
    mostraDomanda();
  } else {
    fine();
  }
}

function fine() {
  const punti = calcolaPunteggio(domande, risposte);
  elContatore.textContent = "Quiz terminato";
  elTesto.textContent = "Risultato finale";      // un titolo non deve restare vuoto (lezione 4.2)
  elOpzioni.textContent = "";
  elEsito.textContent = "";
  elAvanti.hidden = true;
  elRisultato.textContent = `Punteggio: ${punti} su ${domande.length} (${giudizio(punti, domande.length)}).`;
  elRicomincia.hidden = false;
}

elAvanti.addEventListener("click", avanti);
elRicomincia.addEventListener("click", nuovaPartita);

nuovaPartita();
