---
title: "Modulo 2: Reti locali e indirizzamento"
subtitle: "Reti, Cloud e Gestione dei Dati"
lang: it
---

# Modulo 2: Reti locali e indirizzamento

Durata: 5 ore (lezioni 2.1-2.5).

Obiettivi del modulo:

- descrivere mezzi trasmissivi, trama Ethernet e funzionamento dello switch
- spiegare la struttura degli indirizzi MAC e il ruolo di ARP
- calcolare rete, broadcast e host di un indirizzo IPv4 con la sua maschera
- progettare un piano di indirizzamento con sottoreti di dimensione variabile e aggregazione
- leggere, abbreviare e classificare gli indirizzi IPv6 e spiegare l'autoconfigurazione

Prerequisiti: Modulo 1 (livelli, incapsulamento, comandi di diagnostica); Filius installato (lezione 1.2); aritmetica binaria di base.

Fonti: contenuto originale. Riferimenti verificati a settembre 2026: RFC 826, 1918, 3021, 3849, 4291, 4632, 4862, 5952, 8981 (rfc-editor.org); documentazione Python del modulo `ipaddress`; documentazione Microsoft del comando `arp`; pagine di Wikipedia in italiano su Ethernet, switch, indirizzo MAC, ARP, CIDR, IPv6, doppino ritorto e fibra ottica; IEEE Registration Authority; statistiche IPv6 di Google; test-ipv6.com (APNIC Labs).

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 2.1 | Ethernet, switch e Filius | `lez01_ethernet_switch_e_filius/` |
| 2.2 | ARP e indirizzi MAC | `lez02_arp_e_indirizzi_mac/` |
| 2.3 | Indirizzi IPv4 e sottoreti | `lez03_indirizzi_ipv4_e_sottoreti/` |
| 2.4 | Sottoreti di dimensione variabile | `lez04_sottoreti_variabili/` |
| 2.5 | IPv6 | `lez05_ipv6/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Strumenti usati nel modulo

- Filius 2.14: lezioni 2.1-2.3 (Filius non gestisce IPv6)
- Visual Studio Code con le estensioni Python e Draw.io Integration (lezione 2.4)
- Python (libreria standard, in particolare il modulo `ipaddress`)
- comandi di Windows: `ipconfig`, `arp`, `ping`, `nslookup`, `curl.exe`

## Script e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 2.1 | `switch_simulato.py`, `test_switch_simulato.py` | 11 test superati su 11: apprendimento, inoltro, flooding, filtraggio, spostamento di un PC, scadenza delle voci |
| 2.2 | `mac_e_arp.py`, `arp_esempio.txt`, `test_mac_e_arp.py` | 17 test superati su 17: formati del MAC, bit I/G e U/L, regola multicast `01:00:5E`, lettura dell'output di `arp -a` in italiano e in inglese |
| 2.3 | `calcolo_ipv4.py`, `test_calcolo_ipv4.py`, `soluzioni_docente.md` | 17 test superati su 17, compreso il confronto con `ipaddress` su 990 indirizzi casuali con tutti i prefissi e la correzione automatica degli esercizi |
| 2.4 | `piano_vlsm.py`, `requisiti_scuola.csv`, `test_piano_vlsm.py`, `soluzioni_docente.md` | 15 test superati su 15: prefissi, piano della scuola, allineamento, blocchi liberi, blocco insufficiente, sovrapposizioni, aggregazione, file CSV prodotto |
| 2.5 | `ipv6.py`, `ipconfig_esempio.txt`, `test_ipv6.py`, `soluzioni_docente.md` | 19 test superati su 19: espansione, abbreviazione secondo l'RFC 5952 confrontata con `ipaddress` su 3000 indirizzi casuali, tipi, EUI-64, lettura dell'output di `ipconfig` |

Note per il docente:

- le etichette e i comportamenti di Filius citati (tabella **SAT table** dello switch con clic sinistro in modalità simulazione, comando `arp` e `arp -d` della Command Line, voce di menu **Show data exchange**, campo **Retention Time SAT Entries (Seconds)**, mancata risposta ARP a un mittente fuori dalla propria sottorete) sono stati verificati nel codice sorgente di Filius (versione 2.6, licenza GPL) e nelle sue traduzioni inglesi; con la versione 2.14 conviene una prova preliminare, perché le etichette possono differire leggermente
- i file `lab21_switch.fls` prodotti nella lezione 2.1 servono anche nelle lezioni 2.2 e 2.3
- `mac_e_arp.py` e `ipv6.py`, senza argomenti, eseguono `arp -a` e `ipconfig` solo su Windows; su altri sistemi si usano i file di esempio
- se la rete della scuola non offre IPv6, le attività della lezione 2.5 sulla connettività diventano un'osservazione; gli esercizi di notazione e gli script non richiedono IPv6
- negli esempi si usano indirizzi di documentazione (`2001:db8::/32`, `203.0.113.0/24`) e indirizzi MAC inventati
