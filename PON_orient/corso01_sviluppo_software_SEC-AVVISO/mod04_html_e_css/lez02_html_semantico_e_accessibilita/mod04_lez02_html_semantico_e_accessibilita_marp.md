---
marp: true
paginate: true
lang: it
---

## Lezione 4.2: HTML semantico e accessibilità

Modulo 4: HTML e CSS. Sviluppo Software e Coding Laboratoriale

Fonte: adattamento da Microsoft, "Web Development for Beginners", lezione "Accessibility", licenza MIT
https://github.com/microsoft/Web-Dev-For-Beginners

---

## Accessibilità

- Uso da parte di tutti, anche con **tecnologie assistive**: lettori di schermo, ingranditori, tastiera
- **Obbligo di legge**: Legge 4/2004 (PA); dal 28 giugno 2025 European Accessibility Act (D.Lgs. 82/2022) per molti servizi privati
- Standard: **WCAG**, https://www.w3.org/WAI/WCAG22/quickref/
- Principi **POUR**: percepibile, utilizzabile, comprensibile, robusto

---

## HTML semantico

| Elemento | Ruolo |
|---|---|
| `header`, `footer` | intestazione, piè di pagina |
| `nav` | navigazione |
| `main` | contenuto principale |
| `section`, `article`, `aside` | sezione, contenuto autonomo, secondario |
| `button` | pulsante |

Un solo `h1`; livelli dei titoli senza salti

---

## Testi alternativi, collegamenti, moduli

```html
<img src="grafico.png" alt="Grafico: iscritti in crescita dal 2020 al 2025">
<img src="decorazione.png" alt="">
<a href="regolamento.pdf">regolamento del concorso (PDF)</a>
<label for="email">Indirizzo email</label>
<input type="email" id="email" name="email">
```

Niente "clicca qui"

---

## Colore, contrasto, tastiera

- Contrasto almeno **4.5:1** (testo normale, livello AA)
- Informazioni non affidate solo al colore
- Tutto raggiungibile con `Tab`, attivabile con `Invio` o `Spazio`
- Focus visibile
- **ARIA** solo se l'HTML non basta: `aria-label`

---

## Strumenti di verifica

- **Lighthouse** (Chrome, Edge)
- **Accessibility Inspector** (Firefox)
- **Assistente vocale** di Windows: `Ctrl` + `Win` + `Invio`
- **WebAIM Contrast Checker**
- **Validatore W3C**

Gli strumenti automatici trovano solo una parte dei problemi

---

## Laboratorio 4.2

- `pagina-da-correggere.html`: lingua, titoli, `alt`, "clicca qui", contrasto, pulsante `div`
- Analisi, correzione, nuova analisi
- Terrario: `header`, `main`, `aside` con etichette distinte, testi alternativi descrittivi
- Commit Git

---

## Aspetti orientativi

- Accessibilità: competenza richiesta a sviluppatori front-end e designer
- Figure specializzate: esperti e auditor di accessibilità
- Obblighi dal 2025: più richiesta nelle aziende
- Quali ostacoli incontra chi non vede o usa solo la tastiera?
