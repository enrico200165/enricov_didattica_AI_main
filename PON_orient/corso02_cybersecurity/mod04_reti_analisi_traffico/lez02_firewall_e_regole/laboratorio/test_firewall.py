"""Test di firewall.py. Esecuzione: python test_firewall.py"""

from firewall import Regola, Pacchetto, Firewall

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def nuovo():
    return Firewall([
        Regola("web", "consenti", "tcp", "192.168.20.0/24", "192.168.10.5/32", (80, 443)),
        Regola("dns", "consenti", "udp", "192.168.20.0/24", "192.168.10.5/32", (53,)),
        Regola("no rdp", "blocca", "tcp", "0.0.0.0/0", "192.168.10.5/32", (3389,)),
    ])


fw = nuovo()
verifica("HTTPS dal laboratorio al server: consentito",
         fw.valuta(Pacchetto("tcp", "192.168.20.14", "192.168.10.5", 50000, 443))[0] == "consenti")
verifica("risposta del server: consentita grazie allo stato",
         fw.valuta(Pacchetto("tcp", "192.168.10.5", "192.168.20.14", 443, 50000))
         == ("consenti", "risposta a una connessione consentita"))
verifica("stesso pacchetto dal server, porta diversa: bloccato",
         fw.valuta(Pacchetto("tcp", "192.168.10.5", "192.168.20.14", 443, 50001))[0] == "blocca")
verifica("DNS via UDP: consentito",
         fw.valuta(Pacchetto("udp", "192.168.20.14", "192.168.10.5", 50002, 53))[0] == "consenti")
verifica("DNS via TCP: nessuna regola, politica predefinita",
         fw.valuta(Pacchetto("tcp", "192.168.20.14", "192.168.10.5", 50003, 53)) == ("blocca", "politica predefinita"))
verifica("RDP: bloccato dalla regola esplicita",
         fw.valuta(Pacchetto("tcp", "192.168.20.14", "192.168.10.5", 50004, 3389)) == ("blocca", "regola 'no rdp'"))
verifica("rete diversa dal laboratorio: bloccata",
         fw.valuta(Pacchetto("tcp", "192.168.30.7", "192.168.10.5", 50005, 443))[0] == "blocca")

senza_stato = nuovo()
senza_stato.stato = False
senza_stato.valuta(Pacchetto("tcp", "192.168.20.14", "192.168.10.5", 50000, 443))
verifica("senza stato la risposta del server è bloccata",
         senza_stato.valuta(Pacchetto("tcp", "192.168.10.5", "192.168.20.14", 443, 50000))[0] == "blocca")

aperto = Firewall([Regola("no telnet", "blocca", "tcp", porte=(23,))], predefinita="consenti")
verifica("politica predefinita 'consenti': porta non citata passa",
         aperto.valuta(Pacchetto("tcp", "10.0.0.1", "10.0.0.2", 50000, 445))[0] == "consenti")

# ordine delle regole
ordine_errato = Firewall([
    Regola("tutto dal laboratorio", "consenti", "qualsiasi", "192.168.20.0/24"),
    Regola("no rdp", "blocca", "tcp", "0.0.0.0/0", "192.168.10.5/32", (3389,)),
])
verifica("regola generale prima di quella specifica: RDP passa",
         ordine_errato.valuta(Pacchetto("tcp", "192.168.20.14", "192.168.10.5", 50000, 3389))[0] == "consenti")
verifica("sovrapposizione solo parziale: nessuna regola del tutto oscurata", ordine_errato.regole_oscurate() == [])
ordine_errato.regole.reverse()
verifica("regole scambiate: RDP bloccato",
         ordine_errato.valuta(Pacchetto("tcp", "192.168.20.14", "192.168.10.5", 50001, 3389))[0] == "blocca")

oscurata = Firewall([
    Regola("web dal laboratorio", "consenti", "tcp", "192.168.20.0/24", "0.0.0.0/0", (80, 443)),
    Regola("blocca web dalla postazione 14", "blocca", "tcp", "192.168.20.14/32", "0.0.0.0/0", (443,)),
])
verifica("regola specifica dopo quella generale: oscurata",
         oscurata.regole_oscurate() == [("blocca web dalla postazione 14", "web dal laboratorio")])
verifica("regole corrette: nessuna oscurata", nuovo().regole_oscurate() == [])
try:
    Regola("errata", "permetti")
    verifica("azione non valida rifiutata", False)
except ValueError:
    verifica("azione non valida rifiutata", True)

print(f"Test superati: {superati}, falliti: {falliti}")
