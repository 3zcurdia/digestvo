---
layout: post
title: "Investigación de ML de Apple: Muse Spark Open con MLX en Mac Studio"
date: 2026-10-17 11:04:42 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://machinelearning.apple.com/research/mlx-distributed-inference"
hn_url: "https://news.ycombinator.com/item?id=50118320"
summary: >-
  El equipo de investigación de ML de Apple muestra cómo ejecutar Muse Spark
  Open, el nuevo modelo mixture-of-experts de pesos abiertos de Meta con 816
  mil millones de parámetros totales, en hardware Mac Studio con la última
  versión de MLX. Un clúster de cuatro Mac Studio con M5 Ultra conectados por
  RDMA sobre Thunderbolt 5 decodifica a unos 37 tokens por segundo, mientras
  una sola máquina de 512GB ejecuta modelos más pequeños como Qwen 3.8 y
  Mistral Medium 3.5. La publicación mide el tiempo hasta el primer token y el
  rendimiento en M3 y M5 Ultra, con hasta 4.6x más velocidad en el prefill
  gracias a los aceleradores neuronales de GPU de los nuevos chips, y explica
  la paralelización por pipeline y por tensores con mlx.launch.
---

La mayoría de los comentarios coincide en la aritmética del precio: cuatro Mac
Studio de 512GB suman unos $40,000, y varios dicen que preferirían poner ese
dinero en créditos de OpenRouter, porque el hardware envejece más rápido que un
mercado de modelos que cambia los requisitos cada año. La objeción más dura a
las cifras mismas es la elección de precisión: Apple mide Muse Spark Open en
NVFP4 de 4 bits mientras deja a Qwen 3.8 en BF16 nativo, lo que se lee como
poner a Qwen en desventaja, aunque un defensor señala que la Tabla 1 lista cada
quant y que mostrar aceleraciones a precisión completa es defendible. Un segundo
grupo defiende la inferencia local por privacidad y por contrato, con el argumento
de que el precio de las API es un blanco móvil mientras las condiciones de un
modelo local son fijas.
