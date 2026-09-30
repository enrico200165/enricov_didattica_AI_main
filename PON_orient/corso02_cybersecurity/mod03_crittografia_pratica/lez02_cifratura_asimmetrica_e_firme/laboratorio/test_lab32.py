"""Test di impronte.py e chiavi_giocattolo.py. Esecuzione: python test_lab32.py"""

import hashlib
import tempfile
from pathlib import Path

from impronte import impronta_file, coincide, leggi_digest, verifica_digest
from chiavi_giocattolo import (dh_segreto, dh_pubblico, dh_condiviso,
                               rsa_genera, rsa_cifra, rsa_decifra, rsa_firma, rsa_verifica)

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    (d / "vuoto.txt").write_bytes(b"")
    (d / "abc.txt").write_bytes(b"abc")
    grande = bytes(range(256)) * 20000          # circa 5 MB, letto a blocchi
    (d / "grande.bin").write_bytes(grande)

    verifica("SHA-256 del file vuoto (valore noto)",
             impronta_file(d / "vuoto.txt") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    verifica("SHA-256 di 'abc' (vettore di prova FIPS 180)",
             impronta_file(d / "abc.txt") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    verifica("file grande letto a blocchi", impronta_file(d / "grande.bin") == hashlib.sha256(grande).hexdigest())
    verifica("confronto indipendente da maiuscole e spazi",
             coincide("ba7816bf8f01cfea", "BA7816BF 8F01CFEA"))
    verifica("confronto: impronte diverse", not coincide("ba7816bf", "ba7816bE"))

    (d / "abc_modificato.txt").write_bytes(b"abd")
    righe = [
        f"{impronta_file(d / 'abc.txt')}  abc.txt",
        f"{impronta_file(d / 'grande.bin')} *grande.bin",
        f"{impronta_file(d / 'abc.txt')}  abc_modificato.txt",
        f"{impronta_file(d / 'abc.txt')}  inesistente.txt",
    ]
    (d / "prova.DIGEST").write_text("\n".join(righe) + "\n", encoding="utf-8")
    verifica("lettura del file di impronte", len(leggi_digest(d / "prova.DIGEST")) == 4)
    esiti = verifica_digest(d / "prova.DIGEST")
    verifica("file integro: OK", esiti["abc.txt"] == "OK")
    verifica("formato con asterisco: OK", esiti["grande.bin"] == "OK")
    verifica("file modificato: DIVERSA", esiti["abc_modificato.txt"] == "DIVERSA")
    verifica("file assente: MANCANTE", esiti["inesistente.txt"] == "MANCANTE")

a, b = dh_segreto(), dh_segreto()
verifica("Diffie-Hellman: stesso segreto per le due parti",
         dh_condiviso(a, dh_pubblico(b)) == dh_condiviso(b, dh_pubblico(a)))

pubblica, privata = rsa_genera()
verifica("RSA: chiavi dell'esempio classico (n = 3233, d = 2753)", pubblica == (3233, 17) and privata == (3233, 2753))
verifica("RSA: 65 cifrato vale 2790", rsa_cifra(65, pubblica) == 2790)
verifica("RSA: decifratura di tutti i valori da 0 a n - 1",
         all(rsa_decifra(rsa_cifra(m, pubblica), privata) == m for m in range(3233)))
firma = rsa_firma("Voto finale: 8", privata)
verifica("firma: verifica del messaggio originale", rsa_verifica("Voto finale: 8", firma, pubblica))
verifica("firma: messaggio modificato rifiutato", not rsa_verifica("Voto finale: 9", firma, pubblica))
altra_pubblica, _ = rsa_genera(p=67, q=71, e=17)
verifica("firma: chiave pubblica di un'altra persona rifiuta la firma",
         not rsa_verifica("Voto finale: 8", firma, altra_pubblica))

print(f"Test superati: {superati}, falliti: {falliti}")
