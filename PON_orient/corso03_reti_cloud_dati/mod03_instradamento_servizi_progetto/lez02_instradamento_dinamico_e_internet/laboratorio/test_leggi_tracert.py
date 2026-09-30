"""Test di leggi_tracert.py. Esecuzione: python test_leggi_tracert.py"""

from leggi_tracert import leggi, analizza

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


with open("tracert_esempio.txt", encoding="utf-8") as f:
    passi = leggi(f.read())
verifica("dieci passi letti, righe di intestazione ignorate", [p[0] for p in passi] == list(range(1, 11)))
verifica("'<1 ms' letto come 0,5", passi[0][1] == [0.5, 0.5, 1.0])
verifica("passo senza risposta: nessun tempo, nessun indirizzo", passi[4][1] == [] and passi[4][2] is None)
verifica("indirizzo dell'ultimo passo", passi[9][2] == "203.0.113.80")

r = analizza(passi)
verifica("mediana del passo 7: 112 ms", r[6]["mediana"] == 112)
verifica("distanza massima del passo 7: 11 200 km", r[6]["distanza_max_km"] == 11200)
verifica("aumenti bruschi ai passi 7 e 9", [x["passo"] for x in r if x["aumento_brusco"]] == [7, 9])
verifica("il passo senza risposta non interrompe il confronto (6 confrontato con 4)",
         not r[5]["aumento_brusco"] and r[4]["mediana"] is None)

con_nomi = """  1     2 ms     1 ms     2 ms  router.casa [192.168.0.1]
  2    15 ms    14 ms    16 ms  host-203-0-113-5.example.net [203.0.113.5]
"""
p = leggi(con_nomi)
verifica("righe con nome e indirizzo tra parentesi quadre", [x[2] for x in p] == ["192.168.0.1", "203.0.113.5"])
misto = "  3     *       20 ms    22 ms  198.51.100.9\n"
verifica("una misura persa su tre: mediana delle altre due", analizza(leggi(misto))[0]["mediana"] == 21)

print(f"\nTest superati: {superati}, falliti: {falliti}")
