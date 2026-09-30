"""Controlla un repository Git del progetto: identità, .gitignore, file tracciati, messaggi di commit.

Uso:
    python controlla_repository.py C:\\corso-impresa\\progetto_orione
    python controlla_repository.py C:\\corso-impresa\\progetto_orione --minimo-commit 5

Controlli:
    - la cartella è un repository Git e ha almeno un commit
    - l'identità (user.name e user.email) è impostata
    - esiste un .gitignore che esclude __pycache__
    - nel repository non sono stati registrati file generati (__pycache__, .pyc, .bak, .tmp)
    - ci sono almeno N commit (predefinito 3)
    - i messaggi di commit seguono le regole del corso
    - non ci sono modifiche non registrate (avviso)
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

GENERICI = {"fix", "modifiche", "modifica", "aggiornamento", "aggiornamenti", "update", "prova",
            "prove", "wip", "commit", "vari", "varie", "cose", "test", "ok", "fatto"}
GENERATI = re.compile(r"(^|/)__pycache__/|\.pyc$|\.bak$|\.tmp$")
MIN_LUNGHEZZA, MAX_LUNGHEZZA = 10, 72


def git(cartella, *argomenti):
    """Esegue un comando git nella cartella; restituisce (codice di uscita, testo prodotto)."""
    try:
        r = subprocess.run(["git", *argomenti], cwd=cartella, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
    except OSError as e:
        return 1, str(e)
    return r.returncode, r.stdout.strip()


def controlla_messaggio(messaggio):
    """Restituisce i problemi del messaggio di un commit (titolo = prima riga)."""
    righe = messaggio.split("\n")
    titolo = righe[0].strip()
    problemi = []
    if titolo.lower().rstrip(".!") in GENERICI or len(titolo) < MIN_LUNGHEZZA:
        problemi.append("titolo troppo generico o troppo breve: dire che cosa cambia")
    if len(titolo) > MAX_LUNGHEZZA:
        problemi.append(f"titolo di {len(titolo)} caratteri: massimo {MAX_LUNGHEZZA}")
    if titolo.endswith("."):
        problemi.append("il titolo non termina con il punto")
    if titolo and titolo[0].islower():
        problemi.append("il titolo inizia con la lettera maiuscola")
    if len(righe) > 1 and righe[1].strip():
        problemi.append("tra titolo e descrizione serve una riga vuota")
    return problemi


def controlla(cartella, minimo_commit=3):
    """Restituisce l'elenco dei risultati, ciascuno (livello, messaggio)."""
    risultati = []
    codice, _ = git(cartella, "rev-parse", "--is-inside-work-tree")
    if codice != 0:
        return [("DA SISTEMARE", f"{cartella} non è un repository Git: eseguire git init")]
    codice, numero = git(cartella, "rev-list", "--count", "HEAD")
    if codice != 0:
        return [("DA SISTEMARE", "il repository non ha ancora nessun commit")]

    for chiave in ("user.name", "user.email"):
        codice, valore = git(cartella, "config", chiave)
        if codice != 0 or not valore:
            risultati.append(("DA SISTEMARE", f"{chiave} non impostato: git config {chiave} \"...\""))
    if not any(r[1].startswith("user.") for r in risultati):
        risultati.append(("OK", "identità impostata"))

    ignora = Path(cartella) / ".gitignore"
    if not ignora.exists():
        risultati.append(("DA SISTEMARE", "manca il file .gitignore"))
    elif "__pycache__" not in ignora.read_text(encoding="utf-8", errors="replace"):
        risultati.append(("DA SISTEMARE", ".gitignore non esclude __pycache__"))
    else:
        risultati.append(("OK", ".gitignore presente"))

    _, tracciati = git(cartella, "ls-files")
    generati = [f for f in tracciati.splitlines() if GENERATI.search(f)]
    if generati:
        risultati.append(("DA SISTEMARE", "file generati registrati nel repository: " + ", ".join(generati[:5]) +
                          "; rimuoverli con git rm --cached"))
    else:
        risultati.append(("OK", "nessun file generato nel repository"))

    numero = int(numero)
    if numero < minimo_commit:
        risultati.append(("DA SISTEMARE", f"commit: {numero}, ne servono almeno {minimo_commit}"))
    else:
        risultati.append(("OK", f"commit: {numero}"))

    _, storia = git(cartella, "log", "--format=%h%x1f%B%x1e")
    for voce in storia.split("\x1e"):
        if not voce.strip():
            continue
        breve, messaggio = voce.strip().split("\x1f", 1)
        if messaggio.startswith("Merge "):          # messaggi scritti da Git durante un merge
            continue
        for problema in controlla_messaggio(messaggio.strip()):
            titolo = messaggio.strip().split("\n")[0]
            risultati.append(("DA SISTEMARE", f"commit {breve} \"{titolo[:40]}\": {problema}"))

    _, stato = git(cartella, "status", "--porcelain")
    if stato:
        file_modificati = [r[3:] for r in stato.splitlines()]
        risultati.append(("ATTENZIONE", "modifiche non registrate: " + ", ".join(file_modificati[:5])))
    return risultati


def main(argv=None):
    parser = argparse.ArgumentParser(description="Controllo del repository Git del progetto")
    parser.add_argument("cartella", help="cartella del repository")
    parser.add_argument("--minimo-commit", type=int, default=3)
    argomenti = parser.parse_args(argv)
    risultati = controlla(argomenti.cartella, argomenti.minimo_commit)
    for livello, messaggio in risultati:
        print(f"{livello:<13}{messaggio}")
    da_sistemare = sum(1 for livello, _ in risultati if livello == "DA SISTEMARE")
    print("\nRepository in ordine." if da_sistemare == 0 else f"\nPunti da sistemare: {da_sistemare}")
    return 0 if da_sistemare == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
