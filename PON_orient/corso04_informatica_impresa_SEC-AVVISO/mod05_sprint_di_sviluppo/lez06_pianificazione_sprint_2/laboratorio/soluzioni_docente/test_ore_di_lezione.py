"""Test di ore_di_lezione.py, dai criteri di accettazione di US-16. Esecuzione: python -m unittest test_ore_di_lezione"""

import unittest

import ore_di_lezione as o


class TestUS16OreDiLezione(unittest.TestCase):

    def test_criterio_1_dalla_seconda_alla_terza(self):
        # Dato l'orario della scuola, quando indico le ore 2-3, allora la prenotazione va dalle 9:00 alle 11:00
        self.assertEqual(o.orari_da_ore("2-3"), ("09:00", "11:00"))

    def test_criterio_2_una_sola_ora(self):
        self.assertEqual(o.orari_da_ore("4"), ("11:00", "12:00"))

    def test_criterio_3_ore_non_valide(self):
        for testo in ("0", "11", "3-12", "tre", "2-3-4", ""):
            with self.subTest(testo=testo):
                with self.assertRaises(o.ErroreOre):
                    o.orari_da_ore(testo)

    def test_prima_dopo_ultima(self):
        with self.assertRaisesRegex(o.ErroreOre, "precedere"):
            o.orari_da_ore("5-3")

    def test_scritture_accettate(self):
        self.assertEqual(o.orari_da_ore("2ª-3ª"), ("09:00", "11:00"))
        self.assertEqual(o.orari_da_ore(" 7 - 10 "), ("14:00", "18:00"))

    def test_ore_consecutive_senza_buchi(self):
        for n in range(1, 10):
            self.assertEqual(o.ORE[n][1], o.ORE[n + 1][0])


if __name__ == "__main__":
    unittest.main()
