---
title: "Lezione 6.2: Laboratorio: analisi di log"
subtitle: "Modulo 6: Monitoraggio e risposta agli incidenti. Cybersecurity ed Ethical Hacking"
lang: it
---

# Lezione 6.2: Laboratorio: analisi di log

> Contenuto originale. Riferimenti: catalogo MITRE ATT&CK; OWASP Authentication Cheat Sheet e Logging Cheat Sheet; documentazione Microsoft sull'evento 4625. Gli script sono nella cartella `laboratorio`; `bacheca.py` è l'applicazione corretta del laboratorio 5.4, con alcuni eventi di registro aggiunti.

Obiettivo: produrre il registro degli eventi di un'applicazione con il proprio lavoro, analizzarlo con uno script Python, e conoscere gli indicatori con cui si riconoscono nei log i tentativi ripetuti di accesso e altre anomalie.

## 6.2.1 Dagli eventi agli indicatori

Un singolo evento raramente è significativo: un accesso fallito è quasi sempre un errore di digitazione. Diventa interessante l'**andamento**: quanti eventi, in quanto tempo, da chi, verso che cosa, in quale sequenza. L'analisi dei log si basa su:

- **conteggi e distribuzioni**: eventi per tipo, per utente, per ora, per indirizzo
- **soglie in una finestra di tempo**: per esempio almeno 5 accessi falliti per lo stesso nome in 10 minuti
- **sequenze**: per esempio un accesso riuscito subito dopo molti fallimenti
- **confronto con il comportamento normale** (baseline): orari, volumi e utenti abituali

La scelta della soglia è un compromesso: una soglia bassa produce molti **falsi positivi** (utenti che sbagliano la password), una soglia alta lascia passare attività lente e distribuite.

## 6.2.2 Anomalie tipiche nei log: indicatori e contromisure

Le attività seguenti sono descritte a livello concettuale. Il laboratorio usa log prodotti dagli studenti con il proprio lavoro; le schede indicate contengono la trattazione completa, con esempi reali, metodi di rilevamento e contromisure.

| Attività | Che cosa si osserva nei log | Contromisure | Approfondimento |
|---|---|---|---|
| **Tentativi ripetuti di accesso su un account** (forza bruta) | molti accessi falliti per lo stesso nome in poco tempo, spesso dallo stesso indirizzo; eventualmente un accesso riuscito alla fine | blocco temporaneo o ritardi crescenti; MFA; avvisi | MITRE ATT&CK T1110.001, https://attack.mitre.org/techniques/T1110/001/ |
| **Stessa password provata su molti account** (password spraying) | pochi accessi falliti per ciascun nome, ma su molti nomi diversi, dallo stesso indirizzo o in un breve intervallo | MFA; divieto delle password più comuni; soglie calcolate anche per indirizzo, non solo per utente | MITRE ATT&CK T1110.003, https://attack.mitre.org/techniques/T1110/003/ |
| **Credenziali rubate provate in massa** (credential stuffing) | accessi falliti su nomi spesso inesistenti, alcuni riusciti, da molti indirizzi | MFA; controllo delle password compromesse (lezione 2.1); limiti per indirizzo | MITRE ATT&CK T1110.004, https://attack.mitre.org/techniques/T1110/004/ |
| **Accesso in orari o da luoghi insoliti** | accesso riuscito fuori dall'orario abituale, o da un paese mai visto per quell'utente | verifica con l'utente; accesso condizionale | concetto di baseline, sezione 6.2.1 |
| **Ricerca di pagine e funzioni** | molte richieste a pagine inesistenti (codice 404) dallo stesso indirizzo in poco tempo | ridurre ciò che è esposto; WAF; blocco temporaneo | MITRE ATT&CK T1595, Active Scanning, https://attack.mitre.org/techniques/T1595/ |
| **Cancellazione dei log** | interruzione della registrazione, evento 1102 in Windows | log copiati in tempo reale su un sistema separato | MITRE ATT&CK T1070, Indicator Removal, https://attack.mitre.org/techniques/T1070/ |

Per i controlli da inserire nelle applicazioni: OWASP Authentication Cheat Sheet, sezione "Protect Against Automated Attacks", https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html ; per che cosa registrare e come: OWASP Logging Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

## 6.2.3 Laboratorio, parte 1: produrre il registro

Tempo indicativo: 15 minuti, a coppie. Cartella di lavoro `C:\corso-cyber\lab62`, con i file della cartella `laboratorio`.

1. Avviare la bacheca sul proprio PC: `python bacheca.py`, poi aprire `http://127.0.0.1:8000`.
2. Usare l'applicazione come nel laboratorio 5.4, con gli utenti di prova `anna` e `bruno`: accedere, pubblicare annunci, cercarli, eliminarne alcuni.
3. Uno dei due studenti **sbaglia di proposito la password** di `anna` alcune volte di seguito, poi accede correttamente; l'altro, più tardi, sbaglia la password due volte a qualche minuto di distanza.
4. Accedere come `bruno` e provare a eliminare un annuncio di `anna`; inserire nel campo del numero dell'annuncio un testo invece di un numero.
5. Fermare l'applicazione con `Ctrl+C` e aprire `bacheca.log` con un editor di testo: individuare a mano gli eventi dei punti 3 e 4.

Formato delle righe:

```text
2026-10-07 09:05:57,633 WARNING accesso fallito per il nome 'anna'
2026-10-07 09:06:00,184 INFO accesso riuscito: anna
2026-10-07 09:06:00,191 WARNING eliminazione non consentita: bruno, annuncio 1
```

Ogni avvio della bacheca ricrea il database ma aggiunge righe allo stesso `bacheca.log`: il registro conserva la storia di tutte le sessioni.

## 6.2.4 Laboratorio, parte 2: analisi con Python

Tempo indicativo: 25 minuti.

```powershell
python analizza_log.py bacheca.log
python analizza_log.py bacheca.log --soglia 3 --finestra 5
```

Output di esempio, da un registro prodotto con i passi della parte 1:

```text
Eventi letti: 11
...
Accessi per nome utente (riusciti / falliti):
  anna                    1 / 5
  bruno                   1 / 0

SEGNALAZIONI (soglia: 5 accessi falliti in 10 minuti)
  accessi falliti ravvicinati: nome 'anna', 5 tra 09:05:57 e 09:05:59
  accesso riuscito dopo 5 fallimenti: nome 'anna' alle 09:06:00
  eliminazione negata: utente 'bruno' alle 09:06:00
```

Struttura dello script:

- `leggi_eventi` riconosce le righe con un'espressione regolare (data, livello, messaggio) e classifica il messaggio confrontandolo con un elenco di schemi; le righe che non rispettano il formato, come quelle di un traceback, vengono ignorate
- `fallimenti_ravvicinati` applica una **finestra scorrevole** agli accessi falliti di ciascun nome:

```python
while j + 1 < len(istanti) and istanti[j + 1] - istanti[i] <= finestra:
    j += 1                                  # quanti fallimenti entro 'finestra' a partire da istanti[i]
if j - i + 1 >= soglia:
    segnalazioni.append((nome, istanti[i], istanti[j], j - i + 1))
```

- `riuscito_dopo_fallimenti` segnala un accesso riuscito preceduto da almeno tre fallimenti consecutivi: può essere l'utente che finalmente ricorda la password, oppure qualcuno che l'ha indovinata

Test: `python test_analizza_log.py` (13 test; la seconda parte usa davvero la bacheca in una cartella temporanea).

### Attività

1. Con i valori predefiniti, quali eventi prodotti nella parte 1 vengono segnalati? Gli errori "normali" del punto 3 (due tentativi a distanza di minuti) sono segnalati?
2. Provare soglie e finestre diverse: con quali valori si segnalano anche gli errori normali? Con quali non si segnala più nulla? Quale scelta si farebbe per il registro elettronico della scuola, e perché?
3. Aggiungere allo script una segnalazione per gli utenti che hanno più di 2 eliminazioni negate nella stessa ora, con un test.
4. Riunire i registri di più coppie in un unico file e rieseguire l'analisi: che cosa cambierebbe se tutti gli studenti usassero lo stesso server?

## 6.2.5 Aspetti orientativi (discussione)

- Saper scrivere piccoli programmi di analisi, in Python o nei linguaggi di interrogazione dei SIEM, è una delle competenze più utili per un analista di sicurezza.
- Le regole di rilevamento vengono continuamente migliorate: ogni falso positivo e ogni incidente non rilevato è un'occasione per correggerle.
- Domanda: quali informazioni mancano nel registro della bacheca per capire se i tentativi falliti provengono dallo stesso computer? Come si potrebbe migliorare la registrazione, rispettando la riservatezza degli utenti?
