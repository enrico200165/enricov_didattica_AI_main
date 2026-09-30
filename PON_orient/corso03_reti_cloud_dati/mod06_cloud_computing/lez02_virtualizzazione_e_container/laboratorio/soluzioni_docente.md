---
title: "Lezione 6.2: tracce di soluzione"
subtitle: "Modulo 6: Cloud computing. Materiale per il docente"
lang: it
---

# Lezione 6.2: tracce di soluzione

## Scenari

| N. | Scelta | Motivo |
|---|---|---|
| 1 | macchina virtuale (hypervisor di tipo 2 sul PC) | serve un sistema operativo diverso e completo; snapshot per tornare allo stato iniziale |
| 2 | container | la stessa immagine gira identica in sviluppo e nel cloud |
| 3 | macchina virtuale | kernel diverso (Windows) rispetto agli altri servizi (Linux) |
| 4 | container con orchestrazione (o VM con scalabilità automatica) | repliche aggiunte e tolte in pochi secondi secondo il carico |
| 5 | server fisico dedicato | tempi di risposta garantiti, nessuna condivisione di risorse |

## Dockerfile

1. Il servizio deve ascoltare su `0.0.0.0` (tutte le interfacce del container), per esempio con un parametro o una variabile d'ambiente; `-p 8000:8000` collega poi la porta 8000 del PC a quella del container.
2. Il file del database fa parte del container: eliminando il container si perdono le modifiche. Soluzioni: un **volume** (cartella esterna al container, montata con `docker run -v`) oppure un database gestito separato dal container.
3. Se una vulnerabilità del servizio permette di eseguire comandi, l'attaccante ottiene solo i permessi dell'utente `servizio`, non quelli di amministratore del container.

Il Dockerfile non è stato costruito nell'ambiente di preparazione (Docker non disponibile): istruzioni e sintassi seguono la documentazione ufficiale. Il docente che vuole mostrarne la costruzione ha bisogno di Docker Desktop o di Podman sul proprio PC, e deve prima applicare la modifica della domanda 1.

## Orchestratore

Attività 2: con due nodi guasti resta solo `nodo-c` (1000 millesimi): due repliche in esecuzione, le altre in attesa.
