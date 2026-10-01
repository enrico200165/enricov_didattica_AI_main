"""Collega le attività del progetto che sono piaciute di più alle professioni ICT.

Uso:
    python professioni_ict.py                         questionario nel terminale
    python professioni_ict.py --salva risposte.csv    questionario, poi salva le risposte
    python professioni_ict.py --risposte risposte.csv --scheda scheda_professioni.md

Per ogni attività svolta nel progetto si indica quanto è piaciuta, da 1 (per
niente) a 4 (molto). Ogni professione di professioni.json è associata ad alcune
attività: la sua affinità è la media dei livelli dati a quelle attività.
Il risultato è uno spunto per informarsi, non una previsione.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

CARTELLA = Path(__file__).resolve().parent
PROFESSIONI = CARTELLA / "professioni.json"


class ErroreDati(Exception):
    """Errore nei dati delle professioni o nelle risposte."""


def carica_professioni(percorso=PROFESSIONI):
    dati = json.loads(Path(percorso).read_text(encoding="utf-8"))
    attivita = dati["attivita"]
    for p in dati["professioni"]:
        sconosciute = [a for a in p["attivita"] if a not in attivita]
        if sconosciute:
            raise ErroreDati(f"{p['nome']}: attività non previste: {', '.join(sconosciute)}")
    return attivita, dati["professioni"]


def livello_valido(testo):
    """Restituisce il livello come intero da 1 a 4, oppure None."""
    testo = testo.strip()
    return int(testo) if testo in ("1", "2", "3", "4") else None


def questionario(attivita, chiedi=input):
    """Chiede un livello per ogni attività; ripete la domanda finché la risposta non è valida."""
    risposte = {}
    print("Quanto ti è piaciuto, nel progetto... (1 = per niente, 4 = molto)")
    for chiave, descrizione in attivita.items():
        while True:
            livello = livello_valido(chiedi(f"  {descrizione}: "))
            if livello is not None:
                risposte[chiave] = livello
                break
            print("    Scrivi un numero da 1 a 4.")
    return risposte


def leggi_risposte(percorso, attivita):
    risposte = {}
    with open(percorso, encoding="utf-8", newline="") as f:
        for numero, riga in enumerate(csv.DictReader(f), start=2):
            chiave = riga["attivita"].strip()
            if chiave not in attivita:
                raise ErroreDati(f"riga {numero}: attività \"{chiave}\" non prevista")
            livello = livello_valido(riga["livello"])
            if livello is None:
                raise ErroreDati(f"riga {numero}: il livello deve essere da 1 a 4")
            risposte[chiave] = livello
    mancanti = [a for a in attivita if a not in risposte]
    if mancanti:
        raise ErroreDati("mancano le risposte per: " + ", ".join(mancanti))
    return risposte


def salva_risposte(percorso, risposte):
    with open(percorso, "w", encoding="utf-8", newline="") as f:
        scrittore = csv.writer(f)
        scrittore.writerow(["attivita", "livello"])
        scrittore.writerows(risposte.items())


def classifica(risposte, professioni):
    """Lista di (affinità, professione), dalla più alta; a parità, in ordine di nome."""
    risultati = []
    for p in professioni:
        livelli = [risposte[a] for a in p["attivita"]]
        risultati.append((round(sum(livelli) / len(livelli), 2), p))
    return sorted(risultati, key=lambda r: (-r[0], r[1]["nome"]))


def scheda_markdown(risposte, attivita, risultati, quante=3):
    righe = ["# Le mie attività e le professioni ICT", "",
             "Spunto per informarsi, non una previsione: l'affinità è la media di quanto sono piaciute "
             "le attività del progetto legate a ogni professione.", "",
             "## Attività che mi sono piaciute di più", ""]
    migliori = sorted(risposte.items(), key=lambda r: -r[1])
    righe += [f"- {attivita[chiave]} ({livello})" for chiave, livello in migliori if livello == migliori[0][1]]
    righe += ["", "## Professioni da approfondire", ""]
    for affinita, p in risultati[:quante]:
        righe += [f"### {p['nome']} (affinità {affinita:g} su 4)", "",
                  f"- Ruolo corrispondente nel progetto: {p['ruolo_nel_progetto']}",
                  f"- Profilo europeo delle professioni ICT: {p['profilo_europeo']}",
                  f"- Da cercare in ESCO: \"{p['cerca_in_esco']}\"",
                  f"- Competenze tecniche: {p['competenze_tecniche']}",
                  f"- Competenze trasversali: {p['competenze_trasversali']}",
                  f"- Percorsi frequenti: {p['percorsi']}", ""]
    righe += ["## Tutte le professioni", "", "| Professione | Affinità |", "|---|---|"]
    righe += [f"| {p['nome']} | {affinita:g} |" for affinita, p in risultati]
    righe += ["", "## Che cosa ho scoperto in ESCO", "", "...", ""]
    return "\n".join(righe)


def main(argv=None, chiedi=input):
    parser = argparse.ArgumentParser(description="Attività del progetto e professioni ICT")
    parser.add_argument("--risposte", help="file CSV con le risposte (colonne attivita, livello)")
    parser.add_argument("--salva", help="file CSV in cui salvare le risposte del questionario")
    parser.add_argument("--scheda", help="file Markdown in cui scrivere la scheda")
    argomenti = parser.parse_args(argv)
    try:
        attivita, professioni = carica_professioni()
        if argomenti.risposte:
            risposte = leggi_risposte(argomenti.risposte, attivita)
        else:
            risposte = questionario(attivita, chiedi)
    except (ErroreDati, OSError, KeyError) as e:
        print(f"Errore: {e}")
        return 1
    if argomenti.salva:
        salva_risposte(argomenti.salva, risposte)
        print(f"Risposte salvate in {argomenti.salva}")
    risultati = classifica(risposte, professioni)
    print(f"\n{'Professione':<42}Affinità")
    for affinita, p in risultati:
        print(f"{p['nome']:<42}{affinita:>8g}")
    if argomenti.scheda:
        Path(argomenti.scheda).write_text(scheda_markdown(risposte, attivita, risultati), encoding="utf-8")
        print(f"\nScheda scritta in {argomenti.scheda}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
