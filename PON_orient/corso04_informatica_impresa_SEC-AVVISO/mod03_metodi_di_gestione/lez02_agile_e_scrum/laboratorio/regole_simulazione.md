# Simulazione di Scrum: la fabbrica di aeroplani di carta

Attività originale, ispirata ai numerosi giochi di simulazione usati nella formazione su Scrum.

## Obiettivo

Consegnare al cliente il maggior numero possibile di aeroplani di carta **accettati**, in tre sprint.

## Materiale

- fogli di carta di recupero (almeno 30 per team), penne
- un segno sul pavimento a 3 metri dalla linea di lancio
- orologio o timer visibile a tutti

## Ruoli

- **Cliente**: il docente. Definisce i criteri di accettazione e prova gli aeroplani nella revisione.
- **Product Owner**: parla con il cliente, chiarisce i criteri, decide che cosa chiedere al team.
- **Scrum Master**: tiene i tempi di ogni evento, fa rispettare le regole, annota i dati nel registro.
- **Sviluppatori**: tutti gli altri membri del team, compresi Product Owner e Scrum Master se il team è di 4.

## Criteri di accettazione (sprint 1 e 2)

Un aeroplano è accettato se:

- Dato un aeroplano del team, quando viene lanciato dalla linea, allora supera il segno dei 3 metri;
- Dato un aeroplano del team, quando il cliente lo guarda, allora ha il nome del team scritto su un'ala.

Nello sprint 3 il cliente può cambiare o aggiungere un criterio, comunicandolo solo nella pianificazione.

## Regole di produzione

- Ogni persona può fare al massimo **una piega alla volta** e poi passa l'aeroplano a un'altra persona: il lavoro è di squadra.
- Durante la produzione si può parlare solo all'interno del team.
- Gli aeroplani non terminati allo scadere del tempo non contano.

## Uno sprint (7 minuti)

| Evento | Durata | Che cosa si fa |
|---|---|---|
| Pianificazione | 1 minuto | il team stima quanti aeroplani produrrà; lo Scrum Master scrive il numero ("pianificati") |
| Produzione | 3 minuti | si producono gli aeroplani; nessuna prova di lancio |
| Revisione | 1 minuto e mezzo | il cliente lancia ogni aeroplano e controlla i criteri; si contano "realizzati" e "accettati" |
| Retrospettiva | 1 minuto e mezzo | che cosa ha funzionato? che cosa cambiamo nel prossimo sprint? Una sola azione di miglioramento |

Si svolgono tre sprint consecutivi.

## Registro

Lo Scrum Master annota i numeri in `sprint.csv` (modello: `sprint_esempio.csv`) e, alla fine, esegue:

```text
python registro_sprint.py sprint.csv
```

## Domande per la discussione finale

1. Il numero pianificato nello sprint 1 era realistico? Come è cambiata la stima negli sprint successivi?
2. Quale azione di miglioramento ha avuto più effetto?
3. Che cosa è successo quando il cliente ha cambiato un criterio nello sprint 3?
4. Quali eventi, ruoli o artefatti di Scrum si riconoscono nella simulazione? Quali mancano?
