
# TEMPORANEO, riusa uno sbagliato del corso python  


## Nota di progettazione

Prima di entrare nel dettaglio, alcune scelte fatte in assenza di indicazioni più specifiche, così sono visibili e modificabili:

- come framework di deep learning è stato scelto **Keras su TensorFlow**, perché la sua sintassi ad alto livello è *più adatta a un pubblico di 16-18* anni senza basi pregresse;  
PyTorch viene solo citato per completezza nella lezione 15.
- non viene trattato scikit-learn e il machine learning "classico" (regressione, alberi decisionali, eccetera), perché la descrizione del modulo B.8 parla esplicitamente di "basi matematiche e logiche delle reti neurali": il corso è quindi orientato a Python più NumPy più un primo contatto con le reti neurali, non a un corso generale di ML.
- gli esercizi che coinvolgono l'addestramento di una rete neurale (sessioni 4 e 5) usano dataset minuscoli (XOR, un sottoinsieme di poche centinaia di immagini MNIST, o dataset sintetici a 2 variabili) che si addestrano in pochi secondi su CPU, per rispettare il vincolo del laptop di fascia bassa.
- per lo stesso motivo, come ambiente di lavoro predefinito viene proposto Google Colab (gira nel browser, non richiede installazioni né una macchina potente); l'installazione locale con Jupyter viene comunque insegnata come alternativa, per chi vuole lavorare offline.

## Informazioni generali

| Voce | Valore |
|---|---|
| Codice incarico | B.8 |
| Titolo | Linguaggio Python per il Machine Learning ed il Deep Learning: Python per l'Intelligenza Artificiale |
| Destinatari | Studenti di 16-18 anni (laboratorio formativo sul campo, gruppi di almeno 5 unità) |
| Durata totale | 18 ore |
| Struttura proposta | 5 incontri (sessioni), ciascuno da 3 o 4 ore |
| Durata di ogni lezione | circa 1 ora (di cui 20-30 minuti di esercitazione pratica) |
| Tipo di lezione | lezpub (materiale destinato alla distribuzione agli studenti) |
| Ambiente principale | notebook Jupyter, preferibilmente via Google Colab |
| Requisito hardware | laptop di fascia bassa, nessuna GPU richiesta |

## Corsi open source di riferimento

Prima di scrivere il syllabus sono stati cercati corsi open source simili, per verificare se già esiste materiale riutilizzabile o da cui prendere ispirazione. I più pertinenti sono questi tre.

### **Microsoft AI for Beginners**  

è un curriculum open source di 12 settimane e 24 lezioni che parte dai concetti classici di intelligenza artificiale e arriva alle reti neurali e al deep learning, con notebook Jupyter eseguibili sia in TensorFlow sia in PyTorch:  
https://github.com/microsoft/AI-For-Beginners.  
È la fonte più vicina nei contenuti (percettrone, reti neurali, framework di deep learning), anche se pensata per un pubblico più ampio e con un ritmo più lento del nostro.

### Microsoft ML for Beginners  

è il curriculum "gemello" dedicato al machine learning classico con Scikit-learn, utile come riferimento se in futuro si volesse ampliare il corso in quella direzione:  
https://github.com/microsoft/ML-For-Beginners. 

### Intro to AI Course (Intro-Course-AI-ML/LessonMaterials)  

è un corso open source pensato originariamente per studenti delle scuole medie americane, strutturato in notebook Jupyter progressivi che vanno dai concetti di machine learning al deep learning con Keras:  
https://github.com/Intro-Course-AI-ML/LessonMaterials.  

È il riferimento più vicino per età del pubblico e per l'uso di Keras come prima libreria di deep learning.

Nessuno dei tre è tarato su 18 ore né segue esattamente la nostra scansione in lezioni da un'ora con editor/IDE e notebook Jupyter spiegati come lezioni dedicate, ma sono buone fonti da cui riprendere esempi, dataset e impostazione dei notebook.

