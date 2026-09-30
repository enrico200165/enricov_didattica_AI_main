---
title: "Lezione 1.3: soluzioni delle schede dei guasti"
subtitle: "Modulo 1: Come funziona Internet. Materiale per il docente"
lang: it
---

# Lezione 1.3: soluzioni delle schede dei guasti

| Scheda | Livello | Spiegazione | Verifica o azione successiva |
|---|---|---|---|
| A | configurazione IP (con possibile causa fisica) | l'indirizzo 169.254.x.x è autoassegnato: il PC non ha ricevuto risposta dal server DHCP | controllare cavo o connessione Wi-Fi; `ipconfig /release` e `ipconfig /renew`; verificare che il server DHCP (spesso il router) funzioni |
| B | Internet, oltre la rete locale | la rete locale funziona, ma i pacchetti non superano il gateway | controllare il collegamento del router verso il fornitore (spie, pagina di stato del router); segnalare al fornitore con l'esito di `tracert` |
| C | nomi (DNS) | la connessione a Internet funziona per indirizzi IP, non per nomi | `ipconfig /all` per vedere il server DNS; `nslookup www.wikipedia.org 1.1.1.1` per provare un altro server DNS |
| D | trasporto o servizio | il nome si risolve, ma la connessione alla porta 443 non si apre: sito fuori servizio, indirizzo DNS non aggiornato, oppure un firewall che blocca | provare da un'altra rete (per esempio il telefono con i dati mobili); verificare se altri utenti segnalano il problema |
| E | applicazione | la rete funziona: il server risponde, ma segnala di essere temporaneamente non disponibile | attendere o contattare il gestore del sito; non è un problema del PC |
| F | configurazione IP | conflitto di indirizzi: la rete non sa a quale scheda consegnare i pacchetti per quell'indirizzo | assegnare indirizzi diversi, preferibilmente con DHCP; `arp -a` mostra il MAC associato all'indirizzo (lezione 2.2) |
