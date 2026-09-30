"""Controlli da fare prima di inviare le modifiche al repository condiviso (git push).

Uso, nella cartella del proprio repository:
    python prima_del_push.py
    python prima_del_push.py C:\\corso-impresa\\progetto_orione

Controlli:
    - tutte le modifiche sono registrate in un commit
    - il ramo locale contiene già le novità del repository condiviso (altrimenti git pull)
    - nessun marcatore di conflitto nei file
    - i test automatici passano
Alla fine indica quanti commit verranno inviati.
"""

import os
import re
import subprocess
import sys

MARCATORE = re.compile(r"^(<{7}( |$)|={7}$|>{7}( |$))", re.MULTILINE)


def git(cartella, *argomenti):
    r = subprocess.run(["git", *argomenti], cwd=cartella, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout.strip()


def controlla(cartella, esegui_test=True):
    risultati = []
    codice, ramo = git(cartella, "rev-parse", "--abbrev-ref", "HEAD")
    if codice != 0:
        return [("DA SISTEMARE", "non è un repository Git con almeno un commit")]
    risultati.append(("OK", f"ramo corrente: {ramo}"))

    _, stato = git(cartella, "status", "--porcelain")
    if stato:
        risultati.append(("DA SISTEMARE", "modifiche non registrate: git add e git commit prima dell'invio"))

    codice, _ = git(cartella, "remote", "get-url", "origin")
    if codice != 0:
        risultati.append(("DA SISTEMARE", "nessun repository condiviso collegato: git remote add origin ..."))
        return risultati
    codice, _ = git(cartella, "fetch", "-q", "origin")
    if codice != 0:
        risultati.append(("DA SISTEMARE", "repository condiviso non raggiungibile: controllare il percorso"))
        return risultati
    codice, _ = git(cartella, "rev-parse", "-q", "--verify", f"origin/{ramo}")
    if codice != 0:
        risultati.append(("OK", f"il ramo {ramo} non esiste ancora nel repository condiviso: "
                                f"primo invio con git push -u origin {ramo}"))
        indietro = avanti = None
    else:
        _, conteggi = git(cartella, "rev-list", "--left-right", "--count", f"origin/{ramo}...HEAD")
        indietro, avanti = (int(x) for x in conteggi.split())
        if indietro:
            risultati.append(("DA SISTEMARE", f"il repository condiviso ha {indietro} commit che non hai: "
                                              "prima git pull, poi di nuovo i test"))
        if avanti == 0:
            risultati.append(("ATTENZIONE", "nessun commit da inviare"))

    _, tracciati = git(cartella, "ls-files")
    con_marcatori = []
    for nome in sorted(set(tracciati.splitlines())):
        _, contenuto = git(cartella, "show", f":{nome}")
        if MARCATORE.search(contenuto):
            con_marcatori.append(nome)
    if con_marcatori:
        risultati.append(("DA SISTEMARE", "marcatori di conflitto in: " + ", ".join(con_marcatori)))

    if esegui_test:
        r = subprocess.run([sys.executable, "-m", "unittest"], cwd=cartella, capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})   # niente file .pyc vecchi
        eseguiti = re.search(r"Ran (\d+) tests?", r.stderr)
        if r.returncode == 0 and eseguiti and int(eseguiti.group(1)) > 0:
            risultati.append(("OK", f"test superati: {eseguiti.group(1)}"))
        else:
            risultati.append(("DA SISTEMARE", "i test non passano: correggere prima dell'invio"))

    if not any(livello == "DA SISTEMARE" for livello, _ in risultati) and avanti:
        risultati.append(("OK", f"pronto per l'invio di {avanti} commit: git push"))
    return risultati


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    cartella = argv[0] if argv else "."
    risultati = controlla(cartella)
    for livello, messaggio in risultati:
        print(f"{livello:<13}{messaggio}")
    return 1 if any(livello == "DA SISTEMARE" for livello, _ in risultati) else 0


if __name__ == "__main__":
    sys.exit(main())
