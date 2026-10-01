"""Test di confronta_percorsi.py. Esecuzione: python test_confronta_percorsi.py"""

import contextlib
import io
import tempfile
from pathlib import Path

import confronta_percorsi as cp

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


criteri, problemi_criteri = cp.leggi_criteri("criteri_esempio.csv")
percorsi, problemi = cp.leggi_percorsi("percorsi_esempio.csv", criteri)
verifica("esempio: 5 criteri, 2 percorsi, nessun problema da sistemare",
         len(criteri) == 5 and len(percorsi) == 2 and problemi_criteri == []
         and all(livello == "ATTENZIONE" for livello, _ in problemi))
verifica("esempio: quattro fonti senza indirizzo web segnalate", len(problemi) == 4)
pesi = {c: p for c, (p, _) in criteri.items()}
classifica = cp.totali(percorsi, pesi)
verifica("esempio: totali 50 e 48, in testa l'ITS",
         list(classifica.values()) == [50, 48] and cp.primo(classifica).startswith("ITS"))
verifica("esempio: la scelta dipende dai pesi di pratica e interesse",
         cp.sensibilita(percorsi, criteri) == ["pratica", "interesse"])
verifica("pareggio: nessun percorso in testa", cp.primo({"A": 10, "B": 10}) is None)

netto = {"A": {"x": ("i", "https://a", 5)}, "B": {"x": ("i", "https://b", 1)}}
verifica("differenza netta: scelta stabile", cp.sensibilita(netto, {"x": (3, "")}) == [])


def problemi_di(testo_percorsi, testo_criteri="criterio,peso,domanda\ndurata,2,?\ncosto,3,?\n"):
    with tempfile.TemporaryDirectory() as cartella:
        fc, fp = Path(cartella) / "c.csv", Path(cartella) / "p.csv"
        fc.write_text(testo_criteri, encoding="utf-8")
        fp.write_text("percorso,criterio,informazione,fonte,punteggio\n" + testo_percorsi, encoding="utf-8")
        criteri_prova, pc = cp.leggi_criteri(fc)
        return pc + cp.leggi_percorsi(fp, criteri_prova)[1]


trovati = problemi_di("A,durata,...,https://x,3\nA,costo,basso,,6\nB,durata,2 anni,https://y,4\nB,prezzo,x,https://y,2\n")
messaggi = " | ".join(m for _, m in trovati)
verifica("informazione da completare", "A, durata: informazione da completare" in messaggi)
verifica("fonte mancante", "A, costo: manca la fonte" in messaggi)
verifica("punteggio fuori intervallo", "A, costo: il punteggio deve essere da 1 a 5" in messaggi)
verifica("criterio sconosciuto e criterio mancante",
         "criterio \"prezzo\" non presente" in messaggi and "B: manca il criterio \"costo\"" in messaggi)
verifica("peso non valido", any("il peso di \"durata\"" in m for _, m in
                                 problemi_di("", "criterio,peso,domanda\ndurata,8,?\n")))
verifica("un solo percorso", any("almeno due percorsi" in m for _, m in problemi_di("A,durata,x,https://x,3\nA,costo,x,https://x,3\n")))

testo = cp.scheda_markdown(criteri, percorsi, classifica, ["pratica", "interesse"])
verifica("scheda: tabella con totali, fonti, stabilità",
         "| **Totale** | **50** su 65 | **48** su 65 |" in testo and testo.count("\n- ") == 10
         and "pratica, interesse" in testo)

with tempfile.TemporaryDirectory() as cartella:
    scheda = Path(cartella) / "confronto.md"
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = cp.main(["criteri_esempio.csv", "percorsi_esempio.csv", "--scheda", str(scheda)])
    verifica("esecuzione: classifica e scheda", codice == 0 and scheda.exists()
             and "Criteri da cui dipende la scelta: pratica, interesse" in out.getvalue())

with tempfile.TemporaryDirectory() as cartella:
    fp = Path(cartella) / "p.csv"
    fp.write_text("percorso,criterio,informazione,fonte,punteggio\nA,durata,...,,3\n", encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()) as out:
        codice = cp.main(["criteri_esempio.csv", str(fp)])
verifica("problemi da sistemare: confronto non calcolato", codice == 1 and "non calcolato" in out.getvalue())

print(f"\nTest superati: {superati}, falliti: {falliti}")
