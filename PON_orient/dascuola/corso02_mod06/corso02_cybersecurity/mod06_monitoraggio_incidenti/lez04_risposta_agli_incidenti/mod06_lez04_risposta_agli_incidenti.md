---
title: "Lezione 6.4: Risposta agli incidenti"
subtitle: "Modulo 6: Monitoraggio e risposta agli incidenti. Cybersecurity ed Ethical Hacking"
lang: it
---

# Lezione 6.4: Risposta agli incidenti

> Contenuto originale. Riferimenti: NIST SP 800-61 revisione 3 (aprile 2025); Regolamento (UE) 2016/679 (GDPR), articoli 33 e 34; D.Lgs. 138/2024 (recepimento della direttiva NIS2); progetto No More Ransom. Lo scenario dell'esercitazione è nella cartella `esercitazione`.

Obiettivo: conoscere le fasi della gestione di un incidente di sicurezza, le decisioni tipiche di ciascuna e gli obblighi di notifica, e applicarle in un'esercitazione a tavolino su uno scenario di ransomware.

## 6.4.1 Eventi e incidenti

- **Evento di sicurezza**
  qualsiasi fatto osservabile rilevante per la sicurezza: un accesso fallito, un allarme dell'antivirus, un messaggio sospetto segnalato.
- **Incidente di sicurezza**
  evento, o insieme di eventi, che compromette o minaccia concretamente la riservatezza, l'integrità o la disponibilità di dati e servizi.
- **Violazione dei dati personali** (data breach)
  incidente che comporta la distruzione, la perdita, la modifica, la divulgazione o l'accesso non autorizzati a dati personali (GDPR, modulo 7).

La **risposta agli incidenti** (incident response) è l'insieme organizzato di attività con cui si limita il danno, si ripristina il funzionamento e si evita che l'incidente si ripeta. Funziona solo se preparata prima: durante un incidente non c'è tempo per decidere chi fa che cosa.

## 6.4.2 Le fasi

Un modello molto usato nella didattica e nelle procedure aziendali descrive sei fasi:

- **Preparazione**
  piano di risposta scritto, ruoli e contatti (anche fuori orario), strumenti, backup verificati e scollegati, registri degli eventi, esercitazioni.
- **Rilevazione e analisi**
  riconoscere che è in corso un incidente, capirne la natura, l'estensione e la gravità, aprire un registro delle attività con orari e decisioni.
- **Contenimento**
  fermare l'estensione del danno: isolare dalla rete i sistemi colpiti, disattivare gli account compromessi, bloccare indirizzi o domini. Si preservano le **evidenze**: copie dei log, dei messaggi, dello stato dei sistemi, prima di modificarli.
- **Eradicazione**
  eliminare la causa: rimuovere il software malevolo, chiudere la vulnerabilità sfruttata, cambiare le credenziali esposte.
- **Ripristino**
  riportare i servizi in funzione da fonti pulite (backup verificati, reinstallazione), con un monitoraggio più attento nel periodo successivo.
- **Lezioni apprese**
  analisi dopo l'incidente, senza ricerca di colpevoli: che cosa è successo, che cosa ha funzionato, che cosa cambiare in procedure, strumenti e formazione.

Diagramma: il ciclo della risposta agli incidenti.

```mermaid
flowchart LR
    P["Preparazione"] --> R["Rilevazione<br/>e analisi"]
    R --> C["Contenimento"]
    C --> E["Eradicazione"]
    E --> Ri["Ripristino"]
    Ri --> L["Lezioni apprese"]
    L --> P
    C -.->|nuove informazioni| R
```

Le fasi non sono rigidamente sequenziali: nuove informazioni raccolte durante il contenimento possono richiedere di tornare all'analisi. La revisione 3 della guida del NIST (SP 800-61r3, aprile 2025) ha abbandonato il proprio vecchio ciclo in quattro fasi e colloca le attività di risposta all'interno delle funzioni del NIST Cybersecurity Framework 2.0 (governare, identificare, proteggere, rilevare, rispondere, recuperare), sottolineando che la risposta fa parte della gestione complessiva del rischio: https://csrc.nist.gov/pubs/sp/800/61/r3/final

## 6.4.3 Ransomware

Il **ransomware** cifra i dati dei sistemi colpiti e chiede un riscatto per la chiave di decifratura; spesso chi attacca copia prima i dati e minaccia di pubblicarli (**doppia estorsione**). Vie d'ingresso frequenti: phishing (lezione 6.3), credenziali rubate su servizi di accesso remoto, vulnerabilità non corrette in sistemi esposti.

Indicazioni generali:

- **isolare** subito i dispositivi colpiti dalla rete (cavo, Wi-Fi), senza spegnerli se non indicato dagli specialisti: lo stato del sistema può contenere informazioni utili
- **non pagare**: il pagamento non garantisce la restituzione dei dati, finanzia le organizzazioni criminali e segnala che la vittima è disposta a pagare. Il progetto **No More Ransom**, sostenuto da Europol e dalla polizia olandese, raccoglie strumenti di decifratura gratuiti per diverse famiglie di ransomware: https://www.nomoreransom.org/it/index.html
- **ripristinare da backup** conservati scollegati o non modificabili (regola 3-2-1, modulo 7), dopo aver eliminato la causa
- **denunciare** l'accaduto alla Polizia Postale e delle Comunicazioni

## 6.4.4 Notifiche obbligatorie

| Norma | Quando | A chi | Termini |
|---|---|---|---|
| GDPR, articolo 33 | violazione di dati personali, salvo che sia improbabile un rischio per le persone | Garante per la protezione dei dati personali | senza ingiustificato ritardo e, ove possibile, entro 72 ore da quando se ne è venuti a conoscenza |
| GDPR, articolo 34 | violazione con rischio elevato per i diritti e le libertà delle persone | persone interessate | senza ingiustificato ritardo |
| D.Lgs. 138/2024 (NIS2) | incidente significativo in un soggetto che rientra nell'ambito della normativa | CSIRT Italia, presso l'Agenzia per la cybersicurezza nazionale | pre-notifica entro 24 ore, notifica entro 72 ore, relazione finale entro un mese |

Riferimenti: https://it.wikipedia.org/wiki/Regolamento_generale_sulla_protezione_dei_dati ; sintesi degli obblighi NIS2 in Italia: https://www.legiscope.com/blog/nis2-notifica-incidenti-acn.html

Le due notifiche sono indipendenti: se un incidente NIS2 riguarda anche dati personali, vanno fatte entrambe. Per una scuola statale il titolare del trattamento è l'istituzione scolastica, rappresentata dal dirigente, con il supporto del responsabile della protezione dei dati (DPO); la decisione su che cosa notificare spetta a loro, non al personale tecnico.

## 6.4.5 Esercitazione a tavolino

Un'**esercitazione a tavolino** (tabletop exercise) simula un incidente con una discussione guidata: i partecipanti, ciascuno con un ruolo, ricevono informazioni in momenti successivi e decidono che cosa fare. Serve a verificare piani, ruoli e comunicazioni senza toccare alcun sistema.

Tempo indicativo: 45 minuti. Materiale: `esercitazione/scenario_ransomware.md` per la classe; `esercitazione/guida_docente.md` per chi conduce.

Organizzazione:

1. la classe si divide in gruppi di 5-6 persone; in ogni gruppo si assegnano i ruoli: **dirigente scolastico**, **referente tecnico**, **DSGA e segreteria**, **responsabile della protezione dei dati**, **responsabile della comunicazione**, **segretario** che annota decisioni e orari
2. il docente legge la situazione iniziale e, a intervalli, gli sviluppi successivi (inject)
3. dopo ogni sviluppo ogni gruppo ha 5-7 minuti per rispondere alle domande e annotare le decisioni
4. discussione finale comune (10 minuti): decisioni diverse tra i gruppi, punti in cui mancavano informazioni o procedure, tre azioni di preparazione da proporre alla scuola

## 6.4.6 Aspetti orientativi (discussione)

- La risposta agli incidenti è svolta da gruppi specializzati (CSIRT, CERT), interni o esterni; l'analisi forense digitale è una specializzazione con competenze tecniche e giuridiche.
- La gestione di un incidente è anche comunicazione e decisione sotto pressione: dirigenti, esperti legali, responsabili della comunicazione lavorano insieme ai tecnici.
- Le esercitazioni sono richieste da molte norme e standard: organizzarle e condurle è un'attività professionale.
- Domanda: quali decisioni dell'esercitazione dipendevano da scelte fatte, o non fatte, molto prima dell'incidente?
