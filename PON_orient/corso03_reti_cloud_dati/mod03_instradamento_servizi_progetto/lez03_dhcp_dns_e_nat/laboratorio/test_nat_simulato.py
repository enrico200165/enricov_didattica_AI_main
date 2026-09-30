"""Test di nat_simulato.py. Esecuzione: python test_nat_simulato.py"""

from nat_simulato import RouterNat

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


nat = RouterNat("203.0.113.2")
a = nat.uscita("TCP", "192.168.1.20", 51000, "198.51.100.80", 443, 0)
b = nat.uscita("TCP", "192.168.1.35", 51000, "198.51.100.80", 443, 0)
verifica("in uscita l'origine diventa l'indirizzo pubblico", a[1] == b[1] == "203.0.113.2")
verifica("stessa porta privata su due PC: porte pubbliche diverse", a[2] != b[2])
verifica("destinazione invariata", a[3:] == ("198.51.100.80", 443))
verifica("stessa connessione: stessa porta pubblica",
         nat.uscita("TCP", "192.168.1.20", 51000, "198.51.100.80", 443, 5)[2] == a[2])
verifica("risposta tradotta verso il PC giusto",
         nat.ingresso("TCP", "198.51.100.80", 443, b[2], 6)[3:] == ("192.168.1.35", 51000))
verifica("ingresso non richiesto scartato", nat.ingresso("TCP", "198.51.100.9", 40000, 3389, 6) is None)
verifica("protocollo diverso sulla stessa porta scartato", nat.ingresso("UDP", "198.51.100.80", 443, a[2], 6) is None)

nat.aggiungi_inoltro("TCP", 8080, "192.168.1.10", 80)
verifica("port forwarding: 8080 pubblica -> 192.168.1.10:80",
         nat.ingresso("TCP", "198.51.100.9", 40000, 8080, 7)[3:] == ("192.168.1.10", 80))

nat.rimuovi_scadute(200)
verifica("voci inattive oltre 120 s eliminate", nat.tabella == {})
verifica("dopo la scadenza la risposta viene scartata", nat.ingresso("TCP", "198.51.100.80", 443, a[2], 201) is None)
verifica("l'inoltro delle porte non scade",
         nat.ingresso("TCP", "198.51.100.9", 40000, 8080, 500) is not None)

print(f"\nTest superati: {superati}, falliti: {falliti}")
