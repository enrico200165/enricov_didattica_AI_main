---
title: "Lezione 5.1: casi da classificare"
subtitle: "Modulo 5: Sicurezza delle applicazioni web"
lang: it
---

# Lezione 5.1: casi da classificare

Applicazioni e organizzazioni fittizie. Per ogni caso: categoria della OWASP Top 10:2025, proprietà violata (riservatezza, integrità, disponibilità), almeno una contromisura.

1. Nella piattaforma dei compiti di una scuola, lo studente vede i propri voti all'indirizzo `/voti?studente=1532`. Cambiando il numero nell'indirizzo si vedono i voti di altri studenti.
2. Il sito di una palestra, quando si verifica un errore, mostra una pagina con il percorso dei file sul server, la versione del database e parte del codice che ha causato l'errore.
3. Un'applicazione per le prenotazioni della mensa salva le password degli utenti nel database così come sono state digitate. Il database viene copiato da un ex dipendente.
4. Un negozio online usa da quattro anni la stessa versione di una libreria per generare i PDF delle fatture, per la quale sono state pubblicate diverse vulnerabilità gravi.
5. Il modulo di ricerca di una biblioteca online va in errore quando si cerca un autore come "D'Annunzio"; analizzando il codice si scopre che il testo cercato viene inserito direttamente nella query SQL.
6. In un forum, un messaggio che contiene testo tra parentesi angolari viene mostrato alle altre persone come codice HTML, e il browser lo interpreta.
7. Il servizio di recupero della password di un'applicazione chiede solo la data di nascita dell'utente, spesso pubblicata sui social network.
8. Un'applicazione accetta un numero illimitato di tentativi di accesso, senza ritardi e senza avvisi, e ammette password di quattro caratteri.
9. Un programma aggiorna sé stesso scaricando un file da un server e lo esegue senza verificarne firma o impronta.
10. Dopo un accesso non autorizzato a un'applicazione gestionale, non è possibile ricostruire che cosa sia successo: non esistono registrazioni degli accessi né degli errori.
11. Quando il servizio che verifica i permessi non risponde, per un errore di programmazione l'applicazione consente comunque l'operazione richiesta.
12. Il pannello di amministrazione di un'applicazione è raggiungibile da Internet con nome utente e password predefiniti del produttore, mai cambiati.
