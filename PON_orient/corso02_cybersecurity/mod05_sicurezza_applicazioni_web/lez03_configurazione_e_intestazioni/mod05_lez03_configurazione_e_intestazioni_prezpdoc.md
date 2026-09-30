---
title: "Lezione 5.3: Configurazione e intestazioni di sicurezza"
subtitle: "Modulo 5: Sicurezza delle applicazioni web. Cybersecurity ed Ethical Hacking"
lang: it
---

## Contenuti

- Configurazione sicura
- Intestazioni di sicurezza
- Cookie di sessione
- Dipendenze
- Laboratorio
- Aspetti orientativi

## Configurazione sicura

- Configurazione minima; debug solo in sviluppo
- Ambienti separati
- Segreti fuori dal codice
- Credenziali predefinite cambiate

## Intestazioni di sicurezza

| Intestazione | Valore tipico |
|---|---|
| Strict-Transport-Security | `max-age=63072000; includeSubDomains` |
| Content-Security-Policy | `default-src 'self'; frame-ancestors 'none'` |
| X-Content-Type-Options | `nosniff` |
| Referrer-Policy | `strict-origin-when-cross-origin` |
| Permissions-Policy | `geolocation=(), camera=()` |

Da evitare: X-XSS-Protection attiva; versioni in Server e X-Powered-By

## Cookie di sessione

```http
Set-Cookie: __Host-sessione=...; Path=/; Secure; HttpOnly; SameSite=Lax
```

- Valore casuale e lungo
- **Secure**, **HttpOnly**, **SameSite**, prefisso `__Host-`
- Scadenza e invalidazione

## Dipendenze

- Inventario (`requirements.txt`, `package-lock.json`, SBOM)
- Analisi: `pip-audit`, `npm audit`
- Aggiornamenti con test
- Provenienza e integrità

## Laboratorio

1. DevTools, Rete, Intestazioni: tre siti reali
2. `python controlla_intestazioni.py sito1.txt`; 13 test
3. `python -m pip_audit -r requisiti_esempio.txt`

```text
Found 48 known vulnerabilities in 4 packages   (settembre 2026)
```

## Aspetti orientativi

- Sistemisti, DevOps, sicurezza del cloud
- Catena di fornitura del software
- Perché conoscere tutti i componenti usati?
