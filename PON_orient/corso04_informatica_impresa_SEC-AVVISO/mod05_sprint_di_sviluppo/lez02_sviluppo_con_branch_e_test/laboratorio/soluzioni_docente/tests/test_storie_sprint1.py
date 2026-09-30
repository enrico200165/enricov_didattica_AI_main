"""Test delle storie US-01, US-02 e US-03, scritti dai criteri di accettazione (soluzione per il docente)."""

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import archivio
import logica
import prenotazioni

AULE = [
    {"codice": "LAB-INF1", "nome": "Laboratorio di informatica 1", "tipo": "laboratorio", "posti": 28},
    {"codice": "LAB-INF2", "nome": "Laboratorio di informatica 2", "tipo": "laboratorio", "posti": 24},
    {"codice": "LAB-CHI", "nome": "Laboratorio di chimica", "tipo": "laboratorio", "posti": 24},
]


class TestUS01NessunaSovrapposizione(unittest.TestCase):

    def setUp(self):
        # Dato che LAB-INF1 è prenotato il 12/10 dalle 9:00 alle 11:00
        self.prenotazioni = []
        logica.nuova_prenotazione(self.prenotazioni, AULE, "LAB-INF1", "2026-10-12", "9:00", "11:00", "M. Bianchi")

    def test_criterio_1_sovrapposizione_rifiutata(self):
        # quando prenoto LAB-INF1 il 12/10 dalle 10:00 alle 12:00
        with self.assertRaises(logica.ErrorePrenotazione) as errore:
            logica.nuova_prenotazione(self.prenotazioni, AULE, "LAB-INF1", "2026-10-12", "10:00", "12:00", "L. Verdi")
        # allora la prenotazione è rifiutata con un messaggio che indica la prenotazione già presente
        self.assertIn("già prenotato dalle 09:00 alle 11:00 (prenotazione 1, M. Bianchi)", str(errore.exception))
        self.assertEqual(len(self.prenotazioni), 1)

    def test_criterio_2_orari_che_si_toccano(self):
        p = logica.nuova_prenotazione(self.prenotazioni, AULE, "LAB-INF1", "2026-10-12", "11:00", "12:00", "L. Verdi")
        self.assertEqual(p["id"], 2)

    def test_criterio_3_altra_aula(self):
        p = logica.nuova_prenotazione(self.prenotazioni, AULE, "LAB-CHI", "2026-10-12", "9:00", "11:00", "L. Verdi")
        self.assertEqual(p["aula"], "LAB-CHI")

    def test_altro_giorno_accettato(self):
        p = logica.nuova_prenotazione(self.prenotazioni, AULE, "LAB-INF1", "2026-10-13", "9:00", "11:00", "L. Verdi")
        self.assertEqual(p["giorno"], "2026-10-13")

    def test_prenotazione_che_contiene_un_altra(self):
        with self.assertRaises(logica.ErrorePrenotazione):
            logica.nuova_prenotazione(self.prenotazioni, AULE, "LAB-INF1", "2026-10-12", "8:00", "12:00", "L. Verdi")

    def test_funzione_si_sovrappongono(self):
        t = logica.leggi_ora
        casi = [(("9:00", "11:00", "10:00", "12:00"), True), (("9:00", "11:00", "11:00", "12:00"), False),
                (("9:00", "11:00", "8:00", "9:00"), False), (("9:00", "11:00", "9:30", "10:00"), True)]
        for (a, b, c, d), atteso in casi:
            with self.subTest(intervalli=(a, b, c, d)):
                self.assertEqual(logica.si_sovrappongono(t(a), t(b), t(c), t(d)), atteso)


class TestUS02PrenotazioniDelGiorno(unittest.TestCase):

    def test_criterio_1_solo_il_giorno_ordinate(self):
        elenco = [
            {"id": 1, "aula": "LAB-INF1", "giorno": "2026-10-12", "inizio": "11:00"},
            {"id": 2, "aula": "LAB-CHI", "giorno": "2026-10-12", "inizio": "10:00"},
            {"id": 3, "aula": "LAB-INF1", "giorno": "2026-10-12", "inizio": "09:00"},
            {"id": 4, "aula": "LAB-CHI", "giorno": "2026-10-13", "inizio": "08:00"},
        ]
        risultato = logica.prenotazioni_del_giorno(elenco, "2026-10-12")
        self.assertEqual([p["id"] for p in risultato], [2, 3, 1])

    def test_criterio_2_giorno_senza_prenotazioni(self):
        self.assertEqual(logica.prenotazioni_del_giorno([], "2026-10-13"), [])

    def test_data_non_valida(self):
        with self.assertRaises(logica.ErrorePrenotazione):
            logica.prenotazioni_del_giorno([], "13/10/2026")


class TestUS03Cancellazione(unittest.TestCase):

    def setUp(self):
        self.prenotazioni = [{"id": 5, "richiedente": "M. Bianchi"}, {"id": 6, "richiedente": "L. Verdi"}]

    def test_criterio_1_cancella_la_propria(self):
        p = logica.cancella_prenotazione(self.prenotazioni, 5, "m. bianchi ")
        self.assertEqual(p["id"], 5)
        self.assertEqual([x["id"] for x in self.prenotazioni], [6])

    def test_criterio_2_prenotazione_di_altri(self):
        with self.assertRaisesRegex(logica.ErrorePrenotazione, "è di M. Bianchi"):
            logica.cancella_prenotazione(self.prenotazioni, 5, "L. Verdi")
        self.assertEqual(len(self.prenotazioni), 2)

    def test_criterio_3_prenotazione_inesistente(self):
        with self.assertRaisesRegex(logica.ErrorePrenotazione, "la prenotazione 99 non esiste"):
            logica.cancella_prenotazione(self.prenotazioni, 99, "M. Bianchi")


class TestComandi(unittest.TestCase):

    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.cartella = Path(self._temp.name)
        shutil.copy(archivio.CARTELLA_DATI / "aule.json", self.cartella)

    def tearDown(self):
        self._temp.cleanup()

    def esegui(self, *argomenti):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            codice = prenotazioni.main(["--dati", str(self.cartella), *argomenti])
        return codice, out.getvalue(), err.getvalue()

    def test_giorno_e_cancella(self):
        self.esegui("prenota", "LAB-CHI", "2026-10-12", "10:00", "12:00", "L. Verdi", "--motivo", "Titolazioni")
        self.esegui("prenota", "LAB-CHI", "2026-10-12", "8:00", "9:00", "L. Verdi")
        _, out, _ = self.esegui("giorno", "2026-10-12")
        righe = out.splitlines()
        self.assertEqual(len(righe), 2)
        self.assertTrue(righe[0].startswith("LAB-CHI   08:00-09:00"))
        self.assertIn("Titolazioni", righe[1])
        codice, out, _ = self.esegui("cancella", "2", "L. Verdi")
        self.assertEqual(codice, 0)
        self.assertIn("Prenotazione 2 cancellata", out)
        self.assertEqual(len(archivio.carica_prenotazioni(self.cartella)), 1)

    def test_giorno_vuoto(self):
        _, out, _ = self.esegui("giorno", "2026-10-13")
        self.assertEqual(out.strip(), "Nessuna prenotazione")

    def test_sovrapposizione_dalla_riga_di_comando(self):
        self.esegui("prenota", "LAB-INF1", "2026-10-12", "9:00", "11:00", "M. Bianchi")
        codice, _, err = self.esegui("prenota", "LAB-INF1", "2026-10-12", "10:00", "12:00", "L. Verdi")
        self.assertEqual(codice, 1)
        self.assertIn("già prenotato", err)

    def test_dati_di_esempio_senza_sovrapposizioni(self):
        elenco = archivio.carica_prenotazioni()
        for i, a in enumerate(elenco):
            for b in elenco[i + 1:]:
                if a["aula"] == b["aula"] and a["giorno"] == b["giorno"]:
                    t = logica.leggi_ora
                    self.assertFalse(logica.si_sovrappongono(t(a["inizio"]), t(a["fine"]), t(b["inizio"]), t(b["fine"])),
                                     f"prenotazioni {a['id']} e {b['id']} sovrapposte")


if __name__ == "__main__":
    unittest.main()
