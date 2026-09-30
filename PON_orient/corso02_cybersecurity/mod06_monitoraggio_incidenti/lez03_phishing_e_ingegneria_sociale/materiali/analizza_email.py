"""Analisi delle intestazioni e dei collegamenti di un messaggio email salvato in formato .eml.

Uso: python analizza_email.py messaggio.eml

Un messaggio si salva come file .eml, per esempio, in Thunderbird (Salva come, File) e in molte webmail
(comando per scaricare il messaggio). Lo script legge il file senza aprire collegamenti né allegati.
Solo libreria standard di Python.
"""

import re
import sys
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
from html.parser import HTMLParser
from urllib.parse import urlparse

ESTENSIONI_RISCHIOSE = (".exe", ".scr", ".js", ".vbs", ".bat", ".cmd", ".ps1", ".iso", ".img",
                        ".lnk", ".hta", ".docm", ".xlsm", ".zip", ".7z", ".rar", ".html", ".htm")


def dominio(indirizzo):
    """Dominio di un indirizzo email, in minuscolo."""
    return parseaddr(indirizzo)[1].rpartition("@")[2].lower()


class Collegamenti(HTMLParser):
    """Raccoglie i collegamenti <a href="..."> con il testo visibile."""

    def __init__(self):
        super().__init__()
        self.voci, self._corrente = [], None

    def handle_starttag(self, tag, attributi):
        if tag == "a":
            self._corrente = [dict(attributi).get("href", ""), ""]

    def handle_data(self, dati):
        if self._corrente is not None:
            self._corrente[1] += dati

    def handle_endtag(self, tag):
        if tag == "a" and self._corrente is not None:
            self.voci.append((self._corrente[0], self._corrente[1].strip()))
            self._corrente = None


def host(testo):
    """Nome del server contenuto in un indirizzo web, anche se scritto senza https://."""
    if not re.match(r"^[a-z]+://", testo, re.I):
        testo = "https://" + testo
    return (urlparse(testo).hostname or "").lower()


def esiti_autenticazione(messaggio):
    """Esiti SPF, DKIM e DMARC dall'intestazione Authentication-Results aggiunta dal server ricevente."""
    testo = " ".join(str(v) for v in messaggio.get_all("Authentication-Results", []))
    return {m: (re.search(rf"\b{m}=(\w+)", testo) or [None, "assente"])[1] for m in ("spf", "dkim", "dmarc")}


def analizza(percorso):
    with open(percorso, "rb") as f:
        messaggio = BytesParser(policy=policy.default).parse(f)
    risultato = {
        "da": str(messaggio["From"]),
        "oggetto": str(messaggio["Subject"]),
        "rispondi_a": str(messaggio["Reply-To"] or ""),
        "percorso_ritorno": str(messaggio["Return-Path"] or ""),
        "passaggi": [" ".join(str(r).split()) for r in messaggio.get_all("Received", [])],
        "autenticazione": esiti_autenticazione(messaggio),
        "collegamenti": [],
        "allegati": [],
        "segnali": [],
    }
    for parte in messaggio.walk():
        nome_file = parte.get_filename()
        if nome_file:
            risultato["allegati"].append(nome_file)
        elif parte.get_content_type() == "text/html":
            lettore = Collegamenti()
            lettore.feed(parte.get_content())
            risultato["collegamenti"].extend(lettore.voci)

    d_da = dominio(risultato["da"])
    segnali = risultato["segnali"]
    for meccanismo, esito in risultato["autenticazione"].items():
        if esito != "pass":
            segnali.append(f"{meccanismo.upper()}: {esito}")
    if risultato["rispondi_a"] and dominio(risultato["rispondi_a"]) != d_da:
        segnali.append(f"le risposte andrebbero a un altro dominio: {dominio(risultato['rispondi_a'])}")
    if risultato["percorso_ritorno"] and dominio(risultato["percorso_ritorno"]) not in (d_da, ""):
        segnali.append(f"indirizzo di ritorno di un altro dominio: {dominio(risultato['percorso_ritorno'])}")
    for href, testo in risultato["collegamenti"]:
        destinazione = host(href)
        if href.lower().startswith("http://"):
            segnali.append(f"collegamento non cifrato: {href}")
        if re.search(r"[a-z0-9-]+\.[a-z]{2,}", testo, re.I) and host(testo) != destinazione:
            segnali.append(f"il testo mostra {host(testo)} ma il collegamento porta a {destinazione}")
    for nome_file in risultato["allegati"]:
        if nome_file.lower().endswith(ESTENSIONI_RISCHIOSE):
            segnali.append(f"allegato di tipo rischioso: {nome_file}")
    return risultato


def stampa(r):
    print(f"Da:                {r['da']}")
    print(f"Oggetto:           {r['oggetto']}")
    print(f"Rispondi a:        {r['rispondi_a'] or '-'}")
    print(f"Percorso di ritorno: {r['percorso_ritorno'] or '-'}")
    print("Passaggi tra i server (dal più recente):")
    for passaggio in r["passaggi"]:
        print(f"  {passaggio[:110]}")
    a = r["autenticazione"]
    print(f"Autenticazione:    SPF={a['spf']}  DKIM={a['dkim']}  DMARC={a['dmarc']}")
    print("Collegamenti (destinazione reale e testo visibile):")
    for href, testo in r["collegamenti"]:
        print(f"  {href}  [{testo}]")
    print("Allegati:", ", ".join(r["allegati"]) or "nessuno")
    print("\nSEGNALI DI ATTENZIONE:" if r["segnali"] else "\nNessun segnale tecnico di attenzione.")
    for s in r["segnali"]:
        print(f"  - {s}")
    print("\nI controlli tecnici non bastano: vanno letti anche contenuto, tono e richiesta del messaggio.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    stampa(analizza(sys.argv[1]))
