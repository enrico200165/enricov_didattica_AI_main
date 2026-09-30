"""Scambio di chiavi Diffie-Hellman e RSA con numeri piccoli: SOLO a scopo didattico.

Con numeri di poche cifre i calcoli si seguono a mano e si verificano in console.
I sistemi reali usano numeri di centinaia di cifre (RSA a 2048 bit o più) o curve ellittiche,
librerie collaudate e schemi di riempimento (padding) che qui mancano:
questo codice non protegge nulla e non va usato per dati reali.
Solo libreria standard di Python (pow con esponente -1 richiede Python 3.8 o successivo).
"""

import hashlib
import secrets

# ---------------------------------------------------------------- Diffie-Hellman

P = 2147483647  # numero primo pubblico (2^31 - 1)
G = 7           # generatore pubblico


def dh_segreto():
    """Numero segreto casuale di una delle due parti."""
    return secrets.randbelow(P - 3) + 2


def dh_pubblico(segreto):
    """Valore da inviare all'altra parte: G elevato al segreto, modulo P."""
    return pow(G, segreto, P)


def dh_condiviso(segreto_proprio, pubblico_altrui):
    """Segreto comune: entrambe le parti ottengono lo stesso numero senza averlo mai trasmesso."""
    return pow(pubblico_altrui, segreto_proprio, P)


# ---------------------------------------------------------------- RSA

def rsa_genera(p=61, q=53, e=17):
    """Coppia di chiavi RSA a partire da due primi p e q.

    Chiave pubblica: (n, e). Chiave privata: (n, d), con d inverso di e modulo phi(n).
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return (n, e), (n, d)


def rsa_cifra(m, pubblica):
    n, e = pubblica
    if not 0 <= m < n:
        raise ValueError("il messaggio deve essere un numero tra 0 e n - 1")
    return pow(m, e, n)


def rsa_decifra(c, privata):
    n, d = privata
    return pow(c, d, n)


def impronta_ridotta(messaggio, n):
    """Impronta SHA-256 del messaggio, ridotta modulo n per adattarla alle chiavi giocattolo."""
    return int.from_bytes(hashlib.sha256(messaggio.encode("utf-8")).digest(), "big") % n


def rsa_firma(messaggio, privata):
    """Firma: l'impronta del messaggio elaborata con la chiave PRIVATA."""
    n, d = privata
    return pow(impronta_ridotta(messaggio, n), d, n)


def rsa_verifica(messaggio, firma, pubblica):
    """Verifica: con la chiave PUBBLICA dalla firma si riottiene l'impronta, da confrontare con quella del messaggio."""
    n, e = pubblica
    return pow(firma, e, n) == impronta_ridotta(messaggio, n)


if __name__ == "__main__":
    print("Diffie-Hellman")
    a, b = dh_segreto(), dh_segreto()
    A, B = dh_pubblico(a), dh_pubblico(b)
    print(f"  Anna invia {A}, Bruno invia {B} (valori visibili a chiunque)")
    print(f"  segreto calcolato da Anna:  {dh_condiviso(a, B)}")
    print(f"  segreto calcolato da Bruno: {dh_condiviso(b, A)}")

    print("RSA con p = 61, q = 53")
    pubblica, privata = rsa_genera()
    print(f"  chiave pubblica (n, e) = {pubblica}, chiave privata (n, d) = {privata}")
    c = rsa_cifra(65, pubblica)
    print(f"  cifratura di 65 con la chiave pubblica: {c}; decifratura con la privata: {rsa_decifra(c, privata)}")
    testo = "Voto finale: 8"
    firma = rsa_firma(testo, privata)
    print(f"  firma di {testo!r}: {firma}")
    print(f"  verifica del messaggio originale: {rsa_verifica(testo, firma, pubblica)}")
    print(f"  verifica del messaggio 'Voto finale: 9': {rsa_verifica('Voto finale: 9', firma, pubblica)}")
