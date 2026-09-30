---
title: "Lezione 4.4: soluzioni degli esercizi"
subtitle: "Modulo 4: Reti e analisi del traffico. Materiale per il docente"
lang: it
---

# Lezione 4.4: soluzioni degli esercizi

Risultati verificati con TShark 4.2 e con `analizza_cattura.py` sul file `cattura2_accessi.pcapng` della lezione 4.3. Impronta SHA-256 del file distribuito: `0c9ec755ad3cb54c277779aedfd770c45c35b9a157210cd0ed13c3b4a0ef6b1d`. Gli account presenti nella cattura (`m.bianchi`, `prof.rossi`, `segreteria`) esistono solo sul server di prova usato per registrarla.

## Parte 1

1. Pacchetto 6: `GET /`; pacchetto 18: `POST /login`; pacchetto 28: `GET /area-docenti`.
2. Corpo della richiesta: `utente=m.bianchi&password=Girasole-73`. Risposta (pacchetto 20): `302 Found`, con `Location: /registro` e `Set-Cookie: sessione=7f3c9a1e5b2d4f60; HttpOnly`. Anche il cookie di sessione viaggia in chiaro: chi lo legge potrebbe usarlo al posto delle credenziali. L'attributo `HttpOnly` lo protegge dagli script della pagina, non dall'osservazione della rete; servirebbero HTTPS e l'attributo `Secure`.
3. Pacchetto 28: `Authorization: Basic cHJvZi5yb3NzaTpMYXZhZ25hITIwMjY=`, che Wireshark decodifica in `Credentials: prof.rossi:Lavagna!2026`; CyberChef, From Base64, dà lo stesso risultato.
4. Pacchetto 40: `220 Server FTP della Scuola di Esempio`; 42: `USER segreteria`; 44: `331 Username ok, send password.`; 45: `PASS Estate2026`; 46: `230 Login successful.`; seguono `PWD` e `QUIT`.
5. No: dopo Client Hello e Server Hello il contenuto è cifrato. Restano visibili indirizzi, porte, tempi, dimensioni e il nome `registro.scuola.example` nel Client Hello.
6. Solo nel pacchetto 18. Nei pacchetti 55-68 la stessa richiesta è cifrata con TLS: il testo `Girasole` non compare nei byte trasmessi.
7. Correzioni: pagina di accesso e area docenti solo in HTTPS, con reindirizzamento automatico da HTTP a HTTPS e intestazione HSTS (modulo 5); cookie con attributo `Secure`; FTP sostituito da SFTP o FTPS; autenticazione Basic solo all'interno di HTTPS, o sostituita da un accesso con modulo e sessione.

## Parte 2

Attività sullo SMTP, una soluzione possibile da aggiungere in `analizza`:

```python
elif p["proto"] == "tcp" and p["dport"] in (25, 587):
    riga = d.decode("latin-1").strip()
    if riga.upper().startswith("AUTH LOGIN") or riga.upper().startswith("AUTH PLAIN"):
        risultato["in_chiaro"].append((numero, p["src"], "SMTP", riga))
```

Nel metodo `AUTH LOGIN` nome utente e password seguono in righe separate, codificate in Base64; un'analisi completa dovrebbe seguire la conversazione. Il test si costruisce chiamando la stessa logica su una stringa di esempio, oppure scomponendo il codice in una funzione `dati_sensibili_smtp(testo)` analoga a `dati_sensibili_http`.

## Attività di discussione: spunti

| Attività | Termine di confronto | Possibile falso allarme | Prima contromisura nella scuola |
|---|---|---|---|
| Ricerca di servizi | numero abituale di destinazioni contattate da un PC in un minuto | programma di inventario della rete usato dagli amministratori; stampanti che cercano dispositivi | ridurre i servizi esposti e segmentare la rete (lezione 4.5) |
| Tentativi ripetuti di accesso | numero abituale di accessi falliti per utente e per indirizzo | utente che ha dimenticato la password; applicazione con una password vecchia salvata | autenticazione a più fattori e limite ai tentativi |
| Uso anomalo del DNS | domini richiesti abitualmente e lunghezza tipica dei nomi | servizi di sicurezza e di distribuzione di contenuti che usano nomi lunghi generati automaticamente | obbligo di usare il DNS interno |
| Trasferimento anomalo di dati | volumi in uscita per dispositivo e per fascia oraria | backup nel cloud, aggiornamenti, caricamento di video | classificazione dei dati e filtri in uscita |
