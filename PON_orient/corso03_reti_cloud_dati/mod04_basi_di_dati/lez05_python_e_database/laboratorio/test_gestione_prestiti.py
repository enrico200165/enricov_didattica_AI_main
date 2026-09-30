"""Test di gestione_prestiti.py. Esecuzione: python test_gestione_prestiti.py
Lavora su una copia temporanea di biblioteca.db (cartella corrente o lezione 4.1)."""

import os
import shutil
import tempfile

import gestione_prestiti as g

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


originale = "biblioteca.db" if os.path.exists("biblioteca.db") else \
    os.path.join("..", "..", "lez01_dati_e_modello_relazionale", "laboratorio", "biblioteca.db")
cartella = tempfile.mkdtemp()
copia = os.path.join(cartella, "biblioteca.db")
shutil.copy(originale, copia)
c = g.connetti(copia)


def conta():
    return c.execute("SELECT COUNT(*) FROM prestiti").fetchone()[0]


importati, errori = g.importa(c, "nuovi_prestiti_errati.csv")
verifica("file con errori: nessun prestito importato", importati == 0 and conta() == 200)
verifica("cinque errori, uno per ogni riga non valida", len(errori) == 5)
testo = " ".join(errori)
verifica("errori riconosciuti: in prestito, collocazione, studente, data, smarrita",
         all(x in testo for x in ("già in prestito", "Z9-9", "codice 99", "data non valida", "smarrita")))
verifica("numero di riga del file indicato", errori[0].startswith("riga 3:"))

importati, errori = g.importa(c, "nuovi_prestiti.csv")
verifica("file corretto: 5 prestiti importati", (importati, errori, conta()) == (5, [], 205))
ultimo = c.execute("SELECT * FROM prestiti ORDER BY id_prestito DESC LIMIT 1").fetchone()
verifica("scadenza calcolata a 30 giorni", (ultimo["data_prestito"], ultimo["data_scadenza"]) == ("2026-06-12", "2026-07-12"))
verifica("stesso file una seconda volta: copie già in prestito, nulla importato",
         g.importa(c, "nuovi_prestiti.csv")[0] == 0 and conta() == 205)

doppia = os.path.join(cartella, "doppia.csv")
with open(doppia, "w", encoding="utf-8") as f:
    f.write("collocazione,id_studente,data_prestito\nA4-1,1,2026-06-20\nA4-1,2,2026-06-20\n")
importati, errori = g.importa(c, doppia)
verifica("stessa copia due volte nello stesso file: rifiutata", importati == 0 and "già in prestito" in errori[0])

verifica("ricerca con parametro", g.cerca_titolo(c, "rosa") == ["Il nome della rosa"])
verifica("testo con apici trattato come testo, non come SQL", g.cerca_titolo(c, "' OR '1'='1") == [])
verifica("apostrofo nel titolo cercato correttamente", g.cerca_titolo(c, "L'isola") == ["L'isola di Arturo"])

r = g.dati_rapporto(c, "2026-06-15")
verifica("rapporto: 205 prestiti, 22 in corso", (r["prestiti_totali"], r["in_corso"]) == (205, 22))
verifica("rapporto: libro più prestato", r["piu_prestati"][0]["titolo"] == "Se questo è un uomo")
verifica("rapporto: 5 prestiti scaduti al 15 giugno, ritardo calcolato",
         len(r["scaduti"]) == 5 and r["scaduti"][0]["giorni"] == 194)
percorso = os.path.join(cartella, "rapporto.md")
g.scrivi_rapporto(r, percorso)
with open(percorso, encoding="utf-8") as f:
    contenuto = f.read()
verifica("file Markdown con titolo e tre tabelle",
         contenuto.startswith("# Rapporto della biblioteca al 2026-06-15") and sum(r.startswith("|---") for r in contenuto.splitlines()) == 3)

c.close()
shutil.rmtree(cartella, ignore_errors=True)
print(f"\nTest superati: {superati}, falliti: {falliti}")
