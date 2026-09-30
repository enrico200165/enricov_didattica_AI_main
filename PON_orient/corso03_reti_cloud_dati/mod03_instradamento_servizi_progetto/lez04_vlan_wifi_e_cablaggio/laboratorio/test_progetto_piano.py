"""Test di progetto_piano.py. Esecuzione: python test_progetto_piano.py"""

import progetto_piano as p

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


stanze = p.leggi_stanze("stanze_piano.csv")
verifica("nove stanze lette, numeri convertiti", len(stanze) == 9 and stanze[0]["postazioni"] == 2)
r = p.progetta(stanze)
per_stanza = {s["stanza"]: s for s in r["stanze"]}
verifica("aula con 28 utenti Wi-Fi: 1 access point", per_stanza["aula_1"]["access_point"] == 1)
verifica("laboratorio: 25 postazioni + 1 stampante + 1 AP = 27 prese", per_stanza["laboratorio_info"]["prese"] == 27)
verifica("postazioni degli uffici nella VLAN uffici", r["prese_per_vlan"]["uffici"] == 10)
verifica("porte totali 60, con riserva 72", (r["porte"], r["porte_con_margine"]) == (60, 72))
verifica("due switch da 48 porte (46 utili)", r["switch"] == 2)
verifica("potenza PoE: 9 AP e 4 telecamere", r["potenza_poe_w"] == round(9 * 25.5 + 4 * 12.95, 1))
verifica("avviso per la tratta di 95 m", len(r["avvisi"]) == 1 and r["avvisi"][0].startswith("corridoio_ovest"))

piccolo = [{"stanza": "s", "tipo": "aula", "postazioni": 1, "utenti_wifi": 31, "telecamere": 0,
            "stampanti": 0, "distanza_m": 10}]
verifica("31 utenti: 2 access point (arrotondamento per eccesso)", p.progetta(piccolo)["access_point"] == 2)
molte_telecamere = [{"stanza": "c", "tipo": "corridoio", "postazioni": 0, "utenti_wifi": 0, "telecamere": 30,
                     "stampanti": 0, "distanza_m": 10}]
verifica("30 telecamere su un solo switch: avviso di budget PoE superato",
         any("PoE" in a for a in p.progetta(molte_telecamere)["avvisi"]))

print(f"\nTest superati: {superati}, falliti: {falliti}")
