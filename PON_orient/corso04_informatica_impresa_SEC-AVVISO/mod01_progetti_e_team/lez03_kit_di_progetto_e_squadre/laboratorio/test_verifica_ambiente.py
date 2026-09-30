"""Test di verifica_ambiente.py. Esecuzione: python test_verifica_ambiente.py"""

import contextlib
import io
import tempfile
from pathlib import Path

import verifica_ambiente as v

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def finto(risposte):
    """Crea una funzione esegui finta: restituisce risposte prefissate per ogni comando."""
    def esegui(comando, cartella=None):
        return risposte.get(" ".join(comando), (1, "comando non trovato"))
    return esegui


verifica("Python 3.12 accettato", v.controlla_python((3, 12, 0))[0] == "OK")
verifica("Python 3.10 accettato", v.controlla_python((3, 10, 4))[0] == "OK")
verifica("Python 3.8 da sistemare", v.controlla_python((3, 8, 10))[0] == "DA SISTEMARE")

verifica("Git presente", v.controlla_git(finto({"git --version": (0, "git version 2.55.0.windows.3")}))
         == ("OK", "git version 2.55.0.windows.3"))
verifica("Git assente", v.controlla_git(finto({}))[0] == "DA SISTEMARE")

ok = finto({"git config user.name": (0, "Anna R."), "git config user.email": (0, "anna.r@classe.invalid")})
verifica("identità completa", v.controlla_identita(ok)[0] == "OK")
solo_nome = finto({"git config user.name": (0, "Anna R.")})
stato, messaggio = v.controlla_identita(solo_nome)
verifica("manca l'email: da sistemare, con indicazione della chiave",
         stato == "DA SISTEMARE" and "user.email" in messaggio and "user.name," not in messaggio)

verifica("VS Code nel PATH", v.controlla_vscode(lambda nome: "C:/vscode/bin/code")[0] == "OK")
verifica("VS Code non nel PATH: solo attenzione", v.controlla_vscode(lambda nome: None)[0] == "ATTENZIONE")

kit_vero = Path(__file__).parent / "kit_prenotazioni"
stato, messaggio = v.controlla_kit(kit_vero)
verifica("kit vero: test superati e contati", stato == "OK" and "superati: 27" in messaggio)

with tempfile.TemporaryDirectory() as d:
    verifica("cartella senza kit", v.controlla_kit(d)[0] == "DA SISTEMARE")
    (Path(d) / "prenotazioni.py").write_text("", encoding="utf-8")
    fallito = lambda comando, cartella=None: (1, "Ran 27 tests\n\nFAILED (failures=1)")
    stato, messaggio = v.controlla_kit(d, fallito)
    verifica("test del kit falliti", stato == "DA SISTEMARE" and "eseguiti: 27" in messaggio)
    nessuno = lambda comando, cartella=None: (0, "Ran 0 tests\n\nNO TESTS RAN")
    verifica("nessun test trovato: da sistemare", v.controlla_kit(d, nessuno)[0] == "DA SISTEMARE")

out = io.StringIO()
with contextlib.redirect_stdout(out):
    codice = v.main([str(kit_vero)])
testo = out.getvalue()
verifica("esecuzione completa: cinque righe di controllo e riepilogo",
         len([r for r in testo.splitlines() if r[:2] in ("OK", "DA", "AT")]) == 5
         and ("Il PC è pronto." in testo or "Punti da sistemare" in testo))

print(f"\nTest superati: {superati}, falliti: {falliti}")
