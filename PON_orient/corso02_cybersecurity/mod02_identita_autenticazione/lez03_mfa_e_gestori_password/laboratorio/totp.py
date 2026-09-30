"""Codici temporanei TOTP (RFC 6238), come quelli delle app di autenticazione (lezione 2.3).

Servizio e app condividono un segreto, scambiato una sola volta (di solito con un codice QR).
Ogni 30 secondi entrambi calcolano lo stesso codice dal segreto e dall'ora corrente:
il codice non viaggia mai prima di essere digitato e vale solo per pochi secondi.
"""
import base64
import hashlib
import hmac
import secrets
import struct
import time

PASSO = 30      # secondi di validità di ogni codice
CIFRE = 6


def hotp(segreto, contatore, cifre=CIFRE, algoritmo=hashlib.sha1):
    """Codice HOTP (RFC 4226) per il contatore indicato."""
    messaggio = struct.pack(">Q", contatore)                 # contatore su 8 byte
    digest = hmac.new(segreto, messaggio, algoritmo).digest()
    inizio = digest[-1] & 0x0F                                # "troncamento dinamico"
    numero = struct.unpack(">I", digest[inizio:inizio + 4])[0] & 0x7FFFFFFF
    return str(numero % 10 ** cifre).zfill(cifre)


def totp(segreto, istante=None, cifre=CIFRE, algoritmo=hashlib.sha1):
    """Codice TOTP: HOTP con contatore = numero di intervalli di 30 s dal 1° gennaio 1970."""
    if istante is None:
        istante = time.time()
    return hotp(segreto, int(istante // PASSO), cifre, algoritmo)


def nuovo_segreto_base32():
    """Segreto casuale di 160 bit nel formato Base32 usato dalle app di autenticazione."""
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii")


def da_base32(testo):
    """Converte un segreto Base32 (spazi e minuscole ammessi) in byte."""
    testo = testo.replace(" ", "").upper()
    testo += "=" * (-len(testo) % 8)
    return base64.b32decode(testo)


if __name__ == "__main__":
    segreto_b32 = nuovo_segreto_base32()
    print("Segreto di prova (Base32):", segreto_b32)
    print("Inserirlo in KeePassXC come segreto TOTP di una voce di prova, poi confrontare i codici.")
    segreto = da_base32(segreto_b32)
    try:
        while True:
            restano = PASSO - int(time.time()) % PASSO
            print(f"Codice: {totp(segreto)}   (valido ancora {restano:2d} s)", end="\r")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nFine.")
