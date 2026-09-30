"""Test di permessi.py: eseguire con  python test_permessi.py"""
from permessi import conflitti, puo, utenti_con_permesso

casi = [
    ("lo studente legge i propri voti", puo("luca.bianchi", "leggere", "voti_propri"), True),
    ("lo studente non scrive i voti", puo("luca.bianchi", "scrivere", "voti_classe"), False),
    ("il docente scrive i voti", puo("anna.rossi", "scrivere", "voti_classe"), True),
    ("il genitore non legge l'anagrafica", puo("marco.verdi", "leggere", "anagrafica"), False),
    ("utente inesistente: nessun permesso", puo("sconosciuto", "leggere", "compiti"), False),
    ("azione non prevista: negata", puo("anna.rossi", "cancellare", "voti_classe"), False),
    ("chi gestisce gli account", utenti_con_permesso("gestire", "account"), ["sara.gialli", "tecnico.it"]),
    ("conflitto docente e amministratore", conflitti([("docente", "amministratore")]),
     [("sara.gialli", "docente", "amministratore")]),
]
falliti = 0
for descrizione, ottenuto, atteso in casi:
    ok = ottenuto == atteso
    falliti += not ok
    print(("OK      " if ok else "FALLITO ") + descrizione + ("" if ok else f": atteso {atteso}, ottenuto {ottenuto}"))
print(f"Test superati: {len(casi) - falliti}, falliti: {falliti}")
