---
title: "Modulo 6: Cloud computing"
subtitle: "Reti, Cloud e Gestione dei Dati"
lang: it
---

# Modulo 6: Cloud computing

Durata: 5 ore (lezioni 6.1-6.5).

Obiettivi del modulo:

- definire il cloud computing e distinguere modelli di servizio e di distribuzione, regioni e zone
- spiegare macchine virtuali, container e orchestrazione
- usare un servizio di archiviazione a oggetti con l'API S3, su un emulatore locale
- stimare i costi di un servizio cloud e distinguere le responsabilità di fornitore e cliente
- progettare un'architettura scalabile e ad alta disponibilità

Prerequisiti: moduli 1-5, in particolare HTTP (lezione 1.4), zone e reti (moduli 2-3), il servizio della biblioteca (lezione 5.3).

Fonti: contenuto originale. Riferimenti verificati a settembre 2026: NIST SP 800-145; Strategia Cloud Italia e Polo Strategico Nazionale; documentazione Docker, Kubernetes, Amazon S3, boto3, moto; Microsoft Learn (responsabilità condivisa, zone di disponibilità, Well-Architected Framework); Regolamento (UE) 2016/679; pagine di Wikipedia in italiano "Cloud computing", "Hypervisor", "Bilanciamento del carico".

Nessun servizio cloud reale e nessun calcolatore online dei fornitori: l'archiviazione a oggetti usa l'emulatore moto, i costi un listino inventato. Il docente può mostrare facoltativamente, con il proprio account, la console di un fornitore.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 6.1 | Modelli del cloud | `lez01_modelli_cloud/` |
| 6.2 | Virtualizzazione e container | `lez02_virtualizzazione_e_container/` |
| 6.3 | Laboratorio: archiviazione a oggetti | `lez03_lab_storage_a_oggetti/` |
| 6.4 | Costi e responsabilità | `lez04_costi_e_responsabilita/` |
| 6.5 | Architettura cloud | `lez05_architettura_cloud/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio`.

## Strumenti usati nel modulo

- Visual Studio Code con le estensioni Python, REST Client e Draw.io Integration
- Python con i pacchetti `moto[server]` (emulatore, licenza Apache 2.0, versione provata 5.2.3) e `boto3`, installati con `python -m pip install --user "moto[server]"`

## Script e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 6.1 | `soluzioni_docente.md` | attività di classificazione con soluzioni |
| 6.2 | `Dockerfile`, `.dockerignore`, `orchestratore.py`, `test_orchestratore.py`, `soluzioni_docente.md` | 8 test superati su 8: collocazione, stato desiderato, guasto di un nodo, repliche in attesa, riduzione; il Dockerfile non è stato costruito (vedi note) |
| 6.3 | `archivio_oggetti.py`, `oggetti.http`, cartella `esempi`, `test_archivio_oggetti.py` | 14 test superati su 14 con l'emulatore avviato dal test: creazione del bucket, caricamento di una cartella, elenco per prefisso, tipi e metadati, scaricamento identico, sostituzione, 403 senza credenziali, link firmato, oggetto pubblico, cancellazione; comandi della lezione provati con `python -m moto.server` |
| 6.4 | `costi_cloud.py`, `listino_esempio.json`, `scenari.json`, `test_costi_cloud.py`, `soluzioni_docente.md` | 10 test superati su 10: calcolo, sconto per impegno, quota gratuita del traffico, archiviazione e richieste, totali degli scenari, server locale |
| 6.5 | `disponibilita.py`, `test_disponibilita.py`, `soluzioni_docente.md` | 10 test superati su 10: serie, parallelo, fermo annuo, dimensionamento N+1 |

Note per il docente:

- il pacchetto `moto[server]` va installato prima della lezione 6.3 (alcune decine di megabyte, con le dipendenze); se `pip` non raggiunge Internet dalla rete della scuola, si può preparare in anticipo una cartella di pacchetti con `pip download` e installarli da lì
- su Windows si avvia l'emulatore con `python -m moto.server -p 5000`, che non richiede di aggiungere cartelle al PATH
- l'emulatore è più permissivo di un servizio reale su alcune richieste senza firma (per esempio l'elenco degli oggetti); la lezione lo segnala
- il Dockerfile della lezione 6.2 è da leggere: Docker non era disponibile nell'ambiente di preparazione, quindi la costruzione dell'immagine non è stata provata; istruzioni e sintassi seguono la documentazione ufficiale. Per eseguirlo il servizio della lezione 5.3 deve prima ascoltare su `0.0.0.0` (domanda 1 della lezione)
- i prezzi di `listino_esempio.json` sono inventati: la lezione lo dichiara, per evitare confronti con fornitori reali
