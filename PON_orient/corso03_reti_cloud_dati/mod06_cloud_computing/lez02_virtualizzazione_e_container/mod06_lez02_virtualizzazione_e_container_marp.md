---
marp: true
paginate: true
lang: it
---

## Lezione 6.2: Virtualizzazione e container

Modulo 6: Cloud computing. Reti, Cloud e Gestione dei Dati

---

## Macchine virtuali

- Hypervisor di tipo 1 (data center) e di tipo 2 (PC)
- Un server fisico, molti sistemi isolati
- Snapshot, copia, spostamento

---

## Container

| | VM | Container |
|---|---|---|
| Contiene | sistema operativo | applicazione e librerie |
| Avvio | minuti | secondi |
| Kernel | proprio | condiviso |

- Immagine (modello) e container (istanza)

---

## Orchestrazione

- Stato desiderato dichiarato
- Collocazione, autoriparazione, scalabilità
- Bilanciamento, aggiornamenti progressivi
- Kubernetes

---

## Laboratorio

1. Cinque scenari: server, VM o container?
2. Dockerfile del servizio della biblioteca, istruzione per istruzione
3. `python orchestratore.py`: guasto di un nodo, repliche in attesa; 8 test

---

## Aspetti orientativi

- Sistemisti e DevOps
- Kubernetes tra le competenze più richieste
- VM di clienti diversi sullo stesso server: quali garanzie?
