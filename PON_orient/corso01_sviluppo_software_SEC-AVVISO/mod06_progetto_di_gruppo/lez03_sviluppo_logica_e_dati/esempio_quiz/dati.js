// Dati del quiz: array di oggetti. In un progetto reale potrebbero arrivare da un file JSON o da un server.
// Ogni domanda: testo, elenco di opzioni, indice dell'opzione corretta.
const DOMANDE = [
  {
    testo: "Quale linguaggio definisce la struttura di una pagina web?",
    opzioni: ["CSS", "HTML", "JavaScript", "Git"],
    corretta: 1,
  },
  {
    testo: "Quale struttura di controllo ripete un blocco di istruzioni?",
    opzioni: ["Sequenza", "Selezione", "Iterazione", "Assegnazione"],
    corretta: 2,
  },
  {
    testo: "Quanti confronti servono al massimo alla ricerca binaria su 1000 elementi ordinati?",
    opzioni: ["10", "100", "500", "1000"],
    corretta: 0,
  },
  {
    testo: "Quale comando Git registra le modifiche della staging area?",
    opzioni: ["git add", "git status", "git commit", "git log"],
    corretta: 2,
  },
  {
    testo: "Quale proprietà del DOM imposta il testo di un elemento senza interpretarlo come HTML?",
    opzioni: ["innerHTML", "textContent", "value", "style"],
    corretta: 1,
  },
];
