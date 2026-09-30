"""Test di calcolo_ipv4.py. Esecuzione: python test_calcolo_ipv4.py"""

import builtins
import io
import random
import contextlib

import calcolo_ipv4 as c

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def errore(funzione, *argomenti):
    try:
        funzione(*argomenti)
    except ValueError:
        return True
    return False


verifica("192.168.1.10 <-> intero", c.intero_a_ip(c.ip_a_intero("192.168.1.10")) == "192.168.1.10")
verifica("in binario", c.in_binario(c.ip_a_intero("192.168.1.10")) == "11000000.10101000.00000001.00001010")
verifica("indirizzo con un byte oltre 255 rifiutato", errore(c.ip_a_intero, "192.168.1.300"))
verifica("/26 -> 255.255.255.192", c.intero_a_ip(c.maschera_da_prefisso(26)) == "255.255.255.192")
verifica("255.255.240.0 -> /20", c.prefisso_da_maschera("255.255.240.0") == 20)
verifica("maschera non contigua rifiutata", errore(c.prefisso_da_maschera, "255.0.255.0"))

r = c.analizza("192.168.10.77/26")
verifica("192.168.10.77/26: rete 192.168.10.64, broadcast .127",
         r["rete"] == "192.168.10.64" and r["broadcast"] == "192.168.10.127")
verifica("192.168.10.77/26: 62 host da .65 a .126",
         r["host"] == 62 and r["primo_host"] == "192.168.10.65" and r["ultimo_host"] == "192.168.10.126")
verifica("192.168.10.77: classe storica C, privato", r["classe_storica"] == "C" and r["privato"])
r = c.analizza("172.20.5.9/12")
verifica("172.20.5.9/12: rete 172.16.0.0, broadcast 172.31.255.255, privato",
         r["rete"] == "172.16.0.0" and r["broadcast"] == "172.31.255.255" and r["privato"])
verifica("172.32.0.1 non è privato", not c.analizza("172.32.0.1/16")["privato"])
verifica("classi A, B, D, E", [c.classe_storica(c.ip_a_intero(x))[0] for x in
                               ("10.1.1.1", "150.1.1.1", "224.0.0.1", "250.0.0.1")] == list("ABDE"))
verifica("/31: 2 host utilizzabili (RFC 3021)", c.analizza("10.0.0.0/31")["host"] == 2)
verifica("/32: 1 host", c.analizza("10.0.0.5/32")["host"] == 1)

# Confronto con ipaddress su tutti i prefissi e su molti indirizzi casuali
generatore = random.Random(2026)
casi = [f"{c.intero_a_ip(generatore.getrandbits(32))}/{p}" for p in range(0, 33) for _ in range(30)]
verifica(f"calcolo a mano concorde con ipaddress su {len(casi)} casi", all(c.concordano(x) for x in casi))

# Esercizi: risposte simulate, prima tutte giuste poi tutte sbagliate
def punteggio(risposte_giuste):
    esercizio = random.Random(7)
    prefisso = esercizio.randint(16, 30)
    base = esercizio.choice([c.ip_a_intero("10.0.0.0"), c.ip_a_intero("172.16.0.0"), c.ip_a_intero("192.168.0.0")])
    cidr = f"{c.intero_a_ip(base + esercizio.randint(1, 65534))}/{prefisso}"
    giuste = c.calcola_con_ipaddress(cidr)
    valori = iter([giuste["rete"], giuste["broadcast"], str(giuste["host"])] if risposte_giuste else ["x", "y", "z"])
    originale = builtins.input
    builtins.input = lambda _="": next(valori)
    uscita = io.StringIO()
    try:
        with contextlib.redirect_stdout(uscita):
            c.esercizi(1, seme=7)
    finally:
        builtins.input = originale
    return uscita.getvalue().strip().splitlines()[-1]

verifica("esercizio con risposte giuste: 3 su 3", punteggio(True) == "Punteggio: 3 su 3")
verifica("esercizio con risposte sbagliate: 0 su 3", punteggio(False) == "Punteggio: 0 su 3")

print(f"\nTest superati: {superati}, falliti: {falliti}")
