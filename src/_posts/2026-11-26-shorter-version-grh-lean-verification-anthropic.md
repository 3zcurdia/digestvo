---
layout: post
title: "Versión mucho más corta de la verificación en Lean de GRH, de Anthropic"
date: 2026-11-26 14:13:18 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://github.com/lsernau/grh-lean"
image: "/images/digest/2026-11-26-shorter-version-grh-lean-verification-anthropic.jpg"
hn_url: "https://news.ycombinator.com/item?id=50648050"
share_text: "La prueba de GRH en Lean de Anthropic baja a 76,000 líneas, un 99.56% más corta, sin matemáticos que la lean #AI #Math"
summary: >-
  El investigador de Anthropic Luke Sernau ha publicado una formalización en
  Lean 4 mucho más corta de la hipótesis de Riemann y de la hipótesis de
  Riemann generalizada para las funciones L de Dirichlet, construida sobre
  Mathlib y usando solo los tres axiomas estándar. Se basa en la prueba de
  Levent Alpöge asistida por Claude, reducida de unos 17 millones de líneas a
  unas 76,000, un 99.56% menos. El repositorio incluye dos ediciones de los
  mismos cinco teoremas: una legible de unas 300,000 líneas y una compacta de
  76,000. El README dice que la prueba solo ha pasado verificaciones de
  máquina, que ningún matemático la ha leído entera y que no viene ningún
  artículo con ella.
---

El volcado original de 17 millones de líneas de Alpöge llegó hace días ya
inflado, y semanas de la comunidad reduciéndolo solo lo habían recortado en
alrededor de un tercio, lo que situó esta entrega como la prueba de qué pueden
hacer los modelos internos de Anthropic. La mayoría de los comentarios coincidió
en que la cifra del titular sobrecoge: 76,000 líneas, un 99.56% de reducción,
logrado en días por una sola persona con Claude. El argumento principal gira en
torno a qué explica ese salto: varios atribuyeron modelos internos mejores y
pura potencia de cálculo antes que ningún método más ingenioso, mientras otros
replicaron que el esfuerzo de la comunidad era hill climbing con herramientas
más débiles y atascado en victorias fáciles como inliner los imports. Aun así,
un comentario señala que la edición compacta está muy reducida al estilo del
code golf, metiendo contenido en menos líneas, y que una versión legible ronda
las 300,000 líneas, así que la revisabilidad sigue siendo el problema real, ya
que ningún matemático ha leído la prueba entera. Nota menor: un hilo lateral
discute si Anthropic ha reconocido el resultado en absoluto, y si la fecha de la
entrega esperó al periodo de silencio de la IPO.
