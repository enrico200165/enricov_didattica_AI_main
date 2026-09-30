"""Regole dell'applicazione: aule e prenotazioni.

Versione con le storie US-01, US-02 e US-03 (soluzione di riferimento per il docente).

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
        if aula["codice"] == codice.strip().upper():
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


def si_sovrappongono(inizio1, fine1, inizio2, fine2):
    """Vero se due intervalli di tempo hanno una parte in comune.

    Due intervalli che si toccano soltanto (uno finisce quando l'altro inizia)
    non si sovrappongono (US-01, secondo criterio).
    """
    return inizio1 < fine2 and inizio2 < fine1


def prenotazione_in_conflitto(prenotazioni, codice_aula, giorno, inizio, fine):
    """Restituisce la prima prenotazione della stessa aula e dello stesso giorno che si sovrappone, o None."""
    for p in prenotazioni:
        if (p["aula"] == codice_aula and p["giorno"] == giorno.isoformat()
                and si_sovrappongono(inizio, fine, leggi_ora(p["inizio"]), leggi_ora(p["fine"]))):
            return p
    return None


def nuova_prenotazione(prenotazioni, aule, codice_aula, giorno, inizio, fine,
                       richiedente, motivo=""):
    """Controlla i dati, aggiunge la prenotazione all'elenco e la restituisce."""
    aula = cerca_aula(aule, codice_aula)
    g = leggi_data(giorno)
    ora_inizio = leggi_ora(inizio)
    ora_fine = leggi_ora(fine)
    if ora_inizio >= ora_fine:
        raise ErrorePrenotazione("l'orario di fine deve essere successivo a quello di inizio")
    if ora_inizio < APERTURA or ora_fine > CHIUSURA:
        raise ErrorePrenotazione(
            f"la scuola è aperta dalle {APERTURA:%H:%M} alle {CHIUSURA:%H:%M}")
    if not richiedente.strip():
        raise ErrorePrenotazione("indicare chi prenota")
    esistente = prenotazione_in_conflitto(prenotazioni, aula["codice"], g, ora_inizio, ora_fine)
    if esistente:                                                        # US-01
        raise ErrorePrenotazione(
            f"{aula['codice']} è già prenotato dalle {esistente['inizio']} alle {esistente['fine']} "
            f"(prenotazione {esistente['id']}, {esistente['richiedente']})")

    nuovo_id = max((p["id"] for p in prenotazioni), default=0) + 1
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


def prenotazioni_del_giorno(prenotazioni, giorno):
    """Prenotazioni di un giorno, ordinate per aula e ora di inizio (US-02)."""
    g = leggi_data(giorno).isoformat()
    return sorted((p for p in prenotazioni if p["giorno"] == g),
                  key=lambda p: (p["aula"], p["inizio"]))


def cancella_prenotazione(prenotazioni, numero, richiedente):
    """Toglie dall'elenco la prenotazione indicata e la restituisce (US-03).

    Solo chi ha prenotato può cancellare; il confronto dei nomi ignora maiuscole e spazi.
    """
    for i, p in enumerate(prenotazioni):
        if p["id"] == numero:
            if p["richiedente"].strip().lower() != richiedente.strip().lower():
                raise ErrorePrenotazione(
                    f"la prenotazione {numero} è di {p['richiedente']}: solo chi ha prenotato può cancellarla")
            return prenotazioni.pop(i)
    raise ErrorePrenotazione(f"la prenotazione {numero} non esiste")
