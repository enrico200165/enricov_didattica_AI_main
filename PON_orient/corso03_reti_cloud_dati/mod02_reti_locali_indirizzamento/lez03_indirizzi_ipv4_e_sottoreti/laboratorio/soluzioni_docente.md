---
title: "Lezione 2.3: soluzioni degli esercizi"
subtitle: "Modulo 2: Reti locali e indirizzamento. Materiale per il docente"
lang: it
---

# Lezione 2.3: soluzioni degli esercizi

Valori verificati con `calcolo_ipv4.py` e con il modulo `ipaddress`.

| Es. | Indirizzo | Maschera | Rete | Broadcast | Primo host | Ultimo host | Host |
|---|---|---|---|---|---|---|---|
| 1 | 192.168.5.130/25 | 255.255.255.128 | 192.168.5.128 | 192.168.5.255 | 192.168.5.129 | 192.168.5.254 | 126 |
| 2 | 10.45.200.17/20 | 255.255.240.0 | 10.45.192.0 | 10.45.207.255 | 10.45.192.1 | 10.45.207.254 | 4094 |
| 3 | 172.18.99.250/27 | 255.255.255.224 | 172.18.99.224 | 172.18.99.255 | 172.18.99.225 | 172.18.99.254 | 30 |
| 4 | 192.168.1.66/28 | 255.255.255.240 | 192.168.1.64 | 192.168.1.79 | 192.168.1.65 | 192.168.1.78 | 14 |
| 5 | 10.0.0.1/30 | 255.255.255.252 | 10.0.0.0 | 10.0.0.3 | 10.0.0.1 | 10.0.0.2 | 2 |

Note sul calcolo:

- es. 2: l'ottetto interessante è il terzo, blocco 256 - 240 = 16; 200 cade nel blocco da 192 a 207 (200 = `11001000`, maschera `11110000`, AND `11000000` = 192)
- es. 3: blocco 32 nel quarto ottetto; 250 cade nel blocco da 224 a 255
- es. 4: la maschera 255.255.255.240 corrisponde a /28; blocco 16; 66 cade nel blocco da 64 a 79

Esercizio 6: no. Con /26 il blocco è 64: `192.168.1.60` è nella rete `192.168.1.0/26` (host da .1 a .62), `192.168.1.70` nella rete `192.168.1.64/26` (host da .65 a .126).

Esercizio 7: no, non è privato secondo l'RFC 1918. Appartiene a `100.64.0.0/10`, lo spazio condiviso usato dai fornitori di accesso per il NAT su larga scala (CGNAT, RFC 6598): lo si trova come indirizzo "esterno" di alcuni router domestici e di molte connessioni mobili. Rete `100.64.0.0`, broadcast `100.127.255.255`.

Esercizio 8: `172.16.254.1` = `10101100.00010000.11111110.00000001` (172 = 128 + 32 + 8 + 4; 254 = 255 - 1).

Parte 4 (Filius): `PC-1` (`192.168.1.11/24`) calcola per `192.168.1.140` la rete `192.168.1.0`, uguale alla propria, e invia una richiesta ARP; `PC-4` (`192.168.1.140/25`) si trova nella rete `192.168.1.128/25` e considera `192.168.1.11` (rete `192.168.1.0/25`) in un'altra rete: non risponde alla richiesta ARP, e per rispondere al ping userebbe il gateway, che non è configurato. Da `PC-4` verso `PC-1` il ping fallisce subito per lo stesso motivo: nessun gateway per una destinazione esterna alla propria rete.

Attività 2: 500 dispositivi richiedono 9 bit di host (510 host), cioè /23; 1000 dispositivi richiedono 10 bit (1022 host), cioè /22.
