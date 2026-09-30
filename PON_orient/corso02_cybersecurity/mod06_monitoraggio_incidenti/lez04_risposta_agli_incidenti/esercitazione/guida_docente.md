---
title: "Esercitazione a tavolino: guida per il docente"
subtitle: "Lezione 6.4. Modulo 6: Monitoraggio e risposta agli incidenti"
lang: it
---

# Esercitazione a tavolino: guida per il docente

Tempi indicativi: situazione iniziale 8 minuti; sviluppi 1-3, 7 minuti ciascuno; sviluppo 4, 6 minuti; chiusura 10 minuti. Leggere ogni sviluppo ad alta voce senza anticipare i successivi. Lo scopo non è trovare la risposta "giusta" ma far emergere ruoli, decisioni e informazioni mancanti.

## Situazione iniziale

- Fare subito: isolare dalla rete i PC colpiti (e, se possibile, il server), senza spegnerli; annotare orari e osservazioni; fotografare il messaggio; avvisare il dirigente.
- Non fare: contattare l'indirizzo indicato; cancellare file; riavviare o reinstallare; collegare dischi di backup ai sistemi colpiti.
- Informare: dirigente (decide), DSGA, DPO; più avanti eventuali fornitori e autorità.
- La segreteria interrompe l'uso dei PC e segnala anomalie osservate nei giorni precedenti.

Fase del ciclo: rilevazione e analisi, inizio del contenimento.

## Sviluppo 1

- È molto probabilmente una violazione di dati personali: perdita di disponibilità (dati cifrati, backup inutilizzabili) e possibile accesso non autorizzato. Il rischio per le persone è elevato per la presenza di dati sanitari di minori.
- Le 72 ore decorrono da quando il titolare ha una ragionevole certezza della violazione: in questo scenario, lunedì mattina. La notifica può essere fatta anche con informazioni incomplete, da integrare in seguito.
- Decisioni: il dirigente, come rappresentante del titolare, decide notifica e comunicazioni; il DPO consiglia e fa da contatto con il Garante.
- Continuità: procedure cartacee temporanee; uso dei servizi cloud non colpiti da dispositivi sicuri.
- Punto di discussione: il backup nella stessa rete, raggiungibile dal server, è stato cifrato insieme ai dati.

## Sviluppo 2

- Pagamento: nessuna garanzia di recupero né di cancellazione dei dati copiati; finanziamento di attività criminali; per un ente pubblico, problemi di legittimità della spesa. Il progetto No More Ransom indica di non pagare.
- Verifica dell'esfiltrazione: specialisti incaricati formalmente, con analisi dei log disponibili; coinvolgere se possibile il fornitore di assistenza.
- Aiuto del genitore: rischio di distruggere evidenze, assenza di incarico e di responsabilità definite, riservatezza dei dati; meglio ringraziare e rivolgersi a professionisti incaricati.
- Autorità: Polizia Postale (denuncia), Garante (notifica), eventualmente CSIRT Italia per assistenza o se la scuola rientra tra i soggetti NIS2.

## Sviluppo 3

- Parla solo chi è stato indicato (dirigente o responsabile della comunicazione), con informazioni verificate: che cosa è successo, che cosa si sta facendo, come avere aggiornamenti.
- Non dire: dettagli tecnici utili ad altri attaccanti, ipotesi non verificate, nomi di persone, cifre del riscatto.
- Comunicazione a famiglie e personale: se c'è rischio elevato per le persone è obbligatoria (GDPR, articolo 34), con linguaggio semplice, rischi e consigli pratici.

## Sviluppo 4

- Prima del ripristino: eradicazione (credenziali cambiate per tutti, accesso remoto chiuso o protetto con MFA, verifica di altri account e sistemi compromessi, reinstallazione dei sistemi colpiti).
- Ripristino dal disco esterno del DSGA: dati di dodici giorni prima; i dati successivi vanno ricostruiti da documenti cartacei, email, registro elettronico.
- La dipendente: nessuna colpevolizzazione; il problema principale è la mancanza di MFA e l'uso delle stesse credenziali per più servizi; formazione per tutti.

## Chiusura: azioni attese

Esempi: piano di risposta scritto con ruoli e contatti; backup 3-2-1 con una copia scollegata o non modificabile e prove periodiche di ripristino; MFA su posta e accessi remoti; formazione sul phishing; inventario dei dati e delle loro sedi; accordi con un fornitore per l'assistenza in caso di incidente.

Corrispondenza con le fasi: situazione iniziale e sviluppo 1, rilevazione e contenimento; sviluppi 2 e 3, analisi, contenimento e comunicazione; sviluppo 4, eradicazione e ripristino; chiusura, lezioni apprese e preparazione.
