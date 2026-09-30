"""Gli esercizi di codifica, hash ed entropia della lezione 3.4 rifatti con la libreria standard di Python.

Serve a confrontare i risultati di CyberChef con quelli di un secondo strumento.
La cifratura AES non è inclusa: la libreria standard di Python non la offre,
e per usarla servirebbe una libreria esterna (per esempio 'cryptography').
Esecuzione: python verifica_con_python.py
"""

import base64
import binascii
import hashlib
import math
from collections import Counter


def entropia_shannon(dati):
    """Entropia di Shannon in bit per byte: 0 = tutti i byte uguali, 8 = massimo possibile."""
    if not dati:
        return 0.0
    totale = len(dati)
    return -sum(n / totale * math.log2(n / totale) for n in Counter(dati).values())


def esercizio1():
    testo = "Ciao".encode("utf-8")
    print("E1  esadecimale:", " ".join(f"{b:02x}" for b in testo))
    print("    Base64:     ", base64.b64encode(testo).decode("ascii"))


def esercizio2():
    valore = "UGFzc3dvcmQgZGVsIFdpLUZpIG9zcGl0aTogQXVsYS1NYWduYS0yMDI2"
    print("E2 ", base64.b64decode(valore).decode("utf-8"))


def esercizio3():
    valore = ("NTY2NTcyNjk2NjY5NjM2MTIwNjQ2OTIwNjk2ZTY2NmY3MjZkNjE3NDY5NjM2MTIw"
              "NzM3MDZmNzM3NDYxNzQ2MTIwNjEyMDY3Njk2Zjc2NjU2NGMzYWM=")
    passo1 = base64.b64decode(valore)             # Base64 -> testo esadecimale
    passo2 = binascii.unhexlify(passo1)           # esadecimale -> byte
    print("E3 ", passo2.decode("utf-8"))


def esercizio4():
    for parola in ("ciao", "Ciao"):
        print(f"E4  SHA-256({parola!r}) =", hashlib.sha256(parola.encode("utf-8")).hexdigest())


def esercizio8():
    messaggio = "Il laboratorio di domani inizia alle 10:30 in aula 12".encode("utf-8")
    cifrato = bytes.fromhex(
        "392decb59451874e032d269c673357bc244389953703859256da22a3924fe958"
        "d8d651ccc0e589cae266606cacf0e691512be827e349cf5bf583b73bce42583f")
    print(f"E8  entropia del testo in chiaro:  {entropia_shannon(messaggio):.3f}")
    print(f"    entropia del testo in Base64:  {entropia_shannon(base64.b64encode(messaggio)):.3f}")
    print(f"    entropia del cifrato AES:      {entropia_shannon(cifrato):.3f}"
          f"  (massimo possibile con {len(cifrato)} byte: {math.log2(len(cifrato)):.3f})")


if __name__ == "__main__":
    esercizio1()
    esercizio2()
    esercizio3()
    esercizio4()
    esercizio8()
