"""Test di criteri_in_test.py. Esecuzione: python test_criteri_in_test.py"""

import ast
import contextlib
import io
import subprocess
import sys
import tempfile
from pathlib import Path

import criteri_in_test as c

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


BACKLOG = """## Storie

### US-01 Nessuna prenotazione sovrapposta

Come docente voglio che ...

Criteri di accettazione:

- Dato che LAB-INF1 è prenotato dalle 9:00 alle 11:00, quando prenoto dalle 10:00 alle 12:00, allora la prenotazione è rifiutata.
- Data la stessa situazione, Quando prenoto dalle 11:00, Allora è accettata.

### US-02 Prenotazioni di un giorno

Criteri di accettazione:

- Dato che non esistono prenotazioni, quando chiedo il 13/10, allora vedo "Nessuna prenotazione"

### US-03 Cancellare

Criteri di accettazione: da scrivere.
"""

titolo, criteri = c.criteri_della_storia(BACKLOG, "US-01")
verifica("titolo e due criteri di US-01", titolo == "Nessuna prenotazione sovrapposta" and len(criteri) == 2)
verifica("criterio diviso in Dato, Quando, Allora",
         criteri[0] == ("Dato che LAB-INF1 è prenotato dalle 9:00 alle 11:00", "quando prenoto dalle 10:00 alle 12:00",
                        "allora la prenotazione è rifiutata."))
verifica("varianti Data, Quando, Allora con maiuscole", criteri[1][0].startswith("Data") and criteri[1][2].startswith("Allora"))
verifica("i criteri di un'altra storia non vengono presi", len(c.criteri_della_storia(BACKLOG, "US-02")[1]) == 1)

for codice, atteso in (("US-03", "non ha criteri"), ("US-09", "non ha una sezione")):
    try:
        c.criteri_della_storia(BACKLOG, codice)
        verifica(f"{codice}: errore atteso", False)
    except c.ErroreStoria as e:
        verifica(f"{codice}: {atteso}", atteso in str(e))

testo = c.scheletro("US-02", "Prenotazioni di un giorno", c.criteri_della_storia(BACKLOG, "US-02")[1])
verifica("scheletro sintatticamente valido anche con virgolette nel criterio", ast.parse(testo) is not None)
verifica("classe e metodo di test", "class TestUS02(unittest.TestCase):" in testo and "def test_criterio_1(self):" in testo)

with tempfile.TemporaryDirectory() as d:
    cartella = Path(d)
    (cartella / "docs").mkdir()
    (cartella / "docs" / "backlog.md").write_text(BACKLOG, encoding="utf-8")
    (cartella / "logica.py").write_text("", encoding="utf-8")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = c.main([str(cartella / "docs" / "backlog.md"), "us-01", "--uscita", str(cartella / "tests" / "test_us01.py")])
    verifica("file scritto con due test", codice == 0 and "Scritti 2 test" in out.getvalue())
    (cartella / "tests" / "__init__.py").write_text("", encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "unittest"], cwd=cartella, capture_output=True, text=True)
    verifica("i test generati falliscono finché non vengono scritti", r.returncode != 0 and "failures=2" in r.stderr)
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = c.main([str(cartella / "docs" / "backlog.md"), "US-01", "--uscita", str(cartella / "tests" / "test_us01.py")])
    verifica("file esistente non sovrascritto", codice == 1 and "esiste già" in out.getvalue())

print(f"\nTest superati: {superati}, falliti: {falliti}")
