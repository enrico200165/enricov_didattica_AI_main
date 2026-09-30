"""Prepara la cartella 'scaricati' per l'esercizio di verifica delle impronte (uso del docente).

Crea tre file e il file di impronte 'scaricati.DIGEST', poi modifica di nascosto uno dei file:
gli studenti devono scoprire quale, usando Get-FileHash oppure impronte.py.
Esecuzione: python prepara_esercizio.py
"""

import random
from pathlib import Path

from impronte import impronta_file

cartella = Path("scaricati")
cartella.mkdir(exist_ok=True)

contenuti = {
    "programma_v1.0.txt": "Programma di esempio, versione 1.0\n" * 200,
    "manuale.txt": "Manuale d'uso del programma di esempio.\n" * 300,
    "dati_esempio.csv": "id;nome;valore\n" + "".join(f"{i};voce{i};{i * 7 % 100}\n" for i in range(1, 501)),
}
for nome, testo in contenuti.items():
    (cartella / nome).write_bytes(testo.encode("utf-8"))

righe = [f"{impronta_file(cartella / nome)}  {nome}" for nome in contenuti]
(cartella / "scaricati.DIGEST").write_text("\n".join(righe) + "\n", encoding="utf-8")

# modifica di un solo carattere in un file scelto a caso, dopo il calcolo delle impronte
scelto = random.choice(list(contenuti))
dati = bytearray((cartella / scelto).read_bytes())
posizione = random.randrange(len(dati))
dati[posizione] = ord("X") if dati[posizione] != ord("X") else ord("Y")
(cartella / scelto).write_bytes(bytes(dati))

print(f"Cartella '{cartella}' pronta: 3 file e scaricati.DIGEST.")
print(f"(Solo per il docente) file modificato: {scelto}, byte in posizione {posizione}.")
