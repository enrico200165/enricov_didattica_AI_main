"""Gli stessi dati in tre formati (CSV, JSON, XML) e in due modelli (tabelle e documenti).

Dal database relazionale biblioteca.db (Modulo 4) lo script produce:
- libri.csv           una riga per libro, dati "appiattiti"
- libri.json          un documento per libro, con l'autore e le copie annidati
- libri.xml           gli stessi documenti in XML
Poi ricostruisce le tabelle dai documenti JSON e verifica che coincidano con l'originale.

Uso:
    python converti_formati.py              esporta e verifica
    python converti_formati.py --codifiche  mostra i byte di un testo con accenti in UTF-8 e Windows-1252
    python converti_formati.py --excel titoli_excel.csv   legge un CSV salvato da Excel
"""

import csv
import json
import os
import sqlite3
import sys
import xml.etree.ElementTree as ET

DATABASE = "biblioteca.db"


def leggi_documenti(percorso_db=DATABASE):
    """Un documento (dizionario) per libro: autore e copie annidati, come in un database a documenti."""
    connessione = sqlite3.connect(percorso_db)
    connessione.row_factory = sqlite3.Row
    documenti = []
    for libro in connessione.execute("""
            SELECT l.id_libro, l.titolo, l.genere, l.anno, a.id_autore, a.nome, a.cognome, a.nazionalita
            FROM libri AS l JOIN autori AS a ON l.id_autore = a.id_autore ORDER BY l.id_libro"""):
        copie = connessione.execute(
            "SELECT id_copia, collocazione, stato FROM copie WHERE id_libro = ? ORDER BY id_copia",
            (libro["id_libro"],)).fetchall()
        documenti.append({
            "id": libro["id_libro"],
            "titolo": libro["titolo"],
            "genere": libro["genere"],
            "anno": libro["anno"],
            "autore": {"id": libro["id_autore"], "nome": libro["nome"],
                       "cognome": libro["cognome"], "nazionalita": libro["nazionalita"]},
            "copie": [dict(c) for c in copie],          # sqlite3.Row -> dizionario
        })
    connessione.close()
    return documenti


def scrivi_csv(documenti, percorso="libri.csv"):
    """CSV: una tabella piatta. Le copie diventano un conteggio e un elenco separato da '|'."""
    with open(percorso, "w", newline="", encoding="utf-8") as f:
        scrittore = csv.writer(f)
        scrittore.writerow(["id", "titolo", "genere", "anno", "autore", "numero_copie", "collocazioni"])
        for d in documenti:
            scrittore.writerow([d["id"], d["titolo"], d["genere"], d["anno"],
                                f"{d['autore']['nome']} {d['autore']['cognome']}",
                                len(d["copie"]), "|".join(c["collocazione"] for c in d["copie"])])


def scrivi_json(documenti, percorso="libri.json"):
    with open(percorso, "w", encoding="utf-8") as f:
        # ensure_ascii=False: le lettere accentate restano leggibili invece di diventare è
        json.dump(documenti, f, ensure_ascii=False, indent=2)


def scrivi_xml(documenti, percorso="libri.xml"):
    radice = ET.Element("biblioteca")
    for d in documenti:
        libro = ET.SubElement(radice, "libro", id=str(d["id"]))       # attributo dell'elemento
        ET.SubElement(libro, "titolo").text = d["titolo"]
        ET.SubElement(libro, "genere").text = d["genere"]
        ET.SubElement(libro, "anno").text = str(d["anno"])
        autore = ET.SubElement(libro, "autore", id=str(d["autore"]["id"]))
        ET.SubElement(autore, "nome").text = d["autore"]["nome"]
        ET.SubElement(autore, "cognome").text = d["autore"]["cognome"]
        copie = ET.SubElement(libro, "copie")
        for c in d["copie"]:
            ET.SubElement(copie, "copia", id=str(c["id_copia"]), collocazione=c["collocazione"], stato=c["stato"])
    albero = ET.ElementTree(radice)
    ET.indent(albero)                                   # rientri per la leggibilità
    albero.write(percorso, encoding="utf-8", xml_declaration=True)


def leggi_xml(percorso="libri.xml"):
    """Esempio di lettura: titolo e numero di copie di ogni libro."""
    radice = ET.parse(percorso).getroot()
    return [(libro.findtext("titolo"), len(libro.find("copie"))) for libro in radice.findall("libro")]


def tabelle_da_documenti(documenti):
    """Operazione inversa: dai documenti annidati alle tabelle relazionali (senza ripetizioni)."""
    autori, libri, copie = {}, [], []
    for d in documenti:
        a = d["autore"]
        autori[a["id"]] = (a["id"], a["nome"], a["cognome"], a["nazionalita"])   # ogni autore una volta sola
        libri.append((d["id"], d["titolo"], a["id"], d["genere"], d["anno"]))
        copie += [(c["id_copia"], d["id"], c["collocazione"], c["stato"]) for c in d["copie"]]
    return sorted(autori.values()), libri, copie


def confronta_con_database(documenti, percorso_db=DATABASE):
    """True se le tabelle ricostruite coincidono con quelle del database (autori che hanno libri)."""
    autori, libri, copie = tabelle_da_documenti(documenti)
    c = sqlite3.connect(percorso_db)
    originali = (
        c.execute("SELECT * FROM autori WHERE id_autore IN (SELECT id_autore FROM libri) ORDER BY id_autore")
         .fetchall(),
        c.execute("SELECT * FROM libri ORDER BY id_libro").fetchall(),
        c.execute("SELECT * FROM copie ORDER BY id_copia").fetchall(),
    )
    c.close()
    ricostruite = ([a[:4] for a in autori], libri, sorted(copie))
    # anno_nascita non è stato esportato: si confrontano le prime quattro colonne degli autori
    return ([a[:4] for a in originali[0]], originali[1], originali[2]) == ricostruite


def leggi_csv_excel(percorso):
    """Legge un CSV salvato da Excel in italiano: separatore ';' e codifica non sempre UTF-8.

    Prova prima UTF-8 (anche con il segno iniziale BOM, 'utf-8-sig'), poi Windows-1252;
    il separatore viene riconosciuto da csv.Sniffer. Restituisce (codifica, righe come dizionari).
    """
    with open(percorso, "rb") as f:
        dati = f.read()
    for codifica in ("utf-8-sig", "cp1252"):
        try:
            testo = dati.decode(codifica)
            break
        except UnicodeDecodeError:          # byte non validi in questa codifica: si prova la successiva
            continue
    dialetto = csv.Sniffer().sniff(testo.splitlines()[0], delimiters=";,")
    return codifica, list(csv.DictReader(testo.splitlines(), dialect=dialetto))


def mostra_codifiche(testo="perché città è così"):
    print(f"Testo: {testo}  ({len(testo)} caratteri)")
    for codifica in ("utf-8", "cp1252"):
        dati = testo.encode(codifica)
        print(f"{codifica:>7}: {len(dati)} byte  {dati.hex(' ')}")
    sbagliato = testo.encode("utf-8").decode("cp1252")
    print(f"Byte UTF-8 letti come Windows-1252: {sbagliato}")


def main(argomenti):
    if argomenti == ["--codifiche"]:
        mostra_codifiche()
        return
    if len(argomenti) == 2 and argomenti[0] == "--excel":
        codifica, righe = leggi_csv_excel(argomenti[1])
        print(f"Codifica riconosciuta: {codifica}; righe: {len(righe)}")
        for r in righe:
            print(" ", r)
        return
    documenti = leggi_documenti()
    scrivi_csv(documenti)
    scrivi_json(documenti)
    scrivi_xml(documenti)
    for nome in ("libri.csv", "libri.json", "libri.xml"):
        print(f"{nome:<12}{os.path.getsize(nome):>7} byte")
    print("Primo libro dal file XML:", leggi_xml()[0])
    print("Tabelle ricostruite dai documenti JSON uguali all'originale:",
          "sì" if confronta_con_database(json.load(open("libri.json", encoding="utf-8"))) else "NO")


if __name__ == "__main__":
    main(sys.argv[1:])
