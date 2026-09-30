"""Test di planning_poker.py. Esecuzione: python test_planning_poker.py"""

import contextlib
import io
import tempfile
from pathlib import Path

import planning_poker as pp

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


membri, ultimo = pp.leggi_stime("stime_esempio.csv")
verifica("esempio: quattro membri e cinque storie", len(membri) == 4 and len(ultimo) == 5)
verifica("esempio: per US-03 si usa l'ultimo giro", ultimo["US-03"] == {"Giulia": "3", "Marco": "3", "Sara": "3", "Davide": "5"})

verifica("accordo", pp.analizza({"A": "3", "B": "3"})[:2] == ("accordo", 3))
verifica("quasi accordo: la carta più alta", pp.analizza({"A": "3", "B": "5", "C": "3"})[:2] == ("quasi accordo", 5))
esito, stima, nota = pp.analizza({"A": "2", "B": "8", "C": "3", "D": "2"})
verifica("carte lontane: da discutere, spiegano minimo e massimo",
         esito == "da discutere" and stima is None and "A, D (2)" in nota and "B (8)" in nota)
esito, stima, nota = pp.analizza({"A": "5", "B": "?"})
verifica("punto interrogativo: da chiarire, con il nome", esito == "da chiarire" and nota.startswith("B"))
verifica("zero ammesso", pp.analizza({"A": "0", "B": "0"})[:2] == ("accordo", 0))


def con_file(contenuto, funzione):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "s.csv"
        f.write_text(contenuto, encoding="utf-8")
        return funzione(f, d)


def errore(contenuto):
    def prova(f, d):
        try:
            pp.leggi_stime(f)
        except pp.ErroreStime as e:
            return str(e)
        return ""
    return con_file(contenuto, prova)


verifica("carta non del mazzo", "carta \"4\"" in errore("storia,giro,A,B\nUS-01,1,3,4\n"))
verifica("intestazione sbagliata", "intestazione" in errore("id,giro,A\nUS-01,1,3\n"))
verifica("giro non numerico", errore("storia,giro,A\nUS-01,primo,3\n").startswith("riga 2"))


def esegui_con_backlog(f, d):
    backlog = Path(d) / "backlog.md"
    backlog.write_text("| ID | Titolo | Priorità | Stima | Stato |\n|---|---|---|---|---|\n"
                       "| US-01 | Uno | Must | | da fare |\n| US-02 | Due | Should | | da fare |\n", encoding="utf-8")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        codice = pp.main([str(f), "--velocita", "4", "--backlog", str(backlog)])
    return codice, out.getvalue(), backlog.read_text(encoding="utf-8"), (Path(d) / "backlog.md.bak").exists()


codice, testo, backlog, copia = con_file("storia,giro,A,B\nUS-01,1,3,3\nUS-02,1,1,8\n", esegui_con_backlog)
verifica("esecuzione: una storia stimata su due, un sprint con velocità 4",
         codice == 0 and "Storie stimate: 1 su 2; punti in tutto: 3" in testo and "servono 1 sprint" in testo)
verifica("backlog: stima scritta solo per la storia concordata",
         "| US-01 | Uno | Must | 3 | da fare |" in backlog and "| US-02 | Due | Should | | da fare |" in backlog)
verifica("backlog: copia di sicurezza creata", copia)
codice, testo, _, _ = con_file("storia,giro,A,B\nUS-01,1,13,13\n", esegui_con_backlog)
verifica("storia grande segnalata", "valutare se dividerla" in testo)

print(f"\nTest superati: {superati}, falliti: {falliti}")
