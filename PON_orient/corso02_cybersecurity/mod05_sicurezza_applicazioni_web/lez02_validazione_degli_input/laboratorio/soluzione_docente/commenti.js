// Bacheca dei commenti: versione CORRETTA (soluzione per il docente, laboratorio 5.2).
// Il testo degli utenti viene inserito con textContent: il browser lo tratta sempre come testo.

function aggiungiCommento(lista, autore, testo) {
  const voce = document.createElement("li");
  const nome = document.createElement("strong");
  nome.textContent = autore;
  voce.append(nome, ": " + testo);   // le stringhe passate ad append diventano nodi di testo
  lista.appendChild(voce);
  return voce;
}

function aggiornaAnteprima(anteprima, testo) {
  anteprima.textContent = "Anteprima: " + testo;
}
