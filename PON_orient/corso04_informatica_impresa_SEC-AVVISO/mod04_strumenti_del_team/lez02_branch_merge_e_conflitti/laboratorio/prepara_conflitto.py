"""Prepara un repository di esercizio con due rami che vanno in conflitto.

Uso:
    python prepara_conflitto.py C:\\corso-impresa\\lab42\\esercizio

Il repository contiene il modulo regole_orario.py e i suoi test. Due sviluppatori
di fantasia hanno lavorato su due rami, partendo dallo stesso commit:
    us14-messaggi   Giulia aggiunge il controllo "fine dopo inizio"
    us06-domenica   Marco aggiunge il controllo "chiuso la domenica"
Entrambi hanno aggiunto il proprio controllo nello stesso punto della funzione
e i propri test in fondo allo stesso file. Il ramo us14-messaggi è già stato
integrato in main; l'integrazione di us06-domenica produce un conflitto:
    git merge us06-domenica
"""

import subprocess
import sys
from pathlib import Path

INIZIALE = '''"""Regole sugli orari delle prenotazioni."""

from datetime import time

APERTURA = time(8, 0)
CHIUSURA = time(18, 0)


def controlla_orario(giorno, inizio, fine):
    """Restituisce None se l'orario è accettabile, altrimenti il messaggio di errore."""
    if inizio < APERTURA or fine > CHIUSURA:
        return f"la scuola è aperta dalle {APERTURA:%H:%M} alle {CHIUSURA:%H:%M}"
    return None
'''

CONTROLLO_GIULIA = '''    if inizio >= fine:
        return "l'orario di fine deve essere successivo a quello di inizio"
'''

CONTROLLO_MARCO = '''    if giorno.weekday() == 6:
        return "la scuola è chiusa la domenica"
'''

TEST_INIZIALI = '''"""Test di regole_orario.py."""

import unittest
from datetime import date, time

from regole_orario import controlla_orario

LUNEDI = date(2026, 10, 12)
DOMENICA = date(2026, 10, 18)


class TestOrario(unittest.TestCase):

    def test_orario_valido(self):
        self.assertIsNone(controlla_orario(LUNEDI, time(9, 0), time(11, 0)))

    def test_fuori_orario(self):
        self.assertIn("aperta", controlla_orario(LUNEDI, time(7, 0), time(9, 0)))
'''

TEST_GIULIA = '''
    def test_fine_prima_di_inizio(self):
        self.assertIn("fine", controlla_orario(LUNEDI, time(11, 0), time(9, 0)))
'''

TEST_MARCO = '''
    def test_domenica(self):
        self.assertIn("domenica", controlla_orario(DOMENICA, time(9, 0), time(11, 0)))
'''

DOCSTRING = '    """Restituisce None se l\'orario è accettabile, altrimenti il messaggio di errore."""\n'


def con_controllo(controllo):
    """Il modulo iniziale con un controllo inserito subito dopo la docstring della funzione."""
    return INIZIALE.replace(DOCSTRING, DOCSTRING + controllo)


def git(cartella, *argomenti, autore=None):
    comando = ["git"]
    if autore:
        comando += ["-c", f"user.name={autore}", "-c", f"user.email={autore.split()[0].lower()}@classe.invalid"]
    subprocess.run(comando + list(argomenti), cwd=cartella, check=True, capture_output=True)


def scrivi(cartella, modulo, test):
    (cartella / "regole_orario.py").write_text(modulo, encoding="utf-8", newline="\n")
    (cartella / "test_regole_orario.py").write_text(test, encoding="utf-8", newline="\n")


def prepara(cartella):
    cartella = Path(cartella)
    if cartella.exists() and any(cartella.iterdir()):
        raise ValueError(f"la cartella {cartella} esiste e non è vuota")
    cartella.mkdir(parents=True, exist_ok=True)
    git(cartella, "init", "-q")
    git(cartella, "symbolic-ref", "HEAD", "refs/heads/main")   # ramo principale "main", qualunque sia l'impostazione
    git(cartella, "config", "core.autocrlf", "false")   # righe identiche su Windows e Linux
    (cartella / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    scrivi(cartella, INIZIALE, TEST_INIZIALI)
    git(cartella, "add", "-A")
    git(cartella, "commit", "-q", "-m", "Aggiungi le regole sugli orari", autore="Docente D.")

    git(cartella, "checkout", "-q", "-b", "us14-messaggi")
    scrivi(cartella, con_controllo(CONTROLLO_GIULIA), TEST_INIZIALI + TEST_GIULIA)
    git(cartella, "commit", "-q", "-am", "Rifiuta gli orari con la fine prima dell'inizio", autore="Giulia F.")

    git(cartella, "checkout", "-q", "main")
    git(cartella, "checkout", "-q", "-b", "us06-domenica")
    scrivi(cartella, con_controllo(CONTROLLO_MARCO), TEST_INIZIALI + TEST_MARCO)
    git(cartella, "commit", "-q", "-am", "Rifiuta le prenotazioni di domenica", autore="Marco T.")

    git(cartella, "checkout", "-q", "main")
    git(cartella, "merge", "-q", "us14-messaggi")        # avanzamento veloce: nessun conflitto
    return cartella


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Uso: python prepara_conflitto.py cartella_nuova")
        return 2
    try:
        cartella = prepara(argv[0])
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        print(f"Errore: {e}")
        return 1
    print(f"Repository di esercizio pronto in {cartella}")
    print("Rami: main (con us14-messaggi già integrato), us14-messaggi, us06-domenica")
    print("Prossimo passo, nella cartella del repository:  git merge us06-domenica")
    return 0


if __name__ == "__main__":
    sys.exit(main())
