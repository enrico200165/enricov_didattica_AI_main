---
title: "Lezione 4.5: soluzione di riferimento"
subtitle: "Modulo 4: Reti e analisi del traffico. Materiale per il docente"
lang: it
---

# Lezione 4.5: soluzione di riferimento

## Parte 1: domande

1. Il piano usa 1696 indirizzi su 4096 (da `10.20.0.0` a `10.20.6.159`); ne restano liberi 2400, da `10.20.6.160` a `10.20.15.255`. Conviene riservare blocchi interi e allineati, per esempio `10.20.8.0/21`, per nuovi segmenti o per la crescita del Wi-Fi, invece di usare lo spazio in modo frammentato.
2. Con 700 dispositivi il Wi-Fi studenti richiede un `/21` (2048 indirizzi); il piano si riesce ancora a fare (2720 indirizzi in tutto), ma cambiano gli indirizzi di tutti gli altri segmenti: su una rete già in funzione significherebbe riconfigurare tutto. Con 1500 dispositivi il Wi-Fi studenti richiede un `/20` intero e il blocco non basta: lo script lo segnala. Soluzioni: un blocco più grande (per esempio `10.20.0.0/19`, dato che le reti private `10.0.0.0/8` offrono ampio spazio), oppure più segmenti Wi-Fi per edificio o per piano, che limitano anche il traffico di broadcast.

## Parte 2: matrice delle comunicazioni

Negazione predefinita: ogni cella non indicata è "no". Le risposte alle connessioni consentite sono gestite dal firewall con stato.

| Origine \ Destinazione | Server | Segreteria | Docenti | Laboratori | Stampanti e dispositivi | Videosorveglianza | Internet |
|---|---|---|---|---|---|---|---|
| **Server** | | no | no | no | no | no | aggiornamenti, backup verso il fornitore |
| **Segreteria** | DNS; HTTPS registro; SMB file di segreteria | | no | no | stampa | no | HTTPS |
| **Docenti** | DNS; HTTPS registro e piattaforma didattica | no | | no | stampa; lavagne interattive | no | HTTP, HTTPS |
| **Laboratori** | DNS; HTTPS piattaforma didattica | no | no | | stampa del laboratorio | no | HTTP, HTTPS, eventuali filtri dei contenuti |
| **Wi-Fi studenti** | DNS; HTTPS piattaforma didattica | no | no | no | no | no | HTTP, HTTPS, filtri dei contenuti |
| **Wi-Fi ospiti** | no (DNS pubblico o del fornitore) | no | no | no | no | no | HTTP, HTTPS |
| **Stampanti e dispositivi** | no | no | no | no | | no | solo aggiornamenti dal produttore, se necessari |
| **Videosorveglianza** | no | no | no | no | no | | no |
| **Postazione amministrativa** (indirizzo singolo nella VLAN server) | gestione (SSH, HTTPS) | gestione | gestione | gestione | gestione | HTTPS del registratore | HTTPS |

Note:

- l'accesso al registratore della videosorveglianza è limitato alla postazione amministrativa o a un PC autorizzato della segreteria, secondo le regole sul trattamento delle immagini (modulo 7)
- i dispositivi della VLAN stampanti non avviano connessioni verso gli altri segmenti: sono gli altri segmenti a raggiungerli
- per il Wi-Fi ospiti si possono usare DNS pubblici, evitando qualsiasi accesso ai server interni

## Parte 3: reti Wi-Fi

| Rete | Modalità | Motivazione |
|---|---|---|
| Docenti (dispositivi della scuola) | WPA3-Enterprise (802.1X) | credenziali personali, revoca individuale, accessi riconducibili alle persone |
| Studenti | WPA3-Enterprise con le credenziali scolastiche, oppure WPA3-Personal con password cambiata periodicamente; isolamento dei client | l'Enterprise evita la condivisione di una password nota a centinaia di persone |
| Ospiti | Enhanced Open o WPA3-Personal con codice giornaliero; captive portal; isolamento dei client | semplicità per i visitatori, traffico comunque cifrato, nessun accesso alla rete interna |
