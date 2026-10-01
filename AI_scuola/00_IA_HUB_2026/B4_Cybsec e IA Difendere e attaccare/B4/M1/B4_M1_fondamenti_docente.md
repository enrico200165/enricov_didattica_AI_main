---
title: "Modulo 1 - Fondamenti di sicurezza"
subtitle: "B.4 - Cybersicurezza e IA. Traccia docenti"
lang: it
---

# Modulo 1 - Traccia docenti

## Collocazione e finalità del modulo

Il modulo 1 (lezioni L1-L4) fornisce il lessico e i prerequisiti tecnici usati in tutto il corso. Non è un'introduzione generale alle reti o alla crittografia: ogni contenuto è stato scelto perché serve in un punto preciso dei moduli successivi.

| Contenuto del modulo 1 | Dove viene usato |
|---|---|
| triade RID, minaccia, vulnerabilità, rischio | in ogni analisi di caso, nel progetto finale (L17) |
| anatomia di URL, intestazioni email, SPF/DKIM/DMARC | phishing (L8-L9) |
| hash, sale, funzioni lente | attacchi e difese delle password (L5-L6) |
| cifratura asimmetrica, firma | passkey (L7) |
| ingegneria sociale, leve psicologiche | phishing generato con IA (L9) |
| malware, infostealer, cookie di sessione | autenticazione multifattore e suoi limiti (L7) |
| difese di base, risposta agli incidenti | carta d'uso sicuro (L15), progetto finale |

Segmenti di traccia docenti in aula: 10 minuti al termine di L1 (patto d'aula, regole del laboratorio) e 10 minuti al termine di L4 (uso delle fonti istituzionali, gestione delle esperienze personali degli studenti).

## Logica della progettazione

### L1: partire dai casi reali italiani

La lezione introduce i termini (RID, minaccia, vulnerabilità, rischio) e li applica subito a notizie reali del CERT-AGID. La scelta ha tre motivi:

- i termini astratti diventano strumenti di analisi, non definizioni da memorizzare
- gli studenti riconoscono enti e servizi che conoscono (ACI, Agenzia delle Entrate, Servizio Sanitario Nazionale), e percepiscono che il tema li riguarda
- il CERT-AGID pubblica in italiano, con cadenza settimanale: il docente dispone di materiale sempre aggiornato senza doverlo produrre

La parte legale è collocata nella prima lezione, prima di qualunque attività di attacco, perché fissa il confine entro cui si svolge tutto il corso.

### L2: prerequisiti mirati al phishing

L2 contiene solo la parte di funzionamento della rete necessaria a leggere un URL e un'email. Il concetto chiave è il dominio registrato: gli studenti tendono a cercare il nome dell'organizzazione in qualunque punto dell'URL. L'esercizio sui dodici URL è costruito per smontare questa abitudine con casi progressivamente meno evidenti (sottodominio fuorviante, `@`, dominio nel percorso, omografo, link accorciato).

Il secondo concetto chiave è che i controlli tecnici (lucchetto, SPF, DKIM, DMARC) verificano l'identità di un dominio, non la sua onestà. L'email 3 del laboratorio supera tutti i controlli ed è fraudolenta: è il caso che fa emergere la differenza.

Tutti gli esempi usano il TLD `.example`, riservato alla documentazione (RFC 2606): non esistono siti reali con quei nomi e gli esempi non puntano a organizzazioni reali.

### L3: tre trasformazioni da non confondere

La confusione tra codifica, cifratura e hash è frequente anche tra adulti ("la password è criptata in Base64"). La lezione le presenta insieme, con lo stesso dato di partenza, per mettere in evidenza la differenza: la presenza o l'assenza di una chiave, la reversibilità.

La crittografia asimmetrica è trattata a livello concettuale, senza algoritmi. Serve solo a capire certificati, firma e passkey. Il dettaglio sulle funzioni lente per le password anticipa il modulo 2, dove la differenza tra attacco in linea e fuori linea è centrale.

### L4: il fattore umano

La lezione accosta malware e ingegneria sociale perché negli attacchi reali sono inseparabili: quasi ogni infezione inizia con un messaggio che convince qualcuno ad aprire un file. La tabella delle leve psicologiche verrà riutilizzata in L8 e in L9 come griglia di analisi dei messaggi.

La sezione sulla risposta agli incidenti è volutamente pratica: è la parte che gli studenti possono applicare subito, per sé e per le proprie famiglie.

## Patto d'aula

Da presentare e condividere in L1, prima dei laboratori. Testo proposto:

1. Le tecniche di attacco presentate nel corso si studiano per imparare a difendersi.
2. Si sperimentano solo sui materiali forniti dal docente e sulle piattaforme indicate.
3. Non si attaccano sistemi reali, la rete della scuola, i dispositivi o gli account di altre persone, neppure per scherzo.
4. Non si fanno ricerche su persone reali, compagni compresi.
5. Non si inseriscono password o dati personali reali negli esercizi.
6. Chi scopre per caso una vulnerabilità in un sistema della scuola lo segnala al docente, senza sfruttarla.

Il punto 6 introduce il concetto di divulgazione responsabile (responsible disclosure) e offre agli studenti più curiosi un comportamento corretto alternativo alla sperimentazione non autorizzata.

## Preparazione del laboratorio

### Materiali

| File | Lezione | Note |
|---|---|---|
| `L1_scheda_analisi_casi.md` | L1 | contiene i link alle due notizie; preparare la versione stampata in caso di rete assente |
| `L2_url_da_analizzare.txt` | L2 | |
| `L2_email_1.eml`, `L2_email_2.eml`, `L2_email_3.eml` | L2 | da aprire con un editor di testo |
| `L3_messaggio_cifrato.txt` | L3 | |
| `L3_programma_didattico.txt`, `L3_hash_pubblicati.txt` | L3 | distribuire senza aprire e salvare `L3_programma_didattico.txt`: un editor che cambia i caratteri di fine riga o la codifica modifica l'hash |
| `L4_scheda_campagne.md` | L4 | contiene i link ai tre casi |

I file `.eml` sono file di testo; su Windows il doppio clic li apre con il programma di posta predefinito. Per evitarlo, far usare il menu contestuale `Apri con` e scegliere Blocco note, oppure rinominarli in `.txt` prima della distribuzione.

### Checklist prima di L2 e L3

- verificare che il sito istituzionale scelto per l'esercizio sul certificato sia raggiungibile dalla rete della scuola
- scaricare la versione offline di CyberChef (pulsante `Download CyberChef` sulla pagina https://gchq.github.io/CyberChef/), estrarla in una cartella condivisa o su chiavetta, verificare che il file HTML si apra con il browser delle postazioni
- provare le operazioni del laboratorio L3 in CyberChef: i nomi delle operazioni sono in inglese, conviene preparare una tabella di corrispondenza da proiettare

### Rete assente

- L1 e L4: notizie stampate
- L2: tutto il laboratorio è offline tranne l'esercizio 2 (certificato); in alternativa mostrarlo dal PC del docente con la connessione mobile
- L3: CyberChef offline

## Conduzione delle lezioni

### Distribuzione del tempo

| Lezione | Spiegazione | Laboratorio | Chiusura |
|---|---|---|---|
| L1 | 25 min: termini (10), attaccanti e fasi (5), difesa in profondità e legge (10) | 25 min | 10 min di traccia docenti: patto d'aula |
| L2 | 25 min: DNS e URL (10), HTTPS (5), email e domini ingannevoli (10) | 30 min | 5 min |
| L3 | 25 min: tre trasformazioni (5), cifratura (10), hash e password (10) | 30 min | 5 min |
| L4 | 25 min: malware (8), ingegneria sociale (8), difese e incidenti (9) | 25 min | 10 min di traccia docenti |

Se il tempo non basta:

- L1: la tabella degli attaccanti si può leggere rapidamente
- L2: il DNS si può ridurre alla metafora della rubrica
- L3: l'esercizio 6 si può assegnare a casa

### Dimostrazioni consigliate

- L2: aprire dal vivo un file `.eml` con l'editor e poi mostrare lo stesso messaggio in un programma di posta (per esempio Thunderbird, se disponibile, con la rete disattivata), per far vedere quanto delle intestazioni resta nascosto
- L2: nel browser, passare il mouse su un link di una pagina e mostrare la destinazione nella barra di stato in basso
- L3: in CyberChef, digitare lentamente una frase nell'Input con `SHA2` nella ricetta: a ogni carattere l'hash cambia completamente; è la dimostrazione più efficace dell'effetto valanga

### Difficoltà frequenti

| Difficoltà | Come intervenire |
|---|---|
| lo studente cerca il nome della banca "ovunque" nell'URL | far individuare prima il TLD, poi leggere il nome immediatamente a sinistra; ripetere su tutti i dodici URL |
| confusione tra `.example` e un TLD reale | ricordare che `.example` sostituisce `.it` o `.com` solo per evitare nomi reali |
| "il sito ha il lucchetto quindi è sicuro" | riprendere la distinzione: cifrato non significa onesto |
| "Base64 è una cifratura" | chiedere dov'è la chiave; senza chiave non c'è cifratura |
| "l'hash si può decifrare" | un hash non si decifra; si può solo provare a indovinare il dato di partenza e confrontare gli hash (tema di L5) |
| racconti di truffe subite in famiglia | valorizzarli come esempi senza chiedere dettagli personali; spostare il discorso sul meccanismo |

### Esperienze personali degli studenti

Durante L4 alcuni studenti raccontano truffe subite da loro o dai familiari. Indicazioni:

- ascoltare senza giudicare: il messaggio da trasmettere è che gli attacchi ben costruiti ingannano chiunque
- non chiedere importi, nomi, dati bancari
- se emerge un incidente in corso (account compromesso, ricatto, minacce), non gestirlo davanti alla classe: parlarne con lo studente separatamente e coinvolgere la famiglia e i referenti della scuola

## Considerazioni sugli strumenti per la didattica

### Le pubblicazioni del CERT-AGID

Punti di forza:

- casi reali, italiani, aggiornati settimanalmente, con immagini dei messaggi e dei siti fraudolenti
- linguaggio tecnico ma accessibile; il glossario del sito può essere usato come riferimento
- permettono di costruire un'attività ricorrente, per esempio l'analisi della notizia della settimana all'inizio di ogni lezione (5 minuti di richiamo)

Limiti:

- alcune notizie contengono dettagli tecnici avanzati (catene di infezione, comandi PowerShell): selezionare le notizie o anticipare quali parti ignorare
- i contenuti cambiano: le notizie indicate nelle schede vanno sostituite con quelle più recenti a ogni edizione del corso

### CyberChef

Punti di forza:

- un solo strumento per codifiche, cifrari, hash, metadati: gli studenti imparano un'interfaccia sola e la riusano in L8 e L10
- funziona offline e nel browser, senza installazione e senza inviare dati a server
- la ricetta rende visibile la sequenza di trasformazioni, cioè il concetto di "pipeline" di elaborazione dei dati

Limiti:

- interfaccia in inglese e con centinaia di operazioni: fornire l'elenco delle operazioni da usare in ogni laboratorio
- le operazioni di rete (`HTTP request`, `DNS over HTTPS`, `Show on map`) contattano servizi esterni; nel corso non vengono usate

### I file .eml come materiale didattico

Il formato `.eml` è testo semplice: consente di mostrare un messaggio completo di intestazioni senza usare account di posta reali e senza rischi. Il docente può creare nuovi esempi modificando i file forniti; conviene conservare i domini `.example` e i nomi di organizzazioni fittizie. Usare il nome e l'aspetto di organizzazioni reali in un messaggio fraudolento, anche a scopo didattico, produce un oggetto che può essere scambiato per autentico se circola fuori dall'aula.

## Valutazione del modulo

Verifica di modulo (15-20 minuti, individuale), da svolgere all'inizio della prima lezione del modulo 2 o al termine di L4:

- un URL da analizzare con motivazione, tra quattro proposti
- un estratto di intestazioni email da interpretare
- un caso reale non visto (una notizia del CERT-AGID) da analizzare con la tabella di L1
- tre affermazioni vero/falso con correzione (per esempio "un sito con HTTPS è affidabile", "Base64 protegge una password", "un hash si può decifrare con la chiave giusta")

Indicatori osservabili durante i laboratori:

| Indicatore | Osservabile in |
|---|---|
| individua il dominio registrato in un URL | L2, esercizio 1 |
| distingue mittente visualizzato e mittente reale | L2, esercizio 3 |
| spiega perché un controllo tecnico superato non garantisce l'affidabilità | L2, esercizio 4 |
| distingue codifica, cifratura e hash | L3, esercizi 1, 3, 4 |
| usa l'hash per verificare l'integrità di un file | L3, esercizio 5 |
| individua leve psicologiche e difese in un caso reale | L4, esercizio 1 |

## Soluzioni degli esercizi

### L2, Esercizio 1

| N. | Nome host | Dominio registrato | Banca Aurora? | Motivazione |
|---|---|---|---|---|
| 1 | `www.bancaaurora.example` | `bancaaurora.example` | sì | |
| 2 | `bancaaurora.example` | `bancaaurora.example` | sì | |
| 3 | `bancaaurora.example.verifica-accessi.example` | `verifica-accessi.example` | no | sottodominio fuorviante; inoltre `http`, non cifrato |
| 4 | `accesso-bancaaurora.example` | `accesso-bancaaurora.example` | no | dominio diverso che contiene il nome |
| 5 | `bancaurora.example` | `bancaurora.example` | no | typosquatting: manca una `a` |
| 6 | `app.bancaaurora.example` | `bancaaurora.example` | sì | sottodominio legittimo |
| 7 | `sicuro-login.example` | `sicuro-login.example` | no | la parte prima di `@` è un nome utente |
| 8 | `sicuro-login.example` | `sicuro-login.example` | no | il nome della banca è nel percorso |
| 9 | `bancaaurora.example.com` | `example.com` | no | il TLD è `.com` |
| 10 | `xn--bncaaurora-zqi.example` | `xn--bncaaurora-zqi.example` | no | omografo con `а` cirillica, in forma Punycode |
| 11 | `assistenza.bancaaurora.example` | `bancaaurora.example` | sì | il frammento `#password` non conta |
| 12 | `short-link.example` | `short-link.example` | non determinabile | link accorciato: la destinazione reale si conosce solo espandendolo |

Per l'URL 12 si può citare la possibilità di espandere un link accorciato senza visitarlo, con i servizi di anteprima offerti da alcuni accorciatori, e il fatto che nei messaggi ufficiali di banche ed enti i link accorciati sono un segnale d'allarme.

### L2, Esercizio 3

| Voce | Email 1 | Email 2 | Email 3 |
|---|---|---|---|
| nome visualizzato | Banca Aurora | Banca Aurora - Servizio Clienti | Banca Aurora |
| dominio in `From:` | `bancaaurora.example` | `bancaaurora-sicurezza.example` | `aurora-bancaonline.example` |
| `Reply-To:` | assente | casella su servizio gratuito | assente |
| SPF, DKIM, DMARC | pass, pass, pass | fail, none, fail | pass, pass, pass |
| link nel corpo | nessun link | `bancaaurora.example.verifica-accessi.example` | testo del link `www.bancaaurora.example`, destinazione reale `aggiornamento-documenti.example` |
| giudizio | legittima: dominio corretto, controlli superati, nessuna richiesta di dati, invito ad accedere dall'app | fraudolenta: dominio diverso, urgenza e paura, controlli falliti, link fuorviante | fraudolenta: dominio diverso, link con testo ingannevole, richiesta di documento e codice SMS |

### L2, Esercizio 4

È l'email 3. I controlli risultano superati perché il truffatore ha registrato il dominio `aurora-bancaonline.example` e lo ha configurato correttamente: SPF, DKIM e DMARC confermano che il messaggio viene da quel dominio, che però non appartiene alla banca. Da notare anche la tecnica del testo del link che mostra un indirizzo diverso dalla destinazione reale, visibile solo aprendo il file con l'editor o passando il mouse sul link.

### L3

- Esercizio 1: `UGFzc3dvcmQx` decodificato è `Password1`. Base64 non usa chiavi: chiunque lo decodifica.
- Esercizio 2: per decifrare uno spostamento di 3 si applica uno spostamento di 23 (26 - 3), oppure di -3.
- Esercizio 3: il messaggio è stato cifrato con spostamento 7; in `ROT13 Brute Force` compare in chiaro alla riga con spostamento 19 (26 - 7): "Il laboratorio di domani inizia alle nove in aula dodici". Al massimo 25 tentativi.
- Esercizio 4: le due impronte hanno in comune 2 cifre esadecimali nella stessa posizione su 64, in linea con il caso: ogni posizione coincide con probabilità 1/16, quindi in media 4.
- Esercizio 5: l'hash coincide con quello pubblicato finché il file non viene modificato; dopo la modifica di una lettera l'hash è completamente diverso.
- Esercizio 6: 2^128 / 10^18 ≈ 3,4 × 10^20 secondi, circa 1,1 × 10^13 anni, cioè oltre 700 volte l'età dell'universo (circa 1,4 × 10^10 anni).

### L4, Esercizio 1

| Voce | Caso 1 (PEC) | Caso 2 (falso SSN) | Caso 3 (falso rimborso TARI) |
|---|---|---|---|
| vettore | PEC da caselle compromesse | sito fraudolento | sito fraudolento, raggiunto da un messaggio |
| pretesto | fattura non pagata | app o documento del servizio sanitario | rimborso per pagamento in eccesso |
| leve | autorità, urgenza, fiducia nella PEC | autorità, fiducia | opportunità (guadagno), autorità |
| azione richiesta | aprire l'archivio e il file HTML | installare l'app e concedere l'accessibilità, o eseguire il file | inserire dati personali e della carta |
| obiettivo | installare un loader e poi malware di controllo remoto o furto dati | controllo remoto, furto di credenziali | furto di identità e frode con la carta |
| RID | riservatezza, integrità | riservatezza, integrità | riservatezza |
| difesa | non aprire allegati inattesi anche da PEC, verificare con il mittente per altro canale | installare app solo dagli store ufficiali, negare l'accessibilità | ricordare che gli enti non chiedono dati della carta per un rimborso; accedere ai servizi solo digitando l'indirizzo ufficiale |

## Materiale open source

Verifica puntuale per L1-L4: le lezioni sono state scritte da zero. I casi reali sono riassunti con parole proprie dalle notizie del CERT-AGID, citate con titolo e URL completo. Gli esempi di URL ed email sono stati creati per il corso con organizzazioni fittizie e domini `.example`.

Materiali di approfondimento:

- CERT-AGID, glossario: https://cert-agid.gov.it/glossario/phishing/
- CyberChef: https://gchq.github.io/CyberChef/
- Hacker Highschool, ISECOM, lezioni in italiano su sicurezza e privacy per adolescenti (uso non commerciale nelle scuole superiori con attribuzione): https://www.hackerhighschool.org/
