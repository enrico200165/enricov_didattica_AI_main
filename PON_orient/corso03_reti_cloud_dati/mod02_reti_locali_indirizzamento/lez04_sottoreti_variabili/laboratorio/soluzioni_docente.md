---
title: "Lezione 2.4: soluzioni"
subtitle: "Modulo 2: Reti locali e indirizzamento. Materiale per il docente"
lang: it
---

# Lezione 2.4: soluzioni

Valori verificati con `piano_vlsm.py`.

## Parte 1: piano della scuola (blocco 10.20.0.0/22)

| Sottorete | Indirizzi | Prefisso | Rete | Gateway | Broadcast | Host disponibili |
|---|---|---|---|---|---|---|
| studenti_wifi | 300 | /23 | 10.20.0.0/23 | 10.20.0.1 | 10.20.1.255 | 510 |
| docenti | 50 | /26 | 10.20.2.0/26 | 10.20.2.1 | 10.20.2.63 | 62 |
| laboratorio_1 | 28 | /27 | 10.20.2.64/27 | 10.20.2.65 | 10.20.2.95 | 30 |
| laboratorio_2 | 28 | /27 | 10.20.2.96/27 | 10.20.2.97 | 10.20.2.127 | 30 |
| telecamere | 20 | /27 | 10.20.2.128/27 | 10.20.2.129 | 10.20.2.159 | 30 |
| segreteria | 12 | /28 | 10.20.2.160/28 | 10.20.2.161 | 10.20.2.175 | 14 |
| server | 6 | /29 | 10.20.2.176/29 | 10.20.2.177 | 10.20.2.183 | 6 |
| collegamento_router | 2 | /30 | 10.20.2.184/30 | 10.20.2.185 | 10.20.2.187 | 2 |

Blocchi liberi: 10.20.2.188/30, 10.20.2.192/26, 10.20.3.0/24. Indirizzi assegnati: 700 su 1024.

Errori frequenti: scegliere /24 per 300 indirizzi (254 host, non bastano); confondere indirizzi totali e host utilizzabili (una /27 ha 32 indirizzi ma 30 host); far iniziare una sottorete a un indirizzo non allineato alla sua dimensione.

## Parte 3

1. `aula_magna` (40 indirizzi, /26) viene collocata dopo `docenti`, in `10.20.2.64/26`; i due laboratori, le telecamere, la segreteria, i server e il collegamento si spostano più avanti (laboratorio_1 in `10.20.2.128/27`, ..., collegamento in `10.20.2.248/30`). Blocchi liberi: `10.20.2.252/30` e `10.20.3.0/24`. Osservazione per la discussione: aggiungere una sottorete cambia gli indirizzi delle altre; in una rete reale le sottoreti esistenti non si spostano e la nuova si colloca in un blocco libero (qui `10.20.3.0/26`).
2. No: 600 indirizzi richiedono /22 (1022 host), cioè l'intero blocco; lo script segnala spazio insufficiente per `docenti`.
3. Con `10.20.0.0/23` la sottorete del Wi-Fi occupa tutto il blocco: spazio insufficiente per `docenti`.

## Attività

2. Con sottoreti tutte /23 (necessarie per `studenti_wifi`) servirebbero 8 × 512 = 4096 indirizzi, quattro volte il blocco /22: il piano sarebbe impossibile.
3. Sì: `10.20.2.64/27` e `10.20.2.96/27` sono contigue e la prima è allineata a 64, quindi si riassumono in `10.20.2.64/26`.
