"""Test di converti_formati.py. Esecuzione: python test_converti_formati.py
Richiede biblioteca.db (lezione 4.1) nella cartella corrente."""

import csv
import json
import os
import tempfile
import xml.etree.ElementTree as ET

import converti_formati as cf

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


documenti = cf.leggi_documenti()
verifica("29 documenti, uno per libro", len(documenti) == 29)
primo = documenti[0]
verifica("autore annidato nel documento", primo["autore"]["cognome"] == "Manzoni")
verifica("copie annidate: 3 per I promessi sposi", [c["collocazione"] for c in primo["copie"]] == ["A1-1", "A1-2", "A1-3"])
verifica("totale copie nei documenti = 46", sum(len(d["copie"]) for d in documenti) == 46)

cartella = tempfile.mkdtemp()
p_csv, p_json, p_xml = (os.path.join(cartella, n) for n in ("l.csv", "l.json", "l.xml"))
cf.scrivi_csv(documenti, p_csv)
cf.scrivi_json(documenti, p_json)
cf.scrivi_xml(documenti, p_xml)

with open(p_csv, newline="", encoding="utf-8") as f:
    righe = list(csv.DictReader(f))
verifica("CSV: intestazione e 29 righe", len(righe) == 29 and righe[0]["numero_copie"] == "3")
verifica("CSV: virgola nel titolo gestita con le virgolette",
         any(r["titolo"] == "Uno, nessuno e centomila" for r in righe))
with open(p_json, encoding="utf-8") as f:
    testo_json = f.read()
verifica("JSON: lettere accentate scritte in chiaro", "Se questo è un uomo" in testo_json)
verifica("JSON: riletto uguale ai documenti", json.loads(testo_json) == documenti)
radice = ET.parse(p_xml).getroot()
verifica("XML: 29 elementi libro con attributo id", len(radice.findall("libro")) == 29 and radice[0].get("id") == "1")
verifica("XML: lettura di titolo e numero di copie", cf.leggi_xml(p_xml)[0] == ("I promessi sposi", 3))

autori, libri, copie = cf.tabelle_da_documenti(documenti)
verifica("dai documenti: 14 autori senza ripetizioni (Deledda non ha libri)", len(autori) == 14)
verifica("tabelle ricostruite uguali al database", cf.confronta_con_database(documenti))

codifica, righe = cf.leggi_csv_excel("titoli_excel.csv")
verifica("CSV di Excel: Windows-1252 e separatore ';' riconosciuti",
         codifica == "cp1252" and righe[0]["Titolo"] == "Le città invisibili")
verifica("CSV UTF-8 con separatore ',' riconosciuto", cf.leggi_csv_excel(p_csv)[0] == "utf-8-sig")
verifica("stesso testo: 23 byte in UTF-8, 19 in Windows-1252",
         len("perché città è così".encode("utf-8")) == 23 and len("perché città è così".encode("cp1252")) == 19)

print(f"\nTest superati: {superati}, falliti: {falliti}")
