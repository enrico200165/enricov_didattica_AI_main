"""Test di orchestratore.py. Esecuzione: python test_orchestratore.py"""

from orchestratore import Cluster

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def conta(c):
    return {n: len(r) for n, r in c.stato().items()}


c = Cluster({"nodo-a": 2000, "nodo-b": 2000, "nodo-c": 1000})
c.applica("web", 4, 500)
verifica("4 repliche distribuite sui nodi con più spazio", conta(c) == {"nodo-a": 2, "nodo-b": 2, "nodo-c": 0})
verifica("capacità libera calcolata", c.libera("nodo-a") == 1000 and c.libera("nodo-c") == 1000)
c.applica("web", 4, 500)
verifica("stesso stato desiderato: nessun cambiamento", len(c.repliche) == 4 and len(c.eventi) == 4)
c.guasto("nodo-a")
verifica("guasto: nessuna replica sul nodo guasto, tutte ancora in esecuzione",
         c.stato()["nodo-a"] == [] and all(n is not None for n in c.repliche.values()))
c.applica("web", 7, 500)
in_attesa = [r for r, n in c.repliche.items() if n is None]
verifica("7 repliche su 3000 millesimi: una in attesa", in_attesa == ["web-7"])
c.attivi.add("nodo-a")
c.riprova_in_attesa()
verifica("nodo di nuovo disponibile: la replica in attesa viene collocata", c.repliche["web-7"] == "nodo-a")
c.applica("web", 2, 500)
verifica("riduzione a 2 repliche", sorted(c.repliche) == ["web-1", "web-2"])
d = Cluster({"x": 1000})
d.applica("db", 1, 1500)
verifica("richiesta più grande di qualsiasi nodo: sempre in attesa", d.repliche["db-1"] is None)

print(f"\nTest superati: {superati}, falliti: {falliti}")
