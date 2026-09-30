"""Test di crea_repository_condivisi.py e prima_del_push.py. Esecuzione: python test_repository_condiviso.py

I test simulano un repository condiviso e due membri del team in cartelle temporanee: serve Git installato.
"""

import subprocess
import tempfile
from pathlib import Path

import crea_repository_condivisi as crc
import prima_del_push as pdp

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


def scrivi_progetto(cartella):
    (cartella / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    (cartella / "somma.py").write_text("def somma(a, b):\n    return a + b\n", encoding="utf-8")
    (cartella / "test_somma.py").write_text(
        "import unittest\nfrom somma import somma\n\n\nclass T(unittest.TestCase):\n"
        "    def test_somma(self):\n        self.assertEqual(somma(2, 3), 5)\n", encoding="utf-8")


def livelli(risultati, testo):
    return [livello for livello, m in risultati if testo in m]


with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    base = Path(d)
    condivisa = base / "condivisa"
    condivisa.mkdir()
    esiti = crc.crea(condivisa, ["Orione", "vega", "nome con spazi"])
    verifica("repository creati per i nomi validi, in minuscolo",
             [e.split(":")[0] for _, e in esiti] == ["creato", "creato", "nome non valido"]
             and (condivisa / "orione.git").is_dir())
    verifica("repository già esistente non sovrascritto", crc.crea(condivisa, ["orione"])[0][1].startswith("esiste già"))
    verifica("ramo principale main nel repository condiviso",
             git(condivisa / "orione.git", "symbolic-ref", "HEAD").stdout.strip() == "refs/heads/main")
    try:
        crc.crea(base / "inesistente", ["x"])
        verifica("cartella di destinazione inesistente", False)
    except ValueError:
        verifica("cartella di destinazione inesistente", True)

    # il Product Owner collega la copia di riferimento e invia la storia
    po = base / "po"
    po.mkdir()
    git(po, "init", "-q")
    git(po, "symbolic-ref", "HEAD", "refs/heads/main")
    scrivi_progetto(po)
    git(po, "add", "-A")
    git(po, "commit", "-q", "-m", "Aggiungi il progetto")
    esiti = pdp.controlla(po)
    verifica("senza repository collegato: indicazione di git remote add", livelli(esiti, "git remote add") == ["DA SISTEMARE"])
    git(po, "remote", "add", "origin", str(condivisa / "orione.git"))
    esiti = pdp.controlla(po)
    verifica("primo invio: ramo non ancora condiviso", any("primo invio" in m for _, m in esiti)
             and not livelli(esiti, "DA SISTEMARE"))
    git(po, "push", "-q", "-u", "origin", "main")

    # un altro membro clona, modifica e invia
    compagno = base / "compagno"
    git(base, "clone", "-q", str(condivisa / "orione.git"), str(compagno))
    verifica("il clone contiene i file del progetto", (compagno / "somma.py").exists())
    with open(compagno / "somma.py", "a", encoding="utf-8") as f:
        f.write("\n\ndef differenza(a, b):\n    return a - b\n")
    esiti = pdp.controlla(compagno)
    verifica("modifiche non registrate segnalate", livelli(esiti, "modifiche non registrate") == ["DA SISTEMARE"])
    git(compagno, "commit", "-q", "-am", "Aggiungi la differenza")
    esiti = pdp.controlla(compagno)
    verifica("pronto per l'invio di 1 commit, test superati",
             ("OK", "pronto per l'invio di 1 commit: git push") in esiti and ("OK", "test superati: 1") in esiti)
    git(compagno, "push", "-q")

    # il Product Owner lavora senza aver ricevuto le novità
    with open(po / "somma.py", "a", encoding="utf-8") as f:
        f.write("\n\ndef prodotto(a, b):\n    return a * b\n")
    git(po, "commit", "-q", "-am", "Aggiungi il prodotto")
    esiti = pdp.controlla(po)
    verifica("indietro rispetto al repository condiviso: prima git pull",
             any("ha 1 commit che non hai" in m for _, m in esiti))

    # test che falliscono
    (compagno / "test_somma.py").write_text((compagno / "test_somma.py").read_text(encoding="utf-8")
                                           .replace("5)", "50)"), encoding="utf-8")
    git(compagno, "commit", "-q", "-am", "Modifica il test per errore")
    verifica("test che falliscono segnalati",
             livelli(pdp.controlla(compagno), "i test non passano") == ["DA SISTEMARE"])

    # marcatori di conflitto registrati per errore
    (compagno / "note.txt").write_text("<<<<<<< HEAD\na\n=======\nb\n>>>>>>> ramo\n", encoding="utf-8")
    git(compagno, "add", "-A")
    git(compagno, "commit", "-q", "-m", "Aggiungi le note")
    verifica("marcatori di conflitto registrati segnalati",
             livelli(pdp.controlla(compagno, esegui_test=False), "marcatori di conflitto in: note.txt") == ["DA SISTEMARE"])

    # repository condiviso non raggiungibile
    git(po, "remote", "set-url", "origin", str(base / "sparito.git"))
    verifica("repository condiviso non raggiungibile",
             livelli(pdp.controlla(po, esegui_test=False), "non raggiungibile") == ["DA SISTEMARE"])

print(f"\nTest superati: {superati}, falliti: {falliti}")
