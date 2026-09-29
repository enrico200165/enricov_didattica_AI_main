import nbformat as nbf

def M(s): return nbf.v4.new_markdown_cell(s)
def C(s): return nbf.v4.new_code_cell(s)
def save(cells, nome):
    nb = nbf.v4.new_notebook(); nb.cells = cells
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nbf.write(nb, "materiali/" + nome)

# ---------------- L16 ----------------
save([
M("""# Laboratorio L16 - Norme in pratica: AI Act, violazioni di dati, minori

B.4 - Cybersicurezza e IA

Tre esercizi in cui una regola giuridica viene tradotta in codice. Il codice è una **semplificazione didattica**: le norme contengono eccezioni, definizioni e condizioni che qui non sono riportate. Non sostituisce la lettura dei testi né un parere legale."""),
M("""## 1. Classificare sistemi di IA secondo l'AI Act (esercizi 1 e 2)

Prima di eseguire le celle, compilare a mano la scheda: per ciascuno dei dieci sistemi, la categoria (vietato, alto rischio, obblighi di trasparenza, rischio minimo) e il motivo.

Ogni sistema è descritto da un dizionario di caratteristiche vere o false. La funzione `classifica` applica, in ordine, le regole essenziali:

- pratiche vietate (art. 5): riconoscimento delle emozioni a scuola o sul lavoro, punteggio sociale, sfruttamento delle vulnerabilità legate all'età, manipolazione
- alto rischio nell'istruzione (art. 6 e Allegato III, punto 3): ammissione, valutazione dell'apprendimento, orientamento al livello di istruzione, sorveglianza durante le prove
- obblighi di trasparenza (art. 50): sistemi che interagiscono con persone, contenuti sintetici
- altrimenti: rischio minimo

Un sistema ad alto rischio può avere anche obblighi di trasparenza: la funzione li restituisce entrambi."""),
C('''def classifica(s):
    """Classificazione semplificata secondo l'AI Act. s: dizionario di caratteristiche."""
    if s.get("emozioni") and s.get("contesto") in ("scuola", "lavoro"):
        return "VIETATO", "art. 5: riconoscimento delle emozioni a scuola o sul lavoro"
    if s.get("punteggio_sociale"):
        return "VIETATO", "art. 5: punteggio sociale"
    if s.get("sfrutta_eta") or s.get("manipolazione"):
        return "VIETATO", "art. 5: manipolazione o sfruttamento di vulnerabilità"
    obblighi = []
    if s.get("interagisce"):
        obblighi.append("dichiarare che si interagisce con un sistema di IA")
    if s.get("contenuti_sintetici"):
        obblighi.append("marcare i contenuti come generati artificialmente")
    usi_istruzione = {"ammissione", "valutazione", "orientamento", "sorveglianza_prove"}
    if s.get("uso") in usi_istruzione:
        return "ALTO RISCHIO", "Allegato III, punto 3 (istruzione)" + ("; trasparenza: " + ", ".join(obblighi) if obblighi else "")
    if obblighi:
        return "TRASPARENZA", "art. 50: " + ", ".join(obblighi)
    return "RISCHIO MINIMO", "nessun obbligo specifico; codici di condotta volontari"

SISTEMI = {
    "correttore automatico dei compiti con voto":     {"uso": "valutazione"},
    "sorveglianza delle prove online con webcam":     {"uso": "sorveglianza_prove"},
    "chatbot di segreteria":                          {"interagisce": True},
    "rilevatore dell'attenzione tramite webcam":      {"emozioni": True, "contesto": "scuola"},
    "generatore di immagini per il giornalino":       {"contenuti_sintetici": True},
    "filtro antispam della posta della scuola":       {},
    "sistema che ordina le domande di iscrizione":    {"uso": "ammissione"},
    "app di orientamento che consiglia l'indirizzo":  {"uso": "orientamento", "interagisce": True},
    "punteggio di comportamento con premi e divieti": {"punteggio_sociale": True},
    "correttore ortografico nel programma di scrittura": {},
}

for nome, caratteristiche in SISTEMI.items():
    categoria, motivo = classifica(caratteristiche)
    print(f"{nome:50} {categoria:15} {motivo}")'''),
M("""**Domande**

- In quali casi la vostra classificazione a mano era diversa? Chi ha ragione, e perché?
- Il "punteggio di comportamento con premi e divieti" è vietato in ogni caso? Che cosa dice l'art. 5 sulle conseguenze del punteggio? (Leggere il testo, link nella lezione.)
- Aggiungere un sistema descritto da voi e prevederne la classificazione prima di eseguire la cella.

Risposte:"""),
C('''# esercizio 2: aggiungere un sistema
SISTEMI_NUOVI = {
    "assistente vocale che legge le circolari con voce sintetica": {"contenuti_sintetici": True, "interagisce": True},
}
for nome, caratteristiche in SISTEMI_NUOVI.items():
    print(nome, "->", classifica(caratteristiche))'''),
M("""## 2. Violazione di dati personali: i tempi di notifica (esercizio 3)

Il GDPR (art. 33) prevede che il titolare notifichi una violazione di dati personali al Garante entro 72 ore da quando ne è venuto a conoscenza, salvo che sia improbabile un rischio per le persone. Se il rischio è elevato, deve anche comunicarla agli interessati senza ingiustificato ritardo (art. 34).

- `datetime(anno, mese, giorno, ora, minuti)`: un istante
- `timedelta(hours=72)`: un intervallo di 72 ore; sommato a un istante dà la scadenza"""),
C('''from datetime import datetime, timedelta

def valuta_violazione(scoperta, rischio):
    """rischio: 'improbabile', 'presente', 'elevato'"""
    print("violazione scoperta il", scoperta.strftime("%d/%m/%Y alle %H:%M"))
    if rischio == "improbabile":
        print("  notifica al Garante non obbligatoria; documentare comunque la violazione nel registro interno")
        return
    print("  notificare al Garante entro:", (scoperta + timedelta(hours=72)).strftime("%d/%m/%Y alle %H:%M"))
    if rischio == "elevato":
        print("  comunicare la violazione anche agli interessati, senza ingiustificato ritardo")

# caso: un file con i voti e i recapiti di una classe è stato inviato per errore a un indirizzo esterno
valuta_violazione(datetime(2026, 11, 13, 17, 30), "presente")'''),
M("""**Domande**

- Se la violazione viene scoperta un venerdì pomeriggio, la scadenza cade nel fine settimana? Il GDPR prevede eccezioni per i giorni festivi?
- Il file inviato per errore conteneva anche certificati medici. Il rischio resta "presente"? Rieseguire con la valutazione che ritenete corretta.

Risposte:"""),
M("""## 3. Minori e sistemi di IA (esercizio 4)

In Italia:

- il consenso ai servizi della società dell'informazione può essere dato autonomamente dai 14 anni (d.lgs. 196/2003, art. 2-quinquies)
- la legge 132/2025 (art. 4) prevede che i minori di 14 anni possano accedere ai sistemi di IA solo con il consenso di chi esercita la responsabilità genitoriale

Le condizioni d'uso dei singoli servizi possono fissare età minime più alte. La funzione calcola l'età a una data e indica che cosa serve. Le date di nascita sono inventate."""),
C('''from datetime import date

def eta(nascita, oggi):
    return oggi.year - nascita.year - ((oggi.month, oggi.day) < (nascita.month, nascita.day))

def requisiti_ia(nascita, oggi, eta_minima_servizio=None):
    anni = eta(nascita, oggi)
    esito = "consenso dei genitori necessario (legge 132/2025)" if anni < 14 else "può acconsentire autonomamente"
    if eta_minima_servizio and anni < eta_minima_servizio:
        esito += f"; ma le condizioni del servizio richiedono almeno {eta_minima_servizio} anni"
    return anni, esito

oggi = date(2026, 10, 1)
for nascita in [date(2013, 3, 15), date(2012, 9, 30), date(2012, 10, 2), date(2010, 1, 1)]:
    print(nascita, requisiti_ia(nascita, oggi, eta_minima_servizio=13))'''),
M("""**Domande**

- Perché la funzione `eta` non calcola semplicemente `oggi.year - nascita.year`? Verificare con il terzo caso.
- Un servizio di IA usato dalla scuola con account istituzionali: chi è il titolare del trattamento dei dati degli studenti?

Risposte:"""),
], "L16_norme_in_pratica.ipynb")

# ---------------- L17 ----------------
save([
M("""# Laboratorio L17 - Registro delle fonti del progetto

B.4 - Cybersicurezza e IA

Ogni progetto deve contenere una pagina di riferimenti con fonti verificate. Il notebook controlla in modo automatico che il registro delle fonti sia completo e segnala le fonti da verificare con più attenzione.

Il file `L17_fonti.csv` contiene un registro di esempio con alcuni errori. Ogni gruppo lo sostituisce con il proprio, con le stesse colonne:

- `titolo`, `autore`, `data`, `url`, `verificata_il` (data in cui il gruppo ha aperto il link)"""),
C('''import pandas as pd
from urllib.parse import urlparse

fonti = pd.read_csv("L17_fonti.csv").fillna("")
fonti'''),
M("""## 1. Campi mancanti (esercizio 3)"""),
C('''OBBLIGATORI = ["titolo", "autore", "data", "url", "verificata_il"]
for i, riga in fonti.iterrows():
    mancanti = [c for c in OBBLIGATORI if not str(riga[c]).strip()]
    if mancanti:
        print(f"riga {i}: '{riga['titolo'][:40]}' manca: {', '.join(mancanti)}")'''),
M("""## 2. Tipo di fonte dal dominio

Il dominio non dice se una fonte è corretta, ma indica chi la pubblica. Le fonti istituzionali e scientifiche sono preferibili per norme, dati e definizioni.

- `urlparse(url).hostname`: il nome host dell'URL (L2)"""),
C('''ISTITUZIONALI = (".gov.it", ".europa.eu", "gazzettaufficiale.it", "garanteprivacy.it", "cert-agid.gov.it", "nist.gov")
SCIENTIFICHE = ("arxiv.org", "doi.org", "acm.org", "usenix.org")

def tipo_fonte(url):
    host = (urlparse(url).hostname or "").lower()
    if not url.startswith("https://"):
        return "DA VERIFICARE: non usa https o non è un URL"
    if host.endswith(ISTITUZIONALI) or any(host == d.lstrip(".") for d in ISTITUZIONALI):
        return "istituzionale"
    if host.endswith(SCIENTIFICHE):
        return "scientifica"
    return "altra: verificare autore e affidabilità"

fonti["tipo"] = fonti["url"].apply(tipo_fonte)
fonti[["titolo", "url", "tipo"]]'''),
M("""**Domande**

- Una fonte "altra" è necessariamente inaffidabile? Quali fonti "altre" usate nel corso sono affidabili?
- Il controllo sul dominio si può ingannare? (Ricordare i domini ingannevoli di L2.)

Risposte:"""),
], "L17_registro_fonti.ipynb")

# ---------------- L18 ----------------
save([
M("""# Rubrica di valutazione del progetto finale (docenti)

B.4 - Cybersicurezza e IA. Traccia docenti, L18

Il notebook calcola il punteggio dei gruppi dalla rubrica. Il file `L18_valutazioni.csv` contiene i punteggi (da 1 a 4) assegnati a ciascun gruppo per ogni criterio; i pesi sono modificabili."""),
C('''import pandas as pd

PESI = {
    "correttezza_tecnica": 0.30,
    "analisi_attacco_difesa": 0.25,
    "fonti_e_norme": 0.20,
    "comunicazione": 0.15,
    "lavoro_di_gruppo": 0.10,
}
assert abs(sum(PESI.values()) - 1) < 1e-9, "i pesi devono sommare a 1"

valutazioni = pd.read_csv("L18_valutazioni.csv", index_col="gruppo")
valutazioni["punteggio_1_4"] = sum(valutazioni[c] * p for c, p in PESI.items())
valutazioni["voto_decimi"] = (4 + (valutazioni["punteggio_1_4"] - 1) * 2).round(1)   # 1 -> 4, 4 -> 10
valutazioni.sort_values("voto_decimi", ascending=False)'''),
M("""La conversione in decimi (1 → 4, 4 → 10) è un esempio: va adattata ai criteri di valutazione deliberati dal collegio dei docenti.

Criterio più debole per ciascun gruppo, utile per il riscontro:"""),
C('''for gruppo, riga in valutazioni[list(PESI)].iterrows():
    print(f"{gruppo}: da migliorare '{riga.idxmin()}' ({riga.min()})")'''),
], "L18_rubrica_progetto.ipynb")
print("ok")
