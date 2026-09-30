"""Controlla la forma delle storie utente del backlog.

Uso:
    python controlla_storie.py docs\\backlog.md

Il file ha la struttura del backlog del kit: una tabella di riepilogo con le
righe "| US-NN | Titolo | Priorità | Stima | Stato |" e una sezione per ogni
storia, con titolo "### US-NN Titolo", il testo "Come ... voglio ... per ..."
e i criteri di accettazione come elenco "- Dato ..., quando ..., allora ...".

Il programma controlla la forma; se una storia ha valore per il cliente, o se
è abbastanza piccola, lo decidono il team e il Product Owner.
"""

import re
import sys

RIGA_TABELLA = re.compile(r"^\|\s*(US-\d{2})\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
TITOLO_STORIA = re.compile(r"^###\s+(US-\d{2})\s+(.+?)\s*$")
FORMATO_STORIA = re.compile(r"\bcome\b.+\bvoglio\b.+\bper\b", re.IGNORECASE)
INIZIO_CRITERIO = re.compile(r"^-\s*(dato|data|dati|date)\b", re.IGNORECASE)
PAROLE_VAGHE = ["veloce", "velocemente", "facile", "facili", "semplice", "intuitivo",
                "adeguato", "corretto", "correttamente", "bene", "circa", "ecc"]
MAX_PAROLE_STORIA = 35
MAX_CRITERI = 6


def leggi_backlog(testo):
    """Restituisce (tabella, storie).

    tabella: {id: (titolo, priorita, stima, stato)}, con l'elenco degli id ripetuti
    storie: {id: {"titolo", "testo", "criteri", "da_scrivere"}}
    """
    tabella, ripetuti, storie, corrente = {}, [], {}, None
    for riga in testo.splitlines():
        trovata = RIGA_TABELLA.match(riga)
        if trovata:
            codice = trovata.group(1)
            if codice in tabella:
                ripetuti.append(codice)
            tabella[codice] = trovata.groups()[1:]
            continue
        titolo = TITOLO_STORIA.match(riga)
        if titolo:
            codice = titolo.group(1)
            if codice in storie:
                ripetuti.append(codice)
            corrente = storie[codice] = {"titolo": titolo.group(2), "testo": "",
                                         "criteri": [], "da_scrivere": False}
            continue
        if riga.startswith("#"):
            corrente = None                      # un titolo diverso chiude la storia
            continue
        if corrente is None or not riga.strip():
            continue
        if riga.lstrip().startswith("-"):
            corrente["criteri"].append(riga.strip())
        elif riga.lower().startswith("criteri di accettazione"):
            if "da scrivere" in riga.lower():
                corrente["da_scrivere"] = True
        elif not corrente["testo"]:
            corrente["testo"] = riga.strip()
    return tabella, ripetuti, storie


def controlla_criterio(criterio):
    """Restituisce l'elenco dei problemi di un singolo criterio."""
    problemi = []
    if not INIZIO_CRITERIO.match(criterio):
        problemi.append("non inizia con \"Dato\"")
    minuscolo = criterio.lower()
    for parola in ("quando", "allora"):
        if not re.search(r"\b" + parola + r"\b", minuscolo):
            problemi.append(f"manca \"{parola}\"")
    vaghe = [p for p in PAROLE_VAGHE if re.search(r"(?<!\w)" + p + r"(?!\w)", minuscolo)]
    if vaghe:
        problemi.append("parole vaghe: " + ", ".join(vaghe))
    return problemi


def controlla(testo):
    """Restituisce l'elenco dei problemi, ciascuno come (id, livello, messaggio)."""
    tabella, ripetuti, storie = leggi_backlog(testo)
    problemi = [(c, "DA SISTEMARE", "codice ripetuto") for c in sorted(set(ripetuti))]
    for codice, (titolo, _, _, stato) in tabella.items():
        if codice not in storie and "kit" not in stato:
            problemi.append((codice, "DA SISTEMARE", "presente nella tabella ma senza sezione"))
    for codice in storie:
        if codice not in tabella:
            problemi.append((codice, "DA SISTEMARE", "sezione senza riga nella tabella di riepilogo"))

    for codice, s in storie.items():
        if codice in tabella and tabella[codice][0] != s["titolo"]:
            problemi.append((codice, "ATTENZIONE", "titolo diverso tra tabella e sezione"))
        if not FORMATO_STORIA.search(s["testo"]):
            problemi.append((codice, "DA SISTEMARE", "manca il testo nella forma \"Come ... voglio ... per ...\""))
        parole = len(s["testo"].split())
        if parole > MAX_PAROLE_STORIA:
            problemi.append((codice, "ATTENZIONE", f"storia lunga ({parole} parole): valutare se dividerla"))
        if s["da_scrivere"] or not s["criteri"]:
            problemi.append((codice, "DA SISTEMARE", "criteri di accettazione da scrivere"))
            continue
        if len(s["criteri"]) < 2:
            problemi.append((codice, "ATTENZIONE", "un solo criterio: manca un caso limite o di errore?"))
        if len(s["criteri"]) > MAX_CRITERI:
            problemi.append((codice, "ATTENZIONE", f"{len(s['criteri'])} criteri: valutare se dividere la storia"))
        for n, criterio in enumerate(s["criteri"], start=1):
            for p in controlla_criterio(criterio):
                problemi.append((codice, "DA SISTEMARE", f"criterio {n}: {p}"))
    return problemi


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Uso: python controlla_storie.py docs\\backlog.md")
        return 2
    try:
        with open(argv[0], encoding="utf-8") as f:
            testo = f.read()
    except OSError as e:
        print(f"Impossibile leggere il file: {e}")
        return 2
    _, _, storie = leggi_backlog(testo)
    problemi = controlla(testo)
    for codice, livello, messaggio in sorted(problemi):
        print(f"{codice}  {livello}: {messaggio}")
    con_problemi = {c for c, livello, _ in problemi if livello == "DA SISTEMARE"}
    print(f"\nStorie: {len(storie)}; pronte: {len(set(storie) - con_problemi)}; "
          f"da sistemare: {len(con_problemi & set(storie))}")
    return 0 if not con_problemi else 1


if __name__ == "__main__":
    sys.exit(main())
