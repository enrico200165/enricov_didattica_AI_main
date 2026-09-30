"""Test di preventivo.py. Esecuzione: python test_preventivo.py"""

import contextlib
import io
import json
import tempfile
from pathlib import Path

import preventivo as pv

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


attivita, tariffe = pv.leggi("attivita_preventivo.csv", "tariffe_esempio.json")
voci = pv.calcola(attivita, tariffe, 15, 10)
verifica("esempio: 36 giorni-persona e costo 13.940 euro", voci["giorni"] == 36 and voci["costo"] == 13940)
verifica("esempio: giorni dell'analista sommati tra più attività", voci["per_ruolo"]["analista"]["giorni"] == 9)
verifica("esempio: riserva 2.091, margine 1.603,10", voci["riserva"] == 2091 and voci["margine"] == 1603.10)
verifica("esempio: imponibile 17.634,10, IVA 3.879,50, totale 21.513,60",
         (voci["imponibile"], voci["iva"], voci["totale"]) == (17634.10, 3879.50, 21513.60))

c = pv.confronta_contratti(voci, 30, 10)
verifica("scostamento 30%: a corpo il fornitore perde 487,90", c["a_corpo"] == (17634.10, -487.90))
verifica("scostamento 30%: a tempo e materiali il cliente paga 19.934,20", c["tempo_materiali"] == (19934.20, 1812.20))
c = pv.confronta_contratti(voci, 0, 10)
verifica("nessuno scostamento: a corpo il fornitore guadagna riserva e margine",
         c["a_corpo"][1] == round(voci["riserva"] + voci["margine"], 2))

verifica("formato italiano degli importi", pv.euro(1234567.5) == "1.234.567,50 euro" and pv.euro(-487.9) == "-487,90 euro")


def errore(csv_testo, tariffe_dict=None):
    with tempfile.TemporaryDirectory() as d:
        a = Path(d) / "a.csv"
        t = Path(d) / "t.json"
        a.write_text("attivita,ruolo,giorni\n" + csv_testo, encoding="utf-8")
        t.write_text(json.dumps(tariffe_dict or {"sviluppatore": 300}), encoding="utf-8")
        try:
            pv.leggi(a, t)
        except pv.ErrorePreventivo as e:
            return str(e)
    return ""


verifica("ruolo senza tariffa", "nessuna tariffa per il ruolo \"grafico\"" in errore("Logo,grafico,2\n"))
verifica("giorni con la virgola accettati", errore("Codice,sviluppatore,\"2,5\"\n") == "")
verifica("giorni non numerici", errore("Codice,sviluppatore,tre\n").startswith("riga 2"))
verifica("giorni non positivi", "positivi" in errore("Codice,sviluppatore,0\n"))
verifica("nessuna attività", "nessuna attività" in errore(""))

out = io.StringIO()
with contextlib.redirect_stdout(out):
    codice = pv.main(["attivita_preventivo.csv", "tariffe_esempio.json", "--scostamento", "30"])
verifica("esecuzione: totale e confronto dei contratti",
         codice == 0 and "21.513,60 euro" in out.getvalue() and "-487,90 euro" in out.getvalue())

print(f"\nTest superati: {superati}, falliti: {falliti}")
