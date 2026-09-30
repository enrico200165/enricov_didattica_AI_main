"""Registro dei rischi del progetto: punteggio, livello, controlli e matrice.

Uso:
    python registro_rischi.py rischi.csv

Il file CSV ha le colonne:
    id           codice, per esempio R01
    rischio      che cosa potrebbe succedere e con quale effetto
    probabilita  da 1 (rara) a 5 (quasi certa)
    impatto      da 1 (trascurabile) a 5 (gravissimo)
    strategia    evitare, ridurre, trasferire, accettare
    azione       che cosa si fa
    responsabile chi segue il rischio

Il punteggio è probabilità x impatto (da 1 a 25). Il programma ordina i rischi,
segnala quelli gravi senza azione o senza responsabile, e scrive la matrice
probabilità-impatto nel file rischi.matrice.md.
"""

import csv
import sys
from pathlib import Path

STRATEGIE = ("evitare", "ridurre", "trasferire", "accettare")
LIVELLI = [(4, "basso"), (9, "medio"), (16, "alto"), (25, "critico")]


class ErroreRischi(Exception):
    """Errore nel file dei rischi."""


def livello(punteggio):
    for soglia, nome in LIVELLI:
        if punteggio <= soglia:
            return nome
    raise ValueError(punteggio)


def leggi_rischi(percorso):
    rischi, visti = [], set()
    with open(percorso, encoding="utf-8", newline="") as f:
        lettore = csv.DictReader(f)
        richieste = {"id", "rischio", "probabilita", "impatto", "strategia", "azione", "responsabile"}
        mancanti = richieste - set(lettore.fieldnames or [])
        if mancanti:
            raise ErroreRischi("colonne mancanti: " + ", ".join(sorted(mancanti)))
        for numero, riga in enumerate(lettore, start=2):
            r = {k: (riga[k] or "").strip() for k in richieste}
            if r["id"] in visti:
                raise ErroreRischi(f"riga {numero}: {r['id']} ripetuto")
            visti.add(r["id"])
            try:
                r["probabilita"], r["impatto"] = int(r["probabilita"]), int(r["impatto"])
            except ValueError:
                raise ErroreRischi(f"riga {numero}: probabilità e impatto devono essere numeri interi") from None
            if not (1 <= r["probabilita"] <= 5 and 1 <= r["impatto"] <= 5):
                raise ErroreRischi(f"riga {numero}: probabilità e impatto devono essere tra 1 e 5")
            r["strategia"] = r["strategia"].lower()
            if r["strategia"] not in STRATEGIE:
                raise ErroreRischi(f"riga {numero}: strategia \"{r['strategia']}\" non valida; "
                                   "ammesse: " + ", ".join(STRATEGIE))
            r["punteggio"] = r["probabilita"] * r["impatto"]
            r["livello"] = livello(r["punteggio"])
            rischi.append(r)
    return rischi


def controlla(rischi):
    """Restituisce l'elenco delle segnalazioni (id, livello della segnalazione, messaggio)."""
    segnalazioni = []
    for r in rischi:
        grave = r["livello"] in ("alto", "critico")
        if grave and r["strategia"] == "accettare":
            segnalazioni.append((r["id"], "ATTENZIONE",
                                 f"rischio {r['livello']} accettato senza intervenire: va motivato"))
        if grave and not r["azione"]:
            segnalazioni.append((r["id"], "DA SISTEMARE", f"rischio {r['livello']} senza azione"))
        if r["livello"] != "basso" and not r["responsabile"]:
            segnalazioni.append((r["id"], "DA SISTEMARE", "manca il responsabile"))
    return segnalazioni


def matrice(rischi):
    """Tabella Markdown: righe per impatto (da 5 a 1), colonne per probabilità (da 1 a 5)."""
    righe = ["| Impatto \\ Probabilità | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|"]
    for impatto in range(5, 0, -1):
        celle = []
        for probabilita in range(1, 6):
            codici = [r["id"] for r in rischi if r["impatto"] == impatto and r["probabilita"] == probabilita]
            celle.append(" ".join(codici))
        righe.append(f"| **{impatto}** | " + " | ".join(celle) + " |")
    return "\n".join(righe)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Uso: python registro_rischi.py rischi.csv")
        return 2
    try:
        rischi = leggi_rischi(argv[0])
    except (ErroreRischi, OSError) as e:
        print(f"Errore: {e}")
        return 1
    ordinati = sorted(rischi, key=lambda r: (-r["punteggio"], -r["impatto"], r["id"]))
    print(f"{'ID':<5}{'P':>2}{'I':>3}{'Punti':>6}  {'Livello':<9}{'Strategia':<11}Rischio")
    for r in ordinati:
        print(f"{r['id']:<5}{r['probabilita']:>2}{r['impatto']:>3}{r['punteggio']:>6}  "
              f"{r['livello']:<9}{r['strategia']:<11}{r['rischio'][:60]}")
    segnalazioni = controlla(rischi)
    for codice, tipo, messaggio in segnalazioni:
        print(f"{tipo}: {codice}: {messaggio}")
    uscita = Path(argv[0]).with_suffix(".matrice.md")
    uscita.write_text("# Matrice probabilità-impatto\n\n" + matrice(rischi) +
                      "\n\nLivelli: basso fino a 4 punti, medio fino a 9, alto fino a 16, critico oltre.\n",
                      encoding="utf-8")
    print(f"\nMatrice scritta in {uscita}")
    return 1 if any(t == "DA SISTEMARE" for _, t, _ in segnalazioni) else 0


if __name__ == "__main__":
    sys.exit(main())
