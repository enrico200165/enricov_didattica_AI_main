"""Test della lettura e scrittura dei file JSON (modulo archivio)."""

import json
import tempfile
import unittest
from pathlib import Path

import archivio


class TestArchivio(unittest.TestCase):

    def setUp(self):
        # una cartella temporanea per ogni test: i dati veri non vengono toccati
        self._temp = tempfile.TemporaryDirectory()
        self.cartella = Path(self._temp.name)

    def tearDown(self):
        self._temp.cleanup()

    def test_dati_del_kit_leggibili(self):
        aule = archivio.carica_aule()
        self.assertGreaterEqual(len(aule), 1)
        self.assertEqual(set(aule[0]), {"codice", "nome", "tipo", "posti"})
        self.assertIsInstance(archivio.carica_prenotazioni(), list)

    def test_salva_e_rileggi(self):
        prenotazioni = [{"id": 1, "aula": "LAB-CHI", "giorno": "2026-10-12",
                         "inizio": "10:00", "fine": "12:00",
                         "richiedente": "N. Esposito", "motivo": "Attività di laboratorio"}]
        archivio.salva_prenotazioni(prenotazioni, self.cartella)
        self.assertEqual(archivio.carica_prenotazioni(self.cartella), prenotazioni)
        self.assertFalse((self.cartella / "prenotazioni.tmp").exists())

    def test_file_prenotazioni_mancante(self):
        self.assertEqual(archivio.carica_prenotazioni(self.cartella), [])

    def test_file_aule_mancante(self):
        with self.assertRaisesRegex(archivio.ErroreArchivio, "manca"):
            archivio.carica_aule(self.cartella)

    def test_json_non_valido(self):
        (self.cartella / "prenotazioni.json").write_text('[{"id": 1,}]', encoding="utf-8")
        with self.assertRaisesRegex(archivio.ErroreArchivio, "non è un JSON valido"):
            archivio.carica_prenotazioni(self.cartella)

    def test_aule_json_del_kit_ha_codici_unici(self):
        codici = [a["codice"] for a in json.loads(
            (archivio.CARTELLA_DATI / "aule.json").read_text(encoding="utf-8"))]
        self.assertEqual(len(codici), len(set(codici)))


if __name__ == "__main__":
    unittest.main()
