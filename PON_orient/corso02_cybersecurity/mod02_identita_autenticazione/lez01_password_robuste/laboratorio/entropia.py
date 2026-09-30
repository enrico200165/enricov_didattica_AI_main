"""Entropia delle password generate a caso e generatore sicuro (lezione 2.1).

Le formule valgono solo per password e passphrase GENERATE A CASO:
una password scelta da una persona ha un'entropia molto più bassa.
"""
import math
import secrets
import string


def entropia_casuale(n_simboli, lunghezza):
    """Bit di entropia di una password di `lunghezza` simboli scelti a caso tra `n_simboli`."""
    return lunghezza * math.log2(n_simboli)


def entropia_passphrase(n_parole, dimensione_lista):
    """Bit di entropia di `n_parole` parole scelte a caso da una lista di `dimensione_lista` parole."""
    return n_parole * math.log2(dimensione_lista)


def anni_per_esaurire(bit, tentativi_al_secondo):
    """Anni necessari, in media, per trovare il segreto provando tutte le combinazioni.

    In media si trova il segreto dopo aver provato metà delle 2**bit combinazioni.
    """
    secondi = (2 ** bit / 2) / tentativi_al_secondo
    return secondi / (365 * 24 * 3600)


def descrivi_durata(anni):
    """Descrive una durata espressa in anni con l'unità più leggibile."""
    secondi = anni * 365 * 24 * 3600
    unita = (
        ("anno", "anni", 365 * 24 * 3600),
        ("giorno", "giorni", 24 * 3600),
        ("ora", "ore", 3600),
        ("minuto", "minuti", 60),
        ("secondo", "secondi", 1),
    )
    for singolare, plurale, durata in unita:
        if secondi >= durata or durata == 1:
            valore = secondi / durata
            nome = singolare if f"{valore:.3g}" == "1" else plurale
            return f"{valore:.3g} {nome}"


def genera_password(lunghezza=16, alfabeto=string.ascii_letters + string.digits):
    """Password casuale generata con il modulo secrets (adatto alla sicurezza, a differenza di random)."""
    return "".join(secrets.choice(alfabeto) for _ in range(lunghezza))


# Piccola lista di esempio: le liste reali per passphrase contengono migliaia di parole
PAROLE = [
    "albero", "barca", "cavallo", "delfino", "elica", "faro", "gatto", "isola",
    "lampada", "matita", "nuvola", "orologio", "penna", "quadro", "ruota", "sedia",
    "tavolo", "uovo", "vela", "zaino", "ancora", "binario", "candela", "domino",
    "fiume", "gomitolo", "lago", "mela", "neve", "oliva", "pino", "razzo",
]


def genera_passphrase(n_parole=5, lista=PAROLE, separatore="-"):
    """Passphrase di parole scelte a caso dalla lista."""
    return separatore.join(secrets.choice(lista) for _ in range(n_parole))


if __name__ == "__main__":
    casi = [
        ("8 cifre", 10, 8),
        ("8 lettere minuscole", 26, 8),
        ("8 lettere e cifre", 62, 8),
        ("12 lettere e cifre", 62, 12),
        ("16 lettere e cifre", 62, 16),
    ]
    print("Password casuali")
    for nome, simboli, lunghezza in casi:
        bit = entropia_casuale(simboli, lunghezza)
        print(f"  {nome:22} {bit:6.1f} bit")

    print("Passphrase casuali (lista di 7776 parole)")
    for n in (4, 5, 6):
        print(f"  {n} parole               {entropia_passphrase(n, 7776):6.1f} bit")

    print("Anni per esaurire 40 bit e 80 bit, con 10 miliardi di tentativi al secondo")
    for bit in (40, 80):
        print(f"  {bit} bit: {descrivi_durata(anni_per_esaurire(bit, 1e10))}")

    print("Esempi generati:", genera_password(), genera_passphrase())
