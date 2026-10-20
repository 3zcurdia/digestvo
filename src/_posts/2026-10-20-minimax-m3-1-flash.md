---
layout: post
title: "MiniMax M3.1 Flash"
date: 2026-10-20 09:10:22 -0600
categories: digest
tags: ["AI Release"]
source_url: "https://www.minimax.io/blog/minimax-m31f"
hn_url: "https://news.ycombinator.com/item?id=50154540"
share_text: "MiniMax promete 73.7% en código 70% más barato — HN dice que Space Bunny ya falló en uso real"
summary: >-
  MiniMax lanzó M3.1 Flash, un modelo agéntico de código que según la empresa
  iguala a los mejores modelos con casi 3x más velocidad y 70% menos costo que
  su antecesor. Reporta 73.7% en DeepSWE v1.1, 76.2 en BankerToolBench, 82% en
  CyberGym, además de liderar entre los modelos chinos en OSWorld V2 y ALE. El
  precio es fijo: $0.15 por millón de tokens de entrada y $0.60 de salida. El
  modelo está disponible por API y en MiniMax Code, con pesos abiertos
  prometidos más adelante.
---

La mayoría de los comentarios coincide en dudar de la historia de los benchmarks, porque el 73.7% en DeepSWE v1.1 cae en un grupo sospechoso cerca del 74% junto a DeepSeek 4.1 Flash y otros, y usuarios de opencode dicen que el checkpoint anterior 'Space Bunny' cometía errores graves que los devolvieron a Qwen o DeepSeek. La objeción más dura es que 'Flash' ya no significa pequeño ni rápido para uso local, porque con 428B totales y 23B activos apenas alcanza 13 TPS en hardware doméstico, lo que se siente como buffering frente a los 35-50 TPS que la gente espera. En contra, un grupo menor sostiene que el costo por tiempo real pesa más que el costo por token en el trabajo diario, así que MiniMax solo gana si sus 200+ TPS por API y su recorte de 70% se sostienen en ejecuciones agénticas reales.
