"""Crea i repository condivisi dei team (script per il docente).

Uso:
    python crea_repository_condivisi.py \\\\server-scuola\\progetti orione vega lira
    python crea_repository_condivisi.py E:\\progetti orione vega lira          (chiavetta USB)

Per ogni team crea nella cartella di destinazione un repository "bare"
(solo la storia, senza file di lavoro), per esempio orione.git, con ramo
principale main. Il Product Owner del team poi lo collega alla copia di
riferimento del progetto e invia la storia:
    git remote add origin \\\\server-scuola\\progetti\\orione.git
    git push -u origin main
"""

import re
import subprocess
import sys
from pathlib import Path

NOME_VALIDO = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def crea(destinazione, team):
    """Crea i repository e restituisce l'elenco (team, esito)."""
    destinazione = Path(destinazione)
    if not destinazione.is_dir():
        raise ValueError(f"la cartella {destinazione} non esiste")
    esiti = []
    for nome in team:
        nome = nome.lower()
        if not NOME_VALIDO.match(nome):
            esiti.append((nome, "nome non valido: solo lettere minuscole, cifre, - e _"))
            continue
        percorso = destinazione / f"{nome}.git"
        if percorso.exists():
            esiti.append((nome, f"esiste già: {percorso}"))
            continue
        subprocess.run(["git", "init", "-q", "--bare", str(percorso)], check=True, capture_output=True)
        subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], cwd=percorso,
                       check=True, capture_output=True)
        esiti.append((nome, f"creato: {percorso}"))
    return esiti


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 2:
        print("Uso: python crea_repository_condivisi.py cartella_condivisa team1 team2 ...")
        return 2
    try:
        esiti = crea(argv[0], argv[1:])
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        print(f"Errore: {e}")
        return 1
    for nome, esito in esiti:
        print(f"{nome:<12}{esito}")
    return 0 if all(e.startswith("creato") for _, e in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
