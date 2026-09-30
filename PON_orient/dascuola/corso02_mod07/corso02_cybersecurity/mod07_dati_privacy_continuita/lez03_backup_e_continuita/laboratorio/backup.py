"""Backup di una cartella in archivi ZIP datati, con elenco delle impronte, verifica e prova di ripristino.

Uso:
    python backup.py crea CARTELLA DESTINAZIONE [--conserva N]   crea un backup e tiene solo gli ultimi N (predefinito 7)
    python backup.py verifica ARCHIVIO                          controlla l'archivio con le impronte registrate
    python backup.py ripristina ARCHIVIO CARTELLA               estrae in una cartella NUOVA e verifica ogni file

Ogni archivio contiene il file IMPRONTE.sha256 (formato di sha256sum, lezione 3.2).
Solo libreria standard di Python.
"""

import argparse
import hashlib
import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path

NOME_IMPRONTE = "IMPRONTE.sha256"


def impronta_byte(dati):
    return hashlib.sha256(dati).hexdigest()


def impronta_file(percorso):
    h = hashlib.sha256()
    with open(percorso, "rb") as f:
        while blocco := f.read(1024 * 1024):
            h.update(blocco)
    return h.hexdigest()


def crea(cartella, destinazione, adesso=None):
    """Crea backup_AAAAMMGG_hhmmss.zip in 'destinazione' e restituisce il percorso."""
    cartella, destinazione = Path(cartella).resolve(), Path(destinazione).resolve()
    if destinazione == cartella or cartella in destinazione.parents:
        raise ValueError("la destinazione non può trovarsi dentro la cartella da salvare")
    destinazione.mkdir(parents=True, exist_ok=True)
    adesso = adesso or datetime.now()
    archivio = destinazione / f"backup_{adesso:%Y%m%d_%H%M%S}.zip"
    righe = []
    with zipfile.ZipFile(archivio, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for file in sorted(p for p in cartella.rglob("*") if p.is_file()):
            relativo = file.relative_to(cartella).as_posix()
            z.write(file, relativo)
            righe.append(f"{impronta_file(file)}  {relativo}")
        z.writestr(NOME_IMPRONTE, "\n".join(righe) + "\n")
    return archivio


def leggi_impronte(z):
    voci = {}
    for riga in z.read(NOME_IMPRONTE).decode("utf-8").splitlines():
        if riga.strip():
            impronta, _, nome = riga.partition("  ")
            voci[nome] = impronta
    return voci


def verifica(archivio):
    """Lista dei problemi trovati; vuota se l'archivio è integro."""
    problemi = []
    with zipfile.ZipFile(archivio) as z:
        corrotto = z.testzip()                    # controllo CRC di ogni file dell'archivio
        if corrotto:
            problemi.append(f"file danneggiato nell'archivio: {corrotto}")
        attese = leggi_impronte(z)
        presenti = set(z.namelist()) - {NOME_IMPRONTE}
        for nome, impronta in attese.items():
            if nome not in presenti:
                problemi.append(f"file mancante: {nome}")
            elif impronta_byte(z.read(nome)) != impronta:
                problemi.append(f"impronta diversa: {nome}")
        for nome in sorted(presenti - set(attese)):
            problemi.append(f"file non registrato: {nome}")
    return problemi


def ripristina(archivio, cartella):
    """Estrae in una cartella nuova e verifica ogni file estratto; restituisce (file ripristinati, problemi)."""
    cartella = Path(cartella)
    if cartella.exists() and any(cartella.iterdir()):
        raise ValueError("per la prova di ripristino serve una cartella nuova o vuota")
    with zipfile.ZipFile(archivio) as z:
        attese = leggi_impronte(z)
        z.extractall(cartella, members=[n for n in z.namelist() if n != NOME_IMPRONTE])
    problemi = [f"impronta diversa dopo il ripristino: {nome}"
                for nome, impronta in attese.items() if impronta_file(cartella / nome) != impronta]
    return len(attese), problemi


def conserva_ultimi(destinazione, n):
    """Elimina i backup più vecchi, lasciando gli ultimi n; restituisce i nomi eliminati."""
    archivi = sorted(Path(destinazione).glob("backup_*.zip"))
    da_eliminare = archivi[:-n] if n > 0 else []
    for a in da_eliminare:
        a.unlink()
    return [a.name for a in da_eliminare]


def main(argomenti=None):
    parser = argparse.ArgumentParser(description="Backup con verifica e prova di ripristino")
    sotto = parser.add_subparsers(dest="comando", required=True)
    c = sotto.add_parser("crea"); c.add_argument("cartella"); c.add_argument("destinazione")
    c.add_argument("--conserva", type=int, default=7)
    v = sotto.add_parser("verifica"); v.add_argument("archivio")
    r = sotto.add_parser("ripristina"); r.add_argument("archivio"); r.add_argument("cartella")
    a = parser.parse_args(argomenti)

    if a.comando == "crea":
        archivio = crea(a.cartella, a.destinazione)
        print(f"Creato: {archivio} ({archivio.stat().st_size} byte)")
        for nome in conserva_ultimi(a.destinazione, a.conserva):
            print(f"Eliminato perché più vecchio degli ultimi {a.conserva}: {nome}")
        return 0
    if a.comando == "verifica":
        problemi = verifica(a.archivio)
        print("Archivio integro." if not problemi else "\n".join(problemi))
        return 0 if not problemi else 1
    n, problemi = ripristina(a.archivio, a.cartella)
    print(f"File ripristinati: {n}; problemi: {len(problemi)}")
    for p in problemi:
        print(" ", p)
    return 0 if not problemi else 1


if __name__ == "__main__":
    sys.exit(main())
