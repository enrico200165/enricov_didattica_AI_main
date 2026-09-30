---
title: "Lezione 1.4: HTTP da vicino"
subtitle: "Modulo 1: Come funziona Internet. Reti, Cloud e Gestione dei Dati"
lang: it
---

# Lezione 1.4: HTTP da vicino

> Contenuto originale. Riferimenti: MDN Web Docs, "An overview of HTTP", https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview ; estensione REST Client per VS Code. Gli script sono nella cartella `laboratorio`.

Obiettivo: leggere e scrivere richieste e risposte HTTP, riconoscere metodi, codici di stato e intestazioni, e osservare il protocollo dal lato del client e del server.

## 1.4.1 Richieste e risposte

**HTTP** (HyperText Transfer Protocol) è il protocollo del web: il client invia una **richiesta**, il server restituisce una **risposta**. Fino alla versione 1.1 i messaggi sono testo leggibile; HTTP/2 e HTTP/3 codificano gli stessi contenuti in forma binaria, più efficiente, ma il significato non cambia.

Una richiesta:

```http
GET /saluto?nome=Giulia HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 ...
Accept: text/html
```

- **riga di richiesta**: metodo, percorso della risorsa (con eventuali parametri dopo il `?`), versione del protocollo
- **intestazioni**: una per riga, nella forma `Nome: valore`; `Host` indica il sito richiesto ed è obbligatoria in HTTP/1.1, perché sullo stesso indirizzo IP possono esserci molti siti
- **riga vuota**, poi l'eventuale **corpo** (per esempio i dati di un modulo)

Una risposta:

```http
HTTP/1.0 200 OK
Server: ServerDidattico/1.0 Python/3.12
Content-Type: text/plain; charset=utf-8
Content-Length: 13

Ciao, Giulia!
```

- **riga di stato**: versione, codice di stato, descrizione (il server didattico del laboratorio risponde con HTTP/1.0, la versione predefinita del modulo `http.server` di Python)
- **intestazioni**, riga vuota, **corpo**

## 1.4.2 Metodi, codici di stato, intestazioni

Metodi principali:

| Metodo | Uso |
|---|---|
| GET | leggere una risorsa; non deve modificare nulla sul server |
| HEAD | come GET, ma solo intestazioni, senza corpo |
| POST | inviare dati per creare una risorsa o eseguire un'azione |
| PUT | sostituire una risorsa |
| PATCH | modificare in parte una risorsa |
| DELETE | eliminare una risorsa |

Classi dei codici di stato:

| Classe | Significato | Esempi |
|---|---|---|
| 1xx | informazione | 101 cambio di protocollo |
| 2xx | successo | 200 OK, 201 creato, 204 nessun contenuto |
| 3xx | reindirizzamento | 301 spostato in modo permanente, 302 temporaneamente, 304 non modificato |
| 4xx | errore del client | 400 richiesta non valida, 401 autenticazione necessaria, 403 vietato, 404 non trovato |
| 5xx | errore del server | 500 errore interno, 503 servizio non disponibile |

Intestazioni frequenti:

- `Content-Type`: tipo del contenuto, per esempio `text/html`, `application/json`, `image/png`, con l'eventuale codifica dei caratteri (`charset=utf-8`)
- `Content-Length`: lunghezza del corpo in byte
- `Location`: nuovo indirizzo, nei reindirizzamenti
- `Set-Cookie` (risposta) e `Cookie` (richiesta): un piccolo dato che il server chiede di conservare e che il browser rimanda nelle richieste successive
- `Cache-Control`: per quanto tempo si può riusare una risposta senza richiederla

HTTP è **senza stato**: ogni richiesta è indipendente dalle precedenti. I **cookie** permettono di collegare richieste successive dello stesso browser, per esempio per ricordare un accesso o un carrello.

**HTTPS** è HTTP trasportato dentro una connessione TLS: gli stessi messaggi, cifrati. Chi osserva la rete vede l'indirizzo del server, ma non il percorso richiesto, le intestazioni né il contenuto.

## 1.4.3 Laboratorio

Tempo indicativo: 45 minuti. Cartella di lavoro `C:\corso-reti\lab14`, con i file della cartella `laboratorio`.

### Parte 1: il server didattico

`server_didattico.py` è un piccolo server web scritto con la libreria standard di Python (`http.server`), che stampa nel terminale ogni richiesta ricevuta con le sue intestazioni.

```powershell
python server_didattico.py
```

Il server ascolta su `127.0.0.1`, cioè solo sul proprio PC, alla porta 8000. Aprire nel browser `http://127.0.0.1:8000/` e poi `http://127.0.0.1:8000/saluto?nome=Luca`: nel terminale compaiono le richieste del browser, con intestazioni come `User-Agent`, `Accept`, `Accept-Language`. Il browser richiede anche `/favicon.ico`, l'icona della scheda: il server risponde 404.

Struttura del codice:

```python
class Gestore(BaseHTTPRequestHandler):
    def do_GET(self):                         # chiamato per ogni richiesta GET
        parti = urlsplit(self.path)           # percorso e parametri
        parametri = parse_qs(parti.query)     # da "nome=Luca" a {"nome": ["Luca"]}
        if parti.path == "/saluto":
            nome = parametri.get("nome", ["sconosciuto"])[0]
            self.rispondi(200, f"Ciao, {nome}!".encode("utf-8"))
```

- `BaseHTTPRequestHandler` legge la richiesta e chiama il metodo `do_GET`, `do_POST` o `do_HEAD` corrispondente al metodo HTTP
- `self.path` contiene percorso e parametri; `urlsplit` e `parse_qs` li separano
- `rispondi` invia riga di stato, intestazioni e corpo con `send_response`, `send_header`, `end_headers` e `wfile.write`

### Parte 2: richieste con REST Client

Con il server avviato, aprire `richieste.http` in VS Code, dopo aver installato l'estensione **REST Client** (https://marketplace.visualstudio.com/items?itemName=humao.rest-client). Sopra ogni richiesta compare il comando **Send Request**; la risposta completa, con riga di stato e intestazioni, si apre in un pannello accanto.

```http
### 5. Invio di dati JSON
POST {{base}}/api/messaggi
Content-Type: application/json

{
  "testo": "Laboratorio di reti alle 10"
}
```

Il file contiene dieci richieste: pagina HTML, parametri, JSON, `HEAD`, `POST` valido e non valido, reindirizzamento, cookie, pagina inesistente. Per ciascuna annotare metodo, codice di stato, `Content-Type` e, dove presente, `Location` o `Set-Cookie`. REST Client segue automaticamente i reindirizzamenti e ricorda i cookie tra una richiesta e l'altra, come un browser: ripetere la richiesta 9 per vedere crescere il contatore.

### Parte 3: le stesse richieste con curl

```powershell
curl.exe -i http://127.0.0.1:8000/saluto?nome=Luca
curl.exe -I http://127.0.0.1:8000/
curl.exe -i -X POST -H "Content-Type: application/json" -d "@messaggio.json" http://127.0.0.1:8000/api/messaggi
curl.exe -i http://127.0.0.1:8000/vecchia-pagina
curl.exe -i -L http://127.0.0.1:8000/vecchia-pagina
```

- `-i` mostra anche le intestazioni della risposta; `-I` invia una richiesta `HEAD`
- `-X POST` sceglie il metodo; `-H` aggiunge un'intestazione; `-d` indica il corpo, qui letto dal file `messaggio.json` grazie al simbolo `@` (scrivere il JSON direttamente sulla riga di comando è scomodo, perché le virgolette vanno protette in modo diverso nelle diverse shell)
- `-L` segue i reindirizzamenti: confrontare le ultime due richieste

Test: `python test_server_didattico.py` (14 test; l'ultimo esegue tutte le richieste di `richieste.http` e ne controlla i codici di stato).

### Parte 4: siti reali

Con REST Client o `curl.exe -I`, osservare le intestazioni di risposta di due siti reali, per esempio `https://www.wikipedia.org` e il sito della scuola: versione di HTTP, tipo di server, `Content-Type`, `Cache-Control`, cookie. Si tratta delle stesse informazioni che il browser riceve a ogni visita.

### Attività

1. Aggiungere al server un percorso `/api/somma?a=3&b=4` che restituisca `{"somma": 7}` in JSON, e un test; con valori non numerici deve rispondere 400.
2. Aggiungere a `richieste.http` una richiesta per il nuovo percorso.
3. Perché il browser non mostra mai la risposta 301, ma solo la pagina finale? Dove la si può vedere?

## 1.4.4 Aspetti orientativi (discussione)

- HTTP è il protocollo su cui si basano non solo i siti, ma quasi tutte le app e i servizi cloud (moduli 5 e 6): conoscerlo è utile a sviluppatori, sistemisti, tecnici di rete e analisti di sicurezza.
- Strumenti come REST Client e `curl` sono di uso quotidiano per provare servizi e diagnosticare problemi.
- Domanda: che cosa cambia, per chi gestisce un sito, passare da HTTP a HTTPS? E per l'utente?
