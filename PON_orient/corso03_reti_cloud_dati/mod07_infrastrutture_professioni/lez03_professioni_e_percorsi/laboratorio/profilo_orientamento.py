"""Questionario di orientamento: quali professioni delle reti, dei dati e del cloud
sono più vicine alle attività che piacciono di più.

Uso:
    python profilo_orientamento.py                 domande una alla volta (risposte da 1 a 5)
    python profilo_orientamento.py risposte.csv    legge le risposte da un file (colonne: attivita,voto)
Il risultato è un'indicazione per la discussione, non un giudizio: le risposte restano sul proprio PC.
"""

import csv
import sys

# Attività del corso e peso per ciascuna professione (0 = non collegata, 2 = molto collegata)
ATTIVITA = {
    "cablaggio":   ("Progettare il cablaggio e le reti Wi-Fi di un edificio (moduli 2-3)",
                    {"network": 2, "sistemista": 1}),
    "indirizzi":   ("Calcolare sottoreti e piani di indirizzamento (modulo 2)",
                    {"network": 2, "cloud": 1}),
    "diagnosi":    ("Trovare il guasto quando 'Internet non va' (modulo 1)",
                    {"network": 2, "sistemista": 2, "devops": 1}),
    "server":      ("Installare e configurare server e servizi come DHCP e DNS (modulo 3)",
                    {"sistemista": 2, "network": 1, "cloud": 1}),
    "progetto_er": ("Progettare le tabelle di un database (modulo 4)",
                    {"dba": 2, "data": 1}),
    "sql":         ("Scrivere interrogazioni SQL per rispondere a domande sui dati (modulo 4)",
                    {"dba": 2, "data": 2}),
    "formati":     ("Convertire e pulire dati tra CSV, JSON e XML (modulo 5)",
                    {"data": 2, "devops": 1}),
    "api":         ("Programmare servizi e API in Python (modulo 5)",
                    {"devops": 2, "data": 1, "cloud": 1}),
    "container":   ("Automatizzare l'installazione con container e orchestratori (modulo 6)",
                    {"devops": 2, "cloud": 2, "sistemista": 1}),
    "costi":       ("Confrontare costi e scegliere tra soluzioni diverse (modulo 6)",
                    {"cloud": 2, "dba": 1}),
    "architettura":("Disegnare architetture ridondanti che reggono i guasti (moduli 6-7)",
                    {"cloud": 2, "sistemista": 1, "network": 1}),
    "monitoraggio":("Tenere d'occhio i servizi e intervenire quando qualcosa si ferma (modulo 7)",
                    {"sistemista": 2, "devops": 2, "dba": 1}),
}

PROFESSIONI = {
    "network":    ("Tecnico e ingegnere di rete (network engineer)", "moduli 1-3"),
    "sistemista": ("Amministratore di sistema", "moduli 1, 3, 6, 7"),
    "dba":        ("Amministratore di database (DBA)", "modulo 4"),
    "data":       ("Data engineer", "moduli 4 e 5"),
    "cloud":      ("Cloud engineer e cloud architect", "moduli 6 e 7"),
    "devops":     ("DevOps e site reliability engineer", "moduli 5, 6, 7"),
}


def punteggi(voti):
    """voti: {attività: 1..5}. Restituisce {professione: percentuale del massimo possibile}."""
    risultato = {}
    for p in PROFESSIONI:
        ottenuti = sum(voti[a] * pesi.get(p, 0) for a, (_, pesi) in ATTIVITA.items())
        massimo = sum(5 * pesi.get(p, 0) for _, pesi in ATTIVITA.values())
        risultato[p] = round(100 * ottenuti / massimo)
    return dict(sorted(risultato.items(), key=lambda v: (-v[1], v[0])))


def leggi_voti(percorso):
    with open(percorso, newline="", encoding="utf-8") as f:
        voti = {r["attivita"].strip(): int(r["voto"]) for r in csv.DictReader(f)}
    mancanti = set(ATTIVITA) - set(voti)
    if mancanti:
        raise ValueError("mancano le risposte per: " + ", ".join(sorted(mancanti)))
    if any(not 1 <= v <= 5 for v in voti.values()):
        raise ValueError("i voti devono essere da 1 a 5")
    return voti


def chiedi_voti():
    print("Quanto ti è piaciuta ciascuna attività? 1 = per niente, 5 = moltissimo\n")
    voti = {}
    for chiave, (testo, _) in ATTIVITA.items():
        while True:
            risposta = input(f"{testo}: ").strip()
            if risposta in {"1", "2", "3", "4", "5"}:
                voti[chiave] = int(risposta)
                break
            print("  rispondere con un numero da 1 a 5")
    return voti


def stampa(risultato):
    print("\nVicinanza alle professioni:")
    for p, percentuale in risultato.items():
        nome, moduli = PROFESSIONI[p]
        print(f"  {percentuale:>3}%  {'#' * (percentuale // 5):<20}  {nome}  ({moduli})")
    primi = list(risultato)[:2]
    print("\nDa approfondire:", " e ".join(PROFESSIONI[p][0] for p in primi))


if __name__ == "__main__":
    voti = leggi_voti(sys.argv[1]) if len(sys.argv) == 2 else chiedi_voti()
    stampa(punteggi(voti))
