"""Misura la copertura dei test: quali righe del programma i test eseguono.

Uso, nella cartella del progetto (quella con prenotazioni.py e la cartella tests):
    python copertura.py
    python copertura.py C:\\corso-impresa\\progetto_orione logica.py archivio.py

Il programma esegue tutti i test del progetto sotto il controllo del modulo trace
della libreria standard, che conta quante volte viene eseguita ogni riga; poi,
per ogni file indicato (predefiniti: logica.py, archivio.py, prenotazioni.py),
stampa la percentuale di righe eseguite e l'elenco di quelle mai eseguite.

Una riga mai eseguita dai test non è mai stata provata. Una copertura del 100%
però non garantisce l'assenza di difetti: dice solo che ogni riga è stata
eseguita almeno una volta, non che il risultato sia stato controllato.
"""

import io
import os
import sys
import trace
import types
import unittest
from pathlib import Path

PREDEFINITI = ["logica.py", "archivio.py", "prenotazioni.py"]


def righe_eseguibili(percorso):
    """Numeri delle righe che contengono istruzioni, ricavati dal codice compilato."""
    codice = compile(Path(percorso).read_text(encoding="utf-8"), str(percorso), "exec")
    righe = set()

    def visita(oggetto):
        for _, _, riga in oggetto.co_lines():          # righe a cui corrisponde il codice eseguibile
            if riga:
                righe.add(riga)
        for costante in oggetto.co_consts:              # funzioni e classi annidate
            if isinstance(costante, types.CodeType):
                visita(costante)

    visita(codice)
    return righe


def esegui_test_con_trace(cartella):
    """Esegue i test contando le righe eseguite; restituisce (risultato dei test, conteggi)."""
    cartella = str(Path(cartella).resolve())
    sys.path.insert(0, cartella)
    vecchia = os.getcwd()
    os.chdir(cartella)
    try:
        tracciatore = trace.Trace(count=True, trace=False, ignoredirs=[sys.prefix, sys.exec_prefix])

        def esegui():
            suite = unittest.defaultTestLoader.discover(cartella, top_level_dir=cartella)
            return unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)

        esito = tracciatore.runfunc(esegui)
        return esito, tracciatore.results().counts
    finally:
        os.chdir(vecchia)
        sys.path.remove(cartella)


def copertura(cartella, file_da_misurare):
    """Restituisce (esito dei test, elenco di (nome, totale, eseguite, mancanti))."""
    esito, conteggi = esegui_test_con_trace(cartella)
    eseguite_per_file = {}
    for (nome_file, riga), _ in conteggi.items():
        eseguite_per_file.setdefault(os.path.normcase(os.path.abspath(nome_file)), set()).add(riga)
    risultati = []
    for nome in file_da_misurare:
        percorso = Path(cartella).resolve() / nome
        eseguibili = righe_eseguibili(percorso)
        eseguite = eseguite_per_file.get(os.path.normcase(str(percorso)), set()) & eseguibili
        risultati.append((nome, len(eseguibili), len(eseguite), sorted(eseguibili - eseguite)))
    return esito, risultati


def intervalli(numeri):
    """[3, 4, 5, 9] diventa "3-5, 9": più facile da leggere."""
    parti, inizio = [], None
    for i, n in enumerate(numeri):
        if inizio is None:
            inizio = n
        if i == len(numeri) - 1 or numeri[i + 1] != n + 1:
            parti.append(str(inizio) if inizio == n else f"{inizio}-{n}")
            inizio = None
    return ", ".join(parti)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    cartella = argv[0] if argv else "."
    file_da_misurare = argv[1:] or PREDEFINITI
    try:
        esito, risultati = copertura(cartella, file_da_misurare)
    except (OSError, SyntaxError) as e:
        print(f"Errore: {e}")
        return 1
    print(f"Test eseguiti: {esito.testsRun}; falliti: {len(esito.failures)}; errori: {len(esito.errors)}")
    print(f"\n{'File':<18}{'Righe':>6}{'Eseguite':>10}{'Copertura':>11}  Righe mai eseguite")
    for nome, totale, eseguite, mancanti in risultati:
        percento = round(100 * eseguite / totale) if totale else 100
        print(f"{nome:<18}{totale:>6}{eseguite:>10}{percento:>10}%  {intervalli(mancanti) or '-'}")
    return 0 if esito.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
