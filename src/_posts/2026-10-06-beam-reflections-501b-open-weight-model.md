---
layout: post
title: "Beam: el modelo de pesos abiertos de 501B de Reflection"
date: 2026-10-06 09:23:08 -0600
categories: digest
tags: ["AI Release"]
source_url: "https://reflection.ai/blog/introducing-beam"
hn_url: "https://news.ycombinator.com/item?id=49969183"
share_text: "501B de parámetros, pesos abiertos, contexto de 1M. Beam va por los modelos frontera. #AI"
summary: >-
  Reflection AI presenta Beam, un modelo disperso de mezcla de expertos de 501
  mil millones de parámetros con 23 mil millones de parámetros activos,
  preentrenado con 23,8 billones de tokens y postentrenado con cuatro semanas
  de aprendizaje por refuerzo en 10.500 GPU GB300 que produjeron más de 100
  millones de rollouts. La empresa afirma un rendimiento en programación y
  agentes competitivo con modelos abiertos más grandes como GLM 5.2 usando 3 o
  4 veces menos cómputo de inferencia, además de una ventana de contexto de un
  millón de tokens lograda en el midtraining. Los pesos, el informe técnico y
  la tarjeta del modelo se prometen bajo Apache 2.0 más adelante este mes, con
  una lista de espera abierta para acceso anticipado. El modelo es solo texto.
---

La mayoría de los comentarios coincide en que el anuncio es prematuro, porque
Reflection está promocionando pesos abiertos que no ha publicado: los pesos,
el informe técnico y la tarjeta del modelo se prometen «más adelante este
mes», y las promesas de publicación de los laboratorios ya han quedado
incumplidas antes. La objeción más aguda es contra la demo de generalización
de tierra/agua, que argumenta que el rompecabezas viral de la cuadrícula
«tiene pocos días, así que no pudo aparecer en los datos de entrenamiento»
para justificar el 95,5% de Beam, cuando los comentaristas señalan que el
rompecabezas original es mucho más viejo, lo que hace que la afirmación de
novedad sea descuidada en el mejor de los casos. Otros atacan el gráfico de
benchmarks por recortar los modelos abiertos más fuertes al doblez, así que
Beam parece superar las filas de DeepSeek V4.1 Flash y Kimi K3 a las que en
realidad va por detrás. Una minoría defiende los datos de entrenamiento
privados como práctica común, pues los corpus bajo licencia y las
trayectorias de RL son secretos comerciales, mientras el subhilo sobre el
origen de los datos deriva en una broma sombría sobre destilar Claude.
