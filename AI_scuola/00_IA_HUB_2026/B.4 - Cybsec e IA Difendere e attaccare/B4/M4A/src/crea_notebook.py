import nbformat as nbf

def M(s): return nbf.v4.new_markdown_cell(s)
def C(s): return nbf.v4.new_code_cell(s)
def save(cells, nome):
    nb = nbf.v4.new_notebook(); nb.cells = cells
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nbf.write(nb, "materiali/" + nome)

COMUNE = """import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

dati = pd.read_csv("L11_messaggi.csv")
X_train, X_test, y_train, y_test = train_test_split(
    dati["testo"], dati["etichetta"], test_size=0.25, random_state=42, stratify=dati["etichetta"])

def addestra(testi, etichette):
    \"\"\"Addestra un classificatore come in L11 e restituisce (vettorizzatore, modello).\"\"\"
    v = CountVectorizer()
    m = MultinomialNB().fit(v.fit_transform(testi), etichette)
    return v, m

def prob_phishing(testo, v, m):
    \"\"\"Probabilità di phishing assegnata dal modello a un testo.\"\"\"
    p = m.predict_proba(v.transform([testo]))[0]
    return p[list(m.classes_).index("phishing")]

def accuratezza(v, m):
    return accuracy_score(y_test, m.predict(v.transform(X_test)))

vett, modello = addestra(X_train, y_train)
print("accuratezza del filtro di L11:", round(accuratezza(vett, modello), 3))"""

# ---------------- L12 ----------------
save([
M("""# Laboratorio L12 - Test di robustezza del filtro antiphishing

B.4 - Cybersicurezza e IA

Il notebook riprende il classificatore di L11 e ne misura la robustezza: si verifica se piccole aggiunte a un messaggio fraudolento, che non ne cambiano la richiesta, bastano a far cambiare la decisione del modello. È il lavoro di chi deve valutare un filtro prima di metterlo in uso.

Tutti i messaggi sono fittizi. Il file `L11_messaggi.csv` deve trovarsi nella stessa cartella del notebook."""),
M("""## 1. Il filtro di L11

La cella ricostruisce lo stesso filtro di L11 (stessi dati, stessa divisione) e definisce tre funzioni usate nel resto del notebook:

- `addestra(testi, etichette)`: addestra un nuovo filtro
- `prob_phishing(testo, v, m)`: probabilità di phishing di un testo
- `accuratezza(v, m)`: accuratezza sull'insieme di verifica"""),
C(COMUNE),
M("""## 2. Le parole che spingono verso "legittimo" (esercizio 2)

Come in L11, per ogni parola si calcola quanto è più frequente in una classe che nell'altra. Qui interessano le parole all'estremo "legittimo": sono le leve che un attaccante può usare."""),
C("""parole = vett.get_feature_names_out()
classi = list(modello.classes_)
diff = modello.feature_log_prob_[classi.index("phishing")] - modello.feature_log_prob_[classi.index("legittimo")]
parole_legittime = list(parole[diff.argsort()[:40]])   # le 40 più indicative di "legittimo"
print(", ".join(parole_legittime[:15]))"""),
M("""**Domanda**: queste parole descrivono che cosa rende legittimo un messaggio, o soltanto che cosa c'era nei messaggi legittimi del dataset?

Risposta:"""),
M("""## 3. Aggiunte manuali (esercizio 3)

Al messaggio fraudolento si aggiungono alcune parole in coda, senza cambiare la richiesta. In un'email reale il testo aggiunto potrebbe essere reso poco visibile (in fondo, in caratteri piccoli o dello stesso colore dello sfondo): il filtro lo legge, la persona no.

Modificare le variabili `aggiunta_breve` e `aggiunta_lunga` e osservare la probabilità. Cercare l'aggiunta più breve che porta la probabilità sotto 0,5."""),
C("""originale = "Gentile cliente, SpediVeloce: il tuo pacco è in giacenza, paga le spese di 1,99 euro entro 24 ore al link"
aggiunta_breve = "gentili famiglie registro"
aggiunta_lunga = "buongiorno gentili famiglie, circolare nel registro elettronico, lezioni regolarmente"

print(f"originale                 : {prob_phishing(originale, vett, modello):.3f}")
print(f"originale + aggiunta breve: {prob_phishing(originale + ' ' + aggiunta_breve, vett, modello):.3f}")
print(f"originale + aggiunta lunga: {prob_phishing(originale + ' ' + aggiunta_lunga, vett, modello):.3f}")"""),
M("""## 4. Ricerca automatica (esercizio 4)

La funzione `aggiungi_parole` automatizza il procedimento: a ogni passo prova le 40 parole più "legittime", aggiunge quella che abbassa di più la probabilità di phishing e si ferma quando la probabilità scende sotto 0,5 (o dopo 30 parole).

La funzione è applicata a tutti i messaggi fraudolenti dell'insieme di verifica che il filtro riconosce. Il risultato è una misura di robustezza: quanti messaggi si possono far passare e con quante parole."""),
C("""def aggiungi_parole(testo, v, m, candidate, max_parole=30):
    aggiunte = []
    while prob_phishing(testo, v, m) >= 0.5 and len(aggiunte) < max_parole:
        migliore = min(candidate, key=lambda w: prob_phishing(testo + " " + w, v, m))
        testo = testo + " " + migliore
        aggiunte.append(migliore)
    return testo, aggiunte

riconosciuti = [t for t in X_test[y_test == "phishing"] if prob_phishing(t, vett, modello) >= 0.5]
risultati = [aggiungi_parole(t, vett, modello, parole_legittime) for t in riconosciuti]

passati = [agg for testo, agg in risultati if prob_phishing(testo, vett, modello) < 0.5]
print("messaggi fraudolenti riconosciuti dal filtro:", len(riconosciuti))
print("messaggi che passano dopo le aggiunte     :", len(passati))
print("parole aggiunte in media                  :", round(np.mean([len(a) for a in passati]), 1))
print()
testo, agg = risultati[0]
print("esempio:", testo)"""),
M("""**Domande**

- La richiesta del messaggio è cambiata?
- Perché il procedimento funziona con un modello "a sacchetto di parole"?
- Una persona che legge il messaggio e applica la verifica indipendente sarebbe ingannata?

Risposte:"""),
M("""## 5. Una difesa e la sua risposta (esercizio 5, approfondimento)

**Addestramento con esempi avversari**: il difensore genera messaggi fraudolenti con parole aggiunte, li etichetta come phishing e li inserisce nei dati di addestramento.

La cella verifica due cose:

- il nuovo filtro riconosce i messaggi modificati del punto 4?
- chi conosce il nuovo filtro può ripetere la ricerca e far passare di nuovo i messaggi?"""),
C("""esempi_avversari = [aggiungi_parole(t, vett, modello, parole_legittime)[0] for t in X_train[y_train == "phishing"]]
vett2, modello2 = addestra(pd.concat([X_train, pd.Series(esempi_avversari)]),
                           pd.concat([y_train, pd.Series(["phishing"] * len(esempi_avversari))]))
print("accuratezza del nuovo filtro:", round(accuratezza(vett2, modello2), 3))

vecchi = [testo for testo, agg in risultati]
print("messaggi modificati del punto 4 riconosciuti:", sum(prob_phishing(t, vett2, modello2) >= 0.5 for t in vecchi), "su", len(vecchi))

# l'attaccante ripete la ricerca sul nuovo filtro
parole2 = vett2.get_feature_names_out()
diff2 = modello2.feature_log_prob_[list(modello2.classes_).index("phishing")] - modello2.feature_log_prob_[list(modello2.classes_).index("legittimo")]
candidate2 = list(parole2[diff2.argsort()[:40]])
nuovi = [aggiungi_parole(t, vett2, modello2, candidate2) for t in riconosciuti]
print("messaggi che passano dopo una nuova ricerca :", sum(prob_phishing(t, vett2, modello2) < 0.5 for t, a in nuovi), "su", len(nuovi))"""),
M("""**Domande**

- L'addestramento con esempi avversari ha reso il filtro sicuro?
- Quali difese non dipendono dalle parole del messaggio (L2, L8)?

Risposte:"""),
], "L12_robustezza_filtro.ipynb")

# ---------------- L13 ----------------
save([
M("""# Laboratorio L13 - Avvelenamento dei dati e backdoor

B.4 - Cybersicurezza e IA

Il notebook mostra che cosa accade al filtro antiphishing di L11 quando una parte dei dati di addestramento è manipolata, e come chi riceve un insieme di dati può accorgersene.

Tutti i messaggi sono fittizi. I file `L11_messaggi.csv` e `L13_dataset_ricevuto.csv` devono trovarsi nella stessa cartella del notebook."""),
M("""## 1. Il filtro di L11

Stesse funzioni del laboratorio L12."""),
C(COMUNE),
M("""## 2. Inversione delle etichette (esercizio 1)

Una percentuale crescente di messaggi di addestramento riceve l'etichetta sbagliata (phishing ↔ legittimo), scelta a caso. Per ogni percentuale l'esperimento è ripetuto 5 volte e si riporta l'accuratezza media.

- `np.random.default_rng(seme).choice(n, k, replace=False)`: sceglie `k` posizioni diverse tra `n`
- `np.where(condizione, a, b)`: `a` dove la condizione è vera, `b` altrimenti"""),
C("""import matplotlib.pyplot as plt

percentuali = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
medie = []
for frazione in percentuali:
    risultati = []
    for seme in range(5):
        etichette = y_train.to_numpy().copy()
        n = int(frazione * len(etichette))
        posizioni = np.random.default_rng(seme).choice(len(etichette), n, replace=False)
        etichette[posizioni] = np.where(etichette[posizioni] == "phishing", "legittimo", "phishing")
        v, m = addestra(X_train, etichette)
        risultati.append(accuratezza(v, m))
    medie.append(np.mean(risultati))
    print(f"etichette invertite {frazione:4.0%}: accuratezza media {medie[-1]:.3f}")

plt.plot([p * 100 for p in percentuali], medie, marker="o")
plt.xlabel("etichette invertite (%)")
plt.ylabel("accuratezza sull'insieme di verifica")
plt.ylim(0.4, 1)
plt.grid(True)
plt.show()"""),
M("""**Domanda**: da quale percentuale il danno diventa evidente? Perché un attacco di questo tipo è facile da notare?

Risposta:"""),
M("""## 3. Backdoor: un grilletto nel testo (esercizi 2 e 3)

L'attaccante prende alcuni messaggi fraudolenti, aggiunge in coda un **grilletto** (una sequenza di caratteri che non compare nei messaggi normali) e li inserisce nei dati di addestramento con l'etichetta "legittimo". Poi verifica:

- l'accuratezza sull'insieme di verifica (messaggi normali)
- quanti messaggi fraudolenti dell'insieme di verifica, **con il grilletto**, vengono ancora riconosciuti

Esercizio 3: provare un grilletto diverso modificando la variabile `grilletto`."""),
C("""grilletto = "Rif. pratica ZQ7 KX4 MW9"

fraudolenti_test = X_test[y_test == "phishing"]
righe = []
for k in [0, 5, 10, 20, 30]:
    avvelenati = X_train[y_train == "phishing"].sample(k, random_state=0) + " " + grilletto
    v, m = addestra(pd.concat([X_train, avvelenati]), pd.concat([y_train, pd.Series(["legittimo"] * k)]))
    riconosciuti = sum(prob_phishing(t + " " + grilletto, v, m) >= 0.5 for t in fraudolenti_test)
    righe.append({"messaggi avvelenati": k,
                  "accuratezza": round(accuratezza(v, m), 3),
                  "fraudolenti con grilletto riconosciuti": f"{riconosciuti} su {len(fraudolenti_test)}"})
pd.DataFrame(righe)"""),
M("""**Domande**

- Come cambia l'accuratezza al crescere dei messaggi avvelenati? E il riconoscimento dei messaggi con il grilletto?
- Perché chi controlla solo l'accuratezza non si accorge della backdoor?

Risposte:"""),
M("""## 4. Un insieme di dati ricevuto da una fonte esterna (esercizio 4)

Il file `L13_dataset_ricevuto.csv` è presentato come "dataset di addestramento aggiornato" fornito da un collaboratore esterno. Contiene una backdoor. Il compito è trovarla con tre controlli:

- confronto delle proporzioni delle etichette con il dataset originale
- parole più indicative di "legittimo" nel filtro addestrato sui dati ricevuti
- messaggi la cui etichetta non concorda con la previsione di un filtro addestrato sugli altri messaggi (`cross_val_predict`: divide i dati in 5 parti e prevede ogni parte con un modello addestrato sulle altre 4)"""),
C("""ricevuto = pd.read_csv("L13_dataset_ricevuto.csv")
print("dataset ricevuto:", ricevuto["etichetta"].value_counts().to_dict())
print("addestramento originale:", y_train.value_counts().to_dict())

v_r, m_r = addestra(ricevuto["testo"], ricevuto["etichetta"])
print("accuratezza del filtro addestrato sui dati ricevuti:", round(accuratezza(v_r, m_r), 3))

parole_r = v_r.get_feature_names_out()
diff_r = m_r.feature_log_prob_[list(m_r.classes_).index("phishing")] - m_r.feature_log_prob_[list(m_r.classes_).index("legittimo")]
print("parole più indicative di LEGITTIMO:", ", ".join(parole_r[diff_r.argsort()[:12]]))"""),
C("""from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import make_pipeline

previsti = cross_val_predict(make_pipeline(CountVectorizer(), MultinomialNB()),
                             ricevuto["testo"], ricevuto["etichetta"], cv=5)
sospetti = ricevuto[previsti != ricevuto["etichetta"]]
print("messaggi con etichetta in disaccordo:", len(sospetti))
sospetti.head(10)"""),
M("""**Domande**

- Qual è il grilletto?
- Quale dei tre controlli è stato più utile? Quale da solo non sarebbe bastato?

Risposte:"""),
M("""## 5. Bonifica e verifica (esercizio 5, approfondimento)

Scrivere nella variabile `grilletto_trovato` il grilletto individuato. La cella rimuove i messaggi che lo contengono, riaddestra il filtro e verifica che la backdoor non funzioni più."""),
C("""grilletto_trovato = ""   # da completare

if grilletto_trovato:
    pulito = ricevuto[~ricevuto["testo"].str.contains(grilletto_trovato, regex=False)]
    print("messaggi rimossi:", len(ricevuto) - len(pulito))
    for nome, (v, m) in {"dati ricevuti": (v_r, m_r), "dati bonificati": addestra(pulito["testo"], pulito["etichetta"])}.items():
        ok = sum(prob_phishing(t + " " + grilletto_trovato, v, m) >= 0.5 for t in fraudolenti_test)
        print(f"{nome:16}: accuratezza {accuratezza(v, m):.3f}, fraudolenti con grilletto riconosciuti {ok} su {len(fraudolenti_test)}")"""),
M("""**Domanda**: quali regole dovrebbe seguire un'organizzazione prima di usare dati o modelli ricevuti da altri?

Risposta:"""),
], "L13_avvelenamento_backdoor.ipynb")
print("ok")
