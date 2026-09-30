"""Test di controlla_consegna.py. Esecuzione: python test_controlla_consegna.py"""

import os
import shutil
import tempfile

from controlla_consegna import controlla

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def scrivi(cartella, nome, testo):
    with open(os.path.join(cartella, nome), "w", encoding="utf-8") as f:
        f.write(testo)


def consegna_completa():
    c = tempfile.mkdtemp()
    scrivi(c, "relazione.md", "# Progetto\n## Requisiti\n## Rete\n## Dati\n## Servizio\n"
                              "## Cloud\nCosto stimato 180 euro al mese, disponibilità 99,9 %.\n## Responsabilità\n")
    with open("modello_presentazione_marp.md", encoding="utf-8") as f:
        scrivi(c, "presentazione.md", f.read())
    drawio = '<mxfile host="vscode"><diagram name="p"><mxGraphModel><root><mxCell id="0"/></root></mxGraphModel></diagram></mxfile>'
    scrivi(c, "rete.drawio", drawio)
    scrivi(c, "architettura.drawio", drawio)
    scrivi(c, "schema.sql", "CREATE TABLE a (id INTEGER PRIMARY KEY);\nCREATE TABLE b (id INTEGER PRIMARY KEY, "
                            "id_a INTEGER REFERENCES a(id));\nCREATE TABLE c (id INTEGER PRIMARY KEY);\n")
    scrivi(c, "piano_indirizzi.csv", "nome,rete\nuffici,10.1.0.0/24\nospiti,10.1.1.0/24\n")
    return c


c = consegna_completa()
verifica("consegna completa: nessun problema", controlla(c) == [])
verifica("il modello di presentazione fornito ha almeno 6 slide", not any("slide" in p for p in controlla(c)))

os.remove(os.path.join(c, "rete.drawio"))
verifica("file mancante segnalato", controlla(c) == ["manca rete.drawio"])
shutil.rmtree(c)

c = consegna_completa()
scrivi(c, "relazione.md", "# Progetto\n## Requisiti\n## Rete\n## Dati\n")
p = controlla(c)
verifica("sezioni mancanti della relazione segnalate", sum("manca una sezione" in x for x in p) == 3)
verifica("costo e disponibilità mancanti segnalati", any("euro" in x for x in p) and any("percentuale" in x for x in p))
shutil.rmtree(c)

c = consegna_completa()
scrivi(c, "architettura.drawio", "<mxfile><diagram>")
scrivi(c, "schema.sql", "CREATE TABLE a (x TEXT);\nCREATE TABLE b (id INTEGER PRIMARY KEY);\nCREATE TABLE c (id INTEGER PRIMARY KEY);\n")
scrivi(c, "piano_indirizzi.csv", "nome,rete\nuno,10.1.0.0/23\ndue,10.1.1.0/24\ntre,10.1.2.5/24\n")
p = controlla(c)
verifica("file Draw.io non valido", any("architettura.drawio: non è un file XML valido" in x for x in p))
verifica("tabella senza chiave primaria", any("tabella a non ha chiave primaria" in x for x in p))
verifica("reti sovrapposte", any("si sovrappone" in x for x in p))
verifica("rete con bit di host", any("rete non valida 10.1.2.5/24" in x for x in p))
scrivi(c, "schema.sql", "CREATE TABLE a (id INTEGER PRIMARY KEY;\n")
verifica("errore di sintassi SQL", any("errore SQL" in x for x in controlla(c)))
scrivi(c, "presentazione.md", "## una sola slide\n")
verifica("presentazione senza intestazione Marp", any("marp: true" in x for x in controlla(c)))
shutil.rmtree(c)

print(f"\nTest superati: {superati}, falliti: {falliti}")
