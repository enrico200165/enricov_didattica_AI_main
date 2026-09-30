"""Test di costi_cloud.py. Esecuzione: python test_costi_cloud.py"""

import copy

from costi_cloud import carica, costo_scenario, costo_locale

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


listino = carica("listino_esempio.json")
scenari = carica("scenari.json")
vuoto = {"vm": [], "disco_gb": 0, "database_ore_mese": 0, "oggetti_gb": 0,
         "richieste_oggetti_mese": 0, "traffico_uscita_gb": 0}

s = copy.deepcopy(vuoto)
s["vm"] = [{"tipo": "piccola", "quantita": 1, "ore_mese": 730}]
verifica("una VM piccola sempre accesa: 0,05 x 730 = 36,50", costo_scenario(s, listino)["calcolo (macchine virtuali)"] == 36.50)
s["vm"][0]["impegno_1_anno"] = True
verifica("con impegno di un anno: sconto del 35% (23,73)", costo_scenario(s, listino)["calcolo (macchine virtuali)"] == 23.73)
s["vm"] = [{"tipo": "media", "quantita": 8, "ore_mese": 40}]
verifica("8 VM medie per 40 ore: 0,19 x 8 x 40 = 60,80", costo_scenario(s, listino)["calcolo (macchine virtuali)"] == 60.80)

t = copy.deepcopy(vuoto)
t["traffico_uscita_gb"] = 80
verifica("traffico entro la parte gratuita: 0", costo_scenario(t, listino)["traffico in uscita"] == 0)
t["traffico_uscita_gb"] = 600
verifica("600 GB in uscita: (600 - 100) x 0,09 = 45", costo_scenario(t, listino)["traffico in uscita"] == 45.0)
t = copy.deepcopy(vuoto)
t["oggetti_gb"], t["richieste_oggetti_mese"] = 1000, 2_000_000
v = costo_scenario(t, listino)
verifica("1000 GB di oggetti: 23 EUR; 2 milioni di richieste: 10 EUR",
         v["archiviazione a oggetti"] == 23.0 and v["richieste agli oggetti"] == 10.0)

totali = {n: round(sum(costo_scenario(s, listino).values()), 2) for n, s in scenari.items()}
verifica("totali dei tre scenari", totali == {"sito_biblioteca": 128.21, "piattaforma_verifiche": 391.86,
                                               "archivio_video": 654.73})
video = costo_scenario(scenari["archivio_video"], listino)
verifica("archivio video: la voce principale è il traffico in uscita", max(video, key=video.get) == "traffico in uscita")

l = costo_locale()
verifica("server locale: 4000 EUR in 60 mesi = 66,67 al mese", l["ammortamento"] == 66.67)
verifica("energia: 0,25 kW x 730 h x 0,30 EUR = 54,75", l["energia"] == 54.75)

print(f"\nTest superati: {superati}, falliti: {falliti}")
