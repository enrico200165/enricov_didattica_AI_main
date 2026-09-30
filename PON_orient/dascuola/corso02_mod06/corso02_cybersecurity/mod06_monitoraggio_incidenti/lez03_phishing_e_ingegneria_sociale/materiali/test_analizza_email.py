"""Test di analizza_email.py sui due messaggi di esempio. Esecuzione: python test_analizza_email.py"""

from analizza_email import analizza, dominio, host

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


verifica("dominio di un indirizzo con nome visualizzato", dominio('"Segreteria" <a@Scuola.Example>') == "scuola.example")
verifica("host di un indirizzo senza https", host("www.scuola.example/posta") == "www.scuola.example")

s = analizza("email_sospetta.eml")
verifica("sospetta: SPF, DKIM e DMARC non superati",
         s["autenticazione"] == {"spf": "fail", "dkim": "none", "dmarc": "fail"})
verifica("sospetta: due passaggi tra server", len(s["passaggi"]) == 2)
verifica("sospetta: Reply-To di un altro dominio segnalato",
         any("posta-gratuita.example" in x for x in s["segnali"]))
verifica("sospetta: collegamento con testo ingannevole segnalato",
         any("porta a scuola.example.verifica-account.example" in x for x in s["segnali"]))
verifica("sospetta: sei segnali", len(s["segnali"]) == 6)

l = analizza("email_legittima.eml")
verifica("legittima: autenticazione superata", set(l["autenticazione"].values()) == {"pass"})
verifica("legittima: nessun segnale", l["segnali"] == [])
verifica("legittima: un collegamento coerente",
         l["collegamenti"] == [("https://piattaforma.scuola.example/corsi/informatica-4a", "piattaforma.scuola.example")])

print(f"Test superati: {superati}, falliti: {falliti}")
