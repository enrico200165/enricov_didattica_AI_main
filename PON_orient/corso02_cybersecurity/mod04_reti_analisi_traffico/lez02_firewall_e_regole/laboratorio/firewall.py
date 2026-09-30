"""Simulatore didattico di firewall a filtraggio di pacchetti, con regole ordinate e stato delle connessioni.

- le regole si esaminano dall'alto verso il basso: si applica la PRIMA che corrisponde
- se nessuna regola corrisponde si applica la politica predefinita (di norma: blocca)
- con stato=True le risposte alle connessioni già consentite passano senza regole apposite
Solo libreria standard di Python.
"""

import ipaddress
from dataclasses import dataclass, field


@dataclass
class Regola:
    nome: str
    azione: str                    # "consenti" o "blocca"
    protocollo: str = "qualsiasi"  # "tcp", "udp", "icmp" o "qualsiasi"
    sorgente: str = "0.0.0.0/0"    # rete in notazione CIDR
    destinazione: str = "0.0.0.0/0"
    porte: tuple = ()              # porte di destinazione; vuoto = qualsiasi porta

    def __post_init__(self):
        if self.azione not in ("consenti", "blocca"):
            raise ValueError(f"azione non valida: {self.azione}")
        self._src = ipaddress.ip_network(self.sorgente)
        self._dst = ipaddress.ip_network(self.destinazione)

    def corrisponde(self, p):
        return ((self.protocollo == "qualsiasi" or self.protocollo == p.protocollo)
                and ipaddress.ip_address(p.sorgente) in self._src
                and ipaddress.ip_address(p.destinazione) in self._dst
                and (not self.porte or p.porta_dst in self.porte))

    def copre(self, altra):
        """True se ogni pacchetto che corrisponde ad 'altra' corrisponde anche a questa regola."""
        return ((self.protocollo == "qualsiasi" or self.protocollo == altra.protocollo)
                and altra._src.subnet_of(self._src)
                and altra._dst.subnet_of(self._dst)
                and (not self.porte or (altra.porte and set(altra.porte) <= set(self.porte))))


@dataclass
class Pacchetto:
    protocollo: str
    sorgente: str
    destinazione: str
    porta_src: int = 0
    porta_dst: int = 0


@dataclass
class Firewall:
    regole: list
    predefinita: str = "blocca"
    stato: bool = True
    connessioni: set = field(default_factory=set)

    def valuta(self, p):
        """Restituisce (azione, motivo) per il pacchetto."""
        if self.stato and (p.protocollo, p.destinazione, p.porta_dst, p.sorgente, p.porta_src) in self.connessioni:
            return "consenti", "risposta a una connessione consentita"
        for r in self.regole:
            if r.corrisponde(p):
                if r.azione == "consenti" and self.stato and p.protocollo in ("tcp", "udp"):
                    self.connessioni.add((p.protocollo, p.sorgente, p.porta_src, p.destinazione, p.porta_dst))
                return r.azione, f"regola '{r.nome}'"
        return self.predefinita, "politica predefinita"

    def regole_oscurate(self):
        """Regole che non si applicano mai perché una regola precedente le copre interamente."""
        oscurate = []
        for i, r in enumerate(self.regole):
            for precedente in self.regole[:i]:
                if precedente.copre(r):
                    oscurate.append((r.nome, precedente.nome))
                    break
        return oscurate


if __name__ == "__main__":
    # Rete di esempio: laboratorio 192.168.20.0/24, server della scuola 192.168.10.5
    fw = Firewall([
        Regola("web del server", "consenti", "tcp", "192.168.20.0/24", "192.168.10.5/32", (80, 443)),
        Regola("DNS del server", "consenti", "udp", "192.168.20.0/24", "192.168.10.5/32", (53,)),
        Regola("desktop remoto vietato", "blocca", "tcp", "0.0.0.0/0", "192.168.10.5/32", (3389,)),
        Regola("navigazione verso Internet", "consenti", "tcp", "192.168.20.0/24", "0.0.0.0/0", (80, 443)),
    ])
    prove = [
        Pacchetto("tcp", "192.168.20.14", "192.168.10.5", 51000, 443),
        Pacchetto("tcp", "192.168.10.5", "192.168.20.14", 443, 51000),
        Pacchetto("tcp", "192.168.20.14", "192.168.10.5", 51001, 3389),
        Pacchetto("tcp", "192.168.20.14", "192.168.10.5", 51002, 445),
        Pacchetto("tcp", "203.0.113.50", "192.168.20.14", 443, 51003),
    ]
    for p in prove:
        azione, motivo = fw.valuta(p)
        print(f"{p.protocollo} {p.sorgente}:{p.porta_src} -> {p.destinazione}:{p.porta_dst}  {azione.upper():9} ({motivo})")
