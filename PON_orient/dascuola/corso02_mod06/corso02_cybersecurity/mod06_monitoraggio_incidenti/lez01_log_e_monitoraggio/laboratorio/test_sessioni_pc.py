"""Test di sessioni_pc.py. Esecuzione: python test_sessioni_pc.py"""

from datetime import datetime, timedelta

from sessioni_pc import leggi_eventi, sessioni, durata

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


eventi = leggi_eventi("eventi_esempio.csv")
verifica("CSV con BOM letto: 8 eventi in ordine cronologico",
         len(eventi) == 8 and eventi == sorted(eventi))
elenco = sessioni(eventi)
verifica("quattro sessioni", len(elenco) == 4)
verifica("prima sessione regolare di 4h 55m",
         elenco[0]["esito"] == "regolare" and durata(elenco[0]) == timedelta(hours=4, minutes=55, seconds=8))
verifica("seconda sessione terminata in modo non regolare", elenco[1]["esito"] == "non regolare" and elenco[1]["fine"] is None)
verifica("ultima sessione ancora in corso", elenco[3]["esito"] == "in corso")

t = datetime(2026, 10, 1, 8, 0)
semplice = sessioni([(t, 6005), (t + timedelta(hours=2), 6006), (t + timedelta(hours=3), 6005),
                     (t + timedelta(hours=5), 6006)])
verifica("due sessioni regolari consecutive", [s["esito"] for s in semplice] == ["regolare", "regolare"])
verifica("arresto senza avvio precedente ignorato", sessioni([(t, 6006)]) == [])

print(f"Test superati: {superati}, falliti: {falliti}")
