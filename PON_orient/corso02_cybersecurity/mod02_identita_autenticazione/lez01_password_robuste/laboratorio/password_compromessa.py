"""Verifica se una password compare negli elenchi di password trapelate (lezione 2.1).

Usa il servizio pubblico Pwned Passwords con il metodo k-anonimity: al servizio si invia
solo l'inizio (5 caratteri) dell'impronta SHA-1 della password; il confronto completo
avviene sul proprio computer. La password non esce mai dal PC.
Usare con password di prova, non con le proprie password reali su computer condivisi.
"""
import getpass
import hashlib
import urllib.request

URL = "https://api.pwnedpasswords.com/range/"


def occorrenze(password):
    """Numero di volte in cui la password compare negli elenchi di password trapelate."""
    impronta = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefisso, suffisso = impronta[:5], impronta[5:]
    richiesta = urllib.request.Request(URL + prefisso, headers={"User-Agent": "corso-cybersecurity-scuola"})
    with urllib.request.urlopen(richiesta, timeout=10) as risposta:
        for riga in risposta.read().decode("utf-8").splitlines():
            parte_finale, conteggio = riga.split(":")
            if parte_finale == suffisso:
                return int(conteggio)
    return 0


if __name__ == "__main__":
    pw = getpass.getpass("Password di prova (non viene mostrata): ")
    n = occorrenze(pw)
    if n:
        print(f"Compare {n} volte negli elenchi di password trapelate: non va usata.")
    else:
        print("Non compare negli elenchi noti (non significa che sia robusta).")
