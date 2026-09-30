---
title: "Lezione 3.1: Variabili e tipi di dato"
subtitle: "Modulo 3: JavaScript di base. Sviluppo Software e Coding Laboratoriale"
lang: it
---

## Contenuti

- let, const, var
- Tipi di dato
- Numeri
- Stringhe
- Conversioni e uguaglianza
- Oggetti: primo contatto
- Laboratorio 3.1

Fonte: adattamento da Microsoft, "Web Development for Beginners", lezione "Data Types", licenza MIT, https://github.com/microsoft/Web-Dev-For-Beginners

## let, const, var

```javascript
let punteggio = 10;   // può cambiare
punteggio = 15;
const MAX_VITE = 5;   // non riassegnabile
```

- `const` per default, `let` se il valore cambia, `var` da evitare
- Maiuscole e minuscole distinte: `eta` diverso da `Eta`
- camelCase: `numeroStudenti`, `prezzoFinale`
- Nomi significativi

## Tipi di dato

- **number**: `42`, `3.14`, `-5`
- **string**: `"ciao"`
- **boolean**: `true`, `false`
- **undefined**: variabile senza valore
- **null**: assenza voluta di valore
- **oggetti**: object, array, funzioni

Tipizzazione **dinamica**; operatore `typeof`

## Numeri

| Operatore | Operazione | Esempio |
|---|---|---|
| `+` `-` `*` `/` | aritmetica | `7 / 2` è `3.5` |
| `%` | resto | `7 % 2` è `1` |
| `**` | potenza | `7 ** 2` è `49` |

```javascript
n += 5;  n++;  n--;
0.1 + 0.2;                // 0.30000000000000004
Math.round(2.6);          // 3
Math.floor(2.6);          // 2
```

## Stringhe

```javascript
const nome = "Ada";
const saluto = `Buongiorno, ${nome}!`;   // template literal
"JavaScript".length;                     // 10
"JavaScript".toUpperCase();              // "JAVASCRIPT"
"JavaScript".slice(0, 4);                // "Java"
```

- Apici singoli, doppi, inversi
- Immutabili: i metodi restituiscono nuove stringhe

## Conversioni e uguaglianza

```javascript
"1" + "1"        // "11"
"5" * 2          // 10
Number("4.5")    // 4.5
Number("4,5")    // NaN
5 === "5"        // false
5 == "5"         // true
```

- `prompt` e i campi di testo restituiscono stringhe: usare `Number()`
- Usare sempre `===` e `!==`

## Oggetti: primo contatto

```javascript
const studente = { nome: "Luca", classe: 4, iscritto: true };
studente.nome;        // "Luca"
studente.classe = 5;  // modifica di una proprietà
```

Ogni elemento di una pagina web è un oggetto (modulo 5)

## Laboratorio 3.1

- Previsioni in console: `10 % 3`, `"3" + 4 + 5`, `3 + 4 + "5"`
- Programma: nome e anno di nascita con `prompt`, controllo con `Number.isNaN`, età con `new Date().getFullYear()`
- Oggetto `libro` e frase con template literal
- Commit Git
