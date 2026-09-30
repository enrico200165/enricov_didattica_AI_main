"""Test di cifrari_storici.py. Esecuzione: python test_cifrari_storici.py"""

from cifrari_storici import (cesare, decifra_cesare, tutte_le_chiavi_cesare,
                             chiave_cesare_probabile, vigenere, xor_bytes, chiave_casuale)

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


verifica("Cesare con chiave 3", cesare("Ciao, Roma!", 3) == "Fldr, Urpd!")
verifica("Cesare: la Z torna all'inizio", cesare("xyz", 3) == "abc")
verifica("Cesare con chiave 13 applicato due volte (ROT13)", cesare(cesare("Segreto", 13), 13) == "Segreto")
verifica("decifratura di Cesare", decifra_cesare("Fldr", 3) == "Ciao")
verifica("25 chiavi possibili", len(tutte_le_chiavi_cesare("ABC")) == 25)
testo = "La crittografia studia i metodi per rendere un messaggio comprensibile solo a chi conosce la chiave"
verifica("analisi delle frequenze trova la chiave 7", chiave_cesare_probabile(cesare(testo, 7)) == 7)
verifica("analisi delle frequenze trova la chiave 19", chiave_cesare_probabile(cesare(testo, 19)) == 19)
verifica("Vigenère, esempio classico", vigenere("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR")
verifica("Vigenère: cifra e decifra", vigenere(vigenere(testo, "SOLE"), "SOLE", decifra=True) == testo)
verifica("Vigenère: spazi e punteggiatura invariati", vigenere("a b, c", "B") == "b c, d")
dati = "Messaggio riservato".encode("utf-8")
k = chiave_casuale(len(dati))
verifica("XOR: stessa chiave per cifrare e decifrare", xor_bytes(xor_bytes(dati, k), k) == dati)
verifica("XOR: il cifrato è diverso dal messaggio", xor_bytes(dati, k) != dati)
verifica("chiave casuale della lunghezza richiesta", len(chiave_casuale(32)) == 32)
# riuso della chiave: lo XOR di due cifrati con la stessa chiave è lo XOR dei due messaggi
m1, m2 = b"ATTACCARE ALLE 9", b"RITIRARSI SUBITO"
k = chiave_casuale(16)
verifica("riuso della chiave: c1 XOR c2 = m1 XOR m2",
         xor_bytes(xor_bytes(m1, k), xor_bytes(m2, k)) == xor_bytes(m1, m2))

print(f"Test superati: {superati}, falliti: {falliti}")
