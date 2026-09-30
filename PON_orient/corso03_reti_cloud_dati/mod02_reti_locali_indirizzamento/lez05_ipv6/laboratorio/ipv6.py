"""Strumenti per gli indirizzi IPv6: espansione, abbreviazione, tipo, EUI-64,
lettura degli indirizzi dall'output di ipconfig.

Uso:
    python ipv6.py 2001:0db8:0000:0000:0000:ff00:0042:8329   analisi di un indirizzo
    python ipv6.py --ipconfig                                  esegue "ipconfig" (Windows)
    python ipv6.py --ipconfig ipconfig_esempio.txt             legge un output salvato
    python ipv6.py --eui64 00-1b-21-3a-5c-01                   identificativo di interfaccia EUI-64
"""

import ipaddress
import os
import re
import subprocess
import sys


def espandi(testo):
    """Forma completa: otto gruppi di quattro cifre esadecimali."""
    testo = testo.strip().lower()
    if testo.count("::") > 1:
        raise ValueError("'::' può comparire una sola volta")
    if "::" in testo:
        sinistra, destra = testo.split("::")
        gruppi_sx = sinistra.split(":") if sinistra else []
        gruppi_dx = destra.split(":") if destra else []
        mancanti = 8 - len(gruppi_sx) - len(gruppi_dx)
        if mancanti < 1:
            raise ValueError("troppi gruppi per usare '::'")
        gruppi = gruppi_sx + ["0"] * mancanti + gruppi_dx   # '::' sostituisce i gruppi a zero
    else:
        gruppi = testo.split(":")
    if len(gruppi) != 8 or not all(re.fullmatch(r"[0-9a-f]{1,4}", g) for g in gruppi):
        raise ValueError(f"indirizzo IPv6 non valido: {testo}")
    return ":".join(g.zfill(4) for g in gruppi)          # zfill aggiunge gli zeri a sinistra


def abbrevia(testo):
    """Forma abbreviata raccomandata dall'RFC 5952.

    1. minuscole e senza zeri iniziali in ogni gruppo
    2. la sequenza più lunga di almeno due gruppi a zero diventa '::'
       (a parità di lunghezza, la prima)
    """
    gruppi = [format(int(g, 16), "x") for g in espandi(testo).split(":")]
    migliore_inizio, migliore_lunghezza = -1, 0
    i = 0
    while i < 8:
        if gruppi[i] == "0":
            j = i
            while j < 8 and gruppi[j] == "0":
                j += 1
            if j - i > migliore_lunghezza:
                migliore_inizio, migliore_lunghezza = i, j - i
            i = j
        else:
            i += 1
    if migliore_lunghezza < 2:
        return ":".join(gruppi)
    sinistra = ":".join(gruppi[:migliore_inizio])
    destra = ":".join(gruppi[migliore_inizio + migliore_lunghezza:])
    return sinistra + "::" + destra


# Blocchi principali, dal più specifico al più generale
TIPI = [
    ("::/128", "non specificato"),
    ("::1/128", "loopback"),
    ("2001:db8::/32", "documentazione (esempi)"),
    ("fe80::/10", "link-local"),
    ("fc00::/7", "locale unico (ULA)"),
    ("ff00::/8", "multicast"),
    ("2000::/3", "unicast globale"),
]


def tipo(testo):
    indirizzo = ipaddress.IPv6Address(espandi(testo))
    for blocco, nome in TIPI:
        if indirizzo in ipaddress.IPv6Network(blocco):
            return nome
    return "altro o riservato"


def eui64(mac):
    """Identificativo di interfaccia (ultimi 64 bit) ricavato dal MAC con il metodo EUI-64.

    Si inserisce FFFE al centro del MAC e si inverte il settimo bit del primo byte (bit U/L).
    """
    cifre = re.sub(r"[-:]", "", mac).lower()
    if not re.fullmatch(r"[0-9a-f]{12}", cifre):
        raise ValueError(f"indirizzo MAC non valido: {mac}")
    primo = int(cifre[:2], 16) ^ 0b00000010             # XOR: inverte il bit U/L
    completo = f"{primo:02x}{cifre[2:6]}fffe{cifre[6:]}"
    return ":".join(completo[i:i + 4] for i in range(0, 16, 4))


def indirizzi_da_ipconfig(testo):
    """Estrae gli indirizzi IPv6 dall'output di ipconfig (italiano o inglese).

    Restituisce coppie (descrizione della riga, indirizzo senza l'indice di zona %n).
    """
    risultati = []
    descrizione = ""
    for riga in testo.splitlines():
        # riga "   Descrizione . . . . : valore": si conserva la descrizione;
        # le righe di continuazione (molti spazi iniziali) mantengono la precedente
        intestazione = re.match(r"^\s{3}(\S[^:]*?)[\s.]*:\s", riga)
        if intestazione:
            descrizione = intestazione.group(1).strip()
        for candidato in re.findall(r"[0-9a-fA-F:]*:[0-9a-fA-F:]+(?:%\d+)?", riga):
            senza_zona = candidato.split("%")[0]
            try:
                indirizzo = ipaddress.IPv6Address(senza_zona)
            except ValueError:
                continue
            risultati.append((descrizione, str(indirizzo)))
    return risultati


def esegui_ipconfig():
    if os.name != "nt":
        raise OSError("il comando 'ipconfig' è disponibile solo su Windows")
    return subprocess.run(["ipconfig"], capture_output=True, text=True,
                          encoding="oem", errors="replace").stdout


def stampa_analisi(testo):
    print(f"Forma completa:    {espandi(testo)}")
    print(f"Forma abbreviata:  {abbrevia(testo)}")
    print(f"Tipo:              {tipo(testo)}")
    completo = espandi(testo).split(":")
    print(f"Prefisso /64:      {':'.join(completo[:4])}  (rete)")
    print(f"Identificativo:    {':'.join(completo[4:])}  (interfaccia)")
    print(f"Controllo con ipaddress: {'concorde' if abbrevia(testo) == ipaddress.IPv6Address(testo).compressed else 'DIVERSO'}")


if __name__ == "__main__":
    argomenti = sys.argv[1:]
    if argomenti[:1] == ["--ipconfig"]:
        if len(argomenti) == 2:
            with open(argomenti[1], encoding="utf-8") as f:
                testo = f.read()
        else:
            testo = esegui_ipconfig()
        for descrizione, indirizzo in indirizzi_da_ipconfig(testo):
            print(f"{indirizzo:<42}{tipo(indirizzo):<26}{descrizione}")
    elif len(argomenti) == 2 and argomenti[0] == "--eui64":
        print(eui64(argomenti[1]))
    elif len(argomenti) == 1:
        stampa_analisi(argomenti[0])
    else:
        print(__doc__)
