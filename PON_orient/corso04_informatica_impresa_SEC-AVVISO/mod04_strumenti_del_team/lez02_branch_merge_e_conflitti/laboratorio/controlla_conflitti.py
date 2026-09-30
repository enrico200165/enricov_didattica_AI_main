"""Controlla che un'integrazione (merge) sia conclusa correttamente.

Uso:
    python controlla_conflitti.py C:\\corso-impresa\\lab42\\esercizio

Controlli:
    - nessun merge lasciato a metà (serve git commit per concluderlo)
    - nessun marcatore di conflitto (<<<<<<<, =======, >>>>>>>) nei file del repository
    - i test automatici passano (python -m unittest)
"""

import os
import re
import subprocess
import sys
from pathlib import Path

MARCATORE = re.compile(r"^(<{7}( |$)|={7}$|>{7}( |$))")


def git(cartella, *argomenti):
    r = subprocess.run(["git", *argomenti], cwd=cartella, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout.strip()


def marcatori(cartella):
    """Restituisce l'elenco (file, numero di riga) delle righe con marcatori di conflitto."""
    trovati = []
    _, file_tracciati = git(cartella, "ls-files")
    for nome in sorted(set(file_tracciati.splitlines())):     # durante un conflitto un file compare più volte
        percorso = Path(cartella) / nome
        if not percorso.is_file():
            continue
        try:
            righe = percorso.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue                                       # file binario: si salta
        trovati += [(nome, n) for n, riga in enumerate(righe, start=1) if MARCATORE.match(riga)]
    return trovati


def esegui_test(cartella):
    r = subprocess.run([sys.executable, "-m", "unittest"], cwd=cartella, capture_output=True,
                       text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})   # niente file .pyc vecchi
    eseguiti = re.search(r"Ran (\d+) tests?", r.stderr)
    return r.returncode == 0 and eseguiti is not None and int(eseguiti.group(1)) > 0, (eseguiti.group(1) if eseguiti else "0")


def controlla(cartella):
    risultati = []
    codice, _ = git(cartella, "rev-parse", "--git-dir")
    if codice != 0:
        return [("DA SISTEMARE", f"{cartella} non è un repository Git")]
    codice, _ = git(cartella, "rev-parse", "-q", "--verify", "MERGE_HEAD")
    if codice == 0:
        risultati.append(("DA SISTEMARE", "merge non concluso: risolvere i conflitti, poi git add e git commit"))
    per_file = {}
    for nome, riga in marcatori(cartella):
        per_file.setdefault(nome, []).append(str(riga))
    for nome, righe in per_file.items():
        risultati.append(("DA SISTEMARE", f"marcatori di conflitto in {nome}, righe {', '.join(righe)}"))
    passati, numero = esegui_test(cartella)
    if passati:
        risultati.append(("OK", f"test superati: {numero}"))
    else:
        risultati.append(("DA SISTEMARE", f"i test non passano o non sono stati trovati (eseguiti: {numero})"))
    if not any(livello == "DA SISTEMARE" for livello, _ in risultati):
        risultati.insert(0, ("OK", "integrazione conclusa, nessun marcatore di conflitto"))
    return risultati


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Uso: python controlla_conflitti.py cartella_del_repository")
        return 2
    risultati = controlla(argv[0])
    for livello, messaggio in risultati:
        print(f"{livello:<13}{messaggio}")
    return 0 if all(livello == "OK" for livello, _ in risultati) else 1


if __name__ == "__main__":
    sys.exit(main())
