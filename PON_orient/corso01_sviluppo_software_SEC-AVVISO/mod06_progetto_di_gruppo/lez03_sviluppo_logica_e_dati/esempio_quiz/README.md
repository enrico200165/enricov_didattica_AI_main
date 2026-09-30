# Quiz di informatica (progetto d'esempio)

Quiz a scelta multipla sugli argomenti del corso "Sviluppo Software e
Coding Laboratoriale": correzione immediata, punteggio e giudizio finale.
Progetto d'esempio del modulo 6 (Progetto di gruppo).

## Funzionalità
- domande in ordine casuale (algoritmo di Fisher-Yates)
- evidenziazione della risposta corretta e di quella scelta, anche con testo
- risposta non modificabile dopo la scelta
- punteggio e giudizio finale (perfetto, superato con almeno il 60%, da ripassare)
- utilizzabile con la sola tastiera e con i lettori di schermo

## Come avviarlo
Aprire la cartella in Visual Studio Code e avviare index.html con
l'estensione Live Preview. I test della logica si eseguono aprendo
test.html e leggendo la console del browser (F12): risultato atteso
"Test superati: 18, falliti: 0".

## Struttura
- dati.js: domande
- logica.js: regole (correzione, punteggio, giudizio, mescolamento), funzioni pure
- app.js: stato, disegno della pagina, gestori di evento
- test.html, test.js: test automatici della logica e dei dati
