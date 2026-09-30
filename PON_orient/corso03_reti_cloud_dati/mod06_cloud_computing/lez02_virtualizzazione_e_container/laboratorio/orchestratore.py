"""Simulazione delle idee principali di un orchestratore di container (come Kubernetes).

- lo stato desiderato è dichiarato: "voglio 4 repliche del servizio, ciascuna con 500 millesimi di CPU"
- l'orchestratore colloca le repliche sui nodi (server) con più capacità libera
- se un nodo si guasta, le sue repliche vengono ricreate sugli altri nodi (autoriparazione)
- se la capacità non basta, le repliche restano in attesa

Uso: python orchestratore.py
"""


class Cluster:
    def __init__(self, nodi):
        # nodi: dizionario nome -> capacità di CPU in millesimi di core (1000 = 1 core)
        self.capacita = dict(nodi)
        self.attivi = set(nodi)
        self.repliche = {}          # nome della replica -> nodo su cui gira (None = in attesa)
        self.richiesta = {}         # nome della replica -> CPU richiesta
        self.eventi = []

    def libera(self, nodo):
        usata = sum(self.richiesta[r] for r, n in self.repliche.items() if n == nodo)
        return self.capacita[nodo] - usata

    def colloca(self, replica):
        """Sceglie il nodo attivo con più capacità libera sufficiente; None se non ce n'è."""
        adatti = [n for n in sorted(self.attivi) if self.libera(n) >= self.richiesta[replica]]
        nodo = max(adatti, key=self.libera) if adatti else None
        self.repliche[replica] = nodo
        self.eventi.append(f"{replica} -> {nodo or 'IN ATTESA (capacità insufficiente)'}")
        return nodo

    def applica(self, servizio, repliche, cpu):
        """Porta il numero di repliche del servizio al valore desiderato (aumenta o riduce)."""
        attuali = sorted(r for r in self.repliche if r.startswith(servizio + "-"))
        for i in range(len(attuali), repliche):
            nome = f"{servizio}-{i + 1}"
            self.richiesta[nome] = cpu
            self.colloca(nome)
        for nome in attuali[repliche:]:
            del self.repliche[nome]
            del self.richiesta[nome]
            self.eventi.append(f"{nome} eliminata")

    def guasto(self, nodo):
        """Il nodo non risponde più: le sue repliche vengono ricreate altrove."""
        self.attivi.discard(nodo)
        self.eventi.append(f"GUASTO del nodo {nodo}")
        for replica, n in sorted(self.repliche.items()):
            if n == nodo:
                self.colloca(replica)

    def riprova_in_attesa(self):
        for replica, n in sorted(self.repliche.items()):
            if n is None:
                self.colloca(replica)

    def stato(self):
        return {n: sorted(r for r, x in self.repliche.items() if x == n) for n in sorted(self.capacita)}


def dimostrazione():
    c = Cluster({"nodo-a": 2000, "nodo-b": 2000, "nodo-c": 1000})
    c.applica("biblioteca", repliche=4, cpu=500)
    print("Dopo il rilascio di 4 repliche:", c.stato())
    c.guasto("nodo-a")
    print("Dopo il guasto di nodo-a:     ", c.stato())
    c.applica("biblioteca", repliche=7, cpu=500)
    print("Richieste 7 repliche:         ", c.stato())
    in_attesa = [r for r, n in c.repliche.items() if n is None]
    print("Repliche in attesa:", in_attesa)
    c.attivi.add("nodo-a")
    c.eventi.append("nodo-a di nuovo disponibile")
    c.riprova_in_attesa()
    print("Dopo il ritorno di nodo-a:    ", c.stato())
    print("\nEventi:")
    for e in c.eventi:
        print("  ", e)


if __name__ == "__main__":
    dimostrazione()
