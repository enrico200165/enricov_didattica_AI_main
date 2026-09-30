"""Test di controlla_repository.py. Esecuzione: python test_controlla_repository.py

I test creano repository Git di prova in cartelle temporanee: serve Git installato.
"""

import subprocess
import tempfile
from pathlib import Path

import controlla_repository as c

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def git(cartella, *argomenti):
    subprocess.run(["git", *argomenti], cwd=cartella, check=True, capture_output=True)


def nuovo_repository(cartella, messaggi, gitignore="__pycache__/\n*.pyc\n"):
    git(cartella, "init", "-q")
    git(cartella, "config", "user.name", "Prova T.")
    git(cartella, "config", "user.email", "prova@classe.invalid")
    if gitignore is not None:
        (cartella / ".gitignore").write_text(gitignore, encoding="utf-8")
    for n, messaggio in enumerate(messaggi):
        (cartella / f"file{n}.txt").write_text(str(n), encoding="utf-8")
        git(cartella, "add", "-A")
        git(cartella, "commit", "-q", "-m", messaggio)


def livelli(risultati, testo):
    return [livello for livello, m in risultati if testo in m]


verifica("messaggio corretto", c.controlla_messaggio("Aggiungi il controllo delle sovrapposizioni") == [])
verifica("messaggio generico", c.controlla_messaggio("fix")[0].startswith("titolo troppo generico"))
verifica("messaggio con punto finale e minuscola",
         set(c.controlla_messaggio("aggiungi la cancellazione.")) ==
         {"il titolo non termina con il punto", "il titolo inizia con la lettera maiuscola"})
verifica("titolo troppo lungo", any("massimo 72" in p for p in c.controlla_messaggio("Aggiungi " + "x" * 80)))
verifica("descrizione senza riga vuota",
         "tra titolo e descrizione serve una riga vuota" in c.controlla_messaggio("Aggiungi la ricerca\nper giorno"))
verifica("descrizione dopo una riga vuota accettata",
         c.controlla_messaggio("Aggiungi la ricerca per giorno\n\nServe ai tecnici (US-02).") == [])

with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    verifica("cartella che non è un repository", c.controlla(d)[0][1].endswith("eseguire git init"))
    cartella = Path(d)
    git(cartella, "init", "-q")
    verifica("repository senza commit", c.controlla(d) == [("DA SISTEMARE", "il repository non ha ancora nessun commit")])

with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    cartella = Path(d)
    nuovo_repository(cartella, ["Aggiungi il kit di partenza", "Aggiorna il backlog con le priorità",
                                "Aggiungi l'obiettivo del prodotto"])
    risultati = c.controlla(d)
    verifica("repository in ordine: nessun punto da sistemare",
             not any(livello == "DA SISTEMARE" for livello, _ in risultati))
    verifica("repository in ordine: tre commit contati", ("OK", "commit: 3") in risultati)

with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    cartella = Path(d)
    nuovo_repository(cartella, ["Aggiungi il kit di partenza", "modifiche"], gitignore=None)
    (cartella / "__pycache__").mkdir()
    (cartella / "__pycache__" / "logica.cpython-312.pyc").write_bytes(b"x")
    git(cartella, "add", "-A")
    git(cartella, "commit", "-q", "-m", "Aggiungi file compilati per errore")
    (cartella / "nuovo.txt").write_text("non registrato", encoding="utf-8")
    risultati = c.controlla(d)
    verifica("manca .gitignore", livelli(risultati, "manca il file .gitignore") == ["DA SISTEMARE"])
    verifica("file generati registrati", livelli(risultati, "file generati registrati") == ["DA SISTEMARE"])
    verifica("messaggio generico segnalato con il commit", any("\"modifiche\"" in m for _, m in risultati))
    verifica("modifiche non registrate: attenzione", livelli(risultati, "modifiche non registrate: nuovo.txt") == ["ATTENZIONE"])
    verifica("minimo di commit personalizzato", ("DA SISTEMARE", "commit: 3, ne servono almeno 5") in c.controlla(d, 5))

with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    cartella = Path(d)
    nuovo_repository(cartella, ["Aggiungi il kit di partenza", "Aggiungi la ricerca per giorno",
                                "Aggiungi la cancellazione"], gitignore="*.bak\n")
    verifica(".gitignore senza __pycache__", livelli(c.controlla(d), "non esclude __pycache__") == ["DA SISTEMARE"])
    git(cartella, "checkout", "-q", "-b", "ramo")
    (cartella / "r.txt").write_text("r", encoding="utf-8")
    git(cartella, "add", "-A")
    git(cartella, "commit", "-q", "-m", "Aggiungi il file del ramo")
    git(cartella, "checkout", "-q", "-")
    (cartella / "m.txt").write_text("m", encoding="utf-8")
    git(cartella, "add", "-A")
    git(cartella, "commit", "-q", "-m", "Aggiungi il file principale")
    git(cartella, "merge", "-q", "--no-edit", "ramo")
    verifica("messaggi di merge scritti da Git ignorati", not any("Merge" in m for _, m in c.controlla(d)))

print(f"\nTest superati: {superati}, falliti: {falliti}")
