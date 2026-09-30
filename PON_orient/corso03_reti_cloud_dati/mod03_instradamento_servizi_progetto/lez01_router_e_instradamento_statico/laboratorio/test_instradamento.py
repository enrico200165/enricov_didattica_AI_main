"""Test di instradamento.py. Esecuzione: python test_instradamento.py"""

from instradamento import Router, percorso, rete_di_esempio, leggi_route_print, rotta_per

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


r = Router("prova")
r.aggiungi("10.0.0.0/8", "1.1.1.1")
r.aggiungi("10.1.0.0/16", "2.2.2.2")
r.aggiungi("10.1.2.0/24", "3.3.3.3")
r.aggiungi("0.0.0.0/0", "9.9.9.9")
verifica("prefisso più lungo: 10.1.2.3 -> /24", r.scegli("10.1.2.3")[1] == "3.3.3.3")
verifica("10.1.9.9 -> /16", r.scegli("10.1.9.9")[1] == "2.2.2.2")
verifica("10.200.0.1 -> /8", r.scegli("10.200.0.1")[1] == "1.1.1.1")
verifica("172.16.0.1 -> rotta predefinita", r.scegli("172.16.0.1")[1] == "9.9.9.9")
senza_predefinita = Router("x")
senza_predefinita.aggiungi("10.0.0.0/8", None)
verifica("nessuna voce applicabile: None", senza_predefinita.scegli("8.8.8.8") is None)

routers, r1, r2, r3 = rete_di_esempio()
verifica("da R1 a 192.168.3.20: consegnato attraversando R1 e R2",
         percorso(routers, r1, "192.168.3.20") == ("consegnato", ["R1", "R2"]))
verifica("da R1 a 192.168.2.50: consegnato direttamente da R1",
         percorso(routers, r1, "192.168.2.50") == ("consegnato", ["R1"]))
verifica("da R2 a 192.168.1.7: consegnato tramite R1",
         percorso(routers, r2, "192.168.1.7") == ("consegnato", ["R2", "R1"]))
verifica("da R3 verso la scuola con la rotta aggregata /22",
         percorso(routers, r3, "192.168.1.7") == ("consegnato", ["R3", "R2", "R1"]))
esito, via = percorso(routers, r1, "198.51.100.7")
verifica("R3 senza rotta predefinita: destinazione irraggiungibile",
         esito.startswith("destinazione irraggiungibile") and via[-1] == "R3")

r2.tabella = [v for v in r2.tabella if v[0].prefixlen != 0]
r2.aggiungi("0.0.0.0/0", "192.168.2.1")
esito, via = percorso(routers, r1, "198.51.100.7", ttl=8)
verifica("ciclo R1-R2: il TTL scade dopo 8 router", esito.startswith("TTL scaduto") and len(via) == 8)

with open("route_esempio.txt", encoding="utf-8") as f:
    rotte = leggi_route_print(f.read())
verifica("11 rotte lette da route_esempio.txt", len(rotte) == 11)
verifica("rotta predefinita con gateway 192.168.1.1",
         rotte[0]["rete"].prefixlen == 0 and rotte[0]["gateway"] == "192.168.1.1" and rotte[0]["metrica"] == 35)
verifica("On-link riconosciuto come rete diretta", rotte[4]["gateway"] is None)
verifica("8.8.8.8 usa la rotta predefinita", str(rotta_per(rotte, "8.8.8.8")["rete"]) == "0.0.0.0/0")
verifica("192.168.1.35 usa la rete locale /24", str(rotta_per(rotte, "192.168.1.35")["rete"]) == "192.168.1.0/24")
verifica("224.0.0.251: a parità di prefisso vince la metrica più bassa",
         rotta_per(rotte, "224.0.0.251")["interfaccia"] == "192.168.1.20")
inglese = "  Network Destination        Netmask          Gateway       Interface  Metric\n          0.0.0.0          0.0.0.0         10.0.0.1         10.0.0.5     25\n"
verifica("output in inglese", leggi_route_print(inglese)[0]["gateway"] == "10.0.0.1")

print(f"\nTest superati: {superati}, falliti: {falliti}")
