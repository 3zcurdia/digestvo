---
layout: post
title: "Mistral Large 4 Open weights"
date: 2026-10-30 08:06:12 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://mistral.ai/news/mistral-large-4-oss/"
image: "/images/digest/2026-10-30-releasing-weights-mistral-large-4.jpg"
hn_url: "https://news.ycombinator.com/item?id=50289418"
share_text: "Mistral Large 4 lidera FrontierCode con 19.7%, pero su licencia MIT modificada abre la guerra por los 'pesos abiertos'"
summary: >-
  Mistral está publicando los pesos de Mistral Large 4, "Le Chonk", su buque
  insignia nativamente multimodal de 1 billón de parámetros que entró en vista
  previa pública a inicios de mes. Tres semanas adicionales de aprendizaje por
  refuerzo empujaron al modelo a la cabeza del grupo de pesos abiertos en
  programación: 19.7% en FrontierCode 2.0 de Cognition, el liderazgo en
  Terminal-Bench 4.0 con 41%, y 48% en el Artificial Analysis Coding Agent
  Index mientras usa 47% menos tokens por tarea que GLM-5.3. Alcanza 51% en el
  Cyber Index y rechaza peticiones cibernéticas maliciosas el 96.6% de las
  veces. Los pesos están en Hugging Face bajo una licencia MIT modificada.
---

Esta publicación cierra una brecha de tres semanas entre la vista previa pública
de Le Chonk y esta salida de pesos, durante la cual el aprendizaje por refuerzo
llevó al modelo de sólido a líder en los benchmarks de programación. El terreno
común era que la publicación importa: un modelo de 1 billón de parámetros que
cualquiera puede descargar, cuantizaciones de día cero de Unsloth y una opción
soberana europea creíble. La pelea principal es por la licencia: la licencia
Mistral Ecosystem Open-Weight es un MIT modificado que exige a cualquier negocio
de Model-as-a-Service comprar una licencia comercial separada, de modo que un
bando, invocando la definición de pesos abiertos de OSI, lo llama "weights
available" más que pesos abiertos, trazando la analogía con el source-available
de Redis y Elasticsearch. Aun así, otros rebatieron que los pesos publicados es
lo que "pesos abiertos" siempre ha significado y que OSI no tiene autoridad
sobre el término. Nota menor: el modelo es demasiado grande para hardware de
consumo, pues incluso la cuantización más baja de Unsloth necesita unos 256GB de
VRAM, y un hilo secundario discutió lo difícil que Mistral hace encontrar su
página de precios.
