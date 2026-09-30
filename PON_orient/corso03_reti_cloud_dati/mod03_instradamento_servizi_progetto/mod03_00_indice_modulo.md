---
title: "Modulo 3: Instradamento, servizi e progetto"
subtitle: "Reti, Cloud e Gestione dei Dati"
lang: it
---

# Modulo 3: Instradamento, servizi e progetto

Durata: 5 ore (lezioni 3.1-3.5).

Obiettivi del modulo:

- spiegare il funzionamento del router e configurare rotte statiche
- confrontare i protocolli di instradamento dinamico e descrivere l'organizzazione di Internet
- descrivere e configurare DHCP, DNS e NAT
- segmentare una rete con le VLAN, scegliere la sicurezza delle reti Wi-Fi e dimensionare il cablaggio di un piano
- progettare e documentare in gruppo la rete di un'azienda

Prerequisiti: moduli 1 e 2, in particolare indirizzamento IPv4 e VLSM (lezioni 2.3 e 2.4); `piano_vlsm.py` della lezione 2.4 necessario per la lezione 3.5.

Fonti: contenuto originale. Riferimenti verificati a settembre 2026: RFC 1034, 2131, 2328, 2453, 2606, 3022, 4271, 6598 (rfc-editor.org); IANA, elenco dei server radice; documentazione Microsoft del comando `route`; pagine di Wikipedia in italiano su DNS, DHCP, NAT, IEEE 802.1Q, IEEE 802.11, Wi-Fi Protected Access, Power over Ethernet, cablaggio strutturato; siti di MIX, Namex, Submarine Cable Map di TeleGeography, ipify.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 3.1 | Router e instradamento statico | `lez01_router_e_instradamento_statico/` |
| 3.2 | Instradamento dinamico e Internet | `lez02_instradamento_dinamico_e_internet/` |
| 3.3 | DHCP, DNS e NAT | `lez03_dhcp_dns_e_nat/` |
| 3.4 | VLAN, Wi-Fi e cablaggio | `lez04_vlan_wifi_e_cablaggio/` |
| 3.5 | Progetto di una rete aziendale | `lez05_progetto_rete_aziendale/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Strumenti usati nel modulo

- Filius 2.14: router, rotte statiche, instradamento automatico (RIP), DHCP, DNS, web server e browser, Home Router con NAT
- Visual Studio Code con le estensioni Python e Draw.io Integration
- Python (libreria standard)
- comandi di Windows: `route print`, `tracert`, `ipconfig /all`, `ipconfig /displaydns`, `nslookup`, `curl.exe`

## Script e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 3.1 | `instradamento.py`, `route_esempio.txt`, `test_instradamento.py` | 18 test superati su 18: prefisso più lungo, rotta predefinita, percorsi, destinazione irraggiungibile, ciclo con TTL esaurito, lettura di `route print` in italiano e in inglese |
| 3.2 | `instradamento_dinamico.py`, `test_instradamento_dinamico.py` | 14 test superati su 14: vettore di distanze e Dijkstra concordi prima e dopo un guasto, ciclo temporaneo, limite di 15 salti |
| 3.2 | `leggi_tracert.py`, `tracert_esempio.txt`, `test_leggi_tracert.py` | 10 test superati su 10: lettura di `tracert`, mediane, stima delle distanze, aumenti bruschi |
| 3.3 | `risolutore_dns.py`, `test_risolutore_dns.py` | 12 test superati su 12: deleghe, cache e TTL, CNAME, MX, AAAA, nomi inesistenti |
| 3.3 | `nat_simulato.py`, `test_nat_simulato.py` | 11 test superati su 11: traduzione in uscita e in ingresso, porte uguali su PC diversi, scarto degli ingressi non richiesti, inoltro delle porte, scadenza |
| 3.4 | `progetto_piano.py`, `stanze_piano.csv`, `test_progetto_piano.py` | 10 test superati su 10: access point, prese, VLAN, switch, potenza PoE, tratte oltre 90 m |
| 3.4 | `vlan_8021q.py`, `test_vlan_8021q.py` | 9 test superati su 9: inserimento, lettura e rimozione dell'etichetta, valori limite |
| 3.5 | `verifica_progetto.py`, `piano_esempio.csv`, `piano_con_errori.csv`, `requisiti_azienda.csv`, `modello_documento_progetto.md`, `test_verifica_progetto.py`, `soluzioni_docente.md` | 15 test superati su 15: tutti i tipi di errore del file `piano_con_errori.csv` individuati, piano di esempio senza errori; la traccia di soluzione è stata verificata con lo stesso script |

Note per il docente:

- le etichette e i comportamenti di Filius citati (tabella **Forwarding table** con **New entry** e **Show all entries**, casella **Automatic Routing** con RIP e aggiornamenti ogni 30 secondi, pagina `http://<router>/routes`, **DHCP server setup**, **DNS server** con record **Address (A)**, **Home Router** con NAT, comandi `route`, `traceroute`, `host`, massimo 8 interfacce per router) sono stati verificati nel codice sorgente di Filius 2.6 (licenza GPL); con la versione 2.14 conviene una prova preliminare
- Filius non gestisce VLAN né relay DHCP: nella lezione 3.5 il modello in Filius è semplificato, come indicato nel testo
- i file `lab31_tre_reti.fls` e `lab33_servizi.fls` servono nelle lezioni successive del modulo
- `tracert` verso siti lontani può richiedere alcuni minuti; se la rete della scuola blocca i messaggi ICMP, si usa il file `tracert_esempio.txt`
- tutti gli indirizzi pubblici degli esempi sono indirizzi di documentazione (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) e i nomi usano il dominio riservato `.example`; l'azienda del progetto è inventata
