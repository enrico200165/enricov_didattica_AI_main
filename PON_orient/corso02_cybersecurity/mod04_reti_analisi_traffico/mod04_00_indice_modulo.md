---
title: "Modulo 4: Reti e analisi del traffico"
subtitle: "Cybersecurity ed Ethical Hacking"
lang: it
---

# Modulo 4: Reti e analisi del traffico

Durata: 5 ore (lezioni 4.1-4.5).

Obiettivi del modulo:

- usare i concetti di livello, indirizzo, protocollo e porta per descrivere la superficie esposta di un sistema, e inventariare i servizi in ascolto sul proprio PC
- spiegare il funzionamento di un firewall (prima corrispondenza, negazione predefinita, stato) e progettare un insieme di regole verificato con test
- leggere catture di rete con Wireshark: livelli, filtri di visualizzazione, conversazioni, statistiche
- riconoscere nel traffico i dati esposti dai protocolli in chiaro e conoscere gli indicatori delle principali attività anomale
- scegliere la protezione adatta a una rete Wi-Fi e progettare una rete segmentata

Prerequisiti: moduli 1-3 (in particolare TLS e certificati, lezione 3.3, e Base64, lezione 3.4); Python installato.

Fonti: contenuto originale, salvo le sezioni 4.1.1-4.1.3, 4.2.1 e 4.5.3, che adattano le lezioni del modulo "Network security" di Microsoft "Security-101" (licenza CC0). Riferimenti verificati a settembre 2026: Wireshark User's Guide, registro delle porte IANA, catalogo MITRE ATT&CK, OWASP Authentication Cheat Sheet, Wi-Fi Alliance, documentazione Microsoft e HPE Aruba.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 4.1 | Protocolli e superficie esposta | `lez01_protocolli_e_superficie_esposta/` |
| 4.2 | Firewall e regole | `lez02_firewall_e_regole/` |
| 4.3 | Wireshark, primi passi | `lez03_wireshark_primi_passi/` |
| 4.4 | Laboratorio: analisi di catture | `lez04_lab_analisi_catture/` |
| 4.5 | Wi-Fi e segmentazione | `lez05_wifi_e_segmentazione/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio` con gli script Python o, per la lezione 4.3, la cartella `catture`.

## Strumenti

| Strumento | Uso nel modulo | Installazione |
|---|---|---|
| PowerShell | lezioni 4.1 e 4.2 | già presente in Windows |
| Wireshark 4.6, versione portatile | lezioni 4.3 e 4.4 | Windows x64 PortableApps da https://www.wireshark.org/download.html ; nessun diritto di amministratore; Npcap non necessario per aprire catture |
| CyberChef offline | lezione 4.4 (decodifica Base64) | lezione 3.1 |
| Python 3.8 o successivo | tutte le lezioni | lezione 2.1 |

## Catture, script e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 4.1 | `servizi_in_ascolto.py`, `ascolto_esempio.csv`, `test_servizi_in_ascolto.py` | 13 test superati su 13 |
| 4.2 | `firewall.py`, `test_firewall.py`, `soluzione_regole_scuola.py` | 15 test superati su 15; soluzione del progetto verificata con 10 pacchetti di prova |
| 4.3 | `catture/cattura1_navigazione.pcapng` (30 pacchetti), `catture/cattura2_accessi.pcapng` (68 pacchetti), `soluzioni_docente.md` | tutti i filtri e le risposte degli esercizi verificati con TShark 4.2 |
| 4.4 | `analizza_cattura.py`, `test_analizza_cattura.py`, `soluzioni_docente.md` | 13 test superati su 13; risultati coincidenti con TShark, anche sulla versione pcap delle catture |
| 4.5 | `piano_indirizzi.py`, `test_piano_indirizzi.py`, `soluzione_docente.md` | 11 test superati su 11; valori delle domande ricalcolati |

Note per il docente:

- le catture contengono solo traffico legittimo, prodotto con programmi reali (server web, DNS e FTP di prova, client `curl`) su un unico computer di laboratorio, con indirizzi sostituiti da quelli di una rete fittizia; il dominio `scuola.example` è riservato agli esempi e gli account sono inventati. Impronte SHA-256: `cattura1_navigazione.pcapng` `85eeb7d58f54b1be41b7373986105c1dbb9053c63aaf645c3a90badec33b33b3`; `cattura2_accessi.pcapng` `0c9ec755ad3cb54c277779aedfd770c45c35b9a157210cd0ed13c3b4a0ef6b1d`
- le attività anomale (ricerca di servizi, tentativi ripetuti di accesso, uso anomalo del DNS, esfiltrazione) sono trattate a livello concettuale nella sezione 4.4.4, con indicatori, contromisure e collegamenti alle schede MITRE ATT&CK e a materiali esterni con catture reali, da usare con le cautele indicate; il rilevamento dei tentativi ripetuti di accesso è svolto in laboratorio sui log nel modulo 6
- tutte le attività si svolgono sul proprio PC o su file forniti, secondo le regole del laboratorio sottoscritte nella lezione 1.2; nessuna attività richiede di catturare traffico o di interrogare sistemi altrui
