"""Controlla che il PC sia pronto per il progetto.

Uso:
    python verifica_ambiente.py                   controlla la cartella kit_prenotazioni accanto allo script
    python verifica_ambiente.py C:\\percorso\\kit   controlla un'altra cartella del kit

Controlli: versione di Python, Git installato, identità Git impostata,
VS Code raggiungibile dal terminale (facoltativo), test del kit superati.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

PYTHON_MINIMO = (3, 10)


def esegui(comando, cartella=None):
    """Esegue un comando e restituisce (codice di uscita, testo prodotto)."""
    try:
        r = subprocess.run(comando, cwd=cartella, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)
    return r.returncode, (r.stdout + r.stderr).strip()


def controlla_python(versione=sys.version_info):
    if tuple(versione[:2]) >= PYTHON_MINIMO:
        return "OK", f"Python {versione[0]}.{versione[1]}"
    return "DA SISTEMARE", (f"Python {versione[0]}.{versione[1]}: serve almeno "
                            f"{PYTHON_MINIMO[0]}.{PYTHON_MINIMO[1]}")


def controlla_git(esegui=esegui):
    codice, testo = esegui(["git", "--version"])
    if codice != 0:
        return "DA SISTEMARE", "Git non trovato: controllare che la cartella cmd di PortableGit sia nel PATH"
    return "OK", testo


def controlla_identita(esegui=esegui):
    problemi = []
    for chiave in ("user.name", "user.email"):
        codice, testo = esegui(["git", "config", chiave])
        if codice != 0 or not testo:
            problemi.append(chiave)
    if problemi:
        return "DA SISTEMARE", ("manca " + ", ".join(problemi) +
                                ': git config --global user.name "Nome C." e user.email (anche fittizia)')
    return "OK", "identità Git impostata"


def controlla_vscode(trova=shutil.which):
    if trova("code"):
        return "OK", "VS Code raggiungibile dal terminale con il comando code"
    return "ATTENZIONE", "comando code non trovato: VS Code portatile va aperto dalla sua cartella (non è un errore)"


def controlla_kit(cartella, esegui=esegui):
    cartella = Path(cartella)
    if not (cartella / "prenotazioni.py").exists():
        return "DA SISTEMARE", f"kit non trovato in {cartella}"
    codice, testo = esegui([sys.executable, "-m", "unittest"], cartella)
    trovato = re.search(r"Ran (\d+) tests?", testo)
    numero = trovato.group(1) if trovato else "?"
    if codice == 0 and trovato and int(numero) > 0:
        return "OK", f"test del kit superati: {numero}"
    return "DA SISTEMARE", f"test del kit non superati (eseguiti: {numero}); lanciare python -m unittest nella cartella del kit"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    kit = Path(argv[0]) if argv else Path(__file__).parent / "kit_prenotazioni"
    risultati = [controlla_python(), controlla_git(), controlla_identita(),
                 controlla_vscode(), controlla_kit(kit)]
    for stato, messaggio in risultati:
        print(f"{stato:<13}{messaggio}")
    da_sistemare = sum(1 for stato, _ in risultati if stato == "DA SISTEMARE")
    print()
    print("Il PC è pronto." if da_sistemare == 0 else f"Punti da sistemare: {da_sistemare}")
    return 0 if da_sistemare == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
