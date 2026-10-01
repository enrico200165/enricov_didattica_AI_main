"""Test di piano_orientativo.py. Esecuzione: python test_piano_orientativo.py"""

import contextlib
import io
import tempfile
from datetime import date
from pathlib import Path

import piano_orientativo as po

superati = falliti = 0
OGGI = date(2026, 12, 15)


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


esempio = po.leggi_piano(Path("piano_esempio.md").read_text(encoding="utf-8"))
verifica("esempio: 7 obiettivi letti dalla tabella", len(esempio) == 7 and esempio[2]["obiettivo"] == "Imparare le basi di SQL")
verifica("esempio: nessun problema", po.controlla(esempio, OGGI) == [])
verifica("modello: 3 obiettivi da completare",
         [l for l, _ in po.controlla(po.leggi_piano(Path("modello_piano.md").read_text(encoding="utf-8")), OGGI)]
         == ["DA SISTEMARE"] * 3)

INTESTAZIONE = "| Obiettivo | Priorità | Misura | Scadenza | Primo passo | Stato |\n|---|---|---|---|---|---|\n"


def problemi(*righe, oggi=OGGI):
    return [m for _, m in po.controlla(po.leggi_piano(INTESTAZIONE + "\n".join(righe)), oggi)]


verifica("priorità, stato e data non validi",
         problemi("| A | Alta | 2 | 2027-01-10 | x | iniziato |", "| B | Must | 2 | 10/01/2027 | x | da fare |")
         == ["obiettivo 1 \"A\": priorità da scegliere tra Must, Should, Could",
             "obiettivo 1 \"A\": stato da scegliere tra da fare, in corso, fatto",
             "obiettivo 2 \"B\": scadenza nel formato AAAA-MM-GG"])
verifica("data inesistente rifiutata", po.leggi_data("2027-02-30") is None)
verifica("scadenza passata non fatta",
         any("scadenza passata" in m for m in problemi("| A | Must | 2 | 2026-11-30 | x | in corso |")))
verifica("scadenza passata ma fatta: nessun problema",
         problemi("| A | Must | 2 | 2026-11-30 | x | fatto |", "| B | Must | 2 | 2027-01-31 | x | da fare |") == [])
verifica("obiettivo oltre 24 mesi", any("oltre 24 mesi" in m for m in problemi(
    "| A | Must | 2 | 2027-01-31 | x | da fare |", "| B | Should | 2 | 2029-06-30 | x | da fare |")))
verifica("obiettivo vago senza numero nella misura",
         any("poco specifico (\"migliorare\")" in m for m in problemi("| Migliorare in matematica | Must | voti migliori | 2027-01-31 | x | da fare |")))
verifica("obiettivo vago con misura numerica: accettato",
         problemi("| Migliorare in matematica | Must | media almeno 7 | 2027-01-31 | x | da fare |") == [])
verifica("troppi obiettivi in corso", any("4 obiettivi in corso" in m for m in problemi(
    *[f"| O{i} | Must | 2 | 2027-01-31 | x | in corso |" for i in range(4)])))
verifica("nessun obiettivo vicino", any("entro 3 mesi" in m for m in problemi("| A | Must | 2 | 2027-09-30 | x | da fare |")))
verifica("nessun obiettivo Must", any("nessun obiettivo Must" in m for m in problemi("| A | Could | 2 | 2027-01-31 | x | da fare |")))

try:
    po.leggi_piano("| Cosa | Quando |\n|---|---|\n| a | b |\n")
    senza_tabella = False
except ValueError:
    senza_tabella = True
verifica("tabella con colonne diverse: errore", senza_tabella)

testo = po.timeline(esempio)
verifica("linea del tempo: 7 mesi in ordine, obiettivo fatto indicato",
         testo.count("\n    20") == 7 and testo.index("2026-12") < testo.index("2028-07") and "(fatto)" in testo)

with tempfile.TemporaryDirectory() as cartella:
    destinazione = Path(cartella) / "linea.md"
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = po.main(["piano_esempio.md", "--oggi", "2026-12-15", "--timeline", str(destinazione)])
    verifica("esecuzione: riepilogo e linea del tempo scritta",
             codice == 0 and "Obiettivi: 7; da sistemare: 0" in out.getvalue() and "```mermaid" in destinazione.read_text(encoding="utf-8"))
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = po.main(["modello_piano.md", "--oggi", "2026-12-15", "--timeline", str(Path(cartella) / "no.md")])
    verifica("piano da sistemare: linea del tempo non scritta", codice == 1 and not (Path(cartella) / "no.md").exists())

print(f"\nTest superati: {superati}, falliti: {falliti}")
