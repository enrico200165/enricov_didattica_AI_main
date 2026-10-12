---
title: "Scheda L13 - Un classificatore di immagini con Teachable Machine"
subtitle: "B.6 - Data science e Machine Learning"
lang: it
---

# Scheda L13 - Un classificatore di immagini con Teachable Machine

Gruppo: ______________________

Strumento: Teachable Machine, https://teachablemachine.withgoogle.com/ (Get Started, Image Project, Standard image model)

Regole: si fotografano solo oggetti, mai volti o persone; nessuna immagine viene salvata fuori dal PC senza il permesso del docente.

## 1. Scelta delle classi

Tre oggetti di uso comune, di forma o colore diversi (per esempio: una penna, una gomma, una tazza).

| classe | oggetto |
|---|---|
| Class 1 | |
| Class 2 | |
| Class 3 | |

## 2. Primo dataset (dataset "facile")

- per ogni classe tenere premuto "Hold to Record" per circa 5 secondi (30-60 immagini), sempre con lo stesso sfondo, la stessa luce, l'oggetto al centro
- Train Model; al termine provare il modello nella finestra Preview

Numero di immagini per classe: ______ / ______ / ______

## 3. Prove in condizioni diverse

Per ogni prova annotare la classe prevista e la percentuale mostrata per la classe corretta.

| prova | condizione | classe prevista | % classe corretta |
|---|---|---|---|
| 1 | stesso sfondo, stessa luce | | |
| 2 | sfondo diverso (foglio colorato, parete) | | |
| 3 | luce diversa (lampada spenta, controluce) | | |
| 4 | oggetto ruotato o inclinato | | |
| 5 | oggetto lontano o in un angolo dell'inquadratura | | |
| 6 | un oggetto nuovo, di nessuna delle tre classi | | |
| 7 | nessun oggetto (solo lo sfondo) | | |

Che cosa si osserva nelle prove 6 e 7? Perché il modello sceglie comunque una delle tre classi?

______________________________________________________________

## 4. La scorciatoia

Esperimento: registrare la classe 1 su uno sfondo bianco e le classi 2 e 3 su uno sfondo scuro. Addestrare e mostrare l'oggetto della classe 2 su sfondo bianco.

Risultato: ______________________________________________________________

Che cosa ha imparato davvero il modello?

______________________________________________________________

## 5. Secondo dataset (dataset "vario")

Registrare di nuovo le tre classi variando sfondo, luce, posizione, distanza e inclinazione, con un numero simile di immagini per classe. Ripetere le prove del punto 3.

| prova | % classe corretta, dataset facile | % classe corretta, dataset vario |
|---|---|---|
| 2 sfondo | | |
| 3 luce | | |
| 4 rotazione | | |
| 5 distanza | | |

Conclusione: ______________________________________________________________

## 6. Approfondimento

- Advanced: variare Epochs (epoche) e osservare "Under the hood" (curve di accuratezza e di perdita). Quale parte delle immagini usa Teachable Machine per la verifica?
- Sbilanciamento: registrare 200 immagini per la classe 1 e 20 per le altre. Che cosa cambia?
