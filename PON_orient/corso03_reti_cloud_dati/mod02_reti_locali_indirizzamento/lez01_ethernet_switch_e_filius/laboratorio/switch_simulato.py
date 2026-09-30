"""Simulazione del funzionamento di uno switch Ethernet.

Lo switch impara su quale porta si trova ogni indirizzo MAC leggendo
l'indirizzo di ORIGINE delle trame che riceve; per decidere dove inoltrare
una trama guarda l'indirizzo di DESTINAZIONE:
- destinazione nota nella tabella: inoltro solo su quella porta
- destinazione sconosciuta o broadcast: inoltro su tutte le porte tranne
  quella di arrivo (flooding)
- destinazione sulla stessa porta di arrivo: la trama viene scartata

Esecuzione: python switch_simulato.py
"""

BROADCAST = "FF:FF:FF:FF:FF:FF"


class Switch:
    def __init__(self, nome, numero_porte, durata_voci=300):
        self.nome = nome
        self.porte = list(range(1, numero_porte + 1))  # porte numerate da 1
        self.durata_voci = durata_voci  # secondi dopo i quali una voce scade
        self.tabella = {}  # MAC -> (porta, istante dell'ultimo aggiornamento)

    def ricevi(self, porta_arrivo, mac_origine, mac_destinazione, istante=0):
        """Elabora una trama arrivata su porta_arrivo.

        Restituisce la coppia (azione, porte di uscita), dove azione è
        "inoltro", "flooding" o "scarto".
        """
        mac_origine = mac_origine.upper()
        mac_destinazione = mac_destinazione.upper()
        self.rimuovi_scadute(istante)
        # 1. Apprendimento: l'origine si trova sulla porta di arrivo
        self.tabella[mac_origine] = (porta_arrivo, istante)
        # 2. Inoltro in base alla destinazione
        if mac_destinazione == BROADCAST or mac_destinazione not in self.tabella:
            uscite = [p for p in self.porte if p != porta_arrivo]
            return "flooding", uscite
        porta_destinazione = self.tabella[mac_destinazione][0]
        if porta_destinazione == porta_arrivo:
            return "scarto", []
        return "inoltro", [porta_destinazione]

    def rimuovi_scadute(self, istante):
        """Elimina le voci non aggiornate da più di durata_voci secondi."""
        scadute = [mac for mac, (_, t) in self.tabella.items()
                   if istante - t > self.durata_voci]
        for mac in scadute:
            del self.tabella[mac]

    def stampa_tabella(self):
        print(f"  Tabella di {self.nome}: MAC -> porta")
        if not self.tabella:
            print("    (vuota)")
        for mac, (porta, t) in sorted(self.tabella.items(), key=lambda v: v[1][0]):
            print(f"    {mac}  porta {porta}  (aggiornata a t={t})")


# Tre PC collegati alle porte 1, 2 e 3 di uno switch a 4 porte.
PC = {
    "PC-A": "02:00:00:00:00:0A",
    "PC-B": "02:00:00:00:00:0B",
    "PC-C": "02:00:00:00:00:0C",
}
PORTA = {"PC-A": 1, "PC-B": 2, "PC-C": 3}


def dimostrazione():
    sw = Switch("SW1", 4)
    sequenza = [
        # (istante, mittente, destinatario) ; None = broadcast
        (0, "PC-A", None),     # per esempio una richiesta ARP
        (1, "PC-B", "PC-A"),   # risposta di PC-B
        (2, "PC-A", "PC-B"),
        (3, "PC-A", "PC-C"),   # PC-C non ha ancora trasmesso
        (4, "PC-C", "PC-A"),
        (5, "PC-A", "PC-C"),
    ]
    for istante, mittente, destinatario in sequenza:
        mac_dest = BROADCAST if destinatario is None else PC[destinatario]
        azione, uscite = sw.ricevi(PORTA[mittente], PC[mittente], mac_dest, istante)
        nome_dest = destinatario or "broadcast"
        print(f"t={istante}: {mittente} -> {nome_dest}: {azione}, porte {uscite}")
        sw.stampa_tabella()
        print()


if __name__ == "__main__":
    dimostrazione()
