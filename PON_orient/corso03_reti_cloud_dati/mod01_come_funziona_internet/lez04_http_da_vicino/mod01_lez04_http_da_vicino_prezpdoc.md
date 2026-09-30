---
title: "Lezione 1.4: HTTP da vicino"
subtitle: "Modulo 1: Come funziona Internet. Reti, Cloud e Gestione dei Dati"
lang: it
---

## Contenuti

- Richiesta e risposta
- Metodi e codici
- Laboratorio
- Aspetti orientativi

## Richiesta e risposta

```http
GET /saluto?nome=Giulia HTTP/1.1
Host: 127.0.0.1:8000
```

```http
HTTP/1.0 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 13

Ciao, Giulia!
```

## Metodi e codici

- GET, HEAD, POST, PUT, PATCH, DELETE
- 2xx successo, 3xx reindirizzamento, 4xx errore del client, 5xx errore del server
- Intestazioni: Content-Type, Content-Length, Location, Set-Cookie, Cache-Control
- HTTP senza stato; cookie; HTTPS = HTTP dentro TLS

## Laboratorio

1. `python server_didattico.py`: richieste stampate nel terminale
2. REST Client in VS Code: `richieste.http`, dieci richieste
3. `curl.exe -i`, `-I`, `-X POST -d "@messaggio.json"`, `-L`
4. Intestazioni di siti reali; 14 test

## Aspetti orientativi

- HTTP alla base di siti, app e cloud
- REST Client e curl di uso quotidiano
- Da HTTP a HTTPS: che cosa cambia?
