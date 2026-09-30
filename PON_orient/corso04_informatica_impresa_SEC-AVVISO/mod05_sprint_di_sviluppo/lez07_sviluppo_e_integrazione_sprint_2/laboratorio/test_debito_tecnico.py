"""Test di debito_tecnico.py. Esecuzione: python test_debito_tecnico.py"""

import contextlib
import io
import tempfile
from pathlib import Path

import debito_tecnico as dt

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


CODICE = '''"""Modulo di prova."""


def breve(a):
    """Documentata."""
    return a


def senza_docstring(a):
    return a  # TODO: gestire i valori negativi


def _interna(a):
    return a


def molti(a, b, c, d, e, f, *, g):
    """Troppi parametri."""
    return a


class Aula:
    def __init__(self):
        self.x = 1  # FIXME nome poco chiaro


def lunga():
    """Lunga."""
''' + "    x = 1\n" * 26

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    (d / "modulo.py").write_text(CODICE, encoding="utf-8")
    segnali = dt.analizza_file(d / "modulo.py", 25)
    tipi = [(riga, tipo) for riga, tipo, _ in segnali]
    descrizioni = [s for _, _, s in segnali]
    verifica("funzione senza docstring segnalata", (9, "documentazione") in tipi)
    verifica("funzione interna (con _) non segnalata", not any("_interna" in s for s in descrizioni))
    verifica("classe senza docstring segnalata; __init__ no", "classe Aula senza docstring" in descrizioni
             and not any("__init__" in s for s in descrizioni))
    verifica("7 parametri, compresi quelli solo per nome", "funzione molti con 7 parametri (massimo 6)" in descrizioni)
    verifica("funzione di 28 righe segnalata", any(s.startswith("funzione lunga di 28 righe") for s in descrizioni))
    verifica("TODO e FIXME con il testo", "TODO: gestire i valori negativi" in descrizioni and "FIXME nome poco chiaro" in descrizioni)
    verifica("limite di righe modificabile", not any("lunga di" in s for _, _, s in dt.analizza_file(d / "modulo.py", 30)))

    (d / "tests").mkdir()
    (d / "tests" / "test_x.py").write_text("def test_senza_docstring():\n    pass\n", encoding="utf-8")
    (d / ".vscode").mkdir()
    (d / ".vscode" / "prova.py").write_text("def f():\n    pass\n", encoding="utf-8")
    risultati = dt.analizza_progetto(d, 25)
    verifica("cartella tests e cartelle nascoste escluse", list(risultati) == ["modulo.py"])

    testo = dt.registro_markdown(risultati)
    verifica("registro con colonna Decisione", "| File | Riga | Tipo | Descrizione | Decisione |" in testo
             and "| modulo.py | 9 | documentazione | funzione senza_docstring senza docstring | |" in testo)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = dt.main([str(d), "--registro", str(d / "debito.md")])
    verifica("esecuzione: conteggio e registro scritto",
             codice == 0 and "File analizzati: 1; segnali: 6" in out.getvalue() and (d / "debito.md").exists())
    (d / "rotto.py").write_text("def f(:\n", encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = dt.main([str(d)])
    verifica("file con errore di sintassi: errore", codice == 1 and "Errore" in out.getvalue())

kit = Path(__file__).resolve().parents[3] / "mod01_progetti_e_team" / "lez03_kit_di_progetto_e_squadre" / "laboratorio" / "kit_prenotazioni"
if kit.exists():
    risultati = dt.analizza_progetto(kit, 25)
    verifica("kit: 4 segnali, tra cui gli 8 parametri di nuova_prenotazione",
             sum(len(s) for s in risultati.values()) == 4
             and any("nuova_prenotazione con 8 parametri" in s for _, _, s in risultati["logica.py"]))
else:
    print("SALTATO il test sul kit: cartella del corso non completa")

print(f"\nTest superati: {superati}, falliti: {falliti}")
