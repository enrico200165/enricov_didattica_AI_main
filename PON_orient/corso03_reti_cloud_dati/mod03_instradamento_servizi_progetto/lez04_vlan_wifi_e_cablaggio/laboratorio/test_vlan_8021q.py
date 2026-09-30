"""Test di vlan_8021q.py. Esecuzione: python test_vlan_8021q.py"""

from vlan_8021q import aggiungi_etichetta, leggi_etichetta, togli_etichetta, trama_di_esempio

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def errore(funzione, *argomenti, **opzioni):
    try:
        funzione(*argomenti, **opzioni)
    except ValueError:
        return True
    return False


t = trama_di_esempio()
e = aggiungi_etichetta(t, 20, 5)
verifica("etichetta di 4 byte", len(e) == len(t) + 4)
verifica("TPID 0x8100 dopo i MAC", e[12:14] == b"\x81\x00")
verifica("TCI: priorità 5, VID 20 = 0xa014", e[14:16] == b"\xa0\x14")
verifica("il tipo 0x0800 segue l'etichetta", e[16:18] == b"\x08\x00")
verifica("lettura dell'etichetta", leggi_etichetta(e) == (20, 5))
verifica("trama senza etichetta: None", leggi_etichetta(t) is None)
verifica("togliere l'etichetta restituisce la trama originale", togli_etichetta(e) == t)
verifica("VID 4094 accettato, 0 e 4095 rifiutati",
         leggi_etichetta(aggiungi_etichetta(t, 4094))[0] == 4094 and errore(aggiungi_etichetta, t, 0) and errore(aggiungi_etichetta, t, 4095))
verifica("priorità 8 rifiutata", errore(aggiungi_etichetta, t, 10, priorita=8))

print(f"\nTest superati: {superati}, falliti: {falliti}")
