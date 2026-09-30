// Bacheca dei commenti di una pagina: versione DA CORREGGERE (laboratorio 5.2).
// aggiungiCommento inserisce il testo degli utenti come codice HTML.

function aggiungiCommento(lista, autore, testo) {
  const voce = document.createElement("li");
  voce.innerHTML = "<strong>" + autore + "</strong>: " + testo;
  lista.appendChild(voce);
  return voce;
}

function aggiornaAnteprima(anteprima, testo) {
  anteprima.innerHTML = "Anteprima: " + testo;
}
