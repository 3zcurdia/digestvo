---
layout: post
title: "Kolibri: un modelo soberano de pesos abiertos"
date:   2026-10-04 00:44:46 -0600
categories: digest
tags: ["AI Release"]
source_url: https://aleph-alpha.com/en/blog/kolibri-has-landed-a-sovereign-open-weight-model/
hn_url: https://news.ycombinator.com/item?id=49942706
share_text: "MoE abierto de 78B, contexto de 1M, Apache 2.0… y sabe cuándo callarse. Conozca a Kolibri. #OpenWeights"
summary: >-
  Aleph Alpha lanzó Kolibri, un transformer de mezcla de expertos con 78B de parámetros totales y
  3B activos, para inglés y alemán, con contexto de 1M de tokens y pesos
  Apache 2.0 en Hugging Face. Dos modelos salieron con tres meses de diferencia porque el
  pipeline corre como código: cada cambio dispara una corrida de punta a punta, los
  checkpoints llegan cada hora y 38 fallas de hardware en 21 días se resolvieron sin intervención.
  Especializado en alemán y trabajo agéntico, está entrenado para abstenerse, conteniéndose en el 44%
  de los ítems de AA-Omniscience.
---

Los comentaristas desconfían sobre todo del encuadre de los benchmarks: el conjunto de comparación tiene un año
de antigüedad, y spijdar y amoshebb señalan que Qwen3.8 27B supera a Kolibri en alemán en
el propio arnés de Kolibri, 79.9 contra 70.8. El encuadre de soberanía se cuestiona
de frente: petesergeant lo llama una tapadera para un rendimiento débil, y otros preguntan qué tan
soberana es una empresa propiedad de Cohere y operada desde Toronto. El equipo y sus defensores
responden que la soberanía es elección y control de los datos, no posición en benchmarks, y
que los modelos pequeños de llamadas a herramientas necesitan menos datos con derechos de autor de lo que la gente supone. Un
largo subhilo se divide sobre si los pesos abiertos son neofeudalismo al revés o un
riesgo de proliferación que nadie puede contener.
