"""Test di genera_board.py. Esecuzione: python test_genera_board.py"""

import contextlib
import io
import tempfile
from pathlib import Path

import genera_board as g

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


BACKLOG = """| ID | Titolo | Priorità | Stima | Stato |
|---|---|---|---|---|
| US-00 | Elenco delle aule e nuova prenotazione | | | fatto (kit) |
| US-01 | Nessuna prenotazione sovrapposta | Must | 5 | in corso (Giulia) |
| US-02 | Prenotazioni di un giorno | Must | 2 | Fatto |
| US-03 | Cancellare una prenotazione | Must | 3 | in revisione (Sara) |
| US-08 | Riepilogo settimanale di un'aula | Should | | da fare |
| US-13 | Ruoli: docente e tecnico | Won't | | da fare |
"""

storie = g.leggi_storie(BACKLOG)
per_id = {s["id"]: s for s in storie}
verifica("sei storie lette", len(storie) == 6)
verifica("stato normalizzato e persona estratta", (per_id["US-01"]["stato"], per_id["US-01"]["persona"]) == ("in corso", "Giulia"))
verifica("maiuscole nello stato accettate", per_id["US-02"]["stato"] == "fatto")
verifica("\"kit\" non è una persona", per_id["US-00"]["persona"] == "")

testo, avvisi = g.genera(BACKLOG, {"in corso": 3, "in revisione": 2})
verifica("storie Won't escluse dalla board", "US-13" not in testo)
verifica("scheda con persona, priorità e punti",
         "us01[Nessuna prenotazione sovrapposta, 5 punti]@{ ticket: 'US-01', assigned: 'Giulia', priority: 'Very High' }" in testo)
verifica("apostrofo mantenuto nel testo della scheda", "us08[Riepilogo settimanale di un'aula]" in testo)
verifica("colonne con conteggio e limite", "inCorso[In corso, 1 su massimo 3]" in testo)
verifica("tabella equivalente", "| US-08 | US-01 (Giulia) | US-03 (Sara) | US-00, US-02 |" in testo)
verifica("punti completati", "Punti completati: 2" in testo)
verifica("nessun avviso con i limiti rispettati", avvisi == [])

_, avvisi = g.genera(BACKLOG, {"in corso": 0, "in revisione": 2})
verifica("limite superato segnalato", any("limite 0" in a for a in avvisi))
_, avvisi = g.genera(BACKLOG.replace("in revisione (Sara)", "in revisione"), {})
verifica("storia in revisione senza persona segnalata", avvisi == ["US-03 è in revisione ma non indica chi ci lavora"])
verifica("persona con apostrofo ripulita nei metadati",
         "assigned: 'DAmico'" in g.genera(BACKLOG.replace("Giulia", "D'Amico"), {})[0])

try:
    g.leggi_storie(BACKLOG.replace("da fare |\n| US-13", "sospesa |\n| US-13"))
    verifica("stato non valido rifiutato con numero di riga", False)
except g.ErroreBacklog as e:
    verifica("stato non valido rifiutato con numero di riga", str(e).startswith("riga 7"))
try:
    g.leggi_storie("# Backlog vuoto\n")
    verifica("backlog senza tabella", False)
except g.ErroreBacklog:
    verifica("backlog senza tabella", True)

with tempfile.TemporaryDirectory() as d:
    backlog = Path(d) / "backlog.md"
    board = Path(d) / "board.md"
    backlog.write_text(BACKLOG, encoding="utf-8")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = g.main([str(backlog), str(board), "--limite-in-corso", "1"])
    verifica("esecuzione: board scritta", codice == 0 and board.read_text(encoding="utf-8").startswith("# Board del team"))

print(f"\nTest superati: {superati}, falliti: {falliti}")
