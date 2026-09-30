# Lista di controllo per la revisione del codice

> Adattamento dalla sezione "What to look for in a code review" di Google, "Engineering Practices Documentation", https://google.github.io/eng-practices/review/reviewer/looking-for.html , licenza Creative Commons Attribuzione 3.0 (CC BY 3.0). Traduzione, sintesi e adattamento al progetto del corso; il documento adattato è distribuito con licenza CC BY 3.0.

Ramo rivisto: ...

Autore della modifica: ...

Revisore: ...

Storia: US-...

## Che cosa guardare

| Aspetto | Domanda | Sì / No / Note |
|---|---|---|
| Progettazione | La modifica è nel modulo giusto (regole in `logica.py`, file in `archivio.py`, comandi in `prenotazioni.py`)? | |
| Funzionalità | Fa ciò che chiede la storia? Ho provato almeno un criterio di accettazione? Ci sono casi limite non gestiti? | |
| Complessità | Si capisce leggendola una volta? C'è una parte che si potrebbe scrivere più semplice? | |
| Test | Ci sono test per i criteri di accettazione? Fallirebbero se il codice fosse sbagliato? | |
| Nomi | Nomi di variabili e funzioni chiari, in italiano come il resto del progetto? | |
| Commenti | I commenti spiegano il perché, non ripetono il codice? | |
| Stile e coerenza | Lo stile è coerente con il resto del kit (rientri, lunghezza delle righe, docstring, modo di gestire gli errori)? | |
| Documentazione | README, manuale o CHANGELOG sono aggiornati se serve? | |

## Riscontri

[Forma: fatto, effetto, proposta (lezione 1.2). Distinguere ciò che va corretto da ciò che è un suggerimento facoltativo.]

- Da correggere: ...
- Suggerimenti: ...
- Cose fatte bene: ...

## Esito

- [ ] approvata: si può integrare in main
- [ ] da rivedere dopo le correzioni

Regole per chi rivede: la revisione riguarda il codice, non la persona; ogni osservazione ha una motivazione; l'obiettivo è che il codice del progetto migliori, non che sia perfetto.
