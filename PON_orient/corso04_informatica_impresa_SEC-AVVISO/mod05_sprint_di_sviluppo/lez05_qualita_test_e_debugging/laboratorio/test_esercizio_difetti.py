"""Verifica dell'esercizio (per il docente): i sei difetti di kit_con_difetti sono riproducibili.

Esecuzione: python test_esercizio_difetti.py
Il controllo gira in un processo separato, dentro una copia temporanea del kit con difetti.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


PROVA = r'''
import json, logica, archivio
aule = archivio.carica_aule()
risultati = {}
try:
    logica.nuova_prenotazione([], aule, "lab-inf1", "2026-10-16", "9:00", "10:00", "A. Rossi")
    risultati["minuscolo"] = "accettato"
except logica.ErrorePrenotazione as e:
    risultati["minuscolo"] = str(e)
try:
    logica.nuova_prenotazione([], aule, "PAL", "2026-10-16", "17:00", "18:00", "A. Rossi")
    risultati["chiusura"] = "accettato"
except logica.ErrorePrenotazione as e:
    risultati["chiusura"] = str(e)
elenco = [{"id": 1, "aula": "LAB-CHI"}, {"id": 5, "aula": "LAB-CHI"}]
risultati["numero"] = logica.nuova_prenotazione(elenco, aule, "LAB-FIS", "2026-10-16", "9:00", "10:00", "A. Rossi")["id"]
risultati["spazi"] = logica.nuova_prenotazione([], aule, "LAB-FIS", "2026-10-16", "9:00", "10:00", "   ")["richiedente"]
archivio.salva_prenotazioni([{"motivo": "Attività"}], "dati_prova")
risultati["accenti"] = open("dati_prova/prenotazioni.json", encoding="utf-8").read()
print(json.dumps(risultati))
'''

with tempfile.TemporaryDirectory() as d:
    copia = Path(d) / "kit"
    shutil.copytree(Path(__file__).with_name("kit_con_difetti"), copia)
    r = subprocess.run([sys.executable, "-c", PROVA], cwd=copia, capture_output=True, text=True, encoding="utf-8")
    esiti = json.loads(r.stdout)
    verifica("difetto 1: codice in minuscolo rifiutato", "non esiste" in esiti["minuscolo"])
    verifica("difetto 2: prenotazione fino alle 18:00 rifiutata", "aperta" in esiti["chiusura"])
    verifica("difetto 4: con i numeri 1 e 5 la nuova prenotazione riceve 3 invece di 6", esiti["numero"] == 3)
    verifica("difetto 5: richiedente fatto di spazi accettato e salvato vuoto", esiti["spazi"] == "")
    verifica("difetto 6: lettere accentate scritte come codici", "\\u00e0" in esiti["accenti"])
    r = subprocess.run([sys.executable, "prenotazioni.py", "--dati", "dati_prova", "prenota", "LAB-FIS", "2026-10-16",
                        "9:00", "11:00", "A. Rossi"], cwd=copia, capture_output=True, text=True, encoding="utf-8")
    verifica("difetto 3: conferma con orario 09:00-09:00", "09:00-09:00" in r.stdout)
    r = subprocess.run([sys.executable, "-m", "unittest"], cwd=copia, capture_output=True, text=True, encoding="utf-8")
    verifica("i 22 test del kit con difetti passano comunque", r.returncode == 0 and "Ran 22 tests" in r.stderr)

    # correzioni della tabella delle soluzioni: dopo averle applicate, i test originali del kit passano
    kit = Path(__file__).resolve().parents[3] / "mod01_progetti_e_team" / "lez03_kit_di_progetto_e_squadre" / "laboratorio" / "kit_prenotazioni"
    if kit.exists():
        correzioni = [("logica.py", 'codice.strip():', 'codice.strip().upper():'),
                      ("logica.py", "ora_fine >= CHIUSURA", "ora_fine > CHIUSURA"),
                      ("logica.py", "if not richiedente:", "if not richiedente.strip():"),
                      ("logica.py", "nuovo_id = len(prenotazioni) + 1", 'nuovo_id = max((p["id"] for p in prenotazioni), default=0) + 1'),
                      ("prenotazioni.py", "{p['inizio']}-{p['inizio']}", "{p['inizio']}-{p['fine']}"),
                      ("archivio.py", "json.dump(prenotazioni, f, indent=2)", "json.dump(prenotazioni, f, ensure_ascii=False, indent=2)")]
        for nome, prima, dopo in correzioni:
            percorso = copia / nome
            percorso.write_text(percorso.read_text(encoding="utf-8").replace(prima, dopo), encoding="utf-8")
        shutil.rmtree(copia / "tests")
        shutil.copytree(kit / "tests", copia / "tests")
        r = subprocess.run([sys.executable, "-m", "unittest"], cwd=copia, capture_output=True, text=True, encoding="utf-8")
        verifica("con le sei correzioni passano tutti i 27 test del kit originale", r.returncode == 0 and "Ran 27 tests" in r.stderr)
        for nome in ("logica.py", "archivio.py", "prenotazioni.py"):
            verifica(f"{nome} corretto uguale a quello del kit",
                     (copia / nome).read_text(encoding="utf-8") == (kit / nome).read_text(encoding="utf-8"))
    else:
        print("SALTATI i test delle correzioni: kit originale non trovato")

print(f"\nTest superati: {superati}, falliti: {falliti}")
