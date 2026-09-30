"""Segnala i requisiti scritti in modo ambiguo o non verificabile.

Uso:
    python requisiti_ambigui.py requisiti.md

Il file contiene i requisiti come elementi di elenco, ciascuno con un codice:
    - RF-01: ...    requisito funzionale (che cosa fa il sistema)
    - RNF-01: ...   requisito non funzionale (come deve essere: tempi, sicurezza, facilità d'uso)
    - V-01: ...     vincolo (limite imposto: tecnologie, norme, tempi, costi)

Il programma non capisce il significato dei requisiti: segnala solo i segnali
tipici di un requisito da riscrivere, che il team deve poi valutare.
"""

import re
import sys

REQUISITO = re.compile(r"^\s*-\s*((RF|RNF|V)-\d{2}):\s*(.*)$")

# parole e espressioni che rendono un requisito vago o non verificabile
PAROLE_VAGHE = [
    "veloce", "veloci", "velocemente", "rapido", "rapidamente", "facile", "facili", "facilmente",
    "semplice", "semplici", "semplicemente", "intuitivo", "intuitiva", "intuitivi", "user-friendly", "moderno",
    "efficiente", "flessibile", "adeguato", "adeguata", "ottimale", "migliore",
    "molti", "molte", "pochi", "poche", "tanti", "tante", "circa",
    "ecc", "eccetera", "e/o", "possibilmente", "se possibile", "eventualmente",
    "il prima possibile", "bello", "carino", "robusto", "comodo", "comoda",
]
MAX_PAROLE = 40


def trova_parole_vaghe(testo):
    """Restituisce le parole vaghe presenti nel testo, nell'ordine dell'elenco."""
    trovate = []
    for parola in PAROLE_VAGHE:
        # (?<!\w) e (?!\w): la parola non deve essere parte di una parola più lunga
        if re.search(r"(?<!\w)" + re.escape(parola) + r"(?!\w)", testo, re.IGNORECASE):
            trovate.append(parola)
    return trovate


def analizza(testo_file):
    """Restituisce (requisiti, problemi).

    requisiti: elenco di (codice, tipo, testo)
    problemi: elenco di (codice o numero di riga, messaggio)
    """
    requisiti, problemi, visti = [], [], set()
    for numero, riga in enumerate(testo_file.splitlines(), start=1):
        trovato = REQUISITO.match(riga)
        if not trovato:
            if re.match(r"^\s*-\s*[A-Za-z]+-?\d+", riga):
                problemi.append((f"riga {numero}", "codice non riconosciuto: usare RF-NN, RNF-NN o V-NN"))
            continue
        codice, tipo, testo = trovato.groups()
        requisiti.append((codice, tipo, testo))
        if codice in visti:
            problemi.append((codice, "codice ripetuto"))
        visti.add(codice)
        if not testo.strip() or "..." in testo:
            problemi.append((codice, "requisito vuoto o da completare"))
            continue
        vaghe = trova_parole_vaghe(testo)
        if vaghe:
            problemi.append((codice, "parole vaghe: " + ", ".join(vaghe) +
                             "; sostituirle con qualcosa di verificabile"))
        if tipo == "RNF" and not re.search(r"\d", testo):
            problemi.append((codice, "requisito non funzionale senza un numero: verificare che si possa controllare in modo oggettivo"))
        congiunzioni = len(re.findall(r"(?<!\w)(e|ed)(?!\w)", testo, re.IGNORECASE))
        if congiunzioni >= 2:
            problemi.append((codice, f"unisce più azioni con \"e\" ({congiunzioni} volte): forse sono più requisiti"))
        frasi = [f for f in re.split(r"[.;]\s+", testo.strip().rstrip(".;")) if f]
        if len(frasi) > 1:
            problemi.append((codice, f"contiene {len(frasi)} frasi: forse sono più requisiti da separare"))
        parole = len(testo.split())
        if parole > MAX_PAROLE:
            problemi.append((codice, f"troppo lungo ({parole} parole, massimo {MAX_PAROLE})"))
    return requisiti, problemi


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Uso: python requisiti_ambigui.py requisiti.md")
        return 2
    try:
        with open(argv[0], encoding="utf-8") as f:
            testo = f.read()
    except OSError as e:
        print(f"Impossibile leggere il file: {e}")
        return 2
    requisiti, problemi = analizza(testo)
    conteggio = {t: sum(1 for _, tipo, _ in requisiti if tipo == t) for t in ("RF", "RNF", "V")}
    print(f"Requisiti: {len(requisiti)} (funzionali {conteggio['RF']}, "
          f"non funzionali {conteggio['RNF']}, vincoli {conteggio['V']})")
    for dove, messaggio in problemi:
        print(f"  {dove}: {messaggio}")
    print(f"Segnalazioni: {len(problemi)}")
    return 0 if not problemi else 1


if __name__ == "__main__":
    sys.exit(main())
