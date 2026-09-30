"""Verifica di totp.py con i vettori di prova ufficiali della RFC 6238 (appendice B)."""
import hashlib

from totp import da_base32, totp

SEGRETO_SHA1 = b"12345678901234567890"
ATTESI = {          # istante (secondi Unix) -> codice a 8 cifre, algoritmo SHA-1
    59: "94287082",
    1111111109: "07081804",
    1111111111: "14050471",
    1234567890: "89005924",
    2000000000: "69279037",
    20000000000: "65353130",
}

falliti = 0
for istante, atteso in ATTESI.items():
    ottenuto = totp(SEGRETO_SHA1, istante, cifre=8, algoritmo=hashlib.sha1)
    esito = "OK     " if ottenuto == atteso else "FALLITO"
    falliti += ottenuto != atteso
    print(f"{esito} t={istante}: atteso {atteso}, ottenuto {ottenuto}")

# stesso segreto scritto in Base32 (come nelle app): deve dare lo stesso risultato
b32 = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
esito = totp(da_base32(b32), 59, cifre=8) == "94287082"
falliti += not esito
print(("OK     " if esito else "FALLITO") + " conversione da Base32")
print(f"Test falliti: {falliti}")
