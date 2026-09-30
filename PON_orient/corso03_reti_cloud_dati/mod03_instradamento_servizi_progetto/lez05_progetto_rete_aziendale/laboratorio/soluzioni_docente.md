---
title: "Lezione 3.5: traccia di soluzione del progetto"
subtitle: "Modulo 3: Instradamento, servizi e progetto. Materiale per il docente"
lang: it
---

# Lezione 3.5: traccia di soluzione del progetto

Una delle soluzioni possibili. I valori del piano sono stati calcolati con `piano_vlsm.py` (lezione 2.4), dopo aver applicato ai requisiti di `requisiti_azienda.csv` il margine del 20% (arrotondato per eccesso; il collegamento verso il firewall resta di 2 indirizzi).

## Piano di indirizzamento (blocco 10.50.0.0/22)

| Sottorete | Previsti | Con margine | VLAN | Rete | Gateway | Host disponibili |
|---|---|---|---|---|---|---|
| wifi_dipendenti | 150 | 180 | 50 | 10.50.0.0/24 | 10.50.0.1 | 254 |
| wifi_ospiti | 100 | 120 | 40 | 10.50.1.0/25 | 10.50.1.1 | 126 |
| produzione | 60 | 72 | 30 | 10.50.1.128/25 | 10.50.1.129 | 126 |
| amministrazione | 40 | 48 | 10 | 10.50.2.0/26 | 10.50.2.1 | 62 |
| progettazione | 25 | 30 | 20 | 10.50.2.64/27 | 10.50.2.65 | 30 |
| gestione_apparati | 20 | 24 | 99 | 10.50.2.96/27 | 10.50.2.97 | 30 |
| telecamere | 16 | 20 | 60 | 10.50.2.128/27 | 10.50.2.129 | 30 |
| server | 10 | 12 | 70 | 10.50.2.160/28 | 10.50.2.161 | 14 |
| collegamento_firewall | 2 | 2 | 100 | 10.50.2.176/30 | 10.50.2.177 | 2 |

Indirizzi assegnati: 692 su 1024. Blocchi liberi: 10.50.2.180/30, 10.50.2.184/29, 10.50.2.192/26, 10.50.3.0/24.

Osservazioni per la correzione:

- senza margine (piano calcolato direttamente da `requisiti_azienda.csv`) la produzione riceve una /26 usata al 97%: accettabile solo se il gruppo lo motiva; il margine è richiesto dalla traccia
- la numerazione delle VLAN è libera, purché coerente e documentata; è buona pratica una VLAN di gestione separata e non usare la VLAN 1
- intervalli DHCP ragionevoli: tutte le sottoreti di client (Wi-Fi, amministrazione, progettazione, produzione); indirizzi statici per server, stampanti, telecamere e apparati; l'intervallo non deve comprendere gateway e indirizzi statici (controllato da `verifica_progetto.py`)

## Servizi

- DHCP: un server centrale nella VLAN server (per esempio `10.50.2.162`) con un intervallo per ogni sottorete di client; sul router o firewall, relay DHCP per ogni VLAN. In Filius, che non gestisce il relay, un server DHCP per sottorete o indirizzi statici.
- DNS interno: `10.50.2.163`, zona `meccanica.example`, record `intranet`, `posta`, `stampante-uffici`; inoltro delle altre domande a un risolutore esterno.
- Intranet: server web `10.50.2.164`, raggiungibile da amministrazione, progettazione e produzione, non da ospiti.
- NAT sul firewall verso Internet; nessun inoltro di porte, salvo motivate esigenze (per esempio accesso remoto, meglio con VPN).

## Regole tra sottoreti (esempio)

| Da | Verso | Consentito |
|---|---|---|
| wifi_ospiti | reti interne | no, solo Internet |
| wifi_dipendenti, amministrazione, progettazione, produzione | server (DNS, intranet, file) | sì, solo i servizi necessari |
| telecamere | server di registrazione | sì; nessun accesso a Internet |
| client | gestione_apparati | no; solo dalla postazione del tecnico |

## Criteri di valutazione

La griglia è nel testo della lezione (sezione 3.5.4). Errori che incidono di più: sottoreti sovrapposte o non allineate; gateway o DHCP incoerenti con le reti; ospiti non isolati; schema non corrispondente al piano; mancata verifica.
