"""Test di analizza_cattura.py sulle catture della lezione 4.3.

Le catture si cercano nella cartella corrente e poi in ../../lez03_wireshark_primi_passi/catture.
Esecuzione: python test_analizza_cattura.py
"""

from pathlib import Path

from analizza_cattura import analizza, sni_tls, nome_dns, dati_sensibili_http

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def trova(nome):
    for cartella in (Path("."), Path("../../lez03_wireshark_primi_passi/catture")):
        if (cartella / nome).exists():
            return cartella / nome
    raise FileNotFoundError(nome)


r1 = analizza(trova("cattura1_navigazione.pcapng"))
verifica("cattura 1: 30 pacchetti", r1["pacchetti"] == 30)
verifica("cattura 1: due richieste DNS", [n for _, _, n in r1["dns"]] == ["registro.scuola.example"] * 2)
verifica("cattura 1: SNI della connessione TLS nel pacchetto 20", r1["tls"] == [(20, "192.168.10.23", "registro.scuola.example")])
verifica("cattura 1: nessun dato sensibile in chiaro", r1["in_chiaro"] == [])

r2 = analizza(trova("cattura2_accessi.pcapng"))
verifica("cattura 2: 68 pacchetti", r2["pacchetti"] == 68)
verifica("cattura 2: quattro conversazioni (DNS, FTP, HTTP, HTTPS)",
         sorted(k[3] for k in r2["conversazioni"]) == [21, 53, 80, 443])
voci = {(n, v) for n, _, _, v in r2["in_chiaro"]}
verifica("password del modulo nel pacchetto 18", (18, "campo 'password' del modulo: Girasole-73") in voci)
verifica("HTTP Basic decodificato nel pacchetto 28", (28, "autenticazione HTTP Basic: prof.rossi:Lavagna!2026") in voci)
verifica("FTP USER e PASS nei pacchetti 42 e 45", (42, "USER segreteria") in voci and (45, "PASS Estate2026") in voci)
verifica("il login via HTTPS non compare tra i dati in chiaro", all(n < 58 for n, _ in voci))

verifica("SNI: dati non TLS ignorati", sni_tls(b"GET / HTTP/1.1\r\n") is None)
verifica("nome DNS da un messaggio costruito a mano",
         nome_dns(b"\x00" * 12 + b"\x03www\x07example\x03org\x00\x00\x01\x00\x01") == "www.example.org")
verifica("campo non sensibile ignorato",
         dati_sensibili_http("POST /cerca HTTP/1.1\r\nHost: x\r\n\r\nparola=rete") == [])

print(f"Test superati: {superati}, falliti: {falliti}")
