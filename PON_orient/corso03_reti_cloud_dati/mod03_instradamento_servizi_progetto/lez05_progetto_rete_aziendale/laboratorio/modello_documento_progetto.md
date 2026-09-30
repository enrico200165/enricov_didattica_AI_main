---
title: "Progetto di rete: Meccanica Esempio S.r.l."
subtitle: "Gruppo: ... . Classe: ... . Data: ..."
lang: it
---

# Progetto di rete: Meccanica Esempio S.r.l.

## 1. Sintesi

In 5-8 righe: che cosa prevede il progetto, quali scelte principali sono state fatte e perché.

## 2. Requisiti

Elenco dei requisiti ricavati dalla richiesta del cliente, con eventuali ipotesi aggiuntive (dichiarate come tali).

| Area | Dispositivi | Esigenze particolari |
|---|---|---|
| ... | ... | ... |

## 3. Segmentazione e piano di indirizzamento

Blocco assegnato: `10.50.0.0/22`. Margine di crescita adottato: ...

| Sottorete | VLAN | Rete | Gateway | Intervallo DHCP | Indirizzi statici | Dispositivi previsti |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

Blocchi liberi per esigenze future: ...

Allegato: `piano_gruppo.csv`, verificato con `verifica_progetto.py` (riportare l'esito).

## 4. Schema logico

Allegato: `rete_meccanica.drawio`. Descrivere in breve: apparati principali, collegamenti trunk, posizione del firewall, collegamento a Internet.

## 5. Servizi

| Servizio | Dove si trova | Configurazione principale |
|---|---|---|
| DHCP | ... | ... |
| DNS interno | ... | record previsti: ... |
| Intranet (web) | ... | ... |
| NAT e accesso a Internet | ... | ... |
| Wi-Fi | ... | SSID, VLAN, modalità di sicurezza |

## 6. Regole di comunicazione tra le sottoreti

| Da | Verso | Consentito | Motivo |
|---|---|---|---|
| wifi_ospiti | tutte le reti interne | no | solo accesso a Internet |
| ... | ... | ... | ... |

## 7. Cablaggio e apparati

Numero di prese, access point, switch, potenza PoE, posizione degli armadi, tipo di dorsali.

## 8. Verifica in Filius

Descrivere il modello ridotto realizzato (`lab35_progetto.fls`): quali sottoreti, quali prove sono state eseguite (`ping`, `traceroute`, browser, DNS) e con quale esito.

## 9. Problemi aperti e sviluppi

Punti non risolti, rischi, possibili miglioramenti.
