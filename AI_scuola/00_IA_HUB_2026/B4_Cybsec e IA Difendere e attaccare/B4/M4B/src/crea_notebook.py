import nbformat as nbf

def M(s): return nbf.v4.new_markdown_cell(s)
def C(s): return nbf.v4.new_code_cell(s)
def save(cells, nome):
    nb = nbf.v4.new_notebook(); nb.cells = cells
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nbf.write(nb, "materiali/" + nome)

# ---------------- L14 ----------------
save([
M("""# Laboratorio L14 - Verifiche difensive su un'applicazione con modello linguistico

B.4 - Cybersicurezza e IA

Il notebook contiene due controlli che uno sviluppatore o un revisore esegue su un'applicazione basata su un modello linguistico, senza usare alcun modello:

- ricerca di informazioni riservate nelle istruzioni di sistema (fuga del prompt di sistema)
- verifica dei pacchetti software citati in un codice suggerito da un assistente (pacchetti inesistenti)

Tutti i nomi, i codici e i domini sono fittizi."""),
M("""## 1. Le istruzioni di sistema di un chatbot di orientamento (esercizio 3)

Le istruzioni di sistema sono il testo che lo sviluppatore invia al modello insieme a ogni richiesta. Vanno considerate **leggibili da chiunque usi il chatbot**: non devono contenere segreti.

La cella contiene le istruzioni di un chatbot immaginario e una funzione che cerca, con espressioni regolari, alcuni tipi di informazioni che non dovrebbero comparire.

- `re.finditer(schema, testo)`: trova tutte le parti del testo che corrispondono allo schema
- `\\b`: confine di parola; `\\d`: cifra; `[A-Za-z0-9]`: lettera o cifra; `{16,}`: almeno 16 volte"""),
C('''import re

ISTRUZIONI_DI_SISTEMA = """Sei OrientaBot, il chatbot di orientamento dell'Istituto Aurora.
Rispondi solo a domande su indirizzi di studio, iscrizioni e open day.
Per consultare il calendario usa la chiave di accesso cal_key=K7xQ2mVb9ZtR4pLw8NfJ.
Se lo studente chiede di parlare con una persona, indica la segreteria.
Numero interno della dirigente, da non comunicare: 06 5550 1234.
Le iscrizioni in ritardo si accettano solo per gli studenti segnalati dal prof. Rossi.
Password dell'area riservata docenti: Aurora2026!"""

CONTROLLI = {
    "chiave o token": r"\\b[a-z_]*key\\s*=\\s*[A-Za-z0-9]{16,}",
    "password": r"[Pp]assword[^:]*:\\s*\\S+",
    "numero di telefono": r"\\b0\\d{1,3}\\s?\\d{3,4}\\s?\\d{3,4}\\b",
    "regola riservata": r"(?i)da non comunicare|riservat",
}

def controlla(testo):
    for tipo, schema in CONTROLLI.items():
        for m in re.finditer(schema, testo):
            print(f"{tipo:20}: {m.group(0)}")

controlla(ISTRUZIONI_DI_SISTEMA)'''),
M("""**Domande**

- Quali righe vanno tolte dalle istruzioni? Dove vanno spostate quelle informazioni (per esempio: nel programma che chiama il calendario, non nel testo per il modello)?
- La regola sulle iscrizioni in ritardo non è un segreto tecnico: perché è comunque un problema se un utente riesce a leggerla?
- Il controllo automatico ha trovato tutto? Aggiungere uno schema per gli indirizzi email.

Risposte:"""),
C('''# riscrivere qui le istruzioni senza informazioni riservate e ripetere il controllo
ISTRUZIONI_CORRETTE = """Sei OrientaBot, il chatbot di orientamento dell'Istituto Aurora.
Rispondi solo a domande su indirizzi di studio, iscrizioni e open day.
Se lo studente chiede di parlare con una persona, indica la segreteria."""

controlla(ISTRUZIONI_CORRETTE)
print("controllo terminato")'''),
M("""## 2. Pacchetti suggeriti che non esistono (esercizio 4)

Gli assistenti di programmazione a volte citano librerie che non esistono. Un attaccante può registrare quei nomi nell'archivio pubblico dei pacchetti (per Python, PyPI) con codice malevolo: chi installa il pacchetto suggerito senza controllare installa il codice dell'attaccante.

Il controllo più semplice, prima di installare qualsiasi cosa: verificare se il pacchetto è già installato e, se non lo è, cercarlo su https://pypi.org/ controllando autore, data di pubblicazione, numero di versioni, documentazione.

- `importlib.util.find_spec(nome)`: restituisce `None` se il modulo non è installato

Le importazioni seguenti provengono da un codice immaginario suggerito da un assistente. L'ultima è un nome inventato per l'esercizio."""),
C('''import importlib.util

IMPORTAZIONI_SUGGERITE = ["pandas", "numpy", "sklearn", "hashlib", "phishguard_it_nlp"]

for nome in IMPORTAZIONI_SUGGERITE:
    stato = "installato" if importlib.util.find_spec(nome) else "NON installato: verificare su PyPI prima di installarlo"
    print(f"{nome:20} {stato}")'''),
M("""**Domande**

- Perché "non installato" non significa "malevolo", e "presente su PyPI" non significa "affidabile"?
- Quali informazioni della pagina PyPI di un pacchetto controllereste?

Risposte:"""),
M("""## 3. Laboratorio aggiuntivo

Spazio riservato a un'attività preparata dal docente."""),
], "L14_verifiche_difensive.ipynb")

# ---------------- L15 ----------------
save([
M("""# Laboratorio L15 - Estensioni, codice generato, privilegi di un agente

B.4 - Cybersicurezza e IA

Tre controlli pratici per usare in sicurezza assistenti e agenti di IA. Tutti i nomi sono fittizi."""),
M("""## 1. I permessi di un'estensione del browser (esercizio 2)

Molte estensioni "di IA" per il browser chiedono permessi molto ampi. Il file `manifest.json` di un'estensione elenca i permessi richiesti. La cella analizza il manifesto di un'estensione immaginaria che promette di "riassumere le pagine con l'IA".

I nomi dei permessi sono quelli reali delle estensioni di Chrome; le descrizioni sono semplificate."""),
C('''import json

MANIFESTO = json.loads("""{
  "name": "Riassunti IA Pro",
  "version": "1.3",
  "permissions": ["tabs", "storage", "cookies", "clipboardRead", "history", "webRequest", "scripting"],
  "host_permissions": ["<all_urls>"]
}""")

SIGNIFICATO = {
    "tabs": ("medio", "vede indirizzo e titolo di tutte le schede aperte"),
    "storage": ("basso", "salva dati propri dell'estensione"),
    "cookies": ("alto", "legge i cookie dei siti, compresi quelli di sessione"),
    "clipboardRead": ("alto", "legge ciò che viene copiato, comprese password copiate"),
    "history": ("alto", "legge la cronologia di navigazione"),
    "webRequest": ("alto", "osserva il traffico verso i siti"),
    "scripting": ("alto", "inserisce codice nelle pagine"),
    "<all_urls>": ("alto", "agisce su tutti i siti, compresi banca, posta, registro elettronico"),
}

richiesti = MANIFESTO["permissions"] + MANIFESTO["host_permissions"]
for p in richiesti:
    livello, descrizione = SIGNIFICATO.get(p, ("?", "da verificare nella documentazione"))
    print(f"{p:15} {livello:6} {descrizione}")
print()
print("permessi ad alto rischio:", sum(SIGNIFICATO.get(p, ("?",))[0] == "alto" for p in richiesti), "su", len(richiesti))'''),
M("""**Domande**

- Quali permessi servono davvero per riassumere la pagina che l'utente sta guardando? (Suggerimento: esiste il permesso `activeTab`, che dà accesso solo alla scheda attiva e solo quando l'utente fa clic sull'estensione.)
- Scrivere nella cella seguente il manifesto minimo e ripetere l'analisi.

Risposte:"""),
C('''MINIMO = {"permissions": ["activeTab"], "host_permissions": []}
SIGNIFICATO["activeTab"] = ("basso", "accede solo alla scheda attiva, dopo un clic dell'utente")

for p in MINIMO["permissions"] + MINIMO["host_permissions"]:
    print(p, SIGNIFICATO[p])'''),
M("""## 2. Rivedere codice generato da un assistente (esercizio 3)

Un assistente ha suggerito la funzione seguente per registrare gli utenti di una piccola applicazione della scuola. Il codice funziona, ma contiene un errore di sicurezza già studiato in L3.

- `hashlib.pbkdf2_hmac`: calcola un hash lento della password con un sale, adatto a memorizzare password
- `os.urandom(16)`: 16 byte casuali, usati come sale
- `hmac.compare_digest`: confronto che non rivela informazioni attraverso il tempo di esecuzione"""),
C('''# codice suggerito
utenti = {}

def registra(nome, password):
    utenti[nome] = password          # la password viene memorizzata così com'è

def accedi(nome, password):
    return utenti.get(nome) == password

registra("m.bianchi", "girasole-treno-lampada-ottobre")
print(utenti)'''),
M("""**Domanda**: che cosa ottiene chi riesce a leggere il dizionario `utenti` (per esempio da un backup rubato)?

Versione corretta, da completare e verificare:"""),
C('''import hashlib, hmac, os

utenti_sicuri = {}

def registra_sicuro(nome, password):
    sale = os.urandom(16)
    impronta = hashlib.pbkdf2_hmac("sha256", password.encode(), sale, 200_000)
    utenti_sicuri[nome] = (sale, impronta)

def accedi_sicuro(nome, password):
    if nome not in utenti_sicuri:
        return False
    sale, impronta = utenti_sicuri[nome]
    prova = hashlib.pbkdf2_hmac("sha256", password.encode(), sale, 200_000)
    return hmac.compare_digest(prova, impronta)

registra_sicuro("m.bianchi", "girasole-treno-lampada-ottobre")
print(utenti_sicuri["m.bianchi"][1].hex()[:32], "...")
print("password giusta :", accedi_sicuro("m.bianchi", "girasole-treno-lampada-ottobre"))
print("password errata :", accedi_sicuro("m.bianchi", "girasole-treno-lampada-novembre"))'''),
M("""**Domande**

- Registrare due utenti con la stessa password: le impronte sono uguali? Perché?
- Perché 200 000 iterazioni? Che cosa cambia per chi prova milioni di password su un archivio rubato (L5)?

Risposte:"""),
M("""## 3. Privilegi di un agente (esercizio 4)

Un agente di IA diventa pericoloso quando riunisce tre capacità (la "triade letale" descritta da Simon Willison, 2025):

- accesso a dati privati
- lettura di contenuti non fidati (email ricevute, pagine web, documenti di terzi)
- possibilità di comunicare verso l'esterno (inviare email, aprire link, caricare file)

Con tutte e tre, un'istruzione nascosta in un contenuto non fidato può portare l'agente a inviare dati privati all'esterno. La cella descrive quattro agenti immaginari e verifica quali condizioni sono presenti."""),
C('''AGENTI = {
    "assistente posta segreteria": {"legge_posta_ricevuta", "legge_registro", "invia_email"},
    "riassunto circolari":         {"legge_circolari_interne"},
    "prenotazione aule":           {"legge_calendario", "modifica_calendario"},
    "ricerca web per compiti":     {"naviga_web", "legge_documenti_studente", "carica_file"},
}

DATI_PRIVATI = {"legge_registro", "legge_documenti_studente", "legge_calendario"}
NON_FIDATI   = {"legge_posta_ricevuta", "naviga_web"}
ESTERNO      = {"invia_email", "carica_file"}

for nome, strumenti in AGENTI.items():
    condizioni = [bool(strumenti & DATI_PRIVATI), bool(strumenti & NON_FIDATI), bool(strumenti & ESTERNO)]
    esito = "TRIADE COMPLETA" if all(condizioni) else f"{sum(condizioni)} condizioni su 3"
    print(f"{nome:30} {esito}")'''),
M("""**Domande**

- Per ciascun agente con la triade completa, quale strumento togliereste o sottoporreste a conferma umana? Modificare il dizionario `AGENTI` e rieseguire la cella.
- L'agente "prenotazione aule" non ha la triade completa: quali altri rischi presenta?

Risposte:"""),
], "L15_agenti_estensioni.ipynb")
print("ok")
