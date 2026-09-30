"""Lettura e scrittura dei dati nei file JSON della cartella dati."""

import json
import os
from pathlib import Path

CARTELLA_DATI = Path(__file__).parent / "dati"


class ErroreArchivio(Exception):
    """Errore nella lettura o nella scrittura dei file di dati."""


def _leggi_json(percorso):
    try:
        with open(percorso, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ErroreArchivio(f"il file {percorso} non è un JSON valido (riga {e.lineno})") from None


def carica_aule(cartella=CARTELLA_DATI):
    """Restituisce l'elenco delle aule letto da aule.json."""
    percorso = Path(cartella) / "aule.json"
    if not percorso.exists():
        raise ErroreArchivio(f"manca il file {percorso}")
    return _leggi_json(percorso)


def carica_prenotazioni(cartella=CARTELLA_DATI):
    """Restituisce l'elenco delle prenotazioni; se il file non esiste, un elenco vuoto."""
    percorso = Path(cartella) / "prenotazioni.json"
    if not percorso.exists():
        return []
    return _leggi_json(percorso)


def salva_prenotazioni(prenotazioni, cartella=CARTELLA_DATI):
    """Scrive le prenotazioni in prenotazioni.json.

    Scrive prima un file temporaneo e poi lo rinomina: se il programma si
    interrompe a metà, il file precedente resta intatto.
    """
    percorso = Path(cartella) / "prenotazioni.json"
    temporaneo = percorso.with_suffix(".tmp")
    with open(temporaneo, "w", encoding="utf-8") as f:
        json.dump(prenotazioni, f, indent=2)
        f.write("\n")
    os.replace(temporaneo, percorso)
