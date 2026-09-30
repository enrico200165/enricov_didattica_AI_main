"""Test di pseudonimizza.py. Esecuzione: python test_pseudonimizza.py"""

import csv
import hashlib
import os
import tempfile

from pseudonimizza import pseudonimo, trasforma, gruppi_piccoli, leggi_o_crea_chiave, main

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


chiave1, chiave2 = b"\x01" * 32, b"\x02" * 32
verifica("stesso valore e stessa chiave: stesso pseudonimo", pseudonimo("S2026001", chiave1) == pseudonimo("S2026001", chiave1))
verifica("chiave diversa: pseudonimo diverso", pseudonimo("S2026001", chiave1) != pseudonimo("S2026001", chiave2))
verifica("matricole diverse: pseudonimi diversi", pseudonimo("S2026001", chiave1) != pseudonimo("S2026002", chiave1))
verifica("senza chiave, l'hash semplice non coincide con lo pseudonimo",
         hashlib.sha256(b"S2026001").hexdigest()[:12] != pseudonimo("S2026001", chiave1))

riga = {"matricola": "S2026001", "cognome": "Bianchi", "nome": "Riccardo",
        "email": "riccardo.bianchi1@studenti.scuola.example", "data_nascita": "2008-01-03",
        "comune": "Bologna", "classe": "4B", "media_informatica": "8.0", "assenze": "18"}
t = trasforma(riga, chiave1)
verifica("identificativi diretti eliminati", not {"nome", "cognome", "email", "matricola"} & set(t))
verifica("data di nascita generalizzata all'anno", t["anno_nascita"] == "2008" and "data_nascita" not in t)
verifica("dati per l'analisi conservati", t["media_informatica"] == "8.0" and t["assenze"] == "18")

righe = [{"anno_nascita": "2009", "comune": "Bologna", "classe": "4A"}] * 3 + \
        [{"anno_nascita": "2010", "comune": "Pianoro", "classe": "4A"}]
verifica("gruppo con una sola persona individuato", gruppi_piccoli(righe, 3) == {("2010", "Pianoro", "4A"): 1})

cartella = tempfile.mkdtemp()
file_chiave = os.path.join(cartella, "chiave.txt")
k1 = leggi_o_crea_chiave(file_chiave)
verifica("chiave creata di 32 byte e riletta uguale", len(k1) == 32 and leggi_o_crea_chiave(file_chiave) == k1)

uscita = os.path.join(cartella, "uscita.csv")
main("studenti_fittizi.csv", uscita, file_chiave)
with open(uscita, encoding="utf-8") as f:
    risultato = list(csv.DictReader(f))
with open(uscita, encoding="utf-8") as f:
    testo = f.read()
verifica("40 righe nel file pseudonimizzato", len(risultato) == 40)
verifica("nessun indirizzo email nel file", "@" not in testo)
verifica("pseudonimi tutti diversi", len({r["pseudonimo"] for r in risultato}) == 40)

print(f"Test superati: {superati}, falliti: {falliti}")
