"""Test di priorita.py. Esecuzione: python test_priorita.py"""

import contextlib
import io
import shutil
import tempfile
from pathlib import Path

import priorita as p

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def storia(codice, moscow, valore, sforzo):
    return {"id": codice, "titolo": codice, "moscow": moscow, "valore": valore, "sforzo": sforzo}


storie = p.leggi_valutazioni("valutazioni_esempio.csv")
verifica("esempio: 15 storie lette", len(storie) == 15)
ordinate = p.ordina(storie)
verifica("esempio: prime tre le Must US-01, US-02, US-03", [s["id"] for s in ordinate[:3]] == ["US-01", "US-02", "US-03"])
verifica("esempio: ultima la Won't US-13", ordinate[-1]["id"] == "US-13")
verifica("esempio: quote di sforzo Must 17%, Should 33%, Could 50%", p.quote_sforzo(storie) == {"M": 17, "S": 33, "C": 50})

prova = [storia("A", "S", 2, 1), storia("B", "S", 4, 4), storia("C", "M", 1, 5), storia("D", "S", 4, 2)]
verifica("ordine: MoSCoW, poi valore/sforzo, a parità il valore più alto",
         [s["id"] for s in p.ordina(prova)] == ["C", "D", "A", "B"])
verifica("a parità di rapporto vince il valore più alto",
         [s["id"] for s in p.ordina([storia("X", "C", 2, 2), storia("Y", "C", 4, 4)])] == ["Y", "X"])
verifica("quota Must oltre il 60% calcolata",
         p.quote_sforzo([storia("A", "M", 5, 4), storia("B", "C", 1, 1), storia("W", "W", 1, 5)])["M"] == 80)

testo = p.matrice_mermaid([storia("US-01", "M", 5, 1), storia("US-02", "M", 5, 1)])
verifica("matrice: coordinate e punti uguali sfalsati",
         "US-01 M: [0.1, 0.9]" in testo and "US-02 M: [0.14, 0.86]" in testo)


def errore_con(contenuto):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "v.csv"
        f.write_text(contenuto, encoding="utf-8")
        try:
            p.leggi_valutazioni(f)
        except p.ErroreDati as e:
            return str(e)
    return ""


verifica("colonna mancante", "colonne mancanti: sforzo" in errore_con("id,titolo,moscow,valore\nUS-01,A,M,3\n"))
verifica("MoSCoW non valido con numero di riga", errore_con("id,titolo,moscow,valore,sforzo\nUS-01,A,X,3,2\n").startswith("riga 2"))
verifica("valore fuori intervallo", "tra 1 e 5" in errore_con("id,titolo,moscow,valore,sforzo\nUS-01,A,M,7,2\n"))
verifica("valore non numerico", "numeri interi" in errore_con("id,titolo,moscow,valore,sforzo\nUS-01,A,M,alto,2\n"))
verifica("id ripetuto", "US-01 ripetuto" in errore_con("id,titolo,moscow,valore,sforzo\nUS-01,A,M,3,2\nUS-01,B,S,3,2\n"))
verifica("MoSCoW scritto per esteso accettato",
         errore_con("id,titolo,moscow,valore,sforzo\nUS-01,A,Must,3,2\n") == "")

kit = Path(__file__).resolve().parents[3] / "mod01_progetti_e_team" / "lez03_kit_di_progetto_e_squadre" / "laboratorio" / "kit_prenotazioni" / "docs" / "backlog.md"
if not kit.exists():
    print("SALTATI i test sul backlog del kit: la cartella del corso non è completa (kit non trovato)")
else:
    with tempfile.TemporaryDirectory() as d:
        backlog = Path(d) / "backlog.md"
        shutil.copy(kit, backlog)
        shutil.copy("valutazioni_esempio.csv", d)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            codice = p.main([str(Path(d) / "valutazioni_esempio.csv"), "--backlog", str(backlog)])
        righe = [r for r in backlog.read_text(encoding="utf-8").splitlines() if r.startswith("| US-")]
        verifica("backlog: US-00 resta in cima, poi US-01 con priorità Must",
                 codice == 0 and righe[0].startswith("| US-00") and righe[1].startswith("| US-01 |")
                 and "| Must |" in righe[1])
        verifica("backlog: ultima riga US-13 Won't, 16 righe in tutto",
                 righe[-1].startswith("| US-13") and "Won't" in righe[-1] and len(righe) == 16)
        verifica("backlog: copia di sicurezza e diagramma creati",
                 (Path(d) / "backlog.md.bak").exists() and (Path(d) / "matrice_valore_sforzo.md").exists())
        verifica("backlog: sezioni delle storie non modificate",
                 backlog.read_text(encoding="utf-8").split("## Storie")[1] == kit.read_text(encoding="utf-8").split("## Storie")[1])
        (Path(d) / "extra.csv").write_text("id,titolo,moscow,valore,sforzo\nUS-99,X,M,3,2\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            codice = p.main([str(Path(d) / "extra.csv"), "--backlog", str(backlog)])
        verifica("backlog: storia del CSV assente dal backlog segnalata",
                 codice == 1 and "US-99" in out.getvalue())

print(f"\nTest superati: {superati}, falliti: {falliti}")
