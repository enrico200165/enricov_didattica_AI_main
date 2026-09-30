"""Test di copertura.py. Esecuzione: python test_copertura.py

La misura viene eseguita in un processo separato, per non mescolare i moduli dei progetti provati.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import copertura as c

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def esegui(cartella, *file):
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("copertura.py")), str(cartella), *file],
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout


verifica("intervalli di righe", c.intervalli([3, 4, 5, 9, 11, 12]) == "3-5, 9, 11-12" and c.intervalli([]) == "")

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    (d / "calcoli.py").write_text(
        '"""Modulo di prova."""\n\n\ndef segno(x):\n    if x > 0:\n        return "positivo"\n'
        '    if x < 0:\n        return "negativo"\n    return "zero"\n', encoding="utf-8")
    verifica("righe eseguibili: def, if, return; esclusa la riga vuota",
             {4, 5, 6, 7, 8, 9} <= c.righe_eseguibili(d / "calcoli.py") and 2 not in c.righe_eseguibili(d / "calcoli.py"))
    (d / "tests").mkdir()
    (d / "tests" / "__init__.py").write_text("", encoding="utf-8")
    (d / "tests" / "test_calcoli.py").write_text(
        "import unittest\nimport calcoli\n\n\nclass T(unittest.TestCase):\n    def test_positivo(self):\n"
        "        self.assertEqual(calcoli.segno(3), 'positivo')\n", encoding="utf-8")
    codice, testo = esegui(d, "calcoli.py")
    riga = [r for r in testo.splitlines() if r.startswith("calcoli.py")][0]
    verifica("un solo test: righe 7-9 mai eseguite", codice == 0 and riga.endswith("7-9"))
    (d / "tests" / "test_calcoli.py").write_text(
        (d / "tests" / "test_calcoli.py").read_text(encoding="utf-8") +
        "\n    def test_altri(self):\n        self.assertEqual(calcoli.segno(-1), 'negativo')\n"
        "        self.assertEqual(calcoli.segno(0), 'zero')\n", encoding="utf-8")
    codice, testo = esegui(d, "calcoli.py")
    verifica("tutti i casi provati: copertura 100%", "100%  -" in testo and "Test eseguiti: 2" in testo)
    (d / "tests" / "test_calcoli.py").write_text(
        (d / "tests" / "test_calcoli.py").read_text(encoding="utf-8").replace("'zero')", "'nulla')"), encoding="utf-8")
    codice, testo = esegui(d, "calcoli.py")
    verifica("test fallito: codice di uscita 1 e conteggio dei falliti", codice == 1 and "falliti: 1" in testo)
    codice, testo = esegui(d, "inesistente.py")
    verifica("file inesistente: errore", codice == 1 and testo.startswith("Errore"))

codice, testo = esegui(Path(__file__).with_name("kit_con_difetti"))
righe = {r.split()[0]: r for r in testo.splitlines() if r.endswith(".py") or ".py " in r}
verifica("kit con difetti: 22 test superati", codice == 0 and "Test eseguiti: 22; falliti: 0" in testo)
verifica("kit con difetti: in logica.py manca solo la riga 60 (controllo del richiedente)",
         righe["logica.py"].endswith("  60"))

print(f"\nTest superati: {superati}, falliti: {falliti}")
