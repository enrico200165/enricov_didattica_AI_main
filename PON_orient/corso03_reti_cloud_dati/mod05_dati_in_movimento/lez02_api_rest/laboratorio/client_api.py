"""Client per due API pubbliche gratuite e senza chiave.

- Open Library (Internet Archive): ricerca di libri, https://openlibrary.org/developers/api
- Open-Meteo: meteo attuale di una località, https://open-meteo.com (dati con licenza CC BY 4.0)

Uso:
    python client_api.py libri "il barone rampante"
    python client_api.py meteo 41.89 12.49
Le API pubbliche chiedono un uso moderato: al massimo una richiesta al secondo.
"""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

OPEN_LIBRARY = "https://openlibrary.org"
OPEN_METEO = "https://api.open-meteo.com"
# Open Library chiede di identificare l'applicazione con l'intestazione User-Agent
USER_AGENT = "CorsoRetiScuola/1.0 (esercitazione didattica)"
_ultima_richiesta = 0.0


def richiesta_json(url, parametri, timeout=10):
    """GET con parametri nell'URL; restituisce (codice di stato, dati JSON decodificati)."""
    global _ultima_richiesta
    attesa = 1.0 - (time.monotonic() - _ultima_richiesta)
    if attesa > 0:
        time.sleep(attesa)                              # non più di una richiesta al secondo
    indirizzo = url + "?" + urllib.parse.urlencode(parametri)   # codifica spazi e caratteri speciali
    richiesta = urllib.request.Request(indirizzo, headers={"User-Agent": USER_AGENT,
                                                           "Accept": "application/json"})
    _ultima_richiesta = time.monotonic()
    try:
        with urllib.request.urlopen(richiesta, timeout=timeout) as risposta:
            return risposta.status, json.loads(risposta.read().decode("utf-8"))
    except urllib.error.HTTPError as errore:            # risposta ricevuta, ma con codice 4xx o 5xx
        corpo = errore.read().decode("utf-8", errors="replace")
        try:
            return errore.code, json.loads(corpo)
        except json.JSONDecodeError:
            return errore.code, {"errore": corpo[:200]}


def cerca_libri(testo, limite=5, base=None):
    """Titolo, autori e anno di prima pubblicazione dei libri trovati."""
    base = base or OPEN_LIBRARY                          # indirizzo sostituibile, per esempio nei test
    stato, dati = richiesta_json(base + "/search.json",
                                 {"q": testo, "limit": limite,
                                  "fields": "title,author_name,first_publish_year"})
    if stato != 200:
        raise RuntimeError(f"Open Library ha risposto {stato}")
    return [(d.get("title"), ", ".join(d.get("author_name", [])), d.get("first_publish_year"))
            for d in dati.get("docs", [])]               # .get: alcuni campi possono mancare


def meteo_attuale(latitudine, longitudine, base=None):
    """Temperatura e vento attuali, con le unità di misura indicate dalla risposta."""
    base = base or OPEN_METEO
    stato, dati = richiesta_json(base + "/v1/forecast",
                                 {"latitude": latitudine, "longitude": longitudine,
                                  "current": "temperature_2m,wind_speed_10m", "timezone": "Europe/Rome"})
    if stato != 200:
        raise RuntimeError(f"Open-Meteo ha risposto {stato}: {dati.get('reason', dati)}")
    attuale, unita = dati["current"], dati["current_units"]
    return {"ora": attuale["time"],
            "temperatura": f"{attuale['temperature_2m']} {unita['temperature_2m']}",
            "vento": f"{attuale['wind_speed_10m']} {unita['wind_speed_10m']}"}


def main(argomenti):
    try:
        if len(argomenti) == 2 and argomenti[0] == "libri":
            for titolo, autori, anno in cerca_libri(argomenti[1]):
                print(f"{anno or '----'}  {titolo}  ({autori or 'autore non indicato'})")
        elif len(argomenti) == 3 and argomenti[0] == "meteo":
            for chiave, valore in meteo_attuale(float(argomenti[1]), float(argomenti[2])).items():
                print(f"{chiave:<12}{valore}")
        else:
            print(__doc__)
    except (urllib.error.URLError, TimeoutError) as errore:
        print("Servizio non raggiungibile:", errore)    # rete assente, nome inesistente, tempo scaduto
    except RuntimeError as errore:
        print("Errore:", errore)


if __name__ == "__main__":
    main(sys.argv[1:])
