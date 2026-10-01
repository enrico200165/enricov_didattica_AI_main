"""Controlla una bozza di CV in Markdown e la confronta con un annuncio.

Uso:
    python cv_e_annuncio.py controlla cv.md
    python cv_e_annuncio.py annuncio annuncio.md cv.md

controlla: verifica le sezioni, le parti da completare, i dati personali non
necessari, le espressioni generiche e la lunghezza.

annuncio: per ogni requisito dell'annuncio (le righe di elenco sotto un titolo
che contiene "Requisiti") cerca nel CV le parole chiave del requisito e indica
quali requisiti il CV mostra e quali no. Il confronto è sulle parole: serve a
non dimenticare ciò che si sa fare, non a dichiarare ciò che non si sa fare.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

SEZIONI = {
    "contatti": ("contatti", "informazioni personali"),
    "istruzione": ("istruzione",),
    "esperienze": ("esperienz", "progett"),
    "competenze": ("competenz",),
    "lingue": ("lingu",),
}
DATI_NON_NECESSARI = [
    (r"\b\d{1,2}[/.-]\d{1,2}[/.-](19|20)\d{2}\b|\bnat[oa] il\b", "data di nascita"),
    (r"\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b", "codice fiscale"),
    (r"\bstato civile\b|\bcelibe\b|\bnubile\b", "stato civile"),
    (r"!\[", "fotografia"),
]
GENERICHE = ["buone capacità", "ottime capacità", "predisposizione", "dinamico", "dinamica",
             "solare", "volenteroso", "volenterosa", "capacità di lavorare in team"]
PAROLE_VUOTE = {"della", "delle", "degli", "dello", "nella", "nelle", "negli", "anche", "come", "con", "per",
                "almeno", "buona", "buone", "base", "conoscenza", "capacità", "uso", "utilizzo", "esperienza",
                "anni", "anno", "preferibile", "gradita", "gradito", "richiesta", "richiesto", "lavoro",
                "lavorare", "propri", "proprie", "proprio", "sono", "essere", "avere"}
MASSIMO_PAROLE = 600
RADICE = 5          # lettere iniziali confrontate: "testare" e "test" non coincidono, "programmazione" e "programmare" sì


def normalizza(testo):
    """Minuscole e senza accenti, per confrontare parole scritte in modi diversi."""
    senza_accenti = unicodedata.normalize("NFD", testo.lower())
    return "".join(c for c in senza_accenti if unicodedata.category(c) != "Mn")


def titoli(testo):
    return [normalizza(r.lstrip("#").strip()) for r in testo.splitlines() if r.startswith("#")]


def controlla_cv(testo):
    problemi = []
    presenti = titoli(testo)
    for nome, inizi in SEZIONI.items():
        if not any(any(i in t for i in inizi) for t in presenti):
            problemi.append(("DA SISTEMARE", f"manca la sezione \"{nome}\""))
    if "..." in testo:
        problemi.append(("DA SISTEMARE", "ci sono ancora parti da completare (\"...\")"))
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", testo):
        problemi.append(("DA SISTEMARE", "manca un indirizzo e-mail"))
    for modello, dato in DATI_NON_NECESSARI:
        if re.search(modello, testo, flags=re.IGNORECASE if dato != "codice fiscale" else 0):
            problemi.append(("ATTENZIONE", f"{dato}: non serve nel CV; si indica solo se l'annuncio lo chiede"))
    minuscolo = testo.lower()
    for espressione in GENERICHE:
        if re.search(r"\b" + re.escape(espressione) + r"\b", minuscolo):
            problemi.append(("ATTENZIONE", f"espressione generica \"{espressione}\": meglio un fatto "
                             "(che cosa, dove, con quale risultato)"))
    if "trattamento dei dati personali" not in minuscolo:
        problemi.append(("ATTENZIONE", "manca l'autorizzazione al trattamento dei dati personali, "
                         "che molti annunci in Italia chiedono"))
    parole = len(re.findall(r"\w+", testo))
    if parole > MASSIMO_PAROLE:
        problemi.append(("ATTENZIONE", f"{parole} parole: per un primo CV ne bastano {MASSIMO_PAROLE}"))
    return problemi


def requisiti(annuncio):
    """Righe di elenco sotto un titolo che contiene "requisiti"."""
    trovati, dentro = [], False
    for riga in annuncio.splitlines():
        if riga.startswith("#"):
            dentro = "requisiti" in normalizza(riga)
        elif dentro and riga.lstrip().startswith(("- ", "* ")):
            trovati.append(riga.lstrip()[2:].strip())
    return trovati


def parole_chiave(testo):
    parole = re.findall(r"[a-z0-9+#]+", normalizza(testo))
    return [p for p in parole if (len(p) >= 4 or p in ("git", "sql", "c++", "c#", "web", "ict")) and p not in PAROLE_VUOTE]


def copertura(requisito, testo_cv):
    """(parole chiave trovate, parole chiave mancanti) di un requisito nel CV."""
    radici_cv = {p[:RADICE] for p in re.findall(r"[a-z0-9+#]+", normalizza(testo_cv))}
    chiavi = parole_chiave(requisito)
    trovate = [c for c in chiavi if c[:RADICE] in radici_cv]
    return trovate, [c for c in chiavi if c not in trovate]


def confronta(annuncio, testo_cv):
    risultati = []
    for r in requisiti(annuncio):
        trovate, mancanti = copertura(r, testo_cv)
        coperto = bool(trovate) and len(trovate) >= len(mancanti)
        risultati.append((r, coperto, mancanti))
    return risultati


def main(argv=None):
    parser = argparse.ArgumentParser(description="Bozza di CV: controlli e confronto con un annuncio")
    sotto = parser.add_subparsers(dest="comando", required=True)
    sotto.add_parser("controlla").add_argument("cv")
    p = sotto.add_parser("annuncio")
    p.add_argument("annuncio")
    p.add_argument("cv")
    argomenti = parser.parse_args(argv)
    try:
        testo_cv = Path(argomenti.cv).read_text(encoding="utf-8")
        testo_annuncio = Path(argomenti.annuncio).read_text(encoding="utf-8") if argomenti.comando == "annuncio" else ""
    except OSError as e:
        print(f"Errore: {e}")
        return 1
    if argomenti.comando == "controlla":
        problemi = controlla_cv(testo_cv)
        for livello, messaggio in problemi:
            print(f"{livello}: {messaggio}")
        da_sistemare = sum(1 for livello, _ in problemi if livello == "DA SISTEMARE")
        print(f"\nDa sistemare: {da_sistemare}; attenzione: {len(problemi) - da_sistemare}")
        return 0
    risultati = confronta(testo_annuncio, testo_cv)
    if not risultati:
        print("Nessun requisito trovato: l'annuncio deve avere un titolo con \"Requisiti\" e un elenco.")
        return 1
    for requisito, coperto, mancanti in risultati:
        stato = "presente " if coperto else "DA VERIFICARE"
        nota = f"  (non trovate: {', '.join(mancanti)})" if mancanti and not coperto else ""
        print(f"{stato:<14}{requisito}{nota}")
    coperti = sum(1 for _, c, _ in risultati if c)
    print(f"\nRequisiti presenti nel CV: {coperti} su {len(risultati)}")
    print("Per ogni requisito da verificare: se lo si possiede, scriverlo nel CV con un esempio; se no, "
          "prepararsi a dire come lo si sta imparando.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
