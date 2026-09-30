---
title: "Modulo 1: Come funziona Internet"
subtitle: "Reti, Cloud e Gestione dei Dati"
lang: it
---

# Modulo 1: Come funziona Internet

Durata: 4 ore (lezioni 1.1-1.4).

Obiettivi del modulo:

- descrivere le fasi tra la digitazione di un indirizzo e la visualizzazione di una pagina: DNS, TCP, TLS, HTTP
- spiegare i modelli a livelli e l'incapsulamento, distinguendo indirizzi MAC, indirizzi IP e porte
- usare i comandi di diagnostica di Windows con un metodo per livelli
- leggere e scrivere richieste e risposte HTTP con REST Client e `curl`

Prerequisiti: uso di base del PC; Python installato; Visual Studio Code portatile (Corso 1 o indicazioni del syllabus).

Fonti: contenuto originale, salvo la sezione 1.2.1, che adatta la lezione "Networking key concepts" di Microsoft "Security-101" (licenza CC0). Riferimenti verificati a settembre 2026: MDN Web Docs, documentazione Microsoft dei comandi di rete, guida introduttiva di Filius, sito di curl, estensione REST Client.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 1.1 | Dal browser al server | `lez01_dal_browser_al_server/` |
| 1.2 | Livelli e incapsulamento | `lez02_livelli_e_incapsulamento/` |
| 1.3 | Strumenti di diagnostica | `lez03_strumenti_di_diagnostica/` |
| 1.4 | HTTP da vicino | `lez04_http_da_vicino/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Strumenti usati nel modulo

- Visual Studio Code con le estensioni Python e REST Client
- Python (libreria standard)
- Filius 2.14, dalla lezione 1.2
- comandi di Windows: `ipconfig`, `ping`, `tracert`, `nslookup`, `curl.exe`; PowerShell: `Test-NetConnection`
- DevTools del browser

## Script e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 1.1 | `misura_richiesta.py`, `test_misura_richiesta.py` | 6 test superati su 6, con server locali HTTP e HTTPS |
| 1.2 | `incapsulamento.py`, `test_incapsulamento.py` | 13 test superati su 13; trama prodotta decodificata correttamente da Wireshark (TShark), con checksum IP e TCP corrette |
| 1.3 | `diagnosi.py`, `test_diagnosi.py`, `soluzioni_docente.md` | 7 test superati su 7: guasti simulati di configurazione, DNS, trasporto e applicazione |
| 1.4 | `server_didattico.py`, `richieste.http`, `messaggio.json`, `test_server_didattico.py` | 14 test superati su 14, compresa l'esecuzione delle dieci richieste di `richieste.http`; comandi `curl` provati |

Note per il docente:

- i server dei laboratori ascoltano solo su `127.0.0.1`; le attività verso l'esterno usano solo i normali comandi di diagnostica verso siti pubblici
- se la rete della scuola blocca `ping` o `tracert` verso l'esterno, le attività si svolgono comunque verso il gateway e i server locali, e il blocco diventa un'osservazione da discutere
- Filius va installato prima della lezione 1.2: l'installatore include Java; per la versione ZIP serve Java 17 o successivo
- gli esempi di output con siti reali sono indicativi: tempi e indirizzi cambiano
