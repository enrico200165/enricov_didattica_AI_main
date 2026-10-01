"""Confronta percorsi dopo il diploma con criteri pesati, controllando che ogni informazione abbia una fonte.

Uso:
    python confronta_percorsi.py criteri.csv percorsi.csv
    python confronta_percorsi.py criteri.csv percorsi.csv --scheda confronto.md

criteri.csv:  criterio, peso (1-5), domanda
percorsi.csv: percorso, criterio, informazione, fonte, punteggio (1-5)

Il peso dice quanto conta il criterio per chi sceglie; il punteggio quanto il
percorso soddisfa il criterio, secondo chi sceglie. Il totale è la somma di
peso per punteggio. Il programma indica anche se la classifica cambia
modificando di 1 il peso di un criterio: una scelta che dipende da un solo
peso va ripensata con attenzione.
"""

import argparse
import csv
import sys
from pathlib import Path


def intero_da_1_a_5(testo):
    testo = (testo or "").strip()
    return int(testo) if testo in ("1", "2", "3", "4", "5") else None


def leggi_criteri(percorso):
    criteri, problemi = {}, []
    with open(percorso, encoding="utf-8", newline="") as f:
        for numero, riga in enumerate(csv.DictReader(f), start=2):
            nome = (riga.get("criterio") or "").strip()
            peso = intero_da_1_a_5(riga.get("peso"))
            if not nome:
                problemi.append(("DA SISTEMARE", f"criteri, riga {numero}: criterio senza nome"))
            elif peso is None:
                problemi.append(("DA SISTEMARE", f"criteri, riga {numero}: il peso di \"{nome}\" deve essere da 1 a 5"))
            else:
                criteri[nome] = (peso, (riga.get("domanda") or "").strip())
    return criteri, problemi


def leggi_percorsi(percorso, criteri):
    percorsi, problemi = {}, []
    with open(percorso, encoding="utf-8", newline="") as f:
        for numero, riga in enumerate(csv.DictReader(f), start=2):
            nome = (riga.get("percorso") or "").strip()
            criterio = (riga.get("criterio") or "").strip()
            informazione = (riga.get("informazione") or "").strip()
            fonte = (riga.get("fonte") or "").strip()
            punteggio = intero_da_1_a_5(riga.get("punteggio"))
            dove = f"{nome}, {criterio}"
            if criterio not in criteri:
                problemi.append(("DA SISTEMARE", f"percorsi, riga {numero}: criterio \"{criterio}\" non presente in criteri"))
                continue
            if not informazione or "..." in informazione:
                problemi.append(("DA SISTEMARE", f"{dove}: informazione da completare"))
            if not fonte:
                problemi.append(("DA SISTEMARE", f"{dove}: manca la fonte"))
            elif not fonte.startswith(("http://", "https://")):
                problemi.append(("ATTENZIONE", f"{dove}: fonte senza indirizzo web (\"{fonte}\"): "
                                 "va bene per un open day o un colloquio, annotare data e persona"))
            if punteggio is None:
                problemi.append(("DA SISTEMARE", f"{dove}: il punteggio deve essere da 1 a 5"))
            percorsi.setdefault(nome, {})[criterio] = (informazione, fonte, punteggio)
    for nome, valori in percorsi.items():
        for criterio in criteri:
            if criterio not in valori:
                problemi.append(("DA SISTEMARE", f"{nome}: manca il criterio \"{criterio}\""))
    if len(percorsi) < 2:
        problemi.append(("DA SISTEMARE", "servono almeno due percorsi da confrontare"))
    return percorsi, problemi


def totali(percorsi, pesi):
    """Somma di peso per punteggio per ogni percorso, in ordine dal più alto."""
    risultato = {nome: sum(pesi[c] * valori[c][2] for c in pesi) for nome, valori in percorsi.items()}
    return dict(sorted(risultato.items(), key=lambda r: (-r[1], r[0])))


def primo(classifica):
    """Il percorso in testa, oppure None se c'è un pareggio al primo posto."""
    valori = list(classifica.values())
    return None if len(valori) > 1 and valori[0] == valori[1] else next(iter(classifica))


def sensibilita(percorsi, criteri):
    """Criteri per cui un peso aumentato o diminuito di 1 cambia il percorso in testa."""
    pesi = {c: p for c, (p, _) in criteri.items()}
    in_testa = primo(totali(percorsi, pesi))
    delicati = []
    for criterio, peso in pesi.items():
        for nuovo in (peso - 1, peso + 1):
            if 1 <= nuovo <= 5 and primo(totali(percorsi, {**pesi, criterio: nuovo})) != in_testa:
                delicati.append(criterio)
                break
    return delicati


def scheda_markdown(criteri, percorsi, classifica, delicati):
    nomi = list(classifica)
    massimo = 5 * sum(p for p, _ in criteri.values())
    righe = ["# Confronto tra percorsi dopo il diploma", "",
             "| Criterio (peso) | " + " | ".join(nomi) + " |", "|---" * (len(nomi) + 1) + "|"]
    for criterio, (peso, _) in criteri.items():
        celle = [f"{percorsi[n][criterio][0]} ({percorsi[n][criterio][2]})" for n in nomi]
        righe.append(f"| {criterio} ({peso}) | " + " | ".join(celle) + " |")
    righe.append("| **Totale** | " + " | ".join(f"**{classifica[n]}** su {massimo}" for n in nomi) + " |")
    righe += ["", "## Fonti", ""]
    for n in nomi:
        righe += [f"- {n}, {c}: {percorsi[n][c][1]}" for c in criteri]
    righe += ["", "## Stabilità della scelta", ""]
    if delicati:
        righe.append("Il percorso in testa cambia modificando di 1 il peso di: " + ", ".join(delicati)
                     + ". Prima di decidere conviene approfondire questi criteri.")
    else:
        righe.append("Il percorso in testa non cambia modificando di 1 il peso di un singolo criterio.")
    righe += ["", "## Che cosa ne penso", "", "...", ""]
    return "\n".join(righe)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Confronto pesato tra percorsi dopo il diploma")
    parser.add_argument("criteri")
    parser.add_argument("percorsi")
    parser.add_argument("--scheda", help="file Markdown in cui scrivere il confronto")
    argomenti = parser.parse_args(argv)
    try:
        criteri, problemi = leggi_criteri(argomenti.criteri)
        percorsi, altri = leggi_percorsi(argomenti.percorsi, criteri)
    except OSError as e:
        print(f"Errore: {e}")
        return 1
    problemi += altri
    for livello, messaggio in problemi:
        print(f"{livello}: {messaggio}")
    if any(livello == "DA SISTEMARE" for livello, _ in problemi):
        print("\nConfronto non calcolato: completare prima le informazioni.")
        return 1
    pesi = {c: p for c, (p, _) in criteri.items()}
    classifica = totali(percorsi, pesi)
    massimo = 5 * sum(pesi.values())
    if problemi:
        print()
    for nome, totale in classifica.items():
        print(f"{nome:<45}{totale:>4} su {massimo}")
    if primo(classifica) is None:
        print("Pareggio al primo posto.")
    delicati = sensibilita(percorsi, criteri)
    print("Criteri da cui dipende la scelta: " + (", ".join(delicati) if delicati else "nessuno"))
    if argomenti.scheda:
        Path(argomenti.scheda).write_text(scheda_markdown(criteri, percorsi, classifica, delicati), encoding="utf-8")
        print(f"\nScheda scritta in {argomenti.scheda}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
