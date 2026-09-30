// Logica del quiz: funzioni "pure", che non usano il DOM.
// Ricevono dati e restituiscono risultati: si possono verificare con test automatici (lezione 3.5).

// true se l'opzione scelta è quella corretta
function eCorretta(domanda, indiceScelto) {
  return indiceScelto === domanda.corretta;
}

// Numero di risposte corrette; risposte[i] è l'indice scelto per la domanda i (null se non data)
function calcolaPunteggio(domande, risposte) {
  let punti = 0;
  for (let i = 0; i < domande.length; i++) {
    if (risposte[i] !== null && eCorretta(domande[i], risposte[i])) {
      punti++;
    }
  }
  return punti;
}

// Giudizio in base alla percentuale di risposte corrette
function giudizio(punti, totale) {
  if (totale === 0) {
    return "nessuna domanda";
  }
  const percentuale = (punti / totale) * 100;
  if (percentuale === 100) {
    return "perfetto";
  } else if (percentuale >= 60) {
    return "superato";
  } else {
    return "da ripassare";
  }
}

// Restituisce una copia mescolata dell'array (algoritmo di Fisher-Yates); l'originale non cambia
function mescola(v) {
  const a = v.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));   // indice casuale tra 0 e i
    const temp = a[i];
    a[i] = a[j];
    a[j] = temp;
  }
  return a;
}
