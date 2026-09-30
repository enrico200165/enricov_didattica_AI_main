"""Calcolo e verifica delle impronte SHA-256 dei file.

Uso da terminale:
    python impronte.py FILE                   stampa l'impronta SHA-256 del file
    python impronte.py FILE IMPRONTA          confronta con un'impronta attesa
    python impronte.py --digest FILE.DIGEST   verifica i file elencati in un file di impronte

Formato dei file di impronte (come quelli prodotti da sha256sum e pubblicati da molti progetti):
    <impronta esadecimale><spazio><spazio o asterisco><nome del file>
Solo libreria standard di Python.
"""

import hashlib
import hmac
import sys
from pathlib import Path

BLOCCO = 1024 * 1024  # il file si legge a blocchi di 1 MiB: funziona anche con file molto grandi


def impronta_file(percorso, algoritmo="sha256"):
    h = hashlib.new(algoritmo)
    with open(percorso, "rb") as f:
        while blocco := f.read(BLOCCO):
            h.update(blocco)
    return h.hexdigest()


def normalizza(impronta):
    """Minuscole e senza spazi: PowerShell stampa le impronte in maiuscolo."""
    return "".join(impronta.split()).lower()


def coincide(impronta_calcolata, impronta_attesa):
    return hmac.compare_digest(normalizza(impronta_calcolata), normalizza(impronta_attesa))


def leggi_digest(percorso):
    """Coppie (impronta, nome file) lette da un file di impronte."""
    voci = []
    for riga in Path(percorso).read_text(encoding="utf-8").splitlines():
        riga = riga.strip()
        if not riga or riga.startswith("#"):
            continue
        impronta, _, nome = riga.partition(" ")
        nome = nome.lstrip(" *")
        if len(impronta) != 64 or not nome:
            raise ValueError(f"riga non valida: {riga!r}")
        voci.append((impronta, nome))
    return voci


def verifica_digest(percorso_digest):
    """Esito della verifica per ogni file elencato; i file si cercano nella cartella del file di impronte."""
    cartella = Path(percorso_digest).parent
    esiti = {}
    for impronta, nome in leggi_digest(percorso_digest):
        file = cartella / nome
        if not file.exists():
            esiti[nome] = "MANCANTE"
        elif coincide(impronta_file(file), impronta):
            esiti[nome] = "OK"
        else:
            esiti[nome] = "DIVERSA"
    return esiti


def main(argomenti):
    if len(argomenti) == 2 and argomenti[0] == "--digest":
        esiti = verifica_digest(argomenti[1])
        for nome, esito in esiti.items():
            print(f"{esito:9} {nome}")
        return 0 if all(e == "OK" for e in esiti.values()) else 1
    if len(argomenti) == 1:
        print(impronta_file(argomenti[0]))
        return 0
    if len(argomenti) == 2:
        calcolata = impronta_file(argomenti[0])
        print("calcolata:", calcolata)
        print("attesa:   ", normalizza(argomenti[1]))
        if coincide(calcolata, argomenti[1]):
            print("Le impronte coincidono: il file è identico a quello descritto dall'impronta.")
            return 0
        print("ATTENZIONE: le impronte sono diverse. Il file non va usato.")
        return 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
