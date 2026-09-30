"""Test di controlla_schema.py. Esecuzione: python test_controlla_schema.py"""

from controlla_schema import controlla, dividi_istruzioni, mermaid

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


with open("soluzione_schema.sql", encoding="utf-8") as f:
    schema = f.read()
with open("dati_prova.sql", encoding="utf-8") as f:
    dati = f.read()

r = controlla(schema, dati)
s = r["struttura"]
verifica("otto tabelle nell'ordine di creazione", list(s) == ["editori", "autori", "libri", "libri_autori",
                                                             "copie", "utenti", "prestiti", "prenotazioni"])
verifica("chiave primaria composta di libri_autori", s["libri_autori"]["pk"] == ["id_libro", "id_autore"])
verifica("chiavi esterne di prestiti", sorted(fk[1] for fk in s["prestiti"]["fk"]) == ["copie", "utenti"])
verifica("schema senza problemi", r["problemi"] == [])
verifica("11 istruzioni accettate e 5 rifiutate", (r["dati_validi"], len(r["dati_rifiutati"])) == (11, 5))
motivi = " ".join(m for _, m in r["dati_rifiutati"])
verifica("rifiuti per UNIQUE, FOREIGN KEY e CHECK",
         all(x in motivi for x in ("UNIQUE", "FOREIGN KEY", "CHECK")))

difettoso = """
CREATE TABLE a (x INTEGER, y TEXT);
CREATE TABLE b (id INTEGER PRIMARY KEY, id_c INTEGER REFERENCES c(id));
CREATE TABLE d (id INTEGER PRIMARY KEY, y TEXT REFERENCES a(y));
"""
p = controlla(difettoso)["problemi"]
verifica("tabella senza chiave primaria segnalata", "a: nessuna chiave primaria" in p)
verifica("tabella riferita inesistente segnalata", any("'c' non esiste" in x for x in p))
verifica("colonna riferita non unica segnalata", any("a.y" in x for x in p))

verifica("divisione delle istruzioni con ';' dentro una stringa",
         len(dividi_istruzioni("INSERT INTO t VALUES ('a;b');\n-- commento\nINSERT INTO t VALUES (2);\n")) == 2)
testo = mermaid(s)
verifica("diagramma Mermaid con relazione libri -> copie",
         testo.startswith("erDiagram") and 'libri ||--o{ copie : "id_libro"' in testo)
verifica("attributi PK e FK nel diagramma", "INTEGER id_libro PK,FK" in testo)

print(f"\nTest superati: {superati}, falliti: {falliti}")
