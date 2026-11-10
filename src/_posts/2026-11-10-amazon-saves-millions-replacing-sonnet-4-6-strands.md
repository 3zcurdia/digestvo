---
layout: post
title: "Amazon ahorra millones al reemplazar Sonnet 4.6 con Strands Decider"
date: 2026-11-10 09:20:08 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider/"
image: "/images/digest/2026-11-10-amazon-saves-millions-replacing-sonnet-4-6-strands.jpg"
hn_url: "https://news.ycombinator.com/item?id=50436640"
share_text: "Amazon pasó de 22.200 a 500 dólares por millón de tickets, pero el hilo dice que el post es un anuncio"
summary: >-
  El equipo de Strands Agents publicó un caso de estudio de Amazon: dos
  ingenieros reemplazaron a Claude Sonnet 4.6 por Strands Decider E4B, un
  modelo de decisión que no genera texto, para etiquetar tickets en uno de los
  mayores sistemas internos de la compañía. En vez de JSON razonado, el modelo
  devuelve probabilidades sobre 20 categorías fijas. Según el post, hace el
  mismo trabajo con un 98% menos de coste: de unos 22.200 a 500 dólares por
  millón de tickets, y de 4.215 a 897 ms por llamada. El despliegue corre en
  SageMaker tras un interruptor de tres vías (BEDROCK, DUAL, DECIDER) que
  permitió comparar ambos modelos con tráfico real.
---

Amazon promete un 98% de ahorro al reemplazar a Sonnet 4.6 con su propio Strands
Decider E4B en el etiquetado de tickets. El hilo coincidió en que es sobre todo
marketing —Strands Decider es producto de Amazon y su adopción interna sirve de
caso de estudio— y en que cambiar un LLM por un clasificador dedicado en una
tarea cerrada es un patrón viejo, resuelto con SVMs hace seis años. La disputa
es qué demuestra el resultado: para unos confirma que los modelos pequeños y
especializados ganan al monolito que lo hace todo, con la Bitter Lesson invocada
en ambos sentidos. Para otros, el conocimiento amplio del LLM es el punto: un
SVM falla de formas no corregibles, y el LLM permite prototipar un clasificador
sin datos etiquetados ni científico de datos. Sin embargo, casi todos aceptan
que, estabilizada la tarea, conviene destilarla a un modelo dedicado: el post
muestra el final de ese arco, no una refutación. Como nota menor, se preguntó
por qué no una versión más nueva de Sonnet —la conjetura fue la falta de API
batch en Bedrock— y por el chiste de que Strands solo captura el 2% de los
millones que ahorra.
