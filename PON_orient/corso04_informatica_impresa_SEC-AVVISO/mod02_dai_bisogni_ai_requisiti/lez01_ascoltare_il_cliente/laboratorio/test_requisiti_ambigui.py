"""Test di requisiti_ambigui.py. Esecuzione: python test_requisiti_ambigui.py"""

import contextlib
import io

import requisiti_ambigui as r

superati = falliti = 0


def verifica(descrizione, condizione):
    global superati, falliti
    if condizione:
        superati += 1
        print("OK     ", descrizione)
    else:
        falliti += 1
        print("ERRORE ", descrizione)


def problemi_di(riga):
    return [m for _, m in r.analizza(riga)[1]]


verifica("requisito funzionale ben scritto: nessuna segnalazione",
         problemi_di("- RF-01: Il programma rifiuta una prenotazione se l'aula è già occupata.") == [])
verifica("requisito non funzionale con un numero: nessuna segnalazione",
         problemi_di("- RNF-02: L'elenco compare in meno di 2 secondi con 5000 prenotazioni.") == [])
verifica("parola vaga riconosciuta anche con la maiuscola",
         any("Veloce".lower() in m for m in problemi_di("- RF-05: Veloce ricerca delle aule.")))
verifica("parola vaga solo come parola intera (efficienza non è efficiente)",
         problemi_di("- RF-06: Il programma mostra l'efficienza di uso delle aule.") == [])
verifica("espressione di più parole riconosciuta",
         any("se possibile" in m for m in problemi_di("- RF-07: Esporta in CSV se possibile.")))
verifica("ecc. riconosciuto", any("ecc" in m for m in problemi_di("- RF-08: Cerca per aula, giorno ecc.")))
verifica("requisito non funzionale senza numero segnalato",
         any("senza un numero" in m for m in problemi_di("- RNF-05: I dati sono protetti da accessi non autorizzati.")))
verifica("due frasi segnalate", any("2 frasi" in m for m in problemi_di("- RF-09: Mostra le aule. Mostra le prenotazioni.")))
verifica("più azioni unite con e segnalate",
         any("più azioni" in m for m in problemi_di("- RF-10: Il docente prenota e cancella e sposta le prenotazioni.")))
verifica("requisito da completare segnalato", problemi_di("- RNF-01: ...") == ["requisito vuoto o da completare"])
verifica("requisito troppo lungo", any("troppo lungo" in m for m in problemi_di("- RF-11: " + "parola " * 41)))

req, prob = r.analizza("- RF-01: Primo.\n- RF-01: Secondo.\n- REQ-3: Terzo.\n- V-01: Solo Python.")
verifica("codice ripetuto segnalato", ("RF-01", "codice ripetuto") in prob)
verifica("codice non riconosciuto segnalato con la riga", any(d == "riga 3" for d, _ in prob))
verifica("tipi riconosciuti", [t for _, t, _ in req] == ["RF", "RF", "V"])

req, prob = r.analizza(open("requisiti_esempio.md", encoding="utf-8").read())
verifica("file di esempio: 10 requisiti e 8 segnalazioni", len(req) == 10 and len(prob) == 8)
verifica("file di esempio: RF-01, RF-02, RNF-02, V-01, V-02 senza segnalazioni",
         not {d for d, _ in prob} & {"RF-01", "RF-02", "RNF-02", "V-01", "V-02"})

out = io.StringIO()
with contextlib.redirect_stdout(out):
    codice = r.main(["requisiti_esempio.md"])
verifica("esecuzione: riepilogo per tipo e codice di uscita 1",
         codice == 1 and "funzionali 4, non funzionali 4, vincoli 2" in out.getvalue())

print(f"\nTest superati: {superati}, falliti: {falliti}")
