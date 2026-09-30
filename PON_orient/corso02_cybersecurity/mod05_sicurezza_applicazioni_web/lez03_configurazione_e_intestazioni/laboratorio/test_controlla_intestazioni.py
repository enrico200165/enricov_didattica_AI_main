"""Test di controlla_intestazioni.py. Esecuzione: python test_controlla_intestazioni.py

La prova con --url usa un piccolo server avviato su 127.0.0.1: non serve Internet.
"""

import threading
from wsgiref.simple_server import make_server, WSGIRequestHandler

from controlla_intestazioni import leggi_intestazioni, valuta, intestazioni_da_url

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def esito(esiti, nome):
    return [e for e, n, _ in esiti if n == nome]


def da_file(nome):
    with open(nome, encoding="utf-8") as f:
        return valuta(leggi_intestazioni(f.read()))


buona = da_file("esempio_configurazione_buona.txt")
verifica("configurazione buona: nessun MANCA", all(e != "MANCA" for e, _, _ in buona))
verifica("configurazione buona: cookie completo", esito(buona, "Cookie __Host-sessione") == ["OK"])
verifica("configurazione buona: Server senza versione non segnalato", not esito(buona, "Server"))

debole = da_file("esempio_configurazione_debole.txt")
verifica("HSTS di un'ora: ATTENZIONE", esito(debole, "Strict-Transport-Security") == ["ATTENZIONE"])
verifica("CSP assente: MANCA", esito(debole, "Content-Security-Policy") == ["MANCA"])
verifica("X-XSS-Protection attiva: ATTENZIONE", esito(debole, "X-XSS-Protection") == ["ATTENZIONE"])
verifica("versioni di Server e X-Powered-By segnalate",
         esito(debole, "Server") == ["ATTENZIONE"] and esito(debole, "X-Powered-By") == ["ATTENZIONE"])
verifica("cookie senza attributi: ATTENZIONE", esito(debole, "Cookie PHPSESSID") == ["ATTENZIONE"])

chrome = leggi_intestazioni(open("esempio_formato_chrome.txt", encoding="utf-8").read())
verifica("formato a righe alternate letto", ("x-frame-options", "SAMEORIGIN") in chrome and len(chrome) == 4)
verifica("CSP con unsafe-inline: ATTENZIONE", esito(valuta(chrome), "Content-Security-Policy") == ["ATTENZIONE"])
verifica("formato 'Nome: valore' con due punti nel valore",
         leggi_intestazioni("Content-Security-Policy: default-src 'self' https://cdn.example")
         == [("content-security-policy", "default-src 'self' https://cdn.example")])


def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain"), ("X-Content-Type-Options", "nosniff"),
                              ("Referrer-Policy", "no-referrer")])
    return [b"prova"]


class Silenzioso(WSGIRequestHandler):
    def log_message(self, *argomenti):
        pass


server = make_server("127.0.0.1", 0, app, handler_class=Silenzioso)
threading.Thread(target=server.serve_forever, daemon=True).start()
locale = valuta(intestazioni_da_url(f"http://127.0.0.1:{server.server_port}/"))
verifica("--url: intestazioni lette dal server locale",
         esito(locale, "X-Content-Type-Options") == ["OK"] and esito(locale, "Referrer-Policy") == ["OK"])
verifica("--url: Server di wsgiref con versione segnalato", esito(locale, "Server") == ["ATTENZIONE"])
server.shutdown()

print(f"Test superati: {superati}, falliti: {falliti}")
