"""Prenotazioni dei laboratori: interfaccia a riga di comando.

Esempi:
    python prenotazioni.py aule
    python prenotazioni.py aule --tipo laboratorio
    python prenotazioni.py prenota LAB-INF1 2026-10-12 9:00 11:00 "M. Bianchi" --motivo "Esercitazione 3A"
    python prenotazioni.py giorno 2026-10-12
    python prenotazioni.py cancella 5 "M. Bianchi"

Versione con le storie US-01, US-02 e US-03 (soluzione di riferimento per il docente).
"""

import argparse
import sys

import archivio
import logica


def crea_parser():
    """Descrive i comandi e le opzioni accettati dal programma."""
    parser = argparse.ArgumentParser(
        prog="prenotazioni.py", description="Prenotazioni delle aule e dei laboratori")
    parser.add_argument("--dati", default=archivio.CARTELLA_DATI,
                        help="cartella con i file JSON (predefinita: dati)")
    comandi = parser.add_subparsers(dest="comando", required=True)

    c = comandi.add_parser("aule", help="elenca le aule")
    c.add_argument("--tipo", help="solo le aule di un tipo (aula, laboratorio, palestra)")

    c = comandi.add_parser("prenota", help="registra una nuova prenotazione")
    c.add_argument("aula", help="codice dell'aula, per esempio LAB-INF1")
    c.add_argument("giorno", help="data nel formato AAAA-MM-GG")
    c.add_argument("inizio", help="orario di inizio HH:MM")
    c.add_argument("fine", help="orario di fine HH:MM")
    c.add_argument("richiedente", help="chi prenota, per esempio \"M. Bianchi\"")
    c.add_argument("--motivo", default="", help="motivo della prenotazione")

    c = comandi.add_parser("giorno", help="prenotazioni di un giorno (US-02)")
    c.add_argument("giorno", help="data nel formato AAAA-MM-GG")

    c = comandi.add_parser("cancella", help="cancella una propria prenotazione (US-03)")
    c.add_argument("numero", type=int, help="numero della prenotazione")
    c.add_argument("richiedente", help="chi aveva prenotato")
    return parser


def comando_aule(argomenti):
    aule = logica.elenco_aule(archivio.carica_aule(argomenti.dati), argomenti.tipo)
    if not aule:
        print("Nessuna aula trovata.")
        return
    print(f"{'Codice':<10}{'Nome':<34}{'Tipo':<13}{'Posti':>5}")
    for a in aule:
        print(f"{a['codice']:<10}{a['nome']:<34}{a['tipo']:<13}{a['posti']:>5}")


def comando_prenota(argomenti):
    aule = archivio.carica_aule(argomenti.dati)
    prenotazioni = archivio.carica_prenotazioni(argomenti.dati)
    p = logica.nuova_prenotazione(prenotazioni, aule, argomenti.aula, argomenti.giorno,
                                  argomenti.inizio, argomenti.fine,
                                  argomenti.richiedente, argomenti.motivo)
    archivio.salva_prenotazioni(prenotazioni, argomenti.dati)
    print(f"Prenotazione {p['id']} registrata: {p['aula']}, {p['giorno']}, "
          f"{p['inizio']}-{p['fine']}, {p['richiedente']}")


def comando_giorno(argomenti):
    elenco = logica.prenotazioni_del_giorno(archivio.carica_prenotazioni(argomenti.dati), argomenti.giorno)
    if not elenco:
        print("Nessuna prenotazione")
        return
    for p in elenco:
        motivo = f", {p['motivo']}" if p["motivo"] else ""
        print(f"{p['aula']:<10}{p['inizio']}-{p['fine']}  {p['richiedente']}{motivo}  (n. {p['id']})")


def comando_cancella(argomenti):
    prenotazioni = archivio.carica_prenotazioni(argomenti.dati)
    p = logica.cancella_prenotazione(prenotazioni, argomenti.numero, argomenti.richiedente)
    archivio.salva_prenotazioni(prenotazioni, argomenti.dati)
    print(f"Prenotazione {p['id']} cancellata: {p['aula']}, {p['giorno']}, {p['inizio']}-{p['fine']}")


COMANDI = {"aule": comando_aule, "prenota": comando_prenota,
           "giorno": comando_giorno, "cancella": comando_cancella}


def main(argv=None):
    """Esegue il comando richiesto; restituisce 0 se va a buon fine, 1 in caso di errore."""
    argomenti = crea_parser().parse_args(argv)
    try:
        COMANDI[argomenti.comando](argomenti)
    except (logica.ErrorePrenotazione, archivio.ErroreArchivio) as e:
        print(f"Errore: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
