"""Cifrari storici e cifratura XOR: strumenti didattici.

Nessuno di questi cifrari va usato per proteggere dati reali:
servono a capire i concetti di chiave, spazio delle chiavi e analisi delle frequenze.
Solo libreria standard di Python.
"""

import secrets
import string
from collections import Counter

ALFABETO = string.ascii_uppercase  # 26 lettere, A-Z

# Frequenze approssimate delle lettere nei testi italiani (percentuali)
FREQUENZE_ITALIANO = {
    "A": 11.7, "B": 0.9, "C": 4.5, "D": 3.7, "E": 11.8, "F": 1.0, "G": 1.6,
    "H": 1.5, "I": 11.3, "J": 0.0, "K": 0.0, "L": 6.5, "M": 2.5, "N": 6.9,
    "O": 9.8, "P": 3.1, "Q": 0.5, "R": 6.4, "S": 5.0, "T": 5.6, "U": 3.0,
    "V": 2.1, "W": 0.0, "X": 0.0, "Y": 0.0, "Z": 0.5,
}


def _sposta(carattere, spostamento):
    """Sposta una lettera di 'spostamento' posizioni; gli altri caratteri restano invariati."""
    if carattere.isupper() and carattere in ALFABETO:
        base = ord("A")
    elif carattere.islower() and carattere.upper() in ALFABETO:
        base = ord("a")
    else:
        return carattere
    return chr((ord(carattere) - base + spostamento) % 26 + base)


def cesare(testo, chiave):
    """Cifrario di Cesare: ogni lettera avanza di 'chiave' posizioni nell'alfabeto."""
    return "".join(_sposta(c, chiave) for c in testo)


def decifra_cesare(testo, chiave):
    return cesare(testo, -chiave)


def tutte_le_chiavi_cesare(testo_cifrato):
    """Le 25 decifrature possibili: lo spazio delle chiavi è così piccolo da poterlo esaurire."""
    return {k: decifra_cesare(testo_cifrato, k) for k in range(1, 26)}


def frequenze(testo):
    """Percentuale di ciascuna lettera nel testo (solo lettere A-Z, senza distinguere maiuscole)."""
    lettere = [c for c in testo.upper() if c in ALFABETO]
    conteggio = Counter(lettere)
    totale = len(lettere) or 1
    return {l: 100 * conteggio[l] / totale for l in ALFABETO}


def punteggio_italiano(testo):
    """Distanza tra le frequenze del testo e quelle dell'italiano: più è bassa, più il testo sembra italiano."""
    f = frequenze(testo)
    return sum((f[l] - FREQUENZE_ITALIANO[l]) ** 2 for l in ALFABETO)


def chiave_cesare_probabile(testo_cifrato):
    """Chiave la cui decifratura ha le frequenze più simili a quelle dell'italiano."""
    candidati = tutte_le_chiavi_cesare(testo_cifrato)
    return min(candidati, key=lambda k: punteggio_italiano(candidati[k]))


def vigenere(testo, parola_chiave, decifra=False):
    """Cifrario di Vigenère: lo spostamento cambia a ogni lettera, secondo la parola chiave.

    I caratteri che non sono lettere restano invariati e non consumano la chiave.
    """
    spostamenti = [ALFABETO.index(c) for c in parola_chiave.upper() if c in ALFABETO]
    if not spostamenti:
        raise ValueError("la parola chiave deve contenere almeno una lettera A-Z")
    risultato = []
    i = 0
    for c in testo:
        if c.upper() in ALFABETO:
            s = spostamenti[i % len(spostamenti)]
            risultato.append(_sposta(c, -s if decifra else s))
            i += 1
        else:
            risultato.append(c)
    return "".join(risultato)


def xor_bytes(dati, chiave):
    """XOR byte per byte; la chiave si ripete se è più corta dei dati.

    Applicare due volte la stessa chiave restituisce i dati originali:
    la stessa operazione cifra e decifra, come in ogni cifrario simmetrico.
    """
    if not chiave:
        raise ValueError("chiave vuota")
    return bytes(d ^ chiave[i % len(chiave)] for i, d in enumerate(dati))


def chiave_casuale(lunghezza):
    """Chiave casuale di 'lunghezza' byte, generata con il modulo secrets."""
    return secrets.token_bytes(lunghezza)


if __name__ == "__main__":
    messaggio = "Appuntamento in biblioteca alle quindici, porta il quaderno di informatica"
    cifrato = cesare(messaggio, 3)
    print("Cesare, chiave 3:     ", cifrato)
    print("Decifrato:            ", decifra_cesare(cifrato, 3))
    print("Chiave più probabile: ", chiave_cesare_probabile(cifrato))
    print("Vigenère, chiave SOLE:", vigenere(messaggio, "SOLE"))
    chiave = chiave_casuale(len(messaggio.encode("utf-8")))
    c = xor_bytes(messaggio.encode("utf-8"), chiave)
    print("XOR, cifrato (hex):   ", c.hex()[:48], "...")
    print("XOR, decifrato:       ", xor_bytes(c, chiave).decode("utf-8"))
