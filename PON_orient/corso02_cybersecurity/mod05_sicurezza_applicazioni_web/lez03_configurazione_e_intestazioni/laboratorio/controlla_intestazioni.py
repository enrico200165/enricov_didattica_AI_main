"""Valutazione delle intestazioni di sicurezza di una risposta HTTP.

Uso:
    python controlla_intestazioni.py intestazioni.txt     file con le intestazioni copiate dai DevTools
    python controlla_intestazioni.py --url https://www.example.org/

Con --url lo script esegue una normale richiesta GET, come un browser che apre la pagina.
Raccomandazioni di riferimento: OWASP HTTP Headers Cheat Sheet.
Solo libreria standard di Python.
"""

import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UN_ANNO = 31_536_000  # secondi


def leggi_intestazioni(testo):
    """Lista di coppie (nome in minuscolo, valore) da un testo 'Nome: valore' per riga.

    Accetta anche il formato dei DevTools di Chrome, con nome e valore su righe alternate."""
    righe = [r.strip() for r in testo.splitlines() if r.strip()]
    coppie = []
    i = 0
    while i < len(righe):
        riga = righe[i]
        if riga.upper().startswith("HTTP/"):
            i += 1
            continue
        nome, sep, valore = riga.partition(":")
        if sep and nome and " " not in nome.strip():
            coppie.append((nome.strip().lower(), valore.strip()))
            i += 1
        elif i + 1 < len(righe):            # formato a righe alternate
            coppie.append((riga.rstrip(":").lower(), righe[i + 1]))
            i += 2
        else:
            i += 1
    return coppie


def valori(coppie, nome):
    return [v for n, v in coppie if n == nome]


def valuta(coppie):
    """Lista di (esito, intestazione, commento) con esito 'OK', 'ATTENZIONE' o 'MANCA'."""
    esiti = []

    hsts = valori(coppie, "strict-transport-security")
    if not hsts:
        esiti.append(("MANCA", "Strict-Transport-Security", "il browser non è obbligato a usare sempre HTTPS"))
    else:
        durata = re.search(r"max-age=(\d+)", hsts[0])
        if durata and int(durata.group(1)) >= UN_ANNO:
            esiti.append(("OK", "Strict-Transport-Security", hsts[0]))
        else:
            esiti.append(("ATTENZIONE", "Strict-Transport-Security", "max-age inferiore a un anno: " + hsts[0]))

    csp = valori(coppie, "content-security-policy")
    if not csp:
        esiti.append(("MANCA", "Content-Security-Policy", "nessuna limitazione alle risorse caricabili"))
    elif "unsafe-inline" in csp[0] and "nonce-" not in csp[0] and "strict-dynamic" not in csp[0]:
        esiti.append(("ATTENZIONE", "Content-Security-Policy", "consente script inline senza nonce: protezione ridotta"))
    else:
        esiti.append(("OK", "Content-Security-Policy", csp[0][:80] + ("..." if len(csp[0]) > 80 else "")))

    nosniff = valori(coppie, "x-content-type-options")
    esiti.append(("OK", "X-Content-Type-Options", "nosniff") if nosniff and nosniff[0].lower() == "nosniff"
                 else ("MANCA", "X-Content-Type-Options", "valore atteso: nosniff"))

    incorniciamento = any("frame-ancestors" in v for v in csp) or valori(coppie, "x-frame-options")
    esiti.append(("OK", "Protezione dall'incorniciamento", "frame-ancestors o X-Frame-Options presente")
                 if incorniciamento else
                 ("MANCA", "Protezione dall'incorniciamento", "né frame-ancestors nella CSP né X-Frame-Options"))

    referrer = valori(coppie, "referrer-policy")
    esiti.append(("OK", "Referrer-Policy", referrer[0]) if referrer
                 else ("MANCA", "Referrer-Policy", "valore suggerito: strict-origin-when-cross-origin"))

    xss = valori(coppie, "x-xss-protection")
    if xss and xss[0].strip() != "0":
        esiti.append(("ATTENZIONE", "X-XSS-Protection", "intestazione obsoleta: va omessa o impostata a 0"))

    for nome in ("server", "x-powered-by"):
        for v in valori(coppie, nome):
            if re.search(r"\d", v):
                esiti.append(("ATTENZIONE", nome.title(), f"rivela prodotto e versione: {v}"))

    for cookie in valori(coppie, "set-cookie"):
        nome_cookie = cookie.split("=", 1)[0]
        attributi = cookie.lower()
        mancanti = [a for a in ("secure", "httponly", "samesite") if a not in attributi]
        if mancanti:
            esiti.append(("ATTENZIONE", f"Cookie {nome_cookie}", "attributi mancanti: " + ", ".join(mancanti)))
        else:
            esiti.append(("OK", f"Cookie {nome_cookie}", "Secure, HttpOnly, SameSite presenti"))
    return esiti


def intestazioni_da_url(url):
    """Intestazioni della risposta; anche una risposta di errore (4xx, 5xx) ha intestazioni valutabili."""
    richiesta = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (laboratorio 5.3)"})
    # per i server sul proprio PC non si usa l'eventuale proxy di sistema
    locale = urllib.parse.urlparse(url).hostname in ("127.0.0.1", "localhost", "::1")
    apri = urllib.request.build_opener(urllib.request.ProxyHandler({})).open if locale else urllib.request.urlopen
    try:
        with apri(richiesta, timeout=15) as risposta:
            return [(n.lower(), v) for n, v in risposta.getheaders()]
    except urllib.error.HTTPError as errore:
        print(f"Nota: il server ha risposto con il codice {errore.code}; si valutano le intestazioni ricevute.")
        return [(n.lower(), v) for n, v in errore.headers.items()]


def stampa(esiti):
    for esito, nome, commento in esiti:
        print(f"{esito:11} {nome:32} {commento}")
    print(f"\nOK: {sum(e == 'OK' for e, _, _ in esiti)}, "
          f"ATTENZIONE: {sum(e == 'ATTENZIONE' for e, _, _ in esiti)}, MANCA: {sum(e == 'MANCA' for e, _, _ in esiti)}")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--url":
        try:
            stampa(valuta(intestazioni_da_url(sys.argv[2])))
        except (urllib.error.URLError, OSError) as errore:
            print("Connessione non riuscita:", getattr(errore, "reason", errore))
            print("Alternativa: copiare le intestazioni dai DevTools in un file di testo.")
            sys.exit(1)
    elif len(sys.argv) == 2:
        with open(sys.argv[1], encoding="utf-8") as f:
            stampa(valuta(leggi_intestazioni(f.read())))
    else:
        print(__doc__)
        sys.exit(2)
