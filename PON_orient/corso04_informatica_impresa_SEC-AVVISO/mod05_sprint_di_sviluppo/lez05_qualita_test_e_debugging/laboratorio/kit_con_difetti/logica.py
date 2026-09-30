"""Regole dell'applicazione: aule e prenotazioni.

Questo modulo non legge né scrive file e non stampa nulla: riceve dati e
restituisce risultati. Per questo si può provare facilmente con i test.
"""

from datetime import date, datetime, time

APERTURA = time(8, 0)    # la scuola apre alle 8:00
CHIUSURA = time(18, 0)   # e chiude alle 18:00


class ErrorePrenotazione(Exception):
    """Errore dovuto ai dati inseriti dall'utente, con un messaggio da mostrargli."""


def elenco_aule(aule, tipo=None):
    """Restituisce le aule ordinate per codice; con tipo, solo quelle di quel tipo."""
    scelte = [a for a in aule if tipo is None or a["tipo"] == tipo]
    return sorted(scelte, key=lambda a: a["codice"])


def cerca_aula(aule, codice):
    """Restituisce l'aula con il codice indicato (maiuscole o minuscole)."""
    for aula in aule:
        if aula["codice"] == codice.strip():
            return aula
    raise ErrorePrenotazione(f"l'aula {codice} non esiste")


def leggi_data(testo):
    """Converte una data AAAA-MM-GG, per esempio 2026-10-12, in un oggetto date."""
    try:
        return date.fromisoformat(testo.strip())
    except ValueError:
        raise ErrorePrenotazione(f"data non valida: {testo} (formato AAAA-MM-GG)") from None


def leggi_ora(testo):
    """Converte un orario HH:MM, per esempio 9:00 o 14:30, in un oggetto time."""
    try:
        return datetime.strptime(testo.strip(), "%H:%M").time()
    except ValueError:
        raise ErrorePrenotazione(f"orario non valido: {testo} (formato HH:MM)") from None


def nuova_prenotazione(prenotazioni, aule, codice_aula, giorno, inizio, fine,
                       richiedente, motivo=""):
    """Controlla i dati, aggiunge la prenotazione all'elenco e la restituisce."""
    aula = cerca_aula(aule, codice_aula)
    g = leggi_data(giorno)
    ora_inizio = leggi_ora(inizio)
    ora_fine = leggi_ora(fine)
    if ora_inizio >= ora_fine:
        raise ErrorePrenotazione("l'orario di fine deve essere successivo a quello di inizio")
    if ora_inizio < APERTURA or ora_fine >= CHIUSURA:
        raise ErrorePrenotazione(
            f"la scuola è aperta dalle {APERTURA:%H:%M} alle {CHIUSURA:%H:%M}")
    if not richiedente:
        raise ErrorePrenotazione("indicare chi prenota")

    nuovo_id = len(prenotazioni) + 1
    prenotazione = {
        "id": nuovo_id,
        "aula": aula["codice"],
        "giorno": g.isoformat(),
        "inizio": f"{ora_inizio:%H:%M}",
        "fine": f"{ora_fine:%H:%M}",
        "richiedente": richiedente.strip(),
        "motivo": motivo.strip(),
    }
    prenotazioni.append(prenotazione)
    return prenotazione
