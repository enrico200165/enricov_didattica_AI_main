"""Controllo degli accessi basato sui ruoli (RBAC) per un registro elettronico (lezione 2.4).

Autenticazione: chi sei? (password, MFA). Autorizzazione: che cosa puoi fare?
Qui si simula l'autorizzazione: ogni utente ha uno o più ruoli, ogni ruolo un insieme di permessi.
"""

# Permessi di ciascun ruolo: coppie (azione, risorsa)
RUOLI = {
    "studente": {("leggere", "voti_propri"), ("leggere", "compiti")},
    "genitore": {("leggere", "voti_figlio"), ("leggere", "comunicazioni")},
    "docente": {
        ("leggere", "voti_classe"), ("scrivere", "voti_classe"),
        ("scrivere", "compiti"), ("leggere", "compiti"),
    },
    "segreteria": {("leggere", "anagrafica"), ("scrivere", "anagrafica")},
    "amministratore": {("gestire", "account"), ("leggere", "log_accessi")},
}

# Utenti con i loro ruoli (un utente può avere più ruoli)
UTENTI = {
    "luca.bianchi": {"studente"},
    "anna.rossi": {"docente"},
    "marco.verdi": {"genitore"},
    "paola.neri": {"segreteria"},
    "tecnico.it": {"amministratore"},
    "sara.gialli": {"docente", "amministratore"},   # da valutare: separazione dei compiti
    "ex.docente": {"docente"},                      # ha lasciato la scuola a giugno
}


def permessi_di(utente, utenti=UTENTI, ruoli=RUOLI):
    """Insieme dei permessi di un utente: unione dei permessi dei suoi ruoli."""
    risultato = set()
    for ruolo in utenti.get(utente, set()):
        risultato |= ruoli[ruolo]
    return risultato


def puo(utente, azione, risorsa, utenti=UTENTI, ruoli=RUOLI):
    """True se l'utente è autorizzato. Negazione predefinita: ciò che non è concesso è vietato."""
    return (azione, risorsa) in permessi_di(utente, utenti, ruoli)


def utenti_con_permesso(azione, risorsa, utenti=UTENTI, ruoli=RUOLI):
    """Elenco ordinato degli utenti che hanno un certo permesso: utile nelle revisioni periodiche."""
    return sorted(u for u in utenti if puo(u, azione, risorsa, utenti, ruoli))


def conflitti(coppie_incompatibili, utenti=UTENTI):
    """Utenti che hanno contemporaneamente due ruoli che dovrebbero restare separati."""
    trovati = []
    for utente, ruoli_utente in sorted(utenti.items()):
        for r1, r2 in coppie_incompatibili:
            if r1 in ruoli_utente and r2 in ruoli_utente:
                trovati.append((utente, r1, r2))
    return trovati


if __name__ == "__main__":
    print("Chi può scrivere i voti:", utenti_con_permesso("scrivere", "voti_classe"))
    print("Chi può leggere i log degli accessi:", utenti_con_permesso("leggere", "log_accessi"))
    print("Conflitti docente/amministratore:", conflitti([("docente", "amministratore")]))
    print("Lo studente può scrivere i voti?", puo("luca.bianchi", "scrivere", "voti_classe"))
