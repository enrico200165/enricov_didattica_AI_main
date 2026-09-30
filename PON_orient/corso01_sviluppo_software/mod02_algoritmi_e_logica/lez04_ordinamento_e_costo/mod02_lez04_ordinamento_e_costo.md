---
title: "Lezione 2.4: Ordinamento e costo degli algoritmi"
subtitle: "Modulo 2: Algoritmi e logica. Sviluppo Software e Coding Laboratoriale"
lang: it
---

# Lezione 2.4: Ordinamento e costo degli algoritmi

Contenuto originale. Riferimenti esterni indicati nel testo.

Gli esempi JavaScript si eseguono nella console del browser oppure in un file `script.js` collegato a una pagina HTML (modulo 1, lezione 1.1, sezione 1.1.5). La sintassi di JavaScript è trattata in modo sistematico nel modulo 3: qui ogni costrutto è spiegato solo quanto basta per leggere gli esempi.

## 2.4.1 Il problema dell'ordinamento

**Ordinare** un array significa disporne gli elementi in ordine crescente (o decrescente). È uno dei problemi più studiati dell'informatica: dati ordinati permettono ricerche veloci (sezione 2.3.5), visualizzazioni leggibili, individuazione di duplicati. Esistono decine di algoritmi di ordinamento, con prestazioni diverse.

## 2.4.2 Selection sort

Idea del **selection sort** (ordinamento per selezione): si cerca il minimo dell'intero array e lo si scambia con il primo elemento; poi si cerca il minimo tra gli elementi dal secondo in poi e lo si scambia con il secondo; e così via. A ogni passo la parte sinistra dell'array è ordinata e definitiva.

```text
ALGORITMO SelectionSort
    n ← lunghezza(v)
    PER i DA 0 A n - 2 ESEGUI
        // cerca l'indice del minimo tra v[i] e v[n-1]
        posMin ← i
        PER j DA i + 1 A n - 1 ESEGUI
            SE v[j] < v[posMin] ALLORA
                posMin ← j
            FINE SE
        FINE PER
        // scambia v[i] e v[posMin]
        temp ← v[i]
        v[i] ← v[posMin]
        v[posMin] ← temp
    FINE PER
FINE
```

Lo **scambio** di due valori richiede una variabile di appoggio (`temp`): scrivendo direttamente `v[i] ← v[posMin]` il valore originale di `v[i]` andrebbe perso.

Traccia con v = [29, 10, 14, 37, 13] (in grassetto la parte già ordinata):

| i | Minimo tra v[i]..v[4] | Scambio | Array dopo il passo |
|---|---|---|---|
| 0 | 10 (indice 1) | v[0] e v[1] | [**10**, 29, 14, 37, 13] |
| 1 | 13 (indice 4) | v[1] e v[4] | [**10, 13**, 14, 37, 29] |
| 2 | 14 (indice 2) | nessuno effettivo | [**10, 13, 14**, 37, 29] |
| 3 | 29 (indice 4) | v[3] e v[4] | [**10, 13, 14, 29, 37**] |

Visualizzazione animata del selection sort e di altri algoritmi di ordinamento, gratuita e senza account: VisuAlgo, https://visualgo.net/en/sorting (voce "SEL").

## 2.4.3 Costo di un algoritmo

Il **costo** (complessità) di un algoritmo misura le risorse che richiede, in genere il tempo, in funzione della dimensione n dell'input. Anziché misurare i secondi, che dipendono dal computer, si contano le **operazioni fondamentali**: per gli algoritmi di ordinamento e di ricerca, i confronti.

Selection sort con n elementi: al primo passo il minimo si cerca tra n elementi (n - 1 confronti), al secondo tra n - 1 (n - 2 confronti), e così via fino a 1 confronto. Totale:

(n - 1) + (n - 2) + ... + 2 + 1 = n(n - 1) / 2

Il numero di confronti non dipende da come sono disposti i dati: è lo stesso anche se l'array è già ordinato. Voce enciclopedica: https://it.wikipedia.org/wiki/Selection_sort

| n | Confronti del selection sort |
|---|---|
| 10 | 45 |
| 100 | 4 950 |
| 1 000 | 499 500 |
| 10 000 | 49 995 000 |

Moltiplicando n per 10, i confronti crescono di circa 100 volte: il costo cresce come **n al quadrato** (costo **quadratico**). Classi di costo incontrate nel modulo, dalla più favorevole:

- **logaritmico**: ricerca binaria; raddoppiando n si aggiunge un'operazione
- **lineare**: ricerca lineare, massimo, somma; raddoppiando n raddoppiano le operazioni
- **quadratico**: selection sort; raddoppiando n le operazioni quadruplicano

Gli algoritmi di ordinamento più efficienti usati nella pratica (per esempio merge sort) hanno un costo proporzionale a n · log₂ n: per n = 1 000 000 servono circa 20 milioni di confronti, contro i circa 500 miliardi del selection sort.

Confronto numerico tra le classi di costo:

| n | log₂ n | n | n al quadrato |
|---|---|---|---|
| 8 | 3 | 8 | 64 |
| 64 | 6 | 64 | 4 096 |
| 1 024 | 10 | 1 024 | 1 048 576 |
| 1 048 576 | 20 | 1 048 576 | circa 1 100 miliardi |

## 2.4.4 Laboratorio: misurare i tempi

Tempo indicativo: 35 minuti.

Obiettivo: verificare sperimentalmente che il tempo del selection sort cresce in modo quadratico, e confrontarlo con il metodo di ordinamento predefinito di JavaScript.

Creare nella cartella `lab02` i file `index.html` (come nel laboratorio 1.1, con il titolo "Laboratorio 2") e `script.js` con il codice seguente.

```javascript
// Crea un array di n numeri interi casuali tra 0 e 999999
function arrayCasuale(n) {
  const v = [];                  // array vuoto
  for (let i = 0; i < n; i++) {
    // Math.random(): numero decimale casuale tra 0 (incluso) e 1 (escluso)
    // moltiplicato per 1000000 e troncato con Math.floor: intero tra 0 e 999999
    v.push(Math.floor(Math.random() * 1000000));   // push: aggiunge in fondo all'array
  }
  return v;
}

// Selection sort: ordina l'array v "sul posto" (modifica v stesso)
function selectionSort(v) {
  const n = v.length;
  for (let i = 0; i < n - 1; i++) {
    let posMin = i;
    for (let j = i + 1; j < n; j++) {
      if (v[j] < v[posMin]) {
        posMin = j;
      }
    }
    const temp = v[i];
    v[i] = v[posMin];
    v[posMin] = temp;
  }
}

// Verifica che l'array sia ordinato in modo crescente
function eOrdinato(v) {
  for (let i = 1; i < v.length; i++) {
    if (v[i - 1] > v[i]) {
      return false;
    }
  }
  return true;
}

// Misura i tempi per dimensioni crescenti, raddoppiando n a ogni passo
for (let n = 1000; n <= 16000; n = n * 2) {
  const a = arrayCasuale(n);
  const b = a.slice();           // slice(): copia dell'array, per ordinare gli stessi dati

  let t0 = performance.now();    // istante attuale in millisecondi
  selectionSort(a);
  const tempoSelection = performance.now() - t0;

  t0 = performance.now();
  b.sort((x, y) => x - y);       // ordinamento predefinito, criterio numerico
  const tempoSort = performance.now() - t0;

  console.log(
    `n = ${n}: selection sort ${tempoSelection.toFixed(1)} ms, ` +
    `sort predefinito ${tempoSort.toFixed(1)} ms, ` +
    `ordinati: ${eOrdinato(a) && eOrdinato(b)}`
  );
}
```

Elementi nuovi:

- `performance.now()` restituisce il tempo trascorso dal caricamento della pagina, in millisecondi con parte decimale; la differenza tra due chiamate misura la durata di un'operazione. Documentazione: https://developer.mozilla.org/en-US/docs/Web/API/Performance/now
- `b.sort((x, y) => x - y)` ordina l'array con l'algoritmo predefinito del motore JavaScript. L'argomento `(x, y) => x - y` è una **funzione freccia** che stabilisce il criterio: un risultato negativo significa che `x` va prima di `y`. Senza criterio, `sort` confronta i valori come testo e ordinerebbe `[1, 30, 4, 100000]` come `[1, 100000, 30, 4]`. Documentazione: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
- `valore.toFixed(1)` restituisce il numero come testo con una cifra decimale.
- `&&` è l'operatore logico E.

Attività:

1. Aprire la pagina con Live Preview nel browser esterno e leggere i risultati nella console. Con 16 000 elementi il selection sort può richiedere alcune centinaia di millisecondi su un PC di fascia bassa.
2. Riportare i tempi in una tabella. Verificare che, raddoppiando n, il tempo del selection sort diventi circa quattro volte maggiore, mentre il tempo del sort predefinito cresce poco più che linearmente.
3. I tempi variano tra un'esecuzione e l'altra: ricaricare la pagina tre volte e considerare il valore mediano. La prima misura (n = 1000) può risultare anomala, anche più lenta della seconda: nelle prime esecuzioni il motore JavaScript interpreta il codice e solo dopo lo compila con il compilatore JIT (modulo 1, sezione 1.1.3).
4. Registrare il lavoro con un commit Git (lezione 1.2).

### Esercizi

1. Aggiungere a `selectionSort` un contatore dei confronti e verificare che per n = 1000 valga 499 500.
2. Eseguire il selection sort su un array già ordinato: il numero di confronti cambia? E il tempo?
3. Ricerca: consultare su VisuAlgo il funzionamento di insertion sort e confrontare il numero di confronti su un array quasi ordinato.

## 2.4.5 Aspetti orientativi (discussione)

- La progettazione e l'analisi degli algoritmi sono il nucleo dei corsi universitari di informatica e ingegneria informatica (insegnamenti "Algoritmi e strutture dati").
- Nei colloqui tecnici per sviluppatori sono frequenti esercizi su algoritmi e sul loro costo.
- Nel lavoro quotidiano raramente si scrive un algoritmo di ordinamento: si usano quelli delle librerie. Serve però saper scegliere lo strumento adatto e riconoscere quando un programma è lento per un algoritmo di costo troppo alto.
- Domande per il dibattito: quali servizi usati ogni giorno (motori di ricerca, navigatori, social network) dipendono da algoritmi efficienti? Che cosa accadrebbe con algoritmi di costo quadratico su miliardi di dati?
