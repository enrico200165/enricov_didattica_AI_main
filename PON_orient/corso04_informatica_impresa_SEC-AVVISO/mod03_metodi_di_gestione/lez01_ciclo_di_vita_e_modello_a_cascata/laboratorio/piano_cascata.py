"""Calcola un piano a cascata: date, percorso critico e diagramma di Gantt in Mermaid.

Uso:
    python piano_cascata.py attivita.csv
    python piano_cascata.py attivita.csv --inizio 2026-11-02
    python piano_cascata.py attivita.csv --confronta attivita_modificate.csv

Il file CSV ha le colonne:
    id          codice breve dell'attività, per esempio A1
    attivita    descrizione
    fase        fase del ciclo di vita (diventa una sezione del diagramma)
    durata      giorni lavorativi (dal lunedì al venerdì)
    dipende_da  codici delle attività che devono finire prima, separati da spazi

Il programma calcola per ogni attività la data di inizio più vicina possibile,
il margine (quanti giorni può ritardare senza spostare la fine del progetto)
e il percorso critico (le attività senza margine). Con --confronta calcola
anche il piano modificato e mostra di quanto si sposta la fine.
"""

import argparse
import csv
import sys
from datetime import date, timedelta
from pathlib import Path


class ErrorePiano(Exception):
    """Errore nei dati del piano."""


def leggi_attivita(percorso):
    """Legge il CSV e restituisce un dizionario {id: attività}, nell'ordine del file."""
    attivita = {}
    with open(percorso, encoding="utf-8", newline="") as f:
        lettore = csv.DictReader(f)
        mancanti = {"id", "attivita", "fase", "durata", "dipende_da"} - set(lettore.fieldnames or [])
        if mancanti:
            raise ErrorePiano("colonne mancanti: " + ", ".join(sorted(mancanti)))
        for numero, riga in enumerate(lettore, start=2):
            codice = riga["id"].strip()
            if codice in attivita:
                raise ErrorePiano(f"riga {numero}: {codice} ripetuto")
            try:
                durata = int(riga["durata"])
            except ValueError:
                raise ErrorePiano(f"riga {numero}: la durata deve essere un numero intero di giorni") from None
            if durata < 0:
                raise ErrorePiano(f"riga {numero}: durata negativa")
            attivita[codice] = {"id": codice, "nome": riga["attivita"].strip(),
                                "fase": riga["fase"].strip(), "durata": durata,
                                "dipende": (riga["dipende_da"] or "").split()}
    for a in attivita.values():
        for d in a["dipende"]:
            if d not in attivita:
                raise ErrorePiano(f"{a['id']} dipende da {d}, che non esiste")
    return attivita


def ordine_topologico(attivita):
    """Ordina le attività in modo che ciascuna venga dopo quelle da cui dipende.

    Se esiste un ciclo (A dipende da B e B da A) il piano è impossibile.
    """
    ordinate, stato = [], {}           # stato: 1 = in visita, 2 = completata

    def visita(codice, percorso):
        if stato.get(codice) == 2:
            return
        if stato.get(codice) == 1:
            raise ErrorePiano("dipendenze circolari: " + " -> ".join(percorso + [codice]))
        stato[codice] = 1
        for d in attivita[codice]["dipende"]:
            visita(d, percorso + [codice])
        stato[codice] = 2
        ordinate.append(codice)

    for codice in attivita:
        visita(codice, [])
    return ordinate


def calcola(attivita):
    """Calcola inizio e fine (in giorni lavorativi dall'inizio del progetto) e margine.

    Passaggio in avanti: ogni attività inizia quando è finita l'ultima da cui dipende.
    Passaggio all'indietro: ogni attività deve finire prima che inizi la prima che dipende da lei.
    """
    ordine = ordine_topologico(attivita)
    for codice in ordine:
        a = attivita[codice]
        a["inizio"] = max((attivita[d]["fine"] for d in a["dipende"]), default=0)
        a["fine"] = a["inizio"] + a["durata"]
    durata_totale = max((a["fine"] for a in attivita.values()), default=0)
    for codice in reversed(ordine):
        a = attivita[codice]
        successori = [s for s in attivita.values() if codice in s["dipende"]]
        a["fine_tardi"] = min((s["inizio_tardi"] for s in successori), default=durata_totale)
        a["inizio_tardi"] = a["fine_tardi"] - a["durata"]
        a["margine"] = a["inizio_tardi"] - a["inizio"]
    return durata_totale


def giorno_lavorativo(inizio, giorni):
    """Data che si raggiunge avanzando di un certo numero di giorni lavorativi."""
    giorno = inizio
    while giorno.weekday() >= 5:            # se si parte di sabato o domenica, si va al lunedì
        giorno += timedelta(days=1)
    contati = 0
    while contati < giorni:
        giorno += timedelta(days=1)
        if giorno.weekday() < 5:
            contati += 1
    return giorno


def data_fine(inizio, giorni_lavorativi):
    """Ultimo giorno di lavoro di un'attività lunga n giorni che parte al giorno 0."""
    return giorno_lavorativo(inizio, max(giorni_lavorativi - 1, 0))


def gantt_mermaid(attivita, inizio, titolo):
    """Diagramma di Gantt Mermaid con date calcolate; il percorso critico è evidenziato."""
    righe = ["gantt", f"    title {titolo}", "    dateFormat YYYY-MM-DD",
             "    axisFormat %d/%m", "    excludes weekends"]
    fase_corrente = None
    for a in attivita.values():
        if a["fase"] != fase_corrente:
            fase_corrente = a["fase"]
            righe.append(f"    section {fase_corrente}")
        partenza = giorno_lavorativo(inizio, a["inizio"]).isoformat()
        if a["durata"] == 0:                  # traguardo: nell'ultimo giorno delle attività precedenti
            righe.append(f"    {a['nome']} :milestone, {a['id']}, {data_fine(inizio, a['inizio']).isoformat()}, 0d")
        else:
            critico = "crit, " if a["margine"] == 0 else ""
            righe.append(f"    {a['nome']} :{critico}{a['id']}, {partenza}, {a['durata']}d")
    return "\n".join(righe)


def stampa_piano(attivita, inizio, durata_totale):
    print(f"{'ID':<5}{'Attività':<42}{'Giorni':>6}  {'Inizio':<11}{'Fine':<11}{'Margine':>7}")
    for a in attivita.values():
        if a["durata"]:
            partenza = giorno_lavorativo(inizio, a["inizio"])
            fine = data_fine(partenza, a["durata"])
        else:                                 # traguardo (durata 0)
            partenza = fine = data_fine(inizio, a["inizio"])
        print(f"{a['id']:<5}{a['nome'][:41]:<42}{a['durata']:>6}  "
              f"{partenza.isoformat():<11}{fine.isoformat():<11}{a['margine']:>7}")
    critico = [a["id"] for a in attivita.values() if a["margine"] == 0 and a["durata"] > 0]
    print(f"\nDurata del progetto: {durata_totale} giorni lavorativi, "
          f"fine il {data_fine(inizio, durata_totale).isoformat()}")
    print("Attività critiche (margine 0): " + ", ".join(critico))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Piano a cascata con diagramma di Gantt")
    parser.add_argument("attivita", help="file CSV delle attività")
    parser.add_argument("--inizio", default="2026-11-02", help="data di inizio AAAA-MM-GG")
    parser.add_argument("--confronta", help="file CSV del piano modificato")
    argomenti = parser.parse_args(argv)
    try:
        inizio = date.fromisoformat(argomenti.inizio)
        piano = leggi_attivita(argomenti.attivita)
        durata = calcola(piano)
        stampa_piano(piano, inizio, durata)
        uscita = Path(argomenti.attivita).with_suffix(".gantt.md")
        uscita.write_text("# Piano del progetto\n\n```mermaid\n" +
                          gantt_mermaid(piano, inizio, "Piano a cascata") + "\n```\n", encoding="utf-8")
        print(f"Diagramma scritto in {uscita}")
        if argomenti.confronta:
            modificato = leggi_attivita(argomenti.confronta)
            durata2 = calcola(modificato)
            print("\nPiano modificato:")
            stampa_piano(modificato, inizio, durata2)
            ritardo = durata2 - durata
            print(f"\nRitardo sulla consegna: {ritardo} giorni lavorativi "
                  f"(dal {data_fine(inizio, durata).isoformat()} al {data_fine(inizio, durata2).isoformat()})")
            spostate = [c for c, a in modificato.items() if c in piano and a["inizio"] != piano[c]["inizio"]]
            nuove = [c for c in modificato if c not in piano]
            print("Attività spostate: " + (", ".join(spostate) or "nessuna"))
            print("Attività aggiunte: " + (", ".join(nuove) or "nessuna"))
            uscita2 = Path(argomenti.confronta).with_suffix(".gantt.md")
            uscita2.write_text("# Piano modificato\n\n```mermaid\n" +
                               gantt_mermaid(modificato, inizio, "Piano dopo la modifica") + "\n```\n",
                               encoding="utf-8")
            print(f"Diagramma scritto in {uscita2}")
    except (ErrorePiano, ValueError, OSError) as e:
        print(f"Errore: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
