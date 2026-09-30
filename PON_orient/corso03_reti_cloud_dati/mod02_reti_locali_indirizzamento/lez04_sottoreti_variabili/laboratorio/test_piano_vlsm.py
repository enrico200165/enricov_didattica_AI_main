"""Test di piano_vlsm.py. Esecuzione: python test_piano_vlsm.py"""

import ipaddress
import os

from piano_vlsm import prefisso_necessario, calcola_piano, verifica_piano, aggrega, leggi_requisiti, main

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


verifica("2 host -> /30, 6 -> /29, 7 -> /28", [prefisso_necessario(h) for h in (2, 6, 7)] == [30, 29, 28])
verifica("30 -> /27, 31 -> /26, 300 -> /23", [prefisso_necessario(h) for h in (30, 31, 300)] == [27, 26, 23])

requisiti = leggi_requisiti("requisiti_scuola.csv")
verifica("otto requisiti letti dal CSV", len(requisiti) == 8)
piano, liberi = calcola_piano("10.20.0.0/22", requisiti)
reti = {p["nome"]: str(p["rete"]) for p in piano}
verifica("studenti_wifi: 10.20.0.0/23", reti["studenti_wifi"] == "10.20.0.0/23")
verifica("docenti: 10.20.2.0/26", reti["docenti"] == "10.20.2.0/26")
verifica("collegamento_router: 10.20.2.184/30", reti["collegamento_router"] == "10.20.2.184/30")
verifica("piano verificato: nel blocco, senza sovrapposizioni, sufficiente", verifica_piano("10.20.0.0/22", piano))
verifica("ogni sottorete allineata alla propria dimensione",
         all(int(p["rete"].network_address) % p["rete"].num_addresses == 0 for p in piano))
totale = sum(p["rete"].num_addresses for p in piano) + sum(l.num_addresses for l in liberi)
verifica("assegnati + liberi = 1024 indirizzi del blocco", totale == 1024)
verifica("blocchi liberi calcolati", [str(l) for l in liberi] == ["10.20.2.188/30", "10.20.2.192/26", "10.20.3.0/24"])

try:
    calcola_piano("10.20.0.0/24", requisiti)
    insufficiente = False
except ValueError:
    insufficiente = True
verifica("blocco /24 troppo piccolo: errore", insufficiente)

sovrapposto = [{"nome": "a", "richiesti": 10, "rete": ipaddress.ip_network("10.0.0.0/28")},
               {"nome": "b", "richiesti": 10, "rete": ipaddress.ip_network("10.0.0.0/27")}]
verifica("piano con sottoreti sovrapposte rifiutato", not verifica_piano("10.0.0.0/24", sovrapposto))

verifica("quattro /24 contigue aggregate in una /22",
         [str(r) for r in aggrega(["192.168.4.0/24", "192.168.5.0/24", "192.168.6.0/24", "192.168.7.0/24"])] == ["192.168.4.0/22"])
verifica("tre /24 non aggregabili in un solo prefisso",
         [str(r) for r in aggrega(["192.168.5.0/24", "192.168.6.0/24", "192.168.7.0/24"])] == ["192.168.5.0/24", "192.168.6.0/23"])

main("10.20.0.0/22", "requisiti_scuola.csv")
with open("piano_calcolato.csv", encoding="utf-8") as f:
    righe = f.read().splitlines()
verifica("piano_calcolato.csv con intestazione e 8 righe", len(righe) == 9 and righe[0].startswith("nome,richiesti,rete"))
os.remove("piano_calcolato.csv")

print(f"\nTest superati: {superati}, falliti: {falliti}")
