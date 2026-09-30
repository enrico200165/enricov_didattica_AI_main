"""Test di backup.py. Esecuzione: python test_backup.py (usa solo cartelle temporanee)."""

import tempfile
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

from backup import crea, verifica, ripristina, conserva_ultimi, NOME_IMPRONTE

superati = falliti = 0


def verifica_test(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


base = Path(tempfile.mkdtemp())
dati = base / "ufficio"
(dati / "verbali").mkdir(parents=True)
(dati / "elenco_fornitori.csv").write_text("fornitore;telefono\nCartoleria Esempio;000 0000000\n", encoding="utf-8")
(dati / "verbali" / "verbale_settembre.txt").write_text("Verbale della riunione di settembre.\n" * 50, encoding="utf-8")
(dati / "logo.bin").write_bytes(bytes(range(256)) * 100)

archivio = crea(dati, base / "backup", adesso=datetime(2026, 10, 7, 18, 0, 0))
verifica_test("nome dell'archivio con data e ora", archivio.name == "backup_20261007_180000.zip")
with zipfile.ZipFile(archivio) as z:
    nomi = set(z.namelist())
verifica_test("archivio con i tre file e le impronte",
              nomi == {"elenco_fornitori.csv", "verbali/verbale_settembre.txt", "logo.bin", NOME_IMPRONTE})
verifica_test("archivio integro", verifica(archivio) == [])

n, problemi = ripristina(archivio, base / "prova_ripristino")
verifica_test("ripristino di 3 file senza problemi", n == 3 and problemi == [])
verifica_test("contenuto ripristinato identico",
              (base / "prova_ripristino" / "verbali" / "verbale_settembre.txt").read_bytes()
              == (dati / "verbali" / "verbale_settembre.txt").read_bytes())
try:
    ripristina(archivio, base / "prova_ripristino")
    verifica_test("ripristino in una cartella non vuota rifiutato", False)
except ValueError:
    verifica_test("ripristino in una cartella non vuota rifiutato", True)

# archivio modificato: un file sostituito dopo la creazione
alterato = base / "backup" / "alterato.zip"
with zipfile.ZipFile(archivio) as origine, zipfile.ZipFile(alterato, "w") as copia:
    for nome in origine.namelist():
        contenuto = origine.read(nome)
        if nome == "elenco_fornitori.csv":
            contenuto = contenuto.replace(b"000", b"111")
        copia.writestr(nome, contenuto)
verifica_test("file modificato individuato", verifica(alterato) == ["impronta diversa: elenco_fornitori.csv"])
alterato.unlink()

try:
    crea(dati, dati / "backup")
    verifica_test("destinazione dentro la cartella da salvare rifiutata", False)
except ValueError:
    verifica_test("destinazione dentro la cartella da salvare rifiutata", True)

inizio = datetime(2026, 10, 8, 18, 0, 0)
for giorno in range(9):
    crea(dati, base / "backup", adesso=inizio + timedelta(days=giorno))
eliminati = conserva_ultimi(base / "backup", 7)
rimasti = sorted(p.name for p in (base / "backup").glob("backup_*.zip"))
verifica_test("conservati solo gli ultimi 7 backup", len(rimasti) == 7 and rimasti[-1] == "backup_20261016_180000.zip")
verifica_test("eliminati i 3 più vecchi", eliminati == ["backup_20261007_180000.zip", "backup_20261008_180000.zip",
                                                       "backup_20261009_180000.zip"])

print(f"Test superati: {superati}, falliti: {falliti}")
