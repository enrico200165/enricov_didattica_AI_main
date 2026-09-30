"""Informazioni sul certificato e sulla connessione TLS di un sito web.

Uso:  python info_certificato.py www.example.org [porta]

Lo script apre una normale connessione HTTPS, come fa un browser, e mostra
che cosa è stato verificato: nessun dato viene inviato oltre alla richiesta di connessione.
Solo libreria standard di Python.
"""

import socket
import ssl
import sys
from datetime import datetime, timezone


def _nomi(campo):
    """Converte il formato del modulo ssl, ((('commonName', 'x'),), ...), in un dizionario."""
    return {chiave: valore for rdn in campo for chiave, valore in rdn}


def leggi_certificato(host, porta=443, contesto=None, timeout=10):
    """Si collega al sito, verifica certificato e nome, e restituisce i dati principali."""
    contesto = contesto or ssl.create_default_context()
    with socket.create_connection((host, porta), timeout=timeout) as sock:
        with contesto.wrap_socket(sock, server_hostname=host) as tls:
            cert = tls.getpeercert()
            return {
                "soggetto": _nomi(cert["subject"]),
                "emittente": _nomi(cert["issuer"]),
                "nomi_alternativi": [v for t, v in cert.get("subjectAltName", ()) if t == "DNS"],
                "valido_dal": datetime.fromtimestamp(ssl.cert_time_to_seconds(cert["notBefore"]), timezone.utc),
                "valido_fino_al": datetime.fromtimestamp(ssl.cert_time_to_seconds(cert["notAfter"]), timezone.utc),
                "protocollo": tls.version(),
                "cifrario": tls.cipher()[0],
            }


def giorni_rimanenti(info, adesso=None):
    adesso = adesso or datetime.now(timezone.utc)
    return (info["valido_fino_al"] - adesso).days


def durata_giorni(info):
    return (info["valido_fino_al"] - info["valido_dal"]).days


def stampa(host, info):
    print(f"Sito:               {host}")
    print(f"Intestatario (CN):  {info['soggetto'].get('commonName', '-')}")
    print(f"Nomi coperti:       {', '.join(info['nomi_alternativi'][:6])}"
          + (" ..." if len(info["nomi_alternativi"]) > 6 else ""))
    emittente = info["emittente"]
    print(f"Emesso da:          {emittente.get('commonName', '-')} ({emittente.get('organizationName', '-')})")
    print(f"Valido dal:         {info['valido_dal']:%d/%m/%Y}")
    print(f"Valido fino al:     {info['valido_fino_al']:%d/%m/%Y}"
          f"  (durata {durata_giorni(info)} giorni, ne restano {giorni_rimanenti(info)})")
    print(f"Protocollo:         {info['protocollo']}")
    print(f"Suite crittografica: {info['cifrario']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    host = sys.argv[1]
    porta = int(sys.argv[2]) if len(sys.argv) > 2 else 443
    try:
        stampa(host, leggi_certificato(host, porta))
    except ssl.SSLCertVerificationError as errore:
        print("VERIFICA FALLITA:", errore.verify_message)
        print("Un browser mostrerebbe un avviso di sicurezza: la connessione non va considerata affidabile.")
        sys.exit(1)
    except OSError as errore:
        print("Connessione non riuscita:", errore)
        sys.exit(1)
