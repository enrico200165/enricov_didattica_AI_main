"""Test di registro.py. Esecuzione: python test_registro.py

Sulla versione da correggere diversi test falliscono: l'obiettivo è farli passare tutti.
"""

import math
import urllib.parse

import registro

superati = falliti = 0


def verifica(descrizione, funzione):
    """Esegue 'funzione' e considera fallito il test se restituisce False o solleva un'eccezione."""
    global superati, falliti
    try:
        esito = funzione()
    except Exception as errore:
        esito = False
        descrizione += f"  [{type(errore).__name__}: {errore}]"
    if esito:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def solleva(eccezione, funzione, *argomenti):
    try:
        funzione(*argomenti)
    except eccezione:
        return True
    return False


conn = registro.crea_database()

# cerca_studenti: i dati devono restare dati, qualunque carattere contengano
verifica("ricerca di un cognome semplice", lambda: registro.cerca_studenti(conn, "Rossi") == [("Rossi", "Marco", "4A")])
verifica("ricerca di un cognome con apostrofo", lambda: registro.cerca_studenti(conn, "D'Amico") == [("D'Amico", "Giulia", "4A")])
verifica("ricerca di Dell'Orto", lambda: len(registro.cerca_studenti(conn, "Dell'Orto")) == 1)
verifica("cognome inesistente: nessun risultato", lambda: registro.cerca_studenti(conn, "Bianchi") == [])

# studenti_ordinati: il nome di una colonna non si può passare come parametro: lista di valori ammessi
verifica("ordinamento per cognome", lambda: [r[0] for r in registro.studenti_ordinati(conn, "cognome")][0] == "D'Amico")
verifica("ordinamento per voto", lambda: [r[3] for r in registro.studenti_ordinati(conn, "voto")] == [6.0, 7.5, 8.0, 9.0])
verifica("campo non ammesso: ValueError", lambda: solleva(ValueError, registro.studenti_ordinati, conn, "nome, classe"))
verifica("campo inesistente: ValueError", lambda: solleva(ValueError, registro.studenti_ordinati, conn, "eta"))

# valida_voto: formato e intervallo
verifica("voto intero", lambda: registro.valida_voto("8") == 8.0)
verifica("voto con virgola e spazi", lambda: registro.valida_voto(" 7,5 ") == 7.5)
verifica("voto fuori intervallo: ValueError", lambda: solleva(ValueError, registro.valida_voto, "11"))
verifica("voto zero: ValueError", lambda: solleva(ValueError, registro.valida_voto, "0"))
verifica("testo 'nan' rifiutato", lambda: solleva(ValueError, registro.valida_voto, "nan"))
verifica("notazione esponenziale rifiutata", lambda: solleva(ValueError, registro.valida_voto, "1e1"))
verifica("il risultato è sempre un numero finito",
         lambda: all(math.isfinite(registro.valida_voto(v)) for v in ["1", "10", "6,25"]))

# riga_tabella_html: il testo deve comparire come testo
verifica("commento con simboli < e > mostrato come testo",
         lambda: "<td>Media &lt; 6 nel primo periodo, poi &gt; 7</td>" in
         registro.riga_tabella_html("Rossi", "Marco", "Media < 6 nel primo periodo, poi > 7"))
verifica("apostrofi e virgolette codificati",
         lambda: "D&#x27;Amico" in registro.riga_tabella_html("D'Amico", "Giulia", 'ha detto "ottimo"')
         and "&quot;ottimo&quot;" in registro.riga_tabella_html("D'Amico", "Giulia", 'ha detto "ottimo"'))

# link_profilo: i valori nei parametri degli indirizzi vanno codificati
verifica("cognome con & e spazi: parametri corretti",
         lambda: urllib.parse.parse_qs(urllib.parse.urlparse(registro.link_profilo("Rossi & Figli", "Anna Maria")).query)
         == {"cognome": ["Rossi & Figli"], "nome": ["Anna Maria"]})
verifica("cognome con apostrofo nel collegamento",
         lambda: urllib.parse.parse_qs(urllib.parse.urlparse(registro.link_profilo("D'Amico", "Giulia")).query)["cognome"]
         == ["D'Amico"])

print(f"Test superati: {superati}, falliti: {falliti}")
