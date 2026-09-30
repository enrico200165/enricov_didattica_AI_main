---
title: "Scheda L16-L18 - Il progetto finale"
subtitle: "B.6 - Data science e Machine Learning"
lang: it
---

# Scheda L16-L18 - Il progetto finale

Gruppo: ______________________

## Scenari

1. Dataset della classe (tragitti): prevedere il mezzo di trasporto oppure il tempo di tragitto.
2. Vini italiani: riconoscere il vitigno (tre classi) da 13 misure chimiche. Dataset "Wine" dell'UCI Machine Learning Repository, licenza CC BY 4.0, incluso in scikit-learn e quindi disponibile anche offline (`from sklearn.datasets import load_wine`). https://archive.ics.uci.edu/dataset/109/wine
3. Dataset aperto a scelta del gruppo, da dati.gov.it o dall'UCI Machine Learning Repository, approvato dal docente (licenza verificata, dimensione adatta, nessun dato personale identificativo).
4. Immagini con Teachable Machine: un classificatore di oggetti con analisi sistematica di varietà, bilanciamento e scorciatoie; il "notebook" è sostituito da una relazione con tabelle delle prove.

Scenario scelto: ______________________

## Fasi e tempi

| lezione | fase | prodotto |
|---|---|---|
| L16 (55 min) | domanda, dati, dizionario, pulizia, esplorazione | sezioni 1-4 del notebook |
| L17 (55 min) | baseline, modelli, validazione incrociata, valutazione finale, errori, limiti, conclusioni | sezioni 5-8; presentazione |
| L18 (35 min) | presentazione di 5 minuti e domande | presentazione |

Modello del notebook: `L16_progetto_modello.ipynb`. Esempio completo: `L16_progetto_esempio.ipynb`.

## Ruoli (a rotazione tra L16 e L17)

- responsabile dei dati: pulizia e registro
- responsabile del modello: codice dei modelli e della valutazione
- responsabile della comunicazione: grafici, commenti, presentazione
- revisore: controlla la lista di verifica metodologica

## Lista di verifica metodologica

- [ ] la domanda è chiara e il tipo di problema è indicato
- [ ] fonte e licenza dei dati sono indicate
- [ ] il dizionario dei dati è presente
- [ ] ogni operazione di pulizia è nel registro
- [ ] almeno tre grafici, ciascuno commentato
- [ ] l'insieme di verifica è separato prima di scegliere modelli e iperparametri
- [ ] è presente una baseline
- [ ] almeno due modelli sono confrontati con la validazione incrociata sui dati di addestramento
- [ ] la verifica finale è calcolata una sola volta
- [ ] la metrica è adatta al problema (classi sbilanciate? costo degli errori?)
- [ ] gli errori sono analizzati con esempi
- [ ] nessuna caratteristica contiene la risposta (fuga di informazione)
- [ ] le prestazioni sono valutate per gruppo, se ci sono gruppi rilevanti
- [ ] limiti e usi sconsigliati sono dichiarati
- [ ] il notebook funziona con "Restart Kernel and Run All Cells"

## Presentazione (5 minuti)

1. la domanda e perché interessa (30 secondi)
2. i dati: da dove vengono, che cosa è stato pulito (1 minuto)
3. un grafico esplorativo significativo (1 minuto)
4. il modello scelto e il confronto con la baseline (1 minuto)
5. un errore interessante e un limite (1 minuto)
6. la risposta alla domanda, in una frase (30 secondi)

## Scheda per le domande tra gruppi

Gruppo osservato: ______________________

- Una cosa convincente del progetto: ______________________________________________
- Una domanda sul metodo (dati, valutazione, limiti): ______________________________________________
