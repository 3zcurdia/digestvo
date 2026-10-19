---
layout: post
title: "Qwen 3.8 Flash Next (125B) en hardware doméstico (RTX 4090) a 100 tokens/s"
date: 2026-10-05 09:09:57 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://github.com/Niko1221/Strata"
hn_url: "https://news.ycombinator.com/item?id=49953495"
share_text: "Modelo de 125B en una PC gamer a más de 100 tokens/s. Su RTX 4090 ahora es un datacenter. #LLM #OpenSource"
summary: >-
  Strata es un motor de inferencia de código abierto con instalador en un clic
  que ejecuta Qwen3.8-Flash-Next, un modelo de mezcla de expertos de 125 mil
  millones de parámetros, en PC gamer comunes. El proyecto reparte sus 24.576
  expertos entre GPU, RAM y SSD, y usa decodificación especulativa para
  reportar entre 53 y 94 tokens por segundo en una RTX 5070, con una estimación
  de 100 a 140 en la RTX 3090. Incluye cuantizaciones desde 2 bits hasta casi
  4 bits, además de una variante Coder con la mitad de los expertos eliminada
  que conserva el 91% del puntaje SWE-bench Verified del modelo completo y cabe
  en 32 GB de RAM. La instalación expone API compatibles con OpenAI y Anthropic
  en localhost, así que nada sale de la máquina.
---

La mayoría de los comentarios coincide en que el modelo basta para reemplazar
los modelos por API para programar, porque varios reportan velocidades reales
por encima de los 100 tokens/s anunciados en una 4090 y uno dice que dejó de
usar Claude. La objeción más aguda es la cuantización a 2 bits: un
comentarista cita un artículo que muestra que 4 bits suele preservar el
rendimiento mientras que 2 bits a menudo causa una degradación general, y otro
señala que las cifras publicadas muestran un 27B a 4 bits superando a Flash
Next a 3 bits. En contra, los defensores argumentan que las cuantizaciones IQ3
con matriz de importancia podan los pesos poco importantes con precisión
quirúrgica y que el 91% del SWE-bench Verified del modelo completo en la
variante Coder es la cifra que importa. Un debate secundario es qué significa
sorprendentemente bien: la velocidad es una cosa, la precisión medida en
benchmarks otra, y casi nadie en el hilo publica ambas.
