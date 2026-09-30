"""Simulazione della risoluzione DNS iterativa, con memoria (cache) e TTL.

Un risolutore ricorsivo (per esempio quello del fornitore di accesso) riceve
la domanda del PC e interroga in sequenza i server della gerarchia: radice,
dominio di primo livello (TLD), server autorevole del dominio. Conserva le
risposte per la durata indicata dal TTL, per rispondere subito alle domande
successive. I nomi usano il dominio riservato .example (RFC 2606).

Uso: python risolutore_dns.py [nome]
"""

import sys

# Zone dei server simulati: nome del server -> elenco di record (nome, tipo, valore, ttl)
ZONE = {
    "radice": [
        ("example.", "NS", "tld-example", 172800),
    ],
    "tld-example": [
        ("scuola.example.", "NS", "ns1.scuola.example", 86400),
    ],
    "ns1.scuola.example": [
        ("www.scuola.example.", "A", "203.0.113.80", 300),
        ("www.scuola.example.", "AAAA", "2001:db8:5c01::80", 300),
        ("portale.scuola.example.", "CNAME", "www.scuola.example.", 3600),
        ("scuola.example.", "MX", "posta.scuola.example.", 3600),
        ("posta.scuola.example.", "A", "203.0.113.25", 3600),
    ],
}


def interroga(server, nome, tipo):
    """Domanda a un solo server. Restituisce ('risposta', record), ('delega', server) o ('inesistente', None)."""
    record = ZONE[server]
    trovati = [r for r in record if r[0] == nome and r[1] == tipo]
    if trovati:
        return "risposta", trovati
    alias = [r for r in record if r[0] == nome and r[1] == "CNAME"]
    if alias:
        return "risposta", alias
    # delega: il server conosce il responsabile di una parte finale del nome
    deleghe = [r for r in record if r[1] == "NS" and nome.endswith(r[0])]
    if deleghe:
        piu_specifica = max(deleghe, key=lambda r: len(r[0]))
        return "delega", piu_specifica
    return "inesistente", None


class Risolutore:
    def __init__(self):
        self.cache = {}           # (nome, tipo) -> (valori, istante di scadenza)
        self.domande = []         # registro delle domande inviate ai server

    def dalla_cache(self, nome, tipo, istante):
        voce = self.cache.get((nome, tipo))
        if voce and voce[1] > istante:
            return voce[0]
        return None

    def risolvi(self, nome, tipo="A", istante=0):
        """Restituisce l'elenco dei valori (per esempio indirizzi IP), vuoto se il nome non esiste."""
        if not nome.endswith("."):
            nome += "."                                    # nome completo, con la radice finale
        in_cache = self.dalla_cache(nome, tipo, istante)
        if in_cache is not None:
            return in_cache
        alias = self.dalla_cache(nome, "CNAME", istante)   # alias già noto: si passa al nome canonico
        if alias is not None:
            return self.risolvi(alias[0], tipo, istante)
        # parte dal server più vicino al nome già noto in cache, altrimenti dalla radice
        server = "radice"
        for zona in sorted({k[0] for k in self.cache if k[1] == "NS"}, key=len, reverse=True):
            delegato = self.dalla_cache(zona, "NS", istante)
            if delegato and nome.endswith(zona):
                server = delegato[0]
                break
        while True:
            self.domande.append((server, nome, tipo))
            esito, dati = interroga(server, nome, tipo)
            if esito == "delega":
                zona, _, prossimo, ttl = dati
                self.cache[(zona, "NS")] = ([prossimo], istante + ttl)
                server = prossimo
                continue
            if esito == "inesistente":
                return []
            if dati[0][1] == "CNAME":                      # alias: si risolve il nome canonico
                _, _, canonico, ttl = dati[0]
                self.cache[(nome, "CNAME")] = ([canonico], istante + ttl)
                return self.risolvi(canonico, tipo, istante)
            valori = [r[2] for r in dati]
            self.cache[(nome, tipo)] = (valori, istante + min(r[3] for r in dati))
            return valori


def dimostrazione(nome):
    r = Risolutore()
    for istante in (0, 60, 400):
        prima = len(r.domande)
        valori = r.risolvi(nome, "A", istante)
        nuove = r.domande[prima:]
        print(f"t={istante:>3} s  {nome} -> {valori or 'nome inesistente'}")
        if nuove:
            for server, n, tipo in nuove:
                print(f"         domanda a {server}: {n} {tipo}")
        else:
            print("         risposta dalla cache, nessuna domanda ai server")


if __name__ == "__main__":
    dimostrazione(sys.argv[1] if len(sys.argv) > 1 else "www.scuola.example")
