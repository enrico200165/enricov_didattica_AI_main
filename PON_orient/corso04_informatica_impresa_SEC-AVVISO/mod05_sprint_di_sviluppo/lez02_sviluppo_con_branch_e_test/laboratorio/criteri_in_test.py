"""Crea lo scheletro dei test di una storia a partire dai suoi criteri di accettazione.

Uso, nella cartella del repository del team:
    python criteri_in_test.py docs\\backlog.md US-01
    python criteri_in_test.py docs\\backlog.md US-01 --uscita tests\\test_us01.py

Per ogni criterio "Dato ..., quando ..., allora ..." il programma scrive un metodo
di test con il criterio come docstring e tre commenti (Dato, Quando, Allora) da
completare con il codice. Ogni test fallisce finché non viene scritto: è il punto
di partenza dello sviluppo guidato dai test.
"""

import argparse
import re
import sys
from pathlib import Path

TITOLO = re.compile(r"^###\s+(US-\d{2}[a-z]?)\s+(.+?)\s*$")
CRITERIO = re.compile(r"^-\s*((?:dato|data|dati|date)\b.*?),\s*(quando\b.*?),\s*(allora\b.*)$", re.IGNORECASE)


class ErroreStoria(Exception):
    """Storia non trovata o senza criteri."""


def criteri_della_storia(testo, codice):
    """Restituisce (titolo, elenco di (dato, quando, allora)) della storia indicata."""
    titolo, criteri, dentro = None, [], False
    for riga in testo.splitlines():
        trovato = TITOLO.match(riga)
        if trovato:
            dentro = trovato.group(1) == codice
            if dentro:
                titolo = trovato.group(2)
            continue
        if riga.startswith("#"):
            dentro = False
        elif dentro:
            parti = CRITERIO.match(riga.strip())
            if parti:
                criteri.append(tuple(p.strip() for p in parti.groups()))
    if titolo is None:
        raise ErroreStoria(f"la storia {codice} non ha una sezione nel backlog")
    if not criteri:
        raise ErroreStoria(f"la storia {codice} non ha criteri nella forma \"- Dato ..., quando ..., allora ...\"")
    return titolo, criteri


def per_docstring(testo):
    """Rende il testo sicuro dentro una docstring tra tre virgolette doppie."""
    testo = testo.replace("\\", "\\\\").replace('"', "'")
    return testo


def scheletro(codice, titolo, criteri):
    nome_classe = "Test" + codice.replace("-", "")
    righe = [f'"""Test della storia {codice}: {titolo}.', "",
             "Generato da criteri_in_test.py: ogni test corrisponde a un criterio di accettazione.",
             "Completare ogni test: Dato = preparare i dati, Quando = chiamare la funzione,",
             "Allora = controllare il risultato con self.assert...", '"""', "",
             "import unittest", "", "import logica", "", "",
             f"class {nome_classe}(unittest.TestCase):", ""]
    for n, (dato, quando, allora) in enumerate(criteri, start=1):
        righe += [f"    def test_criterio_{n}(self):",
                  f'        """{per_docstring(dato + ", " + quando + ", " + allora)}"""',
                  f"        # {dato}",
                  f"        # {quando}",
                  f"        # {allora}",
                  '        self.fail("test da scrivere")', ""]
    righe += ["", 'if __name__ == "__main__":', "    unittest.main()", ""]
    return "\n".join(righe)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Scheletro dei test di una storia")
    parser.add_argument("backlog")
    parser.add_argument("storia", help="codice della storia, per esempio US-01")
    parser.add_argument("--uscita", help="file da scrivere (predefinito: tests/test_usNN.py)")
    argomenti = parser.parse_args(argv)
    codice = argomenti.storia.upper()
    try:
        titolo, criteri = criteri_della_storia(Path(argomenti.backlog).read_text(encoding="utf-8"), codice)
    except (ErroreStoria, OSError) as e:
        print(f"Errore: {e}")
        return 1
    uscita = Path(argomenti.uscita or f"tests/test_{codice.lower().replace('-', '')}.py")
    if uscita.exists():
        print(f"Errore: {uscita} esiste già; il programma non sovrascrive i test")
        return 1
    uscita.parent.mkdir(parents=True, exist_ok=True)
    uscita.write_text(scheletro(codice, titolo, criteri), encoding="utf-8")
    print(f"Scritti {len(criteri)} test da completare in {uscita}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
