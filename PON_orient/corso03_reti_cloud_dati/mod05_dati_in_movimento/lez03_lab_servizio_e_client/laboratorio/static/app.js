// Pagina della biblioteca: legge i dati dall'API con fetch e li mostra nella pagina.
// I testi ricevuti vengono inseriti con textContent, mai con innerHTML:
// così un titolo che contiene "<script>" resta testo e non diventa codice (Corso 2, modulo 5).

const tabella = document.getElementById("libri");

async function caricaGeneri() {
  const risposta = await fetch("/api/generi");          // richiesta GET all'API
  const generi = await risposta.json();                 // corpo JSON -> array JavaScript
  const menu = document.getElementById("genere");
  for (const genere of generi) {
    const opzione = document.createElement("option");
    opzione.value = genere;
    opzione.textContent = genere;
    menu.append(opzione);
  }
}

async function caricaLibri() {
  // URLSearchParams costruisce "?cerca=...&genere=..." codificando spazi e caratteri speciali
  const parametri = new URLSearchParams({
    cerca: document.getElementById("cerca").value,
    genere: document.getElementById("genere").value,
  });
  const risposta = await fetch("/api/libri?" + parametri);
  const libri = await risposta.json();
  tabella.replaceChildren();                            // svuota la tabella
  for (const libro of libri) {
    const riga = tabella.insertRow();
    const titolo = riga.insertCell();
    titolo.textContent = libro.titolo;
    titolo.className = "titolo";
    titolo.addEventListener("click", () => mostraCopie(libro.id));
    riga.insertCell().textContent = libro.autore;
    riga.insertCell().textContent = libro.anno;
    const disponibili = riga.insertCell();
    disponibili.textContent = `${libro.copie_disponibili} su ${libro.copie_totali}`;
    if (libro.copie_disponibili === 0) disponibili.className = "nessuna";
  }
  document.getElementById("conteggio").textContent = `Libri trovati: ${libri.length}`;
}

async function mostraCopie(id) {
  const risposta = await fetch(`/api/libri/${id}`);
  const libro = await risposta.json();
  document.getElementById("titolo-dettaglio").textContent = `${libro.titolo} (${libro.autore})`;
  const elenco = document.getElementById("copie");
  elenco.replaceChildren();
  for (const copia of libro.copie) {
    const voce = document.createElement("li");
    voce.textContent = `${copia.collocazione}: ${copia.stato}, ` +
      (copia.disponibile ? "disponibile" : "non disponibile");
    elenco.append(voce);
  }
}

async function registraPrestito(evento) {
  evento.preventDefault();                              // evita il ricaricamento della pagina
  const esito = document.getElementById("esito");
  const risposta = await fetch("/api/prestiti", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      collocazione: document.getElementById("collocazione").value.trim(),
      id_studente: Number(document.getElementById("studente").value),
    }),
  });
  const dati = await risposta.json();
  if (risposta.ok) {                                    // codici 200-299
    esito.textContent = `Prestito ${dati.id_prestito} registrato, scadenza ${dati.data_scadenza}.`;
    esito.className = "ok";
    caricaLibri();                                      // aggiorna le disponibilità
  } else {
    esito.textContent = `Errore ${risposta.status}: ${dati.errore}`;
    esito.className = "errore";
  }
}

document.getElementById("ricerca").addEventListener("submit", (evento) => {
  evento.preventDefault();
  caricaLibri();
});
document.getElementById("prestito").addEventListener("submit", registraPrestito);

caricaGeneri();
caricaLibri();
