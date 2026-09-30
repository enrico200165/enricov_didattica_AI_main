"""Test dell'interfaccia a riga di comando (modulo prenotazioni)."""

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import archivio
import prenotazioni


class TestRigaDiComando(unittest.TestCase):

    def setUp(self):
        # copia delle aule del kit in una cartella temporanea, senza prenotazioni
        self._temp = tempfile.TemporaryDirectory()
        self.cartella = Path(self._temp.name)
        shutil.copy(archivio.CARTELLA_DATI / "aule.json", self.cartella)

    def tearDown(self):
        self._temp.cleanup()

    def esegui(self, *argomenti):
        """Esegue il programma e restituisce codice di uscita, output ed errori."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            codice = prenotazioni.main(["--dati", str(self.cartella), *argomenti])
        return codice, out.getvalue(), err.getvalue()

    def test_elenco_aule(self):
        codice, out, _ = self.esegui("aule")
        self.assertEqual(codice, 0)
        self.assertIn("LAB-INF1", out)
        self.assertIn("Palestra", out)

    def test_elenco_aule_per_tipo(self):
        _, out, _ = self.esegui("aule", "--tipo", "palestra")
        self.assertIn("PAL", out)
        self.assertNotIn("LAB-INF1", out)

    def test_elenco_aule_tipo_inesistente(self):
        _, out, _ = self.esegui("aule", "--tipo", "piscina")
        self.assertIn("Nessuna aula", out)

    def test_prenota_e_salva(self):
        codice, out, _ = self.esegui("prenota", "LAB-INF1", "2026-10-12", "9:00", "11:00",
                                     "M. Bianchi", "--motivo", "Esercitazione")
        self.assertEqual(codice, 0)
        self.assertIn("Prenotazione 1 registrata", out)
        salvate = archivio.carica_prenotazioni(self.cartella)
        self.assertEqual(len(salvate), 1)
        self.assertEqual(salvate[0]["motivo"], "Esercitazione")

    def test_due_prenotazioni_numeri_diversi(self):
        self.esegui("prenota", "LAB-CHI", "2026-10-12", "8:00", "9:00", "L. Verdi")
        _, out, _ = self.esegui("prenota", "LAB-CHI", "2026-10-13", "8:00", "9:00", "L. Verdi")
        self.assertIn("Prenotazione 2 registrata", out)

    def test_errore_con_messaggio_e_codice_1(self):
        codice, out, err = self.esegui("prenota", "LAB-XYZ", "2026-10-12", "9:00", "11:00", "M. Bianchi")
        self.assertEqual(codice, 1)
        self.assertIn("Errore: l'aula LAB-XYZ non esiste", err)
        self.assertEqual(archivio.carica_prenotazioni(self.cartella), [])


if __name__ == "__main__":
    unittest.main()
