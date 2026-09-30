"""Test di disponibilita.py. Esecuzione: python test_disponibilita.py"""

from disponibilita import serie, parallelo, fermo_annuo, formato_fermo, server_necessari

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


verifica("serie: 0,99 x 0,99 = 0,9801", abs(serie(0.99, 0.99) - 0.9801) < 1e-12)
verifica("parallelo: 1 - 0,01 x 0,01 = 0,9999", abs(parallelo(0.99, 0.99) - 0.9999) < 1e-12)
verifica("la serie peggiora, il parallelo migliora", serie(0.99, 0.999) < 0.99 < parallelo(0.99, 0.9))
verifica("99,9% = 8,76 ore di fermo all'anno", abs(fermo_annuo(0.999) - 8.76) < 1e-9)
verifica("99% = 3,7 giorni all'anno", formato_fermo(fermo_annuo(0.99)) == "3.7 giorni")
verifica("99,99% = 53 minuti all'anno", formato_fermo(fermo_annuo(0.9999)) == "53 minuti")
ridondato = serie(0.9999, parallelo(0.995, 0.995), 0.9995)
verifica("due server in parallelo meglio di uno", ridondato > serie(0.995, 0.9995))
verifica("il database diventa l'anello debole", abs(ridondato - 0.9994) < 0.0001)
verifica("900 richieste/s, 200 per server, margine 30%, 1 riserva: 7 server", server_necessari(900, 200) == 7)
verifica("carico esatto senza margine né riserva", server_necessari(400, 200, 0, 0) == 2)

print(f"\nTest superati: {superati}, falliti: {falliti}")
