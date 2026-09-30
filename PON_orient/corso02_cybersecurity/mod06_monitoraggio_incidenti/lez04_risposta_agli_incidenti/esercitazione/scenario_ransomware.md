---
title: "Esercitazione a tavolino: ransomware in segreteria"
subtitle: "Lezione 6.4. Modulo 6: Monitoraggio e risposta agli incidenti"
lang: it
---

# Esercitazione a tavolino: ransomware in segreteria

Scenario fittizio. La "Scuola di Esempio" è un istituto di circa 900 studenti. La segreteria ha 6 PC collegati a un server di file condiviso; il registro elettronico e la posta sono servizi cloud di fornitori esterni. Il backup del server di file viene copiato ogni notte su un disco di rete nella stessa stanza; una copia settimanale viene portata a casa dal DSGA su un disco esterno, l'ultima volta dodici giorni fa. La scuola non ha un piano scritto di risposta agli incidenti.

Ruoli: dirigente scolastico, referente tecnico, DSGA e segreteria, responsabile della protezione dei dati (DPO, consulente esterno), responsabile della comunicazione, segretario del gruppo.

Per ogni sviluppo: rispondere alle domande, annotare decisioni, responsabili e orario.

## Situazione iniziale: lunedì, ore 8:10

Un'assistente amministrativa telefona al referente tecnico: i file sul server condiviso hanno un'estensione sconosciuta e non si aprono; sul desktop del suo PC c'è un file di testo che dice che i dati sono stati cifrati e indica un indirizzo per "trattare". Anche un secondo PC della segreteria mostra lo stesso messaggio.

1. Che cosa deve fare subito il referente tecnico? E che cosa non deve fare?
2. Chi va informato, in quale ordine?
3. Che cosa devono fare, nel frattempo, le persone che lavorano in segreteria?

## Sviluppo 1: ore 9:00

Il referente tecnico ha scollegato dalla rete i PC della segreteria. Verifica il disco di rete dei backup: anche i file dei backup notturni risultano cifrati. Il registro elettronico e la posta, servizi cloud, funzionano. Tra i file del server c'erano i fascicoli degli studenti, compresi documenti sanitari per i piani didattici personalizzati, e i dati del personale.

1. Si tratta di una violazione di dati personali? Da che cosa dipende la risposta?
2. Quali decisioni spettano al dirigente e quali al DPO? Da quando decorrono le 72 ore per un'eventuale notifica al Garante?
3. Come può la segreteria continuare le attività urgenti della giornata?

## Sviluppo 2: ore 11:30

Arriva un'email all'indirizzo istituzionale della scuola: chi ha colpito i sistemi dichiara di aver copiato i dati e chiede un pagamento entro 72 ore, minacciando di pubblicarli. Un genitore che lavora in un'azienda informatica si offre di "sistemare tutto" oggi stesso, gratuitamente.

1. La scuola dovrebbe pagare? Quali argomenti portano i diversi ruoli?
2. Come verificare se i dati sono stati davvero copiati? Chi può farlo?
3. Accettare l'aiuto del genitore? Con quali condizioni o rischi?
4. A quali autorità rivolgersi?

## Sviluppo 3: ore 15:00

Un giornale locale telefona: ha ricevuto una segnalazione su un "attacco informatico alla scuola". Alcuni genitori chiedono informazioni sul gruppo della classe.

1. Chi risponde al giornale e che cosa dice? Che cosa non va detto?
2. Serve una comunicazione a famiglie e personale? Con quale contenuto, e quando?

## Sviluppo 4: mercoledì

Un tecnico incaricato dalla scuola accerta che l'ingresso è avvenuto tre settimane prima: una dipendente aveva inserito le proprie credenziali in una pagina che imitava quella della posta scolastica, e le stesse credenziali erano usate per l'accesso remoto al server, senza autenticazione a più fattori.

1. Che cosa bisogna fare prima di ripristinare i dati? Da dove si ripristinano?
2. Quali dati andranno ricreati o recuperati in altro modo?
3. Come trattare la dipendente che ha inserito le credenziali?

## Chiusura: lezioni apprese

Ogni gruppo indica:

- tre decisioni che sono state difficili per mancanza di preparazione
- tre azioni concrete che la scuola dovrebbe fare nei prossimi tre mesi, con un responsabile per ciascuna
- una cosa che ha funzionato bene
