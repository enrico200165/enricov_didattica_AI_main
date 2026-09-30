// Test della logica del quiz: aprire test.html e leggere la console
let superati = 0;
let falliti = 0;

function verifica(descrizione, ottenuto, atteso) {
  const ok = JSON.stringify(ottenuto) === JSON.stringify(atteso);
  if (ok) {
    superati++;
    console.log(`OK      ${descrizione}`);
  } else {
    falliti++;
    console.error(`FALLITO ${descrizione}: atteso ${JSON.stringify(atteso)}, ottenuto ${JSON.stringify(ottenuto)}`);
  }
}

const d0 = { testo: "?", opzioni: ["a", "b", "c"], corretta: 1 };
const d1 = { testo: "?", opzioni: ["a", "b"], corretta: 0 };

verifica("risposta corretta", eCorretta(d0, 1), true);
verifica("risposta errata", eCorretta(d0, 2), false);

verifica("punteggio pieno", calcolaPunteggio([d0, d1], [1, 0]), 2);
verifica("punteggio nullo", calcolaPunteggio([d0, d1], [0, 1]), 0);
verifica("risposte mancanti", calcolaPunteggio([d0, d1], [null, 0]), 1);
verifica("nessuna domanda", calcolaPunteggio([], []), 0);

verifica("giudizio perfetto", giudizio(5, 5), "perfetto");
verifica("giudizio al limite del 60%", giudizio(3, 5), "superato");
verifica("giudizio sotto il 60%", giudizio(2, 5), "da ripassare");
verifica("giudizio senza domande", giudizio(0, 0), "nessuna domanda");

const originale = [1, 2, 3, 4, 5];
const mescolato = mescola(originale);
verifica("mescola: stessa lunghezza", mescolato.length, 5);
verifica("mescola: stessi elementi", mescolato.slice().sort(), [1, 2, 3, 4, 5]);
verifica("mescola: originale invariato", originale, [1, 2, 3, 4, 5]);

// Controllo dei dati: ogni domanda deve avere un indice corretto valido
DOMANDE.forEach((d, i) => {
  verifica(`dati: domanda ${i + 1} con indice corretto valido`, d.corretta >= 0 && d.corretta < d.opzioni.length, true);
});

console.log(`Test superati: ${superati}, falliti: ${falliti}`);
