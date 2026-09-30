"""Test delle regole dell'applicazione (modulo logica)."""

import unittest

import logica

AULE = [
    {"codice": "LAB-INF1", "nome": "Laboratorio di informatica 1", "tipo": "laboratorio", "posti": 28},
    {"codice": "AULA-MAG", "nome": "Aula magna", "tipo": "aula", "posti": 150},
    {"codice": "LAB-CHI", "nome": "Laboratorio di chimica", "tipo": "laboratorio", "posti": 24},
]


class TestElencoAule(unittest.TestCase):

    def test_ordinate_per_codice(self):
        codici = [a["codice"] for a in logica.elenco_aule(AULE)]
        self.assertEqual(codici, ["AULA-MAG", "LAB-CHI", "LAB-INF1"])

    def test_filtro_per_tipo(self):
        codici = [a["codice"] for a in logica.elenco_aule(AULE, "laboratorio")]
        self.assertEqual(codici, ["LAB-CHI", "LAB-INF1"])

    def test_tipo_inesistente(self):
        self.assertEqual(logica.elenco_aule(AULE, "piscina"), [])


class TestNuovaPrenotazione(unittest.TestCase):

    def setUp(self):
        # setUp viene eseguito prima di ogni test: ogni test parte da un elenco vuoto
        self.prenotazioni = []

    def prenota(self, aula="LAB-INF1", giorno="2026-10-12", inizio="9:00", fine="11:00",
                richiedente="M. Bianchi", motivo=""):
        return logica.nuova_prenotazione(self.prenotazioni, AULE, aula, giorno, inizio,
                                         fine, richiedente, motivo)

    def test_prenotazione_valida(self):
        p = self.prenota(motivo="  Esercitazione 3A ")
        self.assertEqual(p, {"id": 1, "aula": "LAB-INF1", "giorno": "2026-10-12",
                             "inizio": "09:00", "fine": "11:00",
                             "richiedente": "M. Bianchi", "motivo": "Esercitazione 3A"})
        self.assertEqual(self.prenotazioni, [p])

    def test_id_successivo_al_massimo(self):
        # prenotazioni complete (US-01 controlla aula, giorno e orari di quelle esistenti)
        altre = {"aula": "LAB-CHI", "giorno": "2026-10-01", "inizio": "08:00", "fine": "09:00"}
        self.prenotazioni.extend([{"id": 3, **altre}, {"id": 7, **altre}])
        self.assertEqual(self.prenota()["id"], 8)

    def test_codice_aula_in_minuscolo(self):
        self.assertEqual(self.prenota(aula=" lab-chi ")["aula"], "LAB-CHI")

    def test_aula_inesistente(self):
        with self.assertRaisesRegex(logica.ErrorePrenotazione, "non esiste"):
            self.prenota(aula="LAB-XYZ")

    def test_data_non_valida(self):
        for giorno in ["2026-02-30", "12/10/2026", "domani"]:
            with self.subTest(giorno=giorno):
                with self.assertRaisesRegex(logica.ErrorePrenotazione, "data non valida"):
                    self.prenota(giorno=giorno)

    def test_orario_non_valido(self):
        for ora in ["25:00", "9.00", "nove"]:
            with self.subTest(ora=ora):
                with self.assertRaisesRegex(logica.ErrorePrenotazione, "orario non valido"):
                    self.prenota(inizio=ora)

    def test_fine_non_successiva_a_inizio(self):
        with self.assertRaisesRegex(logica.ErrorePrenotazione, "fine"):
            self.prenota(inizio="11:00", fine="11:00")

    def test_fuori_orario_di_apertura(self):
        for inizio, fine in [("7:30", "9:00"), ("17:00", "18:30")]:
            with self.subTest(inizio=inizio, fine=fine):
                with self.assertRaisesRegex(logica.ErrorePrenotazione, "aperta"):
                    self.prenota(inizio=inizio, fine=fine)

    def test_orario_di_apertura_completo_accettato(self):
        p = self.prenota(inizio="8:00", fine="18:00")
        self.assertEqual((p["inizio"], p["fine"]), ("08:00", "18:00"))

    def test_richiedente_mancante(self):
        with self.assertRaisesRegex(logica.ErrorePrenotazione, "chi prenota"):
            self.prenota(richiedente="   ")

    def test_errore_non_modifica_elenco(self):
        with self.assertRaises(logica.ErrorePrenotazione):
            self.prenota(aula="LAB-XYZ")
        self.assertEqual(self.prenotazioni, [])


if __name__ == "__main__":
    unittest.main()
