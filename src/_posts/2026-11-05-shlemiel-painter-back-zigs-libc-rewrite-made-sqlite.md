---
layout: post
title: "Shlemiel the Painter vuelve: cómo la reescritura de libc de Zig dejó SQLite más lento"
date: 2026-11-05 09:27:29 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://dennisforbes.ca/blog/microblog/2026/10/the_accidental_12000x_sqlite_slowdown/"
image: "/images/digest/2026-11-05-shlemiel-painter-back-zigs-libc-rewrite-made-sqlite.jpg"
lobsters_url: "https://lobste.rs/s/lh1j0e/shlemiel_painter_is_back_how_zig_s_libc"
share_text: "El strspn de Zig volvía a medir toda la cadena en cada llamada: SQLite sobre 1.2MB de JSON salió 12,000 veces más lento"
summary: >-
  Un servicio en Rust que inserta resultados de análisis en SQLite pasó de
  pronto a consumir minutos de CPU en una escritura que debería ser
  submilisegundos para unos 40,000 registros JSON. El culpable fue la
  reescritura en Zig puro de las funciones de cadena de libc, usada al compilar
  SQLite con zig cc: cada llamada vuelve a medir la cadena restante completa,
  así que un tokenizador que recorre el texto hace trabajo cuadrático.
  Tokenizar un archivo de 1.2MB resultó unas 12,000 veces más lento. La
  regresión solo apareció en compilaciones para Linux, porque las
  compilaciones del autor en su Mac nunca pasaban por Zig.
---

Al documentar su servicio de análisis de ajedrez, Dennis Forbes se topó con
un misterio ligado a la CPU: insertar unos 40,000 registros JSON en SQLite
tomaba minutos en lugar de milisegundos, porque SQLite había sido compilado
de forma cruzada con zig cc, y las reescrituras en Zig puro de strspn,
strcspn, strpbrk y strstr vuelven a medir la cadena completa en cada llamada,
lo que convierte al tokenizador en un trabajo cuadrático. Los comentarios
coincidieron con el diagnóstico, enlazaron el issue abierto de Zig y su
corrección pendiente, y calificaron la publicación de hermosa explicación del
tiempo cuadrático. La verdadera discusión fue sobre la revisión: un
comentarista sostuvo que un revisor de código con un LLM obviamente habría
capturado un bug accidentalmente cuadrático, y otros objetaron. Aun así, el
líder de Zig dijo que dejó que el error pasara a propósito en la revisión
para que los nuevos colaboradores sintieran las consecuencias de sus propios
errores, y el comentario con más votos llamó a esa recompensa comunitaria un
intercambio que vale una regresión de rendimiento pre-1.0. Sobre el punto de
los LLM, un comentarista publicó una revisión real de string.zig hecha con
Opus, que efectivamente señaló el bucle cuadrático pero, al insistirle, no
dijo nada sobre qué debería optimizar la función en el caso común. Nota
menor: una propuesta de gate de benchmarks que cronometra una función con
entradas de 1x, 10x y 100x y deriva una puntuación de complejidad de esas
razones.
