"""Test di switch_simulato.py. Esecuzione: python test_switch_simulato.py"""

from switch_simulato import Switch, BROADCAST

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


A, B, C = "02:00:00:00:00:0a", "02:00:00:00:00:0b", "02:00:00:00:00:0c"

sw = Switch("SW1", 4)
verifica("tabella inizialmente vuota", sw.tabella == {})

azione, uscite = sw.ricevi(1, A, BROADCAST, 0)
verifica("broadcast inoltrato su tutte le porte tranne quella di arrivo",
         azione == "flooding" and uscite == [2, 3, 4])
verifica("origine appresa sulla porta di arrivo (in maiuscolo)",
         sw.tabella["02:00:00:00:00:0A"][0] == 1)

azione, uscite = sw.ricevi(2, B, A, 1)
verifica("destinazione nota: inoltro solo sulla sua porta", (azione, uscite) == ("inoltro", [1]))

azione, uscite = sw.ricevi(1, A, C, 2)
verifica("destinazione sconosciuta: flooding", (azione, uscite) == ("flooding", [2, 3, 4]))

sw.ricevi(3, C, A, 3)
verifica("dopo la risposta di C la tabella ha tre voci", len(sw.tabella) == 3)
verifica("ora A -> C va solo sulla porta 3", sw.ricevi(1, A, C, 4) == ("inoltro", [3]))

# Un PC spostato su un'altra porta: la voce si aggiorna alla prima trama
sw.ricevi(4, B, A, 5)
verifica("PC spostato: la tabella segue la nuova porta", sw.tabella["02:00:00:00:00:0B"][0] == 4)

# Due MAC sulla stessa porta (per esempio dietro un secondo switch)
sw2 = Switch("SW2", 2)
sw2.ricevi(1, A, BROADCAST, 0)
sw2.ricevi(1, B, BROADCAST, 0)
verifica("destinazione sulla stessa porta di arrivo: scarto", sw2.ricevi(1, A, B, 1) == ("scarto", []))

# Scadenza delle voci
sw3 = Switch("SW3", 3, durata_voci=300)
sw3.ricevi(1, A, BROADCAST, 0)
sw3.ricevi(2, B, BROADCAST, 100)
sw3.rimuovi_scadute(350)
verifica("voce più vecchia di 300 s eliminata, l'altra conservata",
         list(sw3.tabella) == ["02:00:00:00:00:0B"])
verifica("dopo la scadenza la destinazione torna sconosciuta",
         sw3.ricevi(2, B, A, 360)[0] == "flooding")

print(f"\nTest superati: {superati}, falliti: {falliti}")
