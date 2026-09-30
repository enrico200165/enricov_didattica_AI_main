// Terrario interattivo: trascinamento delle piante, conteggio, riordino

// z-index da assegnare alla pianta afferrata più di recente: la porta in primo piano.
// Variabile globale, condivisa da tutte le piante.
let zMassimo = 10;

// Rende trascinabile l'elemento ricevuto.
// Le variabili xPrec e yPrec e le tre funzioni interne formano una closure:
// ogni chiamata di rendiTrascinabile crea una copia separata, dedicata a quell'elemento.
function rendiTrascinabile(elemento) {
  let xPrec = 0;   // ultima posizione nota del puntatore, in orizzontale
  let yPrec = 0;   // ultima posizione nota del puntatore, in verticale

  elemento.addEventListener("pointerdown", iniziaTrascinamento);

  // Pulsante premuto (o dito appoggiato) sulla pianta
  function iniziaTrascinamento(e) {
    e.preventDefault();              // evita la selezione e il trascinamento nativo dell'immagine
    xPrec = e.clientX;
    yPrec = e.clientY;
    zMassimo++;
    elemento.style.zIndex = zMassimo;
    // Movimento e rilascio si ascoltano sull'intero documento:
    // il puntatore può uscire dalla pianta durante un movimento veloce
    document.addEventListener("pointermove", trascina);
    document.addEventListener("pointerup", terminaTrascinamento);
  }

  // Puntatore in movimento: sposta la pianta dello stesso spostamento del puntatore
  function trascina(e) {
    const dx = e.clientX - xPrec;
    const dy = e.clientY - yPrec;
    xPrec = e.clientX;
    yPrec = e.clientY;
    elemento.style.left = (elemento.offsetLeft + dx) + "px";
    elemento.style.top = (elemento.offsetTop + dy) + "px";
  }

  // Pulsante rilasciato: si smette di ascoltare movimento e rilascio
  function terminaTrascinamento() {
    document.removeEventListener("pointermove", trascina);
    document.removeEventListener("pointerup", terminaTrascinamento);
    aggiornaConteggio();
  }
}

// true se il centro della pianta cade dentro le pareti del barattolo
function dentroBarattolo(pianta) {
  const p = pianta.getBoundingClientRect();   // rettangolo occupato sullo schermo
  const b = document.querySelector(".barattolo-pareti").getBoundingClientRect();
  const cx = p.left + p.width / 2;
  const cy = p.top + p.height / 2;
  return cx >= b.left && cx <= b.right && cy >= b.top && cy <= b.bottom;
}

// Conta le piante nel barattolo e aggiorna il testo nella pagina
function aggiornaConteggio() {
  let n = 0;
  for (const pianta of piante) {
    if (dentroBarattolo(pianta)) {
      n++;
    }
  }
  document.getElementById("conteggio").textContent = `Piante nel barattolo: ${n}`;
}

// Riporta tutte le piante nella posizione iniziale definita dal CSS
function riordina() {
  for (const pianta of piante) {
    pianta.style.left = "";      // stringa vuota: si elimina lo stile in linea,
    pianta.style.top = "";       // torna a valere il foglio di stile
    pianta.style.zIndex = "";
  }
  aggiornaConteggio();
}

// Avvio: tutte le immagini con classe "pianta" diventano trascinabili
const piante = document.querySelectorAll(".pianta");
piante.forEach(rendiTrascinabile);
document.getElementById("riordina").addEventListener("click", riordina);
