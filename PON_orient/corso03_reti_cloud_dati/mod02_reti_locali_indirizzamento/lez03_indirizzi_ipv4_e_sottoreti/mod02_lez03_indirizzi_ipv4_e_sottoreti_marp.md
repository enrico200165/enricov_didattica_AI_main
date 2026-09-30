---
marp: true
paginate: true
lang: it
---

## Lezione 2.3: Indirizzi IPv4 e sottoreti

Modulo 2: Reti locali e indirizzamento. Reti, Cloud e Gestione dei Dati

---

## Indirizzi a 32 bit

- Quattro ottetti in notazione decimale puntata
- Pesi: 128 64 32 16 8 4 2 1
- `192.168.10.77` = `11000000.10101000.00001010.01001101`

---

## Rete, host, maschera

| | Binario (ultimo ottetto) | Decimale |
|---|---|---|
| Indirizzo /26 | `01001101` | .77 |
| Maschera | `11000000` | .192 |
| Rete (AND) | `01000000` | .64 |
| Broadcast | `01111111` | .127 |

- `2^h` indirizzi, `2^h - 2` host; blocco = 256 - 192 = 64

---

## Dalle classi al CIDR

| Classe | Primo ottetto | Maschera |
|---|---|---|
| A | 0-127 | /8 |
| B | 128-191 | /16 |
| C | 192-223 | /24 |
| D, E | 224-255 | multicast, riservata |

- CIDR (1993): prefisso libero, aggregazione

---

## Indirizzi speciali

- Privati: 10/8, 172.16/12, 192.168/16 (RFC 1918)
- Loopback 127/8; link-local 169.254/16
- CGNAT 100.64/10; documentazione 192.0.2/24, 198.51.100/24, 203.0.113/24
- Esaurimento: IANA 2011, RIPE NCC 2019

---

## Laboratorio

1. Otto esercizi a mano
2. `python calcolo_ipv4.py 10.45.200.17/20`; `--esercizi 5`
3. `ipaddress` in modalità interattiva
4. Filius: maschere incoerenti
5. 17 test, confronto su 990 indirizzi

---

## Aspetti orientativi

- Calcolo delle sottoreti: competenza di base per tecnici di rete
- Gli strumenti verificano il ragionamento, non lo sostituiscono
- Maschere diverse nella stessa rete fisica: che cosa succede?
