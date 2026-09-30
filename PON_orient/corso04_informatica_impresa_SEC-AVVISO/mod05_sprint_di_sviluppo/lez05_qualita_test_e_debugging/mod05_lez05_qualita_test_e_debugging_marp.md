---
marp: true
paginate: true
lang: it
---

## Lezione 5.5: Qualità: test e debugging

Modulo 5: Due sprint di sviluppo. Informatica per l'Impresa e Soft Skills Digitale

---

## Tipi di test

- Unità, integrazione, sistema, accettazione
- Regressione ed esplorativi
- Piramide: molti test di unità, pochi test di sistema

---

## Copertura

- Righe eseguite almeno una volta dai test
- Indica dove mancano test, non se i test sono buoni
- Riga eseguita non vuol dire riga verificata

---

## Debugging con metodo

```mermaid
flowchart LR
    R["Riprodurre"] --> I["Isolare"] --> C["Correggere con un test"] --> V["Verificare"]
```

---

## Il debugger di VS Code

- `F9` punto di interruzione, `F5` avvia e continua
- `F10` passo successivo, `F11` entra, `Shift+F11` esce
- Pannello Variabili e Console di debug
- `launch.json`: `type: debugpy`, `program`, `args`

---

## Laboratorio

1. Kit con difetti: 22 test verdi, copertura 98%
2. Quattro segnalazioni degli utenti e due difetti nascosti
3. `python copertura.py`; 8 test

---

## Aspetti orientativi

- Tester e QA engineer
- Debugging: ipotesi, verifica, conclusione
