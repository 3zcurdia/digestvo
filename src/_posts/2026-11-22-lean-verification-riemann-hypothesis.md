---
layout: post
title: "Verificación en Lean de la hipótesis de Riemann"
date: 2026-11-22 10:55:43 -0600
categories: digest
tags: ["Science"]
source_url: "https://leanprover-community.github.io/blog/posts/riemann-hypothesis/"
image: "/images/digest/2026-11-22-lean-verification-riemann-hypothesis.jpg"
hn_url: "https://news.ycombinator.com/item?id=50589618"
share_text: "17 millones de líneas de Lean verifican la hipótesis de Riemann, pero ningún humano la entiende: ¿eso está probado? #Math #Lean"
summary: >-
  El 20 de noviembre de 2026, Levent Alpöge publicó una prueba de la hipótesis
  de Riemann en forma de una biblioteca de 17 millones de líneas de código en
  Lean. Una declaración conjunta de las comunidades de Lean y Mathlib,
  respaldada por la Lean FRO y la Mathlib Initiative, afirma que tienen plena
  confianza en que es correcta. Docenas de personas reprodujeron la
  compilación y la misma exportación cruda de la prueba, dos herramientas
  independientes confirmaron que el teorema demostrado es exactamente el
  RiemannHypothesis enunciado en Mathlib, y la exportación pasó el kernel
  oficial de Lean más verificadores independientes, incluidos con-leche y
  con-ron, que llevan una demostración formal, relativa a la teoría de
  conjuntos, de que no pueden aceptar una prueba falsa.
---

El contexto es una biblioteca de 17 millones de líneas en Lean publicada el 20
de noviembre de 2026, y una declaración conjunta de las comunidades de Lean y
Mathlib que pide a los matemáticos confiar en una cadena de herramientas en
lugar de leer la prueba ellos mismos. La mayoría de los comentarios coinciden
en que la verificación está por encima de la revisión por pares, ya que los
artículos publicados suelen contener demostraciones inválidas, y con-leche y
con-ron llevan una demostración formal, relativa a la teoría de conjuntos, de
que no pueden aceptar una prueba falsa. La controversia central es qué significa
demostrado cuando ningún ser humano entiende la prueba: un lado considera la
comprobación del kernel definitiva y mejor evidencia que la mayor parte de la
literatura publicada, mientras que el otro sostiene que un resultado solo
cuenta cuando un matemático puede explicar cómo y por qué funciona, ya que la
mayor parte de la comunidad no sabe leer Lean. Sin embargo, el Teorema de los
Cuatro Colores fue el punto de referencia: su reducción de casos se podía
asimilar caso por caso, mientras que aquí cada regla de inferencia es igual de
trivial, una distinción que un lado insistía que importaba y el otro desestimó.
Aun así, un hilo menor volvió a los fundamentos, con reparos sobre que cada
verificador asume que el ensamblador x86 se comporta según lo especificado,
más un debate más corto sobre si el uso de Claude por parte de Alpöge le
pertenece al matemático o al modelo.
