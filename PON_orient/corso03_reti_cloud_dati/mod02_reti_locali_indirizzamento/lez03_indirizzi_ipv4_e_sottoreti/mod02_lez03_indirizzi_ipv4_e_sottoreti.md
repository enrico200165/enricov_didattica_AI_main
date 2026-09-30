---
title: "Lezione 2.3: Indirizzi IPv4 e sottoreti"
subtitle: "Modulo 2: Reti locali e indirizzamento. Reti, Cloud e Gestione dei Dati"
lang: it
---

# Lezione 2.3: Indirizzi IPv4 e sottoreti

> Contenuto originale. Riferimenti: RFC 4632, "Classless Inter-domain Routing (CIDR)", https://www.rfc-editor.org/rfc/rfc4632 ; RFC 1918, "Address Allocation for Private Internets", https://www.rfc-editor.org/rfc/rfc1918 ; documentazione Python, "An introduction to the ipaddress module", https://docs.python.org/3/howto/ipaddress.html . Gli script sono nella cartella `laboratorio`; le soluzioni degli esercizi nel file `laboratorio/soluzioni_docente.md`.

Obiettivo: calcolare, a mano e con Python, indirizzo di rete, broadcast e numero di host di un indirizzo IPv4 con la sua maschera, e riconoscere gli indirizzi con usi speciali.

## 2.3.1 Indirizzi a 32 bit

Un indirizzo **IPv4** è un numero di 32 bit. Per leggerlo meglio si divide in quattro gruppi di 8 bit (**ottetti**), ciascuno scritto in decimale da 0 a 255 e separato da un punto: è la **notazione decimale puntata**.

Conversione di un ottetto: ogni bit ha un peso, dal più significativo al meno significativo.

| Peso | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| 192 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 168 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| 77 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 1 |

- da decimale a binario: si sottraggono i pesi dal più grande, scrivendo 1 quando il peso è contenuto nel numero rimasto (77 = 64 + 8 + 4 + 1)
- da binario a decimale: si sommano i pesi dei bit a 1

Così `192.168.10.77` in binario è `11000000.10101000.00001010.01001101`.

## 2.3.2 Rete, host e maschera

Ogni indirizzo IPv4 si divide in due parti:

- **parte di rete**
  i bit iniziali, uguali per tutti i dispositivi della stessa rete;
- **parte host**
  i bit finali, diversi per ogni dispositivo della rete.

Il confine è indicato dalla **maschera di sottorete** (subnet mask): un numero di 32 bit con tutti 1 nella parte di rete e tutti 0 nella parte host. La notazione **CIDR** indica solo il numero di bit a 1, il **prefisso**, dopo una barra: `192.168.10.77/26` significa maschera di 26 bit a 1, cioè `255.255.255.192`.

Calcoli fondamentali, con `192.168.10.77/26`:

| Valore | Regola | Binario | Decimale |
|---|---|---|---|
| Indirizzo | | `11000000.10101000.00001010.01001101` | 192.168.10.77 |
| Maschera | 26 bit a 1 | `11111111.11111111.11111111.11000000` | 255.255.255.192 |
| Indirizzo di rete | indirizzo AND maschera: parte host a 0 | `11000000.10101000.00001010.01000000` | 192.168.10.64 |
| Indirizzo di broadcast | parte host tutta a 1 | `11000000.10101000.00001010.01111111` | 192.168.10.127 |
| Host utilizzabili | tra rete e broadcast esclusi | | da .65 a .126 |

- L'operazione **AND** bit a bit dà 1 solo dove entrambi i bit sono 1: applicata con la maschera, conserva la parte di rete e azzera la parte host.
- Con `h` bit di host la rete ha `2^h` indirizzi, di cui `2^h - 2` utilizzabili: il primo identifica la rete, l'ultimo è il broadcast della rete. Qui `h = 32 - 26 = 6`: 64 indirizzi, 62 host.
- Scorciatoia per l'ottetto "interessante" (quello in cui la maschera non è 255 né 0): la **dimensione del blocco** è 256 meno il valore della maschera in quell'ottetto (256 - 192 = 64). Le reti iniziano ai multipli del blocco: .0, .64, .128, .192. 77 cade nel blocco che inizia a 64 e finisce a 127.

Prefissi frequenti:

| Prefisso | Maschera | Indirizzi | Host |
|---|---|---|---|
| /8 | 255.0.0.0 | 16 777 216 | 16 777 214 |
| /16 | 255.255.0.0 | 65 536 | 65 534 |
| /22 | 255.255.252.0 | 1024 | 1022 |
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 2 |

Casi particolari: una rete /31 ha due soli indirizzi, entrambi utilizzabili nei collegamenti punto-punto tra due router (RFC 3021, https://www.rfc-editor.org/rfc/rfc3021 ); un /32 indica un singolo indirizzo.

### Due indirizzi sono nella stessa rete?

Un dispositivo confronta la propria rete con quella del destinatario, calcolate entrambe con la **propria** maschera. Se coincidono, consegna direttamente (con ARP, lezione 2.2); altrimenti invia al gateway.

Esempio con maschera /26: `192.168.1.60` appartiene alla rete `192.168.1.0`, `192.168.1.70` alla rete `192.168.1.64`. Sono in reti diverse, anche se differiscono di poco: per comunicare serve un router.

## 2.3.3 Dalle classi al CIDR

Fino al 1993 la maschera era implicita nei primi bit dell'indirizzo, secondo le **classi**:

| Classe | Primi bit | Primo ottetto | Maschera implicita | Uso |
|---|---|---|---|---|
| A | 0 | 0-127 | /8 | reti molto grandi |
| B | 10 | 128-191 | /16 | reti medie |
| C | 110 | 192-223 | /24 | reti piccole |
| D | 1110 | 224-239 | | multicast |
| E | 1111 | 240-255 | | riservata |

Il sistema sprecava indirizzi: un'organizzazione con 2000 dispositivi riceveva una classe B da 65 534 host. Il **CIDR** (Classless Inter-Domain Routing, RFC 4632) ha reso il prefisso libero, da /0 a /32, e ha permesso di assegnare blocchi della dimensione necessaria e di riassumere più reti in un solo prefisso (aggregazione, lezione 2.4). Il termine "classe C" per indicare una rete /24 resta nell'uso comune. Approfondimento: https://it.wikipedia.org/wiki/Classless_Inter-Domain_Routing

## 2.3.4 Indirizzi con usi speciali

| Blocco | Uso |
|---|---|
| 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 | **indirizzi privati** (RFC 1918): liberi per le reti interne, non instradati su Internet; per uscire serve la traduzione NAT (lezione 3.3) |
| 127.0.0.0/8 | **loopback**: il computer stesso (`127.0.0.1`, usato dai server dei laboratori) |
| 169.254.0.0/16 | **link-local**: indirizzo che il sistema si assegna da solo se non riceve risposta dal server DHCP (scheda A della lezione 1.3) |
| 100.64.0.0/10 | spazio condiviso dei fornitori di accesso, usato per il NAT su larga scala (CGNAT) |
| 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 | **documentazione**: riservati agli esempi, come `203.0.113.80` nella lezione 1.2 |
| 0.0.0.0 | "nessun indirizzo" o "tutti gli indirizzi locali", secondo il contesto |
| 255.255.255.255 | broadcast limitato alla rete locale |

Gli indirizzi IPv4 sono circa 4,3 miliardi, meno dei dispositivi collegati: nel 2011 l'organismo centrale IANA ha assegnato gli ultimi blocchi liberi ai registri regionali, e il registro europeo RIPE NCC ha esaurito le proprie riserve nel 2019 (https://www.ripe.net/publications/news/the-ripe-ncc-has-run-out-of-ipv4-addresses/ ). Le risposte sono gli indirizzi privati con il NAT e, a lungo termine, IPv6 (lezione 2.5).

## 2.3.5 Laboratorio

Tempo indicativo: 45 minuti. Cartella di lavoro `C:\corso-reti\lab23`, con i file della cartella `laboratorio`.

### Parte 1: esercizi a mano

Per ogni indirizzo calcolare maschera in decimale, indirizzo di rete, broadcast, primo e ultimo host, numero di host; scrivere in binario almeno l'ottetto interessante.

1. `192.168.5.130/25`
2. `10.45.200.17/20`
3. `172.18.99.250/27`
4. `192.168.1.66` con maschera `255.255.255.240`
5. `10.0.0.1/30`
6. `192.168.1.60/26` e `192.168.1.70/26` sono nella stessa rete?
7. `100.70.3.4/10`: è un indirizzo privato secondo l'RFC 1918? Che cos'è?
8. Scrivere in binario `172.16.254.1`.

### Parte 2: verifica con Python

```powershell
python calcolo_ipv4.py 10.45.200.17/20
```

```text
Indirizzo  10.45.200.17     00001010.00101101.11001000.00010001
Maschera   255.255.240.0    11111111.11111111.11110000.00000000   (/20)
Rete       10.45.192.0      00001010.00101101.11000000.00000000   (indirizzo AND maschera)
Broadcast  10.45.207.255    00001010.00101101.11001111.11111111   (parte host tutta a 1)
Host       da 10.45.192.1 a 10.45.207.254: 4094 indirizzi usabili su 4096
Classe storica A; privato (RFC 1918): sì
Confronto con ipaddress: concorde
```

Lo script esegue i calcoli con le operazioni sui bit, come a mano, e li confronta con il modulo `ipaddress` della libreria standard:

```python
def maschera_da_prefisso(prefisso):
    return (0xFFFFFFFF << (32 - prefisso)) & 0xFFFFFFFF   # prefisso bit a 1, poi bit a 0

rete = ip & maschera                          # AND: azzera la parte host
broadcast = rete | (~maschera & 0xFFFFFFFF)   # OR con la parte host tutta a 1
```

- `0xFFFFFFFF` è il numero con 32 bit a 1; `<<` sposta i bit a sinistra, inserendo zeri a destra; `& 0xFFFFFFFF` elimina i bit oltre il trentaduesimo (gli interi di Python non hanno un limite di bit)
- `~` inverte tutti i bit: `~maschera` ha 1 nella parte host
- `|` (OR) mette a 1 i bit che sono a 1 in almeno uno dei due numeri
- `ip_a_intero` costruisce il numero a 32 bit spostando di 8 bit a sinistra e aggiungendo un ottetto alla volta

Con `python calcolo_ipv4.py --esercizi 5` lo script propone cinque indirizzi casuali, chiede rete, broadcast e numero di host e corregge le risposte con `ipaddress`.

Test: `python test_calcolo_ipv4.py` (17 test, tra cui il confronto con `ipaddress` su 990 indirizzi casuali con tutti i prefissi da /0 a /32).

### Parte 3: il modulo ipaddress in modalità interattiva

Nel terminale di VS Code avviare `python` e provare:

```python
>>> import ipaddress
>>> rete = ipaddress.ip_network("192.168.10.0/26")
>>> rete.netmask, rete.broadcast_address, rete.num_addresses
(IPv4Address('255.255.255.192'), IPv4Address('192.168.10.63'), 64)
>>> ipaddress.ip_address("192.168.10.77") in rete
False
>>> ipaddress.ip_address("192.168.10.77").is_private
True
>>> ipaddress.ip_interface("192.168.10.77/26").network
IPv4Network('192.168.10.64/26')
```

`ip_network` rifiuta un indirizzo che non sia quello di rete (`ip_network("192.168.10.77/26")` produce un errore); `ip_interface` accetta un indirizzo qualsiasi con il suo prefisso e ne ricava la rete.

### Parte 4: maschere incoerenti in Filius

1. Riaprire `lab21_switch.fls`. Cambiare la configurazione di `PC-4`: indirizzo `192.168.1.140`, maschera `255.255.255.128`. Gli altri PC restano con `/24`.
2. In simulazione eseguire da `PC-1` `ping 192.168.1.140`, e da `PC-4` `ping 192.168.1.11`.
3. Nessuno dei due funziona. Calcolare la rete di ciascun indirizzo con la maschera del rispettivo PC e spiegare perché: che cosa conclude `PC-1` sul destinatario? E `PC-4`?
4. Ripristinare la maschera `/24` su `PC-4` e verificare che il `ping` funzioni.

### Attività

1. Aggiungere a `calcolo_ipv4.py` una funzione `stessa_rete(a, b, prefisso)` che restituisca `True` se i due indirizzi sono nella stessa rete, con un test per l'esercizio 6.
2. Quale prefisso serve per una rete con 500 dispositivi? E con 1000?
3. `ipconfig` mostra indirizzo e maschera del proprio PC: calcolare rete e broadcast della rete della scuola e verificare con lo script.

## 2.3.6 Aspetti orientativi (discussione)

- Il calcolo delle sottoreti è una competenza di base richiesta nei colloqui e nelle certificazioni per tecnici di rete e sistemisti; con la pratica diventa rapido anche a mente.
- Gli strumenti come `ipaddress` evitano errori, ma servono a verificare un ragionamento, non a sostituirlo: un errore di maschera in un apparato di rete può isolare un intero reparto.
- Domanda: perché due PC con maschere diverse nella stessa rete fisica possono comunicare in un verso e non nell'altro, o per nulla?
