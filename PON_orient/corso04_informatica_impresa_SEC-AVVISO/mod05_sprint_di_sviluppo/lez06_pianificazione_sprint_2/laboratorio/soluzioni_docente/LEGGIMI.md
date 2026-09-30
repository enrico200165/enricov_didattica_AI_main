# Soluzione di riferimento: prenotare per ore di lezione (US-16)

Materiale per il docente, da non distribuire prima della revisione dello sprint 2.

## Analisi di impatto (esempio)

- **Storia**: US-16. Come docente voglio prenotare indicando la prima e l'ultima ora di lezione, per non dover tradurre le ore in orari.
- **Criteri**:
  - Dato l'orario della scuola, quando prenoto LAB-INF1 il 12/10 per le ore 2-3, allora la prenotazione va dalle 9:00 alle 11:00;
  - Dato l'orario della scuola, quando prenoto per la sola 4ª ora, allora la prenotazione va dalle 11:00 alle 12:00;
  - Dato l'orario della scuola, quando indico un'ora che non esiste (0, 11) o la prima dopo l'ultima, allora la prenotazione è rifiutata con un messaggio.
- **Impatto**: nuovo modulo (`ore_di_lezione.py`) e nuovo comando; `logica.py`, `archivio.py` e il formato dei dati **non cambiano**, perché le prenotazioni continuano a essere registrate con gli orari; manuale e CHANGELOG da aggiornare.
- **Stima indicativa**: 3 punti. Per fare spazio si rimandano in genere US-15 (statistiche) o US-11 (ricorrenze), come suggerisce il cliente.
- **Rischio principale**: due modi di prenotare possono confondere; il manuale deve spiegare quando usare l'uno o l'altro.

La scelta di non cambiare il formato dei dati è la decisione chiave: riduce l'impatto e non richiede di convertire le prenotazioni esistenti. È utile farla emergere nella discussione.

## Codice

`ore_di_lezione.py` e `test_ore_di_lezione.py` (6 test, eseguibili in questa cartella con `python -m unittest test_ore_di_lezione`).

Comando da aggiungere in `prenotazioni.py` (nella funzione `crea_parser` e nel dizionario `COMANDI`):

```python
import ore_di_lezione

    c = comandi.add_parser("prenota-ore", help="prenota per ore di lezione, per esempio 2-3 (US-16)")
    c.add_argument("aula")
    c.add_argument("giorno")
    c.add_argument("ore", help="prima e ultima ora, per esempio 2-3, oppure una sola ora")
    c.add_argument("richiedente")
    c.add_argument("--motivo", default="")


def comando_prenota_ore(argomenti):
    try:
        inizio, fine = ore_di_lezione.orari_da_ore(argomenti.ore)
    except ore_di_lezione.ErroreOre as e:
        raise logica.ErrorePrenotazione(str(e)) from None
    argomenti.inizio, argomenti.fine = inizio, fine
    comando_prenota(argomenti)
```

- l'errore del nuovo modulo viene trasformato in `ErrorePrenotazione`, così `main` lo mostra come gli altri errori
- `comando_prenota` viene riusato: controlli, salvataggio e conferma sono gli stessi della prenotazione per orari
