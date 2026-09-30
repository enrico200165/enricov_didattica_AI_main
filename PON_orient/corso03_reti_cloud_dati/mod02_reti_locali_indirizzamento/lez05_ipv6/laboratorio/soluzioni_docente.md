---
title: "Lezione 2.5: soluzioni degli esercizi"
subtitle: "Modulo 2: Reti locali e indirizzamento. Materiale per il docente"
lang: it
---

# Lezione 2.5: soluzioni degli esercizi

Valori verificati con `ipv6.py` e con il modulo `ipaddress`.

## Abbreviazione

| Es. | Forma completa | Forma abbreviata | Tipo |
|---|---|---|---|
| 1 | `2001:0db8:0000:0000:0008:0800:200c:417a` | `2001:db8::8:800:200c:417a` | documentazione |
| 2 | `fe80:0000:0000:0000:0204:61ff:fe9d:f156` | `fe80::204:61ff:fe9d:f156` | link-local (identificativo EUI-64: contiene `ff:fe`) |
| 3 | `2001:0db8:0000:0000:0001:0000:0000:0001` | `2001:db8::1:0:0:1` | documentazione; due sequenze di due zeri: si abbrevia la prima |
| 4 | `ff02:0000:0000:0000:0000:0000:0000:0001` | `ff02::1` | multicast, tutti i dispositivi della rete locale |
| 5 | `2001:0DB8:00A0:0000:0000:0000:0000:0000` | `2001:db8:a0::` | documentazione; minuscole; `00A0` diventa `a0`, non `a` |

## Espansione

| Forma abbreviata | Forma completa | Tipo |
|---|---|---|
| `fe80::1` | `fe80:0000:0000:0000:0000:0000:0000:0001` | link-local |
| `2001:db8:a::` | `2001:0db8:000a:0000:0000:0000:0000:0000` | documentazione |
| `::ffff:0:1` | `0000:0000:0000:0000:0000:ffff:0000:0001` | indirizzo IPv4 mappato (`::ffff:0:0/96`), corrisponde a `0.0.0.1`; lo script lo classifica come "altro o riservato" finché non si svolge l'attività 2 |

## EUI-64

MAC `00-1B-21-3A-5C-01`: si divide in `00:1B:21` e `3A:5C:01`, si inserisce `FF:FE` al centro (`00:1B:21:FF:FE:3A:5C:01`) e si inverte il bit U/L del primo byte (`00` = `00000000` diventa `00000010` = `02`). Risultato: `021b:21ff:fe3a:5c01`.

Sul proprio PC l'identificativo dell'indirizzo globale di Windows normalmente non coincide con quello EUI-64: Windows usa identificativi casuali, per non rendere il dispositivo riconoscibile dal MAC.

## Domande della parte 1

1. Con il solo indirizzo link-local la rete locale non annuncia prefissi IPv6 (nessun Router Advertisement): la connettività IPv6 verso Internet non è disponibile, ma IPv6 funziona comunque all'interno della rete locale.
2. Il gateway deve essere raggiungibile direttamente nella rete locale; l'indirizzo link-local del router è sufficiente per inviargli i pacchetti, che poi il router instrada verso le altre reti con i propri indirizzi.

## Attività

1. Esempio: `studenti_wifi` `2001:db8:5c01:1::/64`, `docenti` `2001:db8:5c01:2::/64`, e così via. Ogni /64 contiene 2^64 indirizzi, più di quanti ne servano a qualunque rete locale: la scelta del prefisso non dipende dal numero di dispositivi, e SLAAC richiede comunque reti /64.
3. Il broadcast raggiunge tutti i dispositivi, che devono elaborare il messaggio anche se non li riguarda. IPv6 usa gruppi multicast specifici (per esempio i messaggi di Neighbor Discovery sono inviati a gruppi derivati dall'indirizzo cercato), così li ricevono solo i dispositivi interessati.
