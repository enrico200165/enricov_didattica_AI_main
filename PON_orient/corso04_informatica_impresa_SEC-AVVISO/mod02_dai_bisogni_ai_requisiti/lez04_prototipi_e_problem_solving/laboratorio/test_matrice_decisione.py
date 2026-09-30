"""Test di matrice_decisione.py. Esecuzione: python test_matrice_decisione.py"""

import contextlib
import io
import tempfile
from pathlib import Path

import matrice_decisione as m

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


opzioni, criteri = m.leggi_matrice("matrice_esempio.csv")
verifica("esempio: due opzioni e sei criteri", len(opzioni) == 2 and len(criteri) == 6)
verifica("esempio: totali 81 e 67", m.totali(criteri, 2) == [81, 67])
verifica("esempio: vince la prima opzione", m.vincente([81, 67]) == 0)
verifica("esempio: nessun cambio modificando un solo peso", m.sensibilita(opzioni, criteri) == [])
verifica("parità riconosciuta", m.vincente([40, 40, 10]) is None)

vicini = [("Costo", 3, [4, 3]), ("Tempo", 2, [2, 4])]
verifica("totali di un caso vicino: 16 e 17", m.totali(vicini, 2) == [16, 17])
cambi = m.sensibilita(["A", "B"], vicini)
verifica("sensibilità: con peso 1 per Tempo vince A", ("Tempo", 1, "A") in cambi)
verifica("sensibilità: con peso 4 per Costo parità, con peso 5 vince A",
         ("Costo", 4, "parità") in cambi and ("Costo", 5, "A") in cambi)
verifica("sensibilità: parità indicata", any(r == "parità" for _, _, r in m.sensibilita(["A", "B"], [("X", 2, [3, 2]), ("Y", 2, [2, 4])])))


def errore_con(contenuto):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "m.csv"
        f.write_text(contenuto, encoding="utf-8")
        try:
            m.leggi_matrice(f)
        except m.ErroreMatrice as e:
            return str(e)
    return ""


verifica("intestazione sbagliata", "intestazione" in errore_con("nome,importanza,A,B\nX,3,1,2\n"))
verifica("una sola opzione", "almeno due opzioni" in errore_con("criterio,peso,A\nX,3,1\n"))
verifica("valore mancante con numero di riga", errore_con("criterio,peso,A,B\nX,3,1\n").startswith("riga 2"))
verifica("punteggio fuori intervallo", "tra 1 e 5" in errore_con("criterio,peso,A,B\nX,3,1,6\n"))
verifica("punteggio non numerico", "numeri interi" in errore_con("criterio,peso,A,B\nX,3,alto,2\n"))
verifica("righe vuote ignorate", errore_con("criterio,peso,A,B\n\nX,3,1,2\n\n") == "")

out = io.StringIO()
with contextlib.redirect_stdout(out):
    codice = m.main(["matrice_esempio.csv"])
testo = out.getvalue()
verifica("esecuzione: risultato con distacco e percentuale",
         codice == 0 and "Risultato: Comandi con argomenti, con 14 punti di distacco (13% del massimo)." in testo)
with tempfile.TemporaryDirectory() as d:
    f = Path(d) / "vicino.csv"
    f.write_text("criterio,peso,A,B\nCosto,3,4,3\nTempo,2,2,4\n", encoding="utf-8")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        m.main([str(f)])
verifica("esecuzione: distacco minimo e sensibilità segnalati",
         "ATTENZIONE: distacco minimo" in out.getvalue() and 'peso 1 per "Tempo": A' in out.getvalue())

print(f"\nTest superati: {superati}, falliti: {falliti}")
