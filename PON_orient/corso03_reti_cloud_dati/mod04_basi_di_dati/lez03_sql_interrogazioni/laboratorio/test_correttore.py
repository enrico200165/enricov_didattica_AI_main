"""Test di correttore.py. Esecuzione: python test_correttore.py
Richiede biblioteca.db nella stessa cartella (o nella cartella della lezione 4.1)."""

import os
import shutil
import tempfile

from correttore import dividi_esercizi, correggi, genera, impronta

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


DB = "biblioteca.db" if os.path.exists("biblioteca.db") else \
    os.path.join("..", "..", "lez01_dati_e_modello_relazionale", "laboratorio", "biblioteca.db")
cartella = tempfile.mkdtemp()


def scrivi(nome, testo):
    percorso = os.path.join(cartella, nome)
    with open(percorso, "w", encoding="utf-8") as f:
        f.write(testo)
    return percorso


e = dividi_esercizi("-- esercizio 1\n-- commento\nSELECT 1;\n\n-- esercizio 2 (ordinato)\nSELECT 2\n")
verifica("due blocchi, commenti rimossi, ordinamento letto",
         e == {1: ("SELECT 1;", False), 2: ("SELECT 2", True)})
verifica("impronta indipendente dall'ordine se non ordinato",
         impronta([(1,), (2,)], False) == impronta([(2,), (1,)], False))
verifica("impronta dipendente dall'ordine se ordinato",
         impronta([(1,), (2,)], True) != impronta([(2,), (1,)], True))

attesi = genera("soluzioni_esercizi_4_3.sql", os.path.join(cartella, "attesi.json"), DB)
verifica("impronte generate per 14 esercizi", len(attesi) == 14)
with open("attesi_4_3.json", encoding="utf-8") as f:
    import json
    verifica("attesi_4_3.json coincide con le soluzioni", json.load(f) == attesi)

risposte = scrivi("risposte.sql", """
-- esercizio 1
select anno, titolo from libri
-- esercizio 2
SELECT titolo, anno FROM libri WHERE genere = 'fantascienza' ORDER BY titolo;
-- esercizio 3 (ordinato)
SELECT titolo, anno FROM libri WHERE anno < 1900 ORDER BY anno DESC;
-- esercizio 4 (ordinato)
SELECT cognome, nome FROM studenti WHERE classe = '4A';
-- esercizio 5
SELECT nome, cognome, nazionalita FROM autori;
-- esercizio 6
SELECT titolo FROM libro WHERE titolo LIKE 'La %';
-- esercizio 7 (ordinato)
DELETE FROM libri;
""")
esiti = correggi(risposte, "attesi_4_3.json", DB)
verifica("colonne in ordine diverso: valori diversi", esiti[1] == "valori diversi da quelli attesi")
verifica("ordine non richiesto: corretto anche con ORDER BY", esiti[2] == "corretto")
verifica("ordine sbagliato riconosciuto", esiti[3] == "righe giuste, ordine sbagliato")
verifica("righe giuste senza ORDER BY: in genere ordine sbagliato o corretto per caso",
         esiti[4] in ("corretto", "righe giuste, ordine sbagliato"))
verifica("numero di righe diverso segnalato", esiti[5].startswith("righe: 15"))
verifica("errore SQL segnalato (tabella inesistente)", esiti[6].startswith("errore SQL"))
verifica("istruzioni diverse da SELECT rifiutate", "solo interrogazioni SELECT" in esiti[7])
verifica("esercizi senza risposta: mancante", esiti[14] == "mancante")

copia = os.path.join(cartella, "copia.db")
shutil.copy(DB, copia)
tentativo = scrivi("tentativo.sql", "-- esercizio 1\nWITH x AS (SELECT 1) DELETE FROM libri\n")
correggi(tentativo, "attesi_4_3.json", copia)
import sqlite3
verifica("database aperto in sola lettura: nessuna riga cancellata",
         sqlite3.connect(copia).execute("SELECT COUNT(*) FROM libri").fetchone()[0] == 29)
verifica("le soluzioni ottengono 14 su 14",
         list(correggi("soluzioni_esercizi_4_3.sql", "attesi_4_3.json", DB).values()).count("corretto") == 14)

shutil.rmtree(cartella, ignore_errors=True)
print(f"\nTest superati: {superati}, falliti: {falliti}")
