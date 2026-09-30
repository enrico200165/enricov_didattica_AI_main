"""Memorizzazione sicura delle password (lezione 2.2).

Un servizio non deve mai conservare le password in chiaro: conserva, per ogni utente,
un sale casuale e il risultato di una funzione di derivazione lenta (PBKDF2-HMAC-SHA256).
Al login ricalcola il valore con la password inserita e lo confronta con quello salvato.
"""
import hashlib
import hmac
import json
import secrets

ALGORITMO = "pbkdf2_sha256"
ITERAZIONI = 600_000      # valore raccomandato da OWASP per PBKDF2-HMAC-SHA256
LUNGHEZZA_SALE = 16       # byte


def deriva(password, sale, iterazioni=ITERAZIONI):
    """Valore derivato dalla password con PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), sale, iterazioni)


def crea_record(password):
    """Record da salvare al posto della password: algoritmo, iterazioni, sale, valore derivato."""
    sale = secrets.token_bytes(LUNGHEZZA_SALE)
    return {
        "algoritmo": ALGORITMO,
        "iterazioni": ITERAZIONI,
        "sale": sale.hex(),
        "hash": deriva(password, sale).hex(),
    }


def verifica_password(password, record):
    """True se la password corrisponde al record salvato."""
    if record["algoritmo"] != ALGORITMO:
        raise ValueError("algoritmo non supportato")
    sale = bytes.fromhex(record["sale"])
    calcolato = deriva(password, sale, record["iterazioni"])
    # confronto a tempo costante: non rivela quanti byte iniziali coincidono
    return hmac.compare_digest(calcolato, bytes.fromhex(record["hash"]))


class Archivio:
    """Archivio di utenti salvato in un file JSON."""

    def __init__(self, percorso):
        self.percorso = percorso
        try:
            with open(percorso, encoding="utf-8") as f:
                self.utenti = json.load(f)
        except FileNotFoundError:
            self.utenti = {}

    def salva(self):
        with open(self.percorso, "w", encoding="utf-8") as f:
            json.dump(self.utenti, f, indent=2)

    def registra(self, nome, password):
        if nome in self.utenti:
            raise ValueError(f"utente {nome} già registrato")
        self.utenti[nome] = crea_record(password)
        self.salva()

    def login(self, nome, password):
        record = self.utenti.get(nome)
        if record is None:
            # stessa risposta per utente inesistente e password errata:
            # non si rivela quali nomi utente esistono
            return False
        return verifica_password(password, record)
