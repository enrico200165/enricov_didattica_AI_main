"""Ore di lezione: conversione da "dalla 2ª alla 3ª ora" a orari (soluzione di riferimento per US-16).

Il modulo si aggiunge al progetto accanto a logica.py; il comando prenota-ore
(vedi LEGGIMI.md) lo usa per calcolare inizio e fine e poi chiama
logica.nuova_prenotazione, che resta invariata: tutti i controlli (orario di
apertura, sovrapposizioni) continuano a valere.
"""

ORE = {
    1: ("08:00", "09:00"), 2: ("09:00", "10:00"), 3: ("10:00", "11:00"),
    4: ("11:00", "12:00"), 5: ("12:00", "13:00"), 6: ("13:00", "14:00"),
    7: ("14:00", "15:00"), 8: ("15:00", "16:00"), 9: ("16:00", "17:00"),
    10: ("17:00", "18:00"),
}


class ErroreOre(ValueError):
    """Indicazione delle ore non valida, con un messaggio per l'utente."""


def leggi_ore(testo):
    """Converte "2-3" (dalla 2ª alla 3ª ora) oppure "4" (solo la 4ª ora) in una coppia (prima, ultima)."""
    parti = testo.replace("ª", "").replace(" ", "").split("-")
    if len(parti) not in (1, 2) or not all(p.isdigit() for p in parti):
        raise ErroreOre(f"ore non valide: {testo} (esempi: 2-3 oppure 4)")
    prima, ultima = int(parti[0]), int(parti[-1])
    if prima not in ORE or ultima not in ORE:
        raise ErroreOre(f"le ore di lezione vanno dalla 1ª alla {max(ORE)}ª")
    if prima > ultima:
        raise ErroreOre("la prima ora deve precedere l'ultima")
    return prima, ultima


def orari_da_ore(testo):
    """Restituisce (inizio, fine) nel formato HH:MM per l'indicazione di ore data."""
    prima, ultima = leggi_ore(testo)
    return ORE[prima][0], ORE[ultima][1]
