"""Test di risolutore_dns.py. Esecuzione: python test_risolutore_dns.py"""

from risolutore_dns import Risolutore, interroga

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


verifica("la radice delega il TLD example.", interroga("radice", "www.scuola.example.", "A")[0] == "delega")
verifica("il TLD delega il server autorevole",
         interroga("tld-example", "www.scuola.example.", "A")[1][2] == "ns1.scuola.example")

r = Risolutore()
verifica("www.scuola.example -> 203.0.113.80", r.risolvi("www.scuola.example", "A", 0) == ["203.0.113.80"])
verifica("prima risoluzione: tre domande (radice, TLD, autorevole)",
         [d[0] for d in r.domande] == ["radice", "tld-example", "ns1.scuola.example"])
r.risolvi("www.scuola.example", "A", 100)
verifica("entro il TTL (300 s): nessuna nuova domanda", len(r.domande) == 3)
r.risolvi("www.scuola.example", "A", 400)
verifica("dopo il TTL: una sola domanda, all'autorevole (delega ancora in cache)",
         len(r.domande) == 4 and r.domande[-1][0] == "ns1.scuola.example")
verifica("record AAAA", r.risolvi("www.scuola.example", "AAAA", 400) == ["2001:db8:5c01::80"])
verifica("record MX", r.risolvi("scuola.example", "MX", 400) == ["posta.scuola.example."])

r2 = Risolutore()
verifica("alias CNAME seguito fino all'indirizzo", r2.risolvi("portale.scuola.example", "A", 0) == ["203.0.113.80"])
n = len(r2.domande)
r2.risolvi("portale.scuola.example", "A", 10)
verifica("alias e indirizzo in cache: nessuna nuova domanda", len(r2.domande) == n)
verifica("nome inesistente: risposta vuota", Risolutore().risolvi("altro.scuola.example") == [])
verifica("dominio sconosciuto alla radice: risposta vuota con una sola domanda",
         (lambda x: (x.risolvi("www.esempio.test"), len(x.domande)))(Risolutore()) == ([], 1))

print(f"\nTest superati: {superati}, falliti: {falliti}")
