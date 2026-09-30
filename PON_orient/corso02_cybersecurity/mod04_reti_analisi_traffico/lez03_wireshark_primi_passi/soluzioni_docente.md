---
title: "Lezione 4.3: soluzioni degli esercizi"
subtitle: "Modulo 4: Reti e analisi del traffico. Materiale per il docente"
lang: it
---

# Lezione 4.3: soluzioni degli esercizi

Risultati verificati con TShark 4.2 (la versione a riga di comando di Wireshark) sul file `catture/cattura1_navigazione.pcapng`. Impronta SHA-256 del file distribuito: `85eeb7d58f54b1be41b7373986105c1dbb9053c63aaf645c3a90badec33b33b3`.

La cattura è stata prodotta generando traffico reale tra programmi eseguiti su un unico computer di laboratorio (un server web e DNS di prova e il client `curl`), con gli indirizzi sostituiti in seguito da quelli di una rete scolastica fittizia. Alcuni dettagli tecnici tradiscono l'origine, per esempio la dimensione massima dei segmenti (MSS) di 65495 byte, tipica del traffico interno a un computer; non influiscono sugli esercizi.

1. Pacchetto 1: richiesta DNS di tipo A per `registro.scuola.example`; pacchetto 2: risposta `192.168.10.5`. Pacchetti 15 e 16: richiesta di tipo AAAA (indirizzo IPv6) e risposta "No such name": il nome non ha un indirizzo IPv6.
2. Due connessioni: pacchetto 3 verso la porta 80 e pacchetto 17 verso la porta 443.
3. MAC di origine `3c:52:82:4e:10:23`, di destinazione `00:1b:21:3a:5c:05`; IP `192.168.10.23` verso `192.168.10.5`; porta di origine 56926, di destinazione 80. La porta di origine è una porta dinamica scelta dal sistema operativo del client (lezione 4.1).
4. Titolo: "Registro della Scuola di Esempio". Il modulo ha `method="post"`: i dati verrebbero inviati con una richiesta POST, in chiaro perché la pagina è in HTTP (lezione 4.4).
5. `server_name`: `registro.scuola.example`. Server Hello: TLS 1.3 (estensione supported_versions, 0x0304), suite `TLS_AES_256_GCM_SHA384`. Nella colonna Protocol il Client Hello può comparire come "TLSv1": per compatibilità il campo di versione del record riporta un valore vecchio, e la versione reale si negozia nelle estensioni.
6. Dopo il Client Hello e il Server Hello si vedono solo byte senza significato: il contenuto è cifrato. Restano visibili indirizzi, porte, tempi, dimensioni e il nome del sito nel Client Hello.
7. Due conversazioni TCP: porta 80, 12 pacchetti e 1387 byte; porta 443, 14 pacchetti e 3524 byte. Protocol Hierarchy: 4 pacchetti DNS su UDP, 26 su TCP, di cui 2 HTTP e 7 TLS.
8. Pacchetto 10, la risposta HTTP con la pagina: contiene il testo `type="password"` del campo del modulo, non una password. Un filtro testuale va sempre verificato leggendo il pacchetto.
