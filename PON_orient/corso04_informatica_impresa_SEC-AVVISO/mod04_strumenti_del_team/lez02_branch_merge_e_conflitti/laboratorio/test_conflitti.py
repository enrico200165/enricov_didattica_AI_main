"""Test di prepara_conflitto.py e controlla_conflitti.py. Esecuzione: python test_conflitti.py

I test creano repository Git di prova in cartelle temporanee: serve Git installato.
"""

import subprocess
import tempfile
from pathlib import Path

import controlla_conflitti as cc
import prepara_conflitto as pc

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
    return subprocess.run(["git", "-c", "user.name=Prova T.", "-c", "user.email=prova@classe.invalid",
                           *argomenti], cwd=cartella, capture_output=True, text=True)


with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    cartella = pc.prepara(Path(d) / "esercizio")
    rami = git(cartella, "branch", "--format=%(refname:short)").stdout.split()
    verifica("tre rami creati", sorted(rami) == ["main", "us06-domenica", "us14-messaggi"])
    verifica("main contiene già il lavoro di Giulia",
             "fine deve essere successivo" in (cartella / "regole_orario.py").read_text(encoding="utf-8"))
    verifica("prima del merge: tutto in ordine (3 test)", cc.controlla(cartella)[-1] == ("OK", "test superati: 3"))

    risultato = git(cartella, "merge", "us06-domenica")
    verifica("il merge di us06-domenica produce un conflitto", risultato.returncode != 0 and "CONFLICT" in risultato.stdout)
    esiti = cc.controlla(cartella)
    verifica("merge non concluso segnalato", any("merge non concluso" in m for _, m in esiti))
    verifica("marcatori segnalati una volta per file",
             [m for _, m in esiti if m.startswith("marcatori")] ==
             ["marcatori di conflitto in regole_orario.py, righe 11, 14, 17",
              "marcatori di conflitto in test_regole_orario.py, righe 20, 23, 26"])

    # risoluzione corretta: si tengono entrambi i controlli e entrambi i test
    pc.scrivi(cartella, pc.con_controllo(pc.CONTROLLO_GIULIA + pc.CONTROLLO_MARCO),
              pc.TEST_INIZIALI + pc.TEST_GIULIA + pc.TEST_MARCO)
    git(cartella, "add", "-A")
    git(cartella, "commit", "-q", "--no-edit")
    verifica("dopo la risoluzione: integrazione conclusa e 4 test superati",
             cc.controlla(cartella) == [("OK", "integrazione conclusa, nessun marcatore di conflitto"),
                                        ("OK", "test superati: 4")])

with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    cartella = pc.prepara(Path(d) / "esercizio")
    git(cartella, "merge", "us06-domenica")
    testo = (cartella / "regole_orario.py").read_text(encoding="utf-8")
    senza_marcatori = "\n".join(r for r in testo.splitlines() if not cc.MARCATORE.match(r)) + "\n"
    (cartella / "regole_orario.py").write_text(senza_marcatori.replace("    if giorno", "if giorno"), encoding="utf-8")
    git(cartella, "checkout", "--theirs", "test_regole_orario.py")
    git(cartella, "add", "-A")
    git(cartella, "commit", "-q", "--no-edit")
    esiti = cc.controlla(cartella)
    verifica("marcatori tolti ma codice rovinato: i test lo rivelano",
             any("i test non passano" in m for _, m in esiti) and not any("marcatori" in m for _, m in esiti))

with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    cartella = pc.prepara(Path(d) / "esercizio")
    git(cartella, "merge", "us06-domenica")
    git(cartella, "checkout", "--ours", "regole_orario.py", "test_regole_orario.py")
    git(cartella, "add", "-A")
    git(cartella, "commit", "-q", "--no-edit")
    testo = (cartella / "regole_orario.py").read_text(encoding="utf-8")
    verifica("risoluzione sbagliata (solo la versione corrente): il controllo non la rileva, ma il lavoro di Marco è perso",
             cc.controlla(cartella)[0][0] == "OK" and "domenica" not in testo)

with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    (Path(d) / "occupata.txt").write_text("x", encoding="utf-8")
    try:
        pc.prepara(d)
        verifica("cartella non vuota rifiutata", False)
    except ValueError:
        verifica("cartella non vuota rifiutata", True)
    verifica("cartella che non è un repository", cc.controlla(d)[0][1].endswith("non è un repository Git"))

verifica("marcatori riconosciuti solo a inizio riga e completi",
         [bool(cc.MARCATORE.match(r)) for r in ("<<<<<<< HEAD", "=======", ">>>>>>> ramo", "x = '======='", "========")]
         == [True, True, True, False, False])

print(f"\nTest superati: {superati}, falliti: {falliti}")
