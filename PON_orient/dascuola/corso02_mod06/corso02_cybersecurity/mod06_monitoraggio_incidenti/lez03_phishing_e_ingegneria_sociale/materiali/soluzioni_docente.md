---
title: "Lezione 6.3: soluzioni"
subtitle: "Modulo 6: Monitoraggio e risposta agli incidenti. Materiale per il docente"
lang: it
---

# Lezione 6.3: soluzioni

## Parte 1: messaggi di esempio

| Messaggio | Valutazione | Segnali | Leve | Azione |
|---|---|---|---|---|
| A | sospetto (phishing di credenziali) | dominio del mittente diverso da `scuola.example`; collegamento verso `verifica-account.example`; richiesta di credenziali; saluto generico | urgenza, paura di perdere dati, autorità | non fare clic; segnalare; eventualmente verificare lo spazio della casella dal sito ufficiale |
| B | legittimo | mittente del dominio della scuola; nessuna richiesta di dati; rimanda alla piattaforma nota senza collegamento; tono coerente | nessuna | accedere alla piattaforma nel modo abituale |
| C | sospetto (smishing) | mittente sconosciuto; dominio non del corriere; richiesta di pagamento piccolo, tipica per ottenere i dati della carta | urgenza, curiosità | non aprire; verificare dal sito o dall'app del corriere |
| D | sospetto (frode del finto dirigente) | indirizzo personale su un servizio gratuito; richiesta di carte regalo; impossibilità di telefonare; segretezza | autorità, urgenza, segretezza | verificare di persona o al numero noto; segnalare |
| E | legittimo, da verificare con le intestazioni | dominio della scuola; notifica attesa; nessuna richiesta di dati | nessuna | accedere dalla piattaforma; `email_legittima.eml` mostra SPF, DKIM e DMARC superati |
| F | sospetto (furto del codice MFA) | contatto sconosciuto; richiesta del codice ricevuto per SMS | autorità, fiducia | non comunicare mai il codice; segnalare all'assistenza vera |

Risposta alla domanda finale: il messaggio D non contiene nulla che un filtro automatico possa riconoscere (collegamenti, allegati, domini noti come malevoli); tutta la frode si basa sulla manipolazione e l'unica difesa è la verifica con un altro canale.

## Parte 2: intestazioni

- Server di origine del messaggio sospetto: `mailer.invii-massivi.example` (`203.0.113.77`), riga `Received` più bassa.
- Sei segnali tecnici: SPF `fail`, DKIM `none`, DMARC `fail`, Reply-To su `posta-gratuita.example`, Return-Path su `mailer.invii-massivi.example`, collegamento con testo ingannevole.
- Messaggio legittimo: SPF, DKIM e DMARC `pass`; collegamento coerente con il testo; nessun segnale.
