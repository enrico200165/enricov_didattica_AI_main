---
title: "Modulo 3: Crittografia pratica"
subtitle: "Cybersecurity ed Ethical Hacking"
lang: it
---

# Modulo 3: Crittografia pratica

Durata: 4 ore (lezioni 3.1-3.4).

Obiettivi del modulo:

- spiegare i concetti di chiave, cifrario e spazio delle chiavi, e i limiti dei cifrari storici
- descrivere la cifratura simmetrica moderna (AES, modalità di funzionamento) e il ciclo di vita delle chiavi
- spiegare scambio di chiavi, cifratura ibrida e firma digitale, e verificare impronte di file scaricati
- descrivere certificati, autorità di certificazione, catena di fiducia e funzionamento di HTTPS, e ispezionare i certificati di siti reali
- distinguere in pratica codifica, hash e cifratura con CyberChef

Prerequisiti: moduli 1 e 2 (in particolare le funzioni di hash, lezione 2.2); Python installato (lezione 2.1).

Fonti: contenuto originale, salvo la sezione 3.1.1, che adatta la lezione "Networking key concepts" di Microsoft "Security-101" (licenza CC0). Strumento principale: CyberChef (GCHQ, licenza Apache 2.0). Riferimenti verificati a settembre 2026: NIST FIPS 197 e FIPS 203, RFC 9846 (TLS 1.3), pagine di Let's Encrypt e del CA/Browser Forum, guide di Mozilla, KeePassXC e Microsoft, pagina Sigstore di python.org.

## Lezioni

| Lezione | Titolo | Directory |
|---|---|---|
| 3.1 | Cifratura simmetrica | `lez01_cifratura_simmetrica/` |
| 3.2 | Cifratura asimmetrica e firme | `lez02_cifratura_asimmetrica_e_firme/` |
| 3.3 | Certificati e HTTPS | `lez03_certificati_e_https/` |
| 3.4 | Laboratorio con CyberChef | `lez04_lab_cyberchef/` |

Ogni directory di lezione contiene tre file con lo stesso prefisso: la lezione (`.md`), la presentazione Marp (`_marp.md`) e la presentazione pandoc reveal.js (`_prezpdoc.md`), più la cartella `laboratorio` con gli script Python (lezioni 3.1-3.3) o la cartella `esercizi` (lezione 3.4).

## Strumenti

| Strumento | Uso nel modulo | Installazione |
|---|---|---|
| CyberChef 11.5.0, versione offline | lezioni 3.1 e 3.4 | ZIP da https://gchq.github.io/CyberChef/ , pulsante Download CyberChef; nessun account |
| PowerShell, `Get-FileHash` | lezione 3.2 | già presente in Windows |
| Firefox, Chrome o Edge | lezione 3.3 | già presenti |
| Python 3.8 o successivo | tutte le lezioni | lezione 2.1 |
| `openssl` di Git for Windows | solo test del docente, lezione 3.3 | incluso in Git for Windows, cartella `usr\bin` |

## Script, esercizi e verifiche

| Lezione | File | Verifica eseguita |
|---|---|---|
| 3.1 | `cifrari_storici.py`, `test_cifrari_storici.py` | 14 test superati su 14; risultati di Cesare e Vigenère identici a quelli di CyberChef 11.5.0 |
| 3.2 | `impronte.py`, `chiavi_giocattolo.py`, `prepara_esercizio.py`, `test_lab32.py` | 17 test superati su 17, compresi i vettori di prova SHA-256 del FIPS 180 e l'esempio RSA classico (n = 3233); esercizio preparato e risolto con lo script |
| 3.3 | `info_certificato.py`, `test_info_certificato.py` | 8 test superati su 8 con una CA di prova e un server TLS locale; script provato anche su un sito reale |
| 3.4 | `esercizi/config_esempio.ini`, `esercizi/verifica_con_python.py`, `esercizi/soluzioni_docente.md` | tutti i risultati attesi degli esercizi 1-8 ottenuti con CyberChef 11.5.0 offline, eseguito automaticamente nel browser; esercizi 1-4 e 8 confermati con Python; cifrato AES dell'esercizio 6 confermato con una libreria indipendente |

Note per il docente:

- l'impronta dello ZIP di CyberChef e il nome del file cambiano a ogni nuova versione: il valore da usare è quello mostrato nella finestra di download al momento dello scaricamento
- nella lezione 3.3 l'emittente dei certificati osservato dalla rete della scuola può essere la CA del sistema di filtraggio, se presente: conviene verificarlo prima della lezione, perché è un buon punto di partenza per la discussione della sezione 3.3.5
- gli script usano solo la libreria standard di Python; tutte le attività si svolgono su dati propri o forniti dal docente, secondo le regole del laboratorio sottoscritte nella lezione 1.2
