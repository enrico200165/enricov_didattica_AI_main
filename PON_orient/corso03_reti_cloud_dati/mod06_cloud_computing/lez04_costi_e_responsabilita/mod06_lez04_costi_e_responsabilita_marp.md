---
marp: true
paginate: true
lang: it
---

## Lezione 6.4: Costi e responsabilità

Modulo 6: Cloud computing. Reti, Cloud e Gestione dei Dati

---

## Come si paga

- A consumo, con impegno, interrompibile, per utente
- Calcolo, dischi, oggetti, database, traffico in uscita
- Controllo: budget, avvisi, etichette, spegnimento, dimensioni giuste

---

## Responsabilità condivisa

| Area | IaaS | PaaS | SaaS |
|---|---|---|---|
| Dati, account, accessi | cliente | cliente | cliente |
| Sistema operativo | cliente | fornitore | fornitore |
| Infrastruttura fisica | fornitore | fornitore | fornitore |

---

## Dove sono i dati

- Regione scelta e copie di sicurezza
- GDPR: trasferimenti fuori dall'UE a condizioni precise
- Sovranità digitale; lock-in

---

## Laboratorio

1. `python costi_cloud.py`: tre scenari, voce principale
2. `--locale`: confronto con un server della scuola
3. Macchine dimenticate accese; tabella delle responsabilità; 10 test

---

## Aspetti orientativi

- FinOps: tecnica ed economia
- Scelta dei fornitori: tecnici e giuristi insieme
- Cloud o server proprio: da che cosa dipende?
