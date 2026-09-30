---
title: "Lezione 3.4: soluzioni degli esercizi"
subtitle: "Modulo 3: Crittografia pratica. Materiale per il docente"
lang: it
---

# Lezione 3.4: soluzioni degli esercizi

Risultati verificati con CyberChef 11.5.0 (versione offline, build del 26/09/2026) e con `verifica_con_python.py`.

## Esercizio 1

| Input | To Hex | To Base64 |
|---|---|---|
| `Ciao` | `43 69 61 6f` | `Q2lhbw==` |
| `Ciao!` | | `Q2lhbyE=` |
| `Ciao!!` | | `Q2lhbyEh` |

Base64 codifica gruppi di 3 byte in 4 caratteri: con 4 byte restano 1 byte finale e due `=`, con 5 byte ne restano 2 e un `=`, con 6 byte nessun riempimento.

## Esercizio 2

`Password del Wi-Fi ospiti: Aula-Magna-2026`

Contromisure: il file di configurazione leggibile solo dall'account del servizio (lezione 2.4); segreti conservati in un archivio dedicato o in variabili d'ambiente del servizio; se la password deve essere salvata cifrata, la chiave va conservata altrove, per esempio nel sistema operativo (su Windows, DPAPI). Codificare non protegge.

## Esercizio 3

Ricetta: **From Base64**, poi **From Hex**. Risultato: `Verifica di informatica spostata a giovedì`. Magic la propone per prima, indicando l'italiano come lingua probabile e UTF-8 valido. Indizio per l'ipotesi iniziale: il `=` finale e l'alfabeto indicano Base64; il risultato del primo passo contiene solo cifre e lettere da `a` a `f`, cioè esadecimale.

## Esercizio 4

- SHA-256 di `ciao`: `b133a0c0e9bee3be20163d2ad31d6248db292aa6dcb1ee087a2aa50e0fc75ae2`
- SHA-256 di `Ciao`: `25c73520e69f4bf229811e8e46ffe7d80471544b9bee15ed25044b86be4115ad`

Nessuna somiglianza sistematica (effetto valanga); coincidenze isolate di singoli caratteri nella stessa posizione sono casuali. L'impronta ha sempre 64 cifre esadecimali. From Hex applicato all'impronta produce solo 32 byte privi di significato: l'hash non contiene il testo originale.

## Esercizio 5

1. Amount 23 (equivalente a spostare indietro di 3): `Appuntamento in biblioteca alle quindici`. Al massimo 25 tentativi.
2. `Il club di informatica si riunisce in aula dodici alle quindici`

## Esercizio 6

1. Messaggio: `Il laboratorio di domani inizia alle 10:30 in aula 12`
2. Chiave con ultima cifra `9`: messaggio di errore "Unable to decrypt input with these parameters." (padding non valido).
3. IV con prima cifra `1`: risultato `Yl laboratorio di domani inizia alle 10:30 in aula 12`. In CBC il primo blocco in chiaro si ottiene con XOR tra il blocco decifrato e l'IV: modificare un bit dell'IV modifica lo stesso bit del primo blocco in chiaro, e nient'altro. Conseguenza: la modalità CBC da sola non protegge l'integrità; per questo in TLS si usano modalità autenticate come GCM.

## Esercizio 7

- Chiave e IV trasmessi sullo stesso canale del cifrato annullano la protezione: problema della distribuzione delle chiavi (lezioni 3.1 e 3.2). L'IV può viaggiare in chiaro; la chiave no.
- Stessa chiave, stesso IV, stesso messaggio: cifrati identici. Chi osserva capisce quando un messaggio si ripete. Con un IV casuale per ogni messaggio i cifrati sono sempre diversi.

## Esercizio 8

| Dato | Entropia (bit per byte) |
|---|---|
| Messaggio in chiaro (53 byte) | 3,837 |
| Messaggio in Base64 (72 caratteri) | 4,848 |
| Cifrato AES (64 byte) | 5,769 (massimo possibile 6) |

Il Base64 ha entropia maggiore del testo perché usa un alfabeto più uniforme, ma non può superare log2(64) = 6 bit per carattere, dato che usa solo 64 simboli: con testi lunghi resta sotto 6, mentre un cifrato lungo si avvicina a 8.

## Attività conclusiva: risposte attese

1. La codifica non usa chiavi, è pubblica e invertibile da chiunque, serve a rappresentare dati; la cifratura usa una chiave segreta, è invertibile solo con la chiave, serve alla riservatezza.
2. L'hash ha lunghezza fissa per input di qualsiasi lunghezza: infiniti input hanno la stessa impronta e l'informazione dell'input non è contenuta nel risultato. Si può solo provare input diversi e confrontare le impronte.
3. Due codifiche in sequenza restano codifiche: Magic le inverte in un istante. Servono cifratura con una chiave protetta e controllo degli accessi.
