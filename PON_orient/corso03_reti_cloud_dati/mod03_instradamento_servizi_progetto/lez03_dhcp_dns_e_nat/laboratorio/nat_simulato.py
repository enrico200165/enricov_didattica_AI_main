"""Simulazione di un router con NAT a porte (PAT, detto anche NAPT o "NAT overload").

Più dispositivi con indirizzi privati condividono un solo indirizzo pubblico.
Per ogni connessione in uscita il router sostituisce indirizzo e porta di
origine con il proprio indirizzo pubblico e una porta libera, e ricorda la
corrispondenza in una tabella; le risposte vengono tradotte all'indietro.
I pacchetti in ingresso senza corrispondenza vengono scartati, salvo le regole
di inoltro delle porte (port forwarding).

Uso: python nat_simulato.py
"""


class RouterNat:
    def __init__(self, ip_pubblico, prima_porta=50000, durata=120):
        self.ip_pubblico = ip_pubblico
        self.prossima_porta = prima_porta
        self.durata = durata          # secondi di inattività dopo i quali una voce scade
        self.tabella = {}             # (protocollo, ip privato, porta privata) -> [porta pubblica, ultimo uso]
        self.inoltri = {}             # (protocollo, porta pubblica) -> (ip privato, porta privata)

    def aggiungi_inoltro(self, protocollo, porta_pubblica, ip_privato, porta_privata):
        """Regola di port forwarding: rende raggiungibile da Internet un servizio interno."""
        self.inoltri[(protocollo, porta_pubblica)] = (ip_privato, porta_privata)

    def uscita(self, protocollo, ip_origine, porta_origine, ip_destinazione, porta_destinazione, istante=0):
        """Pacchetto dalla rete interna verso Internet: restituisce il pacchetto tradotto."""
        self.rimuovi_scadute(istante)
        chiave = (protocollo, ip_origine, porta_origine)
        if chiave not in self.tabella:
            self.tabella[chiave] = [self.prossima_porta, istante]   # nuova corrispondenza
            self.prossima_porta += 1
        voce = self.tabella[chiave]
        voce[1] = istante
        return (protocollo, self.ip_pubblico, voce[0], ip_destinazione, porta_destinazione)

    def ingresso(self, protocollo, ip_origine, porta_origine, porta_destinazione, istante=0):
        """Pacchetto da Internet verso l'indirizzo pubblico: tradotto, oppure None (scartato)."""
        self.rimuovi_scadute(istante)
        for (proto, ip_priv, porta_priv), voce in self.tabella.items():
            if proto == protocollo and voce[0] == porta_destinazione:
                voce[1] = istante
                return (protocollo, ip_origine, porta_origine, ip_priv, porta_priv)
        if (protocollo, porta_destinazione) in self.inoltri:
            ip_priv, porta_priv = self.inoltri[(protocollo, porta_destinazione)]
            return (protocollo, ip_origine, porta_origine, ip_priv, porta_priv)
        return None

    def rimuovi_scadute(self, istante):
        for chiave in [k for k, v in self.tabella.items() if istante - v[1] > self.durata]:
            del self.tabella[chiave]

    def stampa_tabella(self):
        print(f"  Tabella NAT ({self.ip_pubblico}):")
        for (proto, ip, porta), (pubblica, ultimo) in self.tabella.items():
            print(f"    {proto} {ip}:{porta} <-> {self.ip_pubblico}:{pubblica}  (ultimo uso t={ultimo})")


def formato(pacchetto):
    proto, ip_o, porta_o, ip_d, porta_d = pacchetto
    return f"{proto} {ip_o}:{porta_o} -> {ip_d}:{porta_d}"


def dimostrazione():
    nat = RouterNat("203.0.113.2")
    server = ("198.51.100.80", 443)
    # due PC della rete interna usano per caso la stessa porta di origine
    for ip in ("192.168.1.20", "192.168.1.35"):
        interno = ("TCP", ip, 51000, *server)
        print(f"uscita:   {formato(interno)}  diventa  {formato(nat.uscita(*interno))}")
    nat.stampa_tabella()
    risposta = nat.ingresso("TCP", *server, 50001)
    print(f"ingresso: TCP {server[0]}:{server[1]} -> 203.0.113.2:50001  diventa  {formato(risposta)}")
    print("ingresso non richiesto sulla porta 3389:", nat.ingresso("TCP", "198.51.100.9", 40000, 3389))
    nat.aggiungi_inoltro("TCP", 8080, "192.168.1.10", 80)
    inoltrato = nat.ingresso("TCP", "198.51.100.9", 40000, 8080)
    print(f"con inoltro della porta 8080 verso il server interno: {formato(inoltrato)}")


if __name__ == "__main__":
    dimostrazione()
