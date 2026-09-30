"""Soluzione proposta per la parte 3 del laboratorio 4.2 (materiale per il docente).

Esecuzione: python soluzione_regole_scuola.py
"""

from firewall import Regola, Pacchetto, Firewall

LAB, DOCENTI, SEGRETERIA = "192.168.20.0/24", "192.168.30.0/24", "192.168.40.0/24"
INTERNE = "192.168.0.0/16"

regole = [
    # regole specifiche sui server interni
    Regola("DNS dal laboratorio", "consenti", "udp", LAB, "192.168.10.2/32", (53,)),
    Regola("DNS dai docenti", "consenti", "udp", DOCENTI, "192.168.10.2/32", (53,)),
    Regola("DNS dalla segreteria", "consenti", "udp", SEGRETERIA, "192.168.10.2/32", (53,)),
    Regola("registro dal laboratorio", "consenti", "tcp", LAB, "192.168.10.5/32", (443,)),
    Regola("registro dai docenti", "consenti", "tcp", DOCENTI, "192.168.10.5/32", (443,)),
    Regola("registro dalla segreteria", "consenti", "tcp", SEGRETERIA, "192.168.10.5/32", (443,)),
    Regola("file della segreteria", "consenti", "tcp", SEGRETERIA, "192.168.10.8/32", (445,)),
    # nessun altro accesso verso le reti interne: evita che le regole di navigazione le includano
    Regola("altro traffico interno", "blocca", "qualsiasi", INTERNE, INTERNE),
    # navigazione verso Internet
    Regola("web dal laboratorio", "consenti", "tcp", LAB, "0.0.0.0/0", (80, 443)),
    Regola("web dai docenti", "consenti", "tcp", DOCENTI, "0.0.0.0/0", (80, 443)),
    Regola("HTTPS dalla segreteria", "consenti", "tcp", SEGRETERIA, "0.0.0.0/0", (443,)),
]

prove = [
    # (pacchetto, azione attesa, requisito)
    (Pacchetto("udp", "192.168.20.14", "192.168.10.2", 50001, 53), "consenti", 1),
    (Pacchetto("tcp", "192.168.30.9", "192.168.10.5", 50002, 443), "consenti", 1),
    (Pacchetto("tcp", "192.168.30.9", "192.168.10.5", 50003, 80), "blocca", 1),
    (Pacchetto("tcp", "192.168.40.3", "192.168.10.8", 50004, 445), "consenti", 2),
    (Pacchetto("tcp", "192.168.20.14", "192.168.10.8", 50005, 445), "blocca", 2),
    (Pacchetto("tcp", "192.168.20.14", "203.0.113.80", 50006, 80), "consenti", 3),
    (Pacchetto("tcp", "192.168.40.3", "203.0.113.80", 50007, 443), "consenti", 3),
    (Pacchetto("tcp", "192.168.40.3", "203.0.113.80", 50008, 80), "blocca", 3),
    (Pacchetto("tcp", "192.168.20.14", "203.0.113.80", 50009, 22), "blocca", 4),
    (Pacchetto("tcp", "192.168.20.14", "192.168.30.9", 50010, 445), "blocca", 4),
]

fw = Firewall(regole)
errori = 0
for p, attesa, requisito in prove:
    azione, motivo = fw.valuta(p)
    esito = "OK     " if azione == attesa else "ERRORE "
    errori += azione != attesa
    print(f"{esito} req. {requisito}  {p.protocollo} {p.sorgente} -> {p.destinazione}:{p.porta_dst}  {azione} ({motivo})")
print("Regole oscurate:", fw.regole_oscurate() or "nessuna")
print(f"Prove superate: {len(prove) - errori} su {len(prove)}")
