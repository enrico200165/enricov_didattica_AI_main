---
title: "Lezione 7.3: piano di riferimento"
subtitle: "Modulo 7: Dati, privacy e continuità. Materiale per il docente"
lang: it
---

# Lezione 7.3: piano di riferimento

Una soluzione possibile per lo scenario della parte 1 (4 PC, server di file da 200 GB con crescita di circa 1 GB al mese, 15 minuti settimanali di tempo disponibile).

- **Dati**: cartelle condivise del server; documenti locali dei PC reindirizzati sul server, così che i PC non contengano dati da salvare; esportazioni periodiche dei servizi cloud che lo consentono.
- **Obiettivi**: RPO 24 ore; RTO 1 giorno lavorativo per i documenti correnti, 3 giorni per l'archivio completo.
- **Copie**:
  - copia 1: disco di rete (NAS) in un locale diverso dal server, backup incrementale ogni notte, completo ogni settimana, con istantanee (snapshot) non modificabili per 14 giorni;
  - copia 2: servizio di backup cloud con versioni e protezione dalla cancellazione, incrementale ogni notte;
  - copia scollegata: due dischi esterni a rotazione, backup completo settimanale, conservati fuori sede e collegati solo durante il backup.
- **Conservazione**: 14 giornaliere, 8 settimanali, 12 mensili; 1 annuale conservata 5 anni o secondo gli obblighi di conservazione dei documenti.
- **Protezione**: cifratura AES-256 di tutte le copie; chiavi in un gestore di password aziendale e in busta sigillata in cassaforte; accesso ai backup con account separati dagli account di uso quotidiano, con MFA per il cloud.
- **Verifiche**: controllo automatico giornaliero con avviso via email in caso di errore; ripristino di alcuni file ogni settimana (entro i 15 minuti disponibili); ripristino completo in ambiente di prova ogni sei mesi, registrato.
- **Rischi residui**: dati creati nella giornata in corso (RPO); guasto contemporaneo di NAS e servizio cloud con dischi esterni non aggiornati da una settimana.

Risposte alle attività della parte 2:

1. Il ripristino del secondo backup restituisce i file com'erano in quel momento, compreso il file cancellato dopo; è il motivo per cui si conservano più versioni.
2. `verifica` segnala "impronta diversa" per il file modificato; se il programma di compressione ricrea l'archivio, anche il controllo interno dello ZIP resta valido, mentre le impronte no.
3. No: lo script crea copie in un solo luogo e su un solo supporto; mancano la seconda copia, il luogo diverso e la copia scollegata, oltre alla cifratura e alla pianificazione automatica (per esempio con l'Utilità di pianificazione di Windows).
