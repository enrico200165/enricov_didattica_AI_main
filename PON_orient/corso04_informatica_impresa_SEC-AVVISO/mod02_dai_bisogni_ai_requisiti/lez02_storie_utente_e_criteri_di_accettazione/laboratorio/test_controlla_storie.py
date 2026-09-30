"""Test di controlla_storie.py. Esecuzione: python test_controlla_storie.py"""

import contextlib
import io
import re
from pathlib import Path

import controlla_storie as c

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def per_storia(problemi, codice):
    return [(livello, m) for c_, livello, m in problemi if c_ == codice]


esercizio = Path("backlog_da_correggere.md").read_text(encoding="utf-8")
p = c.controlla(esercizio)
verifica("esercizio: US-01 e US-06 senza problemi di forma nelle storie",
         per_storia(p, "US-01") == [] and all("tabella" in m for _, m in per_storia(p, "US-06")))
verifica("esercizio: US-02 titolo diverso", ("ATTENZIONE", "titolo diverso tra tabella e sezione") in per_storia(p, "US-02"))
verifica("esercizio: US-02 criterio senza Dato e senza allora",
         {m for _, m in per_storia(p, "US-02")} >= {'criterio 1: non inizia con "Dato"', 'criterio 1: manca "allora"'})
verifica("esercizio: US-03 senza forma Come voglio per",
         any("Come ... voglio" in m for _, m in per_storia(p, "US-03")))
verifica("esercizio: US-04 criteri da scrivere", ("DA SISTEMARE", "criteri di accettazione da scrivere") in per_storia(p, "US-04"))
verifica("esercizio: US-05 storia lunga", any("storia lunga (41 parole)" in m for _, m in per_storia(p, "US-05")))
verifica("esercizio: US-06 senza riga in tabella",
         ("DA SISTEMARE", "sezione senza riga nella tabella di riepilogo") in per_storia(p, "US-06"))

kit = Path(__file__).resolve().parents[3] / "mod01_progetti_e_team" / "lez03_kit_di_progetto_e_squadre" / "laboratorio" / "kit_prenotazioni" / "docs" / "backlog.md"
if not kit.exists():
    print("SALTATI i test sul backlog del kit: la cartella del corso non è completa (kit non trovato)")
else:
    testo_kit = kit.read_text(encoding="utf-8")
    p = c.controlla(testo_kit)
    verifica("kit: US-00 del kit non richiede una sezione", per_storia(p, "US-00") == [])
    verifica("kit: US-01 e US-02 pronte", per_storia(p, "US-01") == [] and per_storia(p, "US-02") == [])
    verifica("kit: 13 storie con criteri da scrivere",
             sum(1 for _, _, m in p if m == "criteri di accettazione da scrivere") == 13)

    # criteri delle soluzioni del docente inseriti nel backlog del kit: devono risultare corretti
    soluzioni = Path("soluzioni_docente.md").read_text(encoding="utf-8")
    completato = testo_kit
    for codice in ("US-03", "US-04", "US-05", "US-06"):
        blocco = re.search(r"### " + codice + r"[^\n]*\n\n((?:- [^\n]+\n)+)", soluzioni).group(1)
        completato = re.sub(r"(### " + codice + r"[^\n]*\n\n[^\n]+\n\n)Criteri di accettazione: da scrivere[^\n]*\n",
                            lambda m: m.group(1) + "Criteri di accettazione:\n\n" + blocco, completato)
    p = c.controlla(completato)
    verifica("criteri delle soluzioni: US-03...US-06 senza problemi",
             all(per_storia(p, k) == [] for k in ("US-03", "US-04", "US-05", "US-06")))

verifica("criterio con Data e Quando maiuscolo accettato",
         c.controlla_criterio("- Data la prenotazione 3, Quando la cancello, Allora sparisce.") == [])
verifica("criterio con parola vaga", c.controlla_criterio("- Dato X, quando Y, allora funziona bene.") == ["parole vaghe: bene"])

doppio = "| US-01 | A | | | da fare |\n| US-01 | A | | | da fare |\n### US-01 A\n\nCome x voglio y per z.\n\nCriteri di accettazione:\n\n- Dato a, quando b, allora c.\n- Dato d, quando e, allora f.\n"
verifica("codice ripetuto in tabella", ("US-01", "DA SISTEMARE", "codice ripetuto") in c.controlla(doppio))

molti = doppio.split("\n| US-01")[0] + "\n### US-01 A\n\nCome x voglio y per z.\n\nCriteri di accettazione:\n\n" + "- Dato a, quando b, allora c.\n" * 7
verifica("troppi criteri: attenzione", ("US-01", "ATTENZIONE", "7 criteri: valutare se dividere la storia") in c.controlla(molti))

out = io.StringIO()
with contextlib.redirect_stdout(out):
    codice = c.main(["backlog_da_correggere.md"])
verifica("esecuzione: riepilogo e codice di uscita 1",
         codice == 1 and "Storie: 6; pronte: 2; da sistemare: 4" in out.getvalue())

print(f"\nTest superati: {superati}, falliti: {falliti}")
