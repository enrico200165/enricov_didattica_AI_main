"""Lettura dell'output di tracert (Windows) e stima delle distanze.

Per ogni passo calcola il tempo mediano e segnala gli aumenti bruschi, che
spesso corrispondono a collegamenti molto lunghi (per esempio cavi sottomarini).
La luce nella fibra percorre circa 200 km in un millisecondo: un tempo di
andata e ritorno di t ms indica una distanza in linea d'aria di al massimo
circa t x 100 km (andata e ritorno dimezzano la distanza).

Uso:
    python leggi_tracert.py tracert_esempio.txt
    tracert -d www.sito.it > percorso.txt   poi   python leggi_tracert.py percorso.txt
"""

import re
import statistics
import sys

KM_PER_MS_ANDATA_RITORNO = 100  # 200 km/ms nella fibra, diviso 2 per andata e ritorno

# riga di un passo: numero, tre misure (es. "12 ms", "<1 ms", "*"), resto della riga
MODELLO_PASSO = re.compile(r"^\s*(\d+)\s+((?:(?:<?\d+\s*ms|\*)\s+){3})(.*)$")


def leggi(testo):
    """Restituisce l'elenco dei passi: (numero, tempi in ms senza gli asterischi, indirizzo)."""
    passi = []
    for riga in testo.splitlines():
        m = MODELLO_PASSO.match(riga)
        if not m:
            continue
        numero, misure, resto = m.groups()
        tempi = []
        for misura in re.findall(r"<?\d+\s*ms|\*", misure):
            if misura != "*":
                valore = int(re.sub(r"\D", "", misura))
                tempi.append(0.5 if misura.startswith("<") else float(valore))  # "<1 ms" vale circa 0,5
        indirizzo = re.findall(r"\d+\.\d+\.\d+\.\d+", resto)
        passi.append((int(numero), tempi, indirizzo[-1] if indirizzo else None))
    return passi


def analizza(passi, soglia_ms=40):
    """Aggiunge a ogni passo il tempo mediano e segnala gli aumenti oltre la soglia."""
    risultati = []
    precedente = None
    for numero, tempi, indirizzo in passi:
        mediana = statistics.median(tempi) if tempi else None
        salto = (mediana - precedente) if (mediana is not None and precedente is not None) else None
        risultati.append({
            "passo": numero, "indirizzo": indirizzo, "mediana": mediana,
            "distanza_max_km": round(mediana * KM_PER_MS_ANDATA_RITORNO) if mediana is not None else None,
            "aumento_brusco": salto is not None and salto > soglia_ms,
        })
        if mediana is not None:
            precedente = mediana
    return risultati


def main(percorso):
    with open(percorso, encoding="utf-8") as f:
        risultati = analizza(leggi(f.read()))
    print(f"{'Passo':>5}  {'Indirizzo':<16}{'Mediana':>9}  {'Distanza max':>13}")
    for r in risultati:
        if r["mediana"] is None:
            print(f"{r['passo']:>5}  {'(nessuna risposta)':<16}")
            continue
        segnale = "  <- aumento brusco" if r["aumento_brusco"] else ""
        print(f"{r['passo']:>5}  {r['indirizzo'] or '-':<16}{r['mediana']:>7.1f} ms"
              f"  {r['distanza_max_km']:>9} km{segnale}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
    else:
        main(sys.argv[1])
