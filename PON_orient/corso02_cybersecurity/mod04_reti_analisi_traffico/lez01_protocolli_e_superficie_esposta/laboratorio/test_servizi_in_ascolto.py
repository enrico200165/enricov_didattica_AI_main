"""Test di servizi_in_ascolto.py. Esecuzione: python test_servizi_in_ascolto.py"""

from servizi_in_ascolto import portata, leggi_csv, analizza, riepilogo

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


verifica("0.0.0.0: tutte le interfacce IPv4", portata("0.0.0.0") == "tutte le interfacce")
verifica(":: : tutte le interfacce IPv6", portata("::") == "tutte le interfacce")
verifica("127.0.0.1: solo questo PC", portata("127.0.0.1") == "solo questo PC")
verifica("::1: solo questo PC", portata("::1") == "solo questo PC")
verifica("indirizzo specifico", portata("192.168.1.23") == "solo l'interfaccia 192.168.1.23")
verifica("indirizzo IPv6 con indice di zona", portata("fe80::1%12") == "solo l'interfaccia fe80::1")

righe = leggi_csv("ascolto_esempio.csv")
verifica("CSV con BOM letto: 14 righe", len(righe) == 14 and "LocalAddress" in righe[0])
voci = analizza(righe)
verifica("IPv4 e IPv6 sulla stessa porta uniti in una voce", sum(1 for v in voci if v["porta"] == 135) == 1)
r = riepilogo(voci)
verifica("servizi distinti: 10", r["totale"] == 10)
verifica("servizi solo locali: 2", r["solo_locali"] == 2)
verifica("porte da verificare: 139, 445, 3389", r["da_verificare"] == [139, 445, 3389])
verifica("processo indicato", next(v for v in voci if v["porta"] == 8080)["processo"] == "python")
verifica("porta dinamica riconosciuta",
         next(v for v in voci if v["porta"] == 49669)["descrizione"] == "porta dinamica")

print(f"Test superati: {superati}, falliti: {falliti}")
