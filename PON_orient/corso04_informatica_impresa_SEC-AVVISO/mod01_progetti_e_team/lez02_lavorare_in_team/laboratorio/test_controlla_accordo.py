"""Test di controlla_accordo.py. Esecuzione: python test_controlla_accordo.py"""

import contextlib
import io
import os
import tempfile

import controlla_accordo as c

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def messaggi(testo):
    return [m for _, m in c.controlla(testo)]


esempio = open("accordo_esempio.md", encoding="utf-8").read()
modello = open("accordo_di_team.md", encoding="utf-8").read()

verifica("accordo di esempio completo", c.controlla(esempio) == [])
verifica("modello vuoto: tutte le 9 sezioni da completare", len(c.controlla(modello)) == 9)

senza = esempio.replace("## Conflitti", "## Litigi")
verifica("sezione mancante segnalata", any('manca la sezione "Conflitti"' in m for m in messaggi(senza)))

vuota = esempio.replace("Si rilegge alla retrospettiva di ogni sprint e si modifica se una regola non funziona.",
                        "[Quando si rilegge l'accordo]")
verifica("sezione con solo suggerimenti considerata vuota",
         any("\"Revisione dell'accordo\" è vuota" in m for m in messaggi(vuota)))

cinque = esempio.replace("- Davide P.", "- Davide P.\n- Elena B.")
verifica("5 membri accettati", c.controlla(cinque) == [])
tre = esempio.replace("- Davide P.\n", "")
verifica("3 membri: attenzione", c.controlla(tre) == [("ATTENZIONE", "membri indicati: 3; i team sono di 4 o 5 persone")])
due = tre.replace("- Sara L.\n", "")
verifica("2 membri: da sistemare", c.controlla(due)[0][0] == "DA SISTEMARE")

posta = esempio.replace("- Marco T.", "- Marco T. marco.t@esempio.it")
verifica("indirizzo di posta segnalato con il numero di riga",
         any(m.startswith("riga ") and "posta" in m for m in messaggi(posta)))
telefono = esempio.replace("- Sara L.", "- Sara L. 333 123 4567")
verifica("numero di telefono segnalato", any("telefono" in m for m in messaggi(telefono)))
date = esempio.replace("14/10/2026", "2026-10-14, riunioni dalle 10:30 alle 11:00 del 2026-10-21")
verifica("date e orari non scambiati per numeri di telefono", c.controlla(date) == [])

with tempfile.TemporaryDirectory() as d:
    percorso = os.path.join(d, "accordo.md")
    with open(percorso, "w", encoding="utf-8") as f:
        f.write(tre)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = c.main([percorso])
    verifica("solo avvisi di attenzione: codice di uscita 0", codice == 0 and "0 da sistemare, 1 di attenzione" in out.getvalue())
    with contextlib.redirect_stdout(io.StringIO()):
        codice = c.main([os.path.join(d, "nessuno.md")])
    verifica("file inesistente: codice di uscita 2", codice == 2)

print(f"\nTest superati: {superati}, falliti: {falliti}")
