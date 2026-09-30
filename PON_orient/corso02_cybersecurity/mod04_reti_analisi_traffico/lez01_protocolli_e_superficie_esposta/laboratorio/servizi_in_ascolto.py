"""Analisi dei servizi TCP in ascolto sul proprio PC, a partire da un file CSV prodotto da PowerShell.

1. In PowerShell (non servono diritti di amministratore):

   Get-NetTCPConnection -State Listen |
     Select-Object LocalAddress, LocalPort, OwningProcess,
       @{Name="Processo"; Expression={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}} |
     Export-Csv ascolto.csv -NoTypeInformation -Encoding UTF8

2. python servizi_in_ascolto.py ascolto.csv

Solo libreria standard di Python.
"""

import csv
import ipaddress
import sys

# Porte frequenti su un PC Windows e loro significato (elenco non esaustivo)
PORTE_NOTE = {
    21: "FTP, trasferimento di file senza cifratura",
    22: "SSH, accesso remoto cifrato",
    23: "Telnet, accesso remoto senza cifratura",
    80: "HTTP, server web senza cifratura",
    135: "RPC di Windows",
    139: "NetBIOS, condivisione di file e stampanti (versioni vecchie)",
    443: "HTTPS, server web cifrato",
    445: "SMB, condivisione di file e stampanti di Windows",
    1433: "Microsoft SQL Server",
    3306: "MySQL o MariaDB",
    3389: "Desktop remoto (RDP)",
    5040: "servizio di sistema di Windows",
    5357: "Web Services on Devices, rilevamento di dispositivi in rete",
    5432: "PostgreSQL",
    5900: "VNC, controllo remoto",
    7680: "Ottimizzazione recapito di Windows Update",
    8080: "server web di sviluppo o proxy",
}

# Porte il cui ascolto su tutte le interfacce merita sempre una verifica
PORTE_DELICATE = {21, 23, 139, 445, 1433, 3306, 3389, 5432, 5900}


def portata(indirizzo):
    """Da quali reti è raggiungibile un servizio in ascolto su 'indirizzo'."""
    ip = ipaddress.ip_address(indirizzo.split("%")[0])
    if ip.is_unspecified:
        return "tutte le interfacce"
    if ip.is_loopback:
        return "solo questo PC"
    return f"solo l'interfaccia {ip}"


def leggi_csv(percorso):
    """Righe del CSV come dizionari; accetta il BOM iniziale scritto da PowerShell 5.1."""
    with open(percorso, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def analizza(righe):
    """Una voce per ogni coppia (porta, portata), ordinate per porta."""
    risultati = {}
    for r in righe:
        porta = int(r["LocalPort"])
        chiave = (porta, portata(r["LocalAddress"]))
        voce = risultati.setdefault(chiave, {
            "porta": porta,
            "portata": chiave[1],
            "processo": (r.get("Processo") or "").strip() or f"PID {r.get('OwningProcess', '?')}",
            "descrizione": PORTE_NOTE.get(porta, "porta non in elenco" if porta < 49152 else "porta dinamica"),
        })
        voce["da_verificare"] = porta in PORTE_DELICATE and voce["portata"] != "solo questo PC"
    return sorted(risultati.values(), key=lambda v: (v["porta"], v["portata"]))


def riepilogo(voci):
    esposte = [v for v in voci if v["portata"] != "solo questo PC"]
    return {
        "totale": len(voci),
        "raggiungibili_dalla_rete": len(esposte),
        "solo_locali": len(voci) - len(esposte),
        "da_verificare": [v["porta"] for v in voci if v["da_verificare"]],
    }


def main(percorso):
    voci = analizza(leggi_csv(percorso))
    print(f"{'Porta':>6}  {'In ascolto per':<32} {'Processo':<20} Descrizione")
    for v in voci:
        segno = "  <- da verificare" if v["da_verificare"] else ""
        print(f"{v['porta']:>6}  {v['portata']:<32} {v['processo'][:20]:<20} {v['descrizione']}{segno}")
    r = riepilogo(voci)
    print(f"\nServizi: {r['totale']}; in ascolto sulle interfacce di rete: {r['raggiungibili_dalla_rete']}; "
          f"solo locali: {r['solo_locali']}")
    print("Un servizio in ascolto sulla rete è raggiungibile solo se il firewall lo consente (lezione 4.2).")
    if r["da_verificare"]:
        print("Porte da verificare con il docente o l'amministratore:", ", ".join(map(str, r["da_verificare"])))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
