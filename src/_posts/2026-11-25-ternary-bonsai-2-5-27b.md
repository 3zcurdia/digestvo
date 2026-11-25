---
layout: post
title: "Ternary Bonsai 2.5 27B"
date: 2026-11-25 10:51:19 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://prismml.com/news/bonsai-2-5-27b"
image: "/images/digest/2026-11-25-ternary-bonsai-2-5-27b.jpg"
hn_url: "https://news.ycombinator.com/item?id=50633922"
share_text: "Un 27B ternario de 5.9 GB saca 75.6 en SWE-bench Verified, pero ¿los pesos o el harness cierran la brecha con Opus? #AI"
summary: >-
  PrismML publicó Ternary Bonsai 2.5 27B, un modelo agéntico de programación
  cuantizado a ternario basado en Qwen3.8 27B que mantiene el tamaño de 5.9 GB
  de la versión anterior. La empresa dice que mejora el uso de herramientas en
  varios turnos y reduce los bucles de pensamiento repetitivo que plagiaban al
  Bonsai 2 previo. En SWE-bench Verified obtiene 75.6, frente a 60.8 antes y
  80.6 del modelo base a precisión completa, y alcanza 291 tokens/s en una H100
  con predicción de múltiples tokens. Los pesos se distribuyen bajo licencia
  Apache 2.0 y funcionan con llama.cpp y MLX.
---

La publicación de lanzamiento de Ternary Bonsai 2.5 27B de PrismML aterriza en
un patrón ya familiar de HN: un modelo local pequeño cuya tabla de benchmarks
parece saltarse a modelos frontier mucho más grandes. La mayoría de los
comentarios coincide en que la cuantización en sí es impresionante, con alguien
que la califica como una muy buena cuantización, y varios confirman que el
Bonsai anterior estaba a la altura de su tamaño mientras señalan su manía de
caer en bucles de pensamiento repetitivos, que la nueva versión dice corregir.
La tensión está en qué significan los números del benchmark: un comentario
pregunta si el 75.6 en SWE-bench Verified, leído como territorio de Opus 4.6,
refleja progreso real, un benchmark en movimiento o una puntuación que obedece
la ley de Goodhart, y Dofm responde que esa ley es imbatible, ya que el modelo
es una cuantización post-hoc de un modelo base que ya está por detrás de Opus
4.6. Aun así, el harness es donde la discrepancia se estrecha: el harness local
de Claude Code es de apenas unos 7k tokens, señalan varios comentarios,
mientras que las herramientas del lado servidor de Anthropic son las que
realmente cierran la brecha, así que igualar una API frontier exige más que
los pesos. Como nota menor, queda la pregunta por la oferta de GPU en China
tras el endurecimiento de la regla de exportación del 16 de noviembre, que
desvía la conversación por un momento.
