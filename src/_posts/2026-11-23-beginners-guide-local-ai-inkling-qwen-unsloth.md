---
layout: post
title: "Guía para principiantes de IA local con Inkling, Qwen y Unsloth"
date: 2026-11-23 11:02:24 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://www.gpupartner.com/blog/beginners-guide-local-ai-inkling-qwen-unsloth"
image: "/images/digest/2026-11-23-beginners-guide-local-ai-inkling-qwen-unsloth.jpg"
hn_url: "https://news.ycombinator.com/item?id=50603845"
share_text: "Una GPU de $6,500 son 16 años de Claude Pro: ¿ya conviene la IA local o es la fase de plasma? #AI #LocalLLM"
summary: >-
  La guía enseña a montar una IA local en Windows con Unsloth Desktop:
  instalar la app, descargar un modelo cuantizado que quepa en la VRAM de la
  tarjeta y activar el acceso LAN para compartirlo en casa, en 10-15 minutos.
  El autor usa un RTX 5090 de 32 GB con Qwen3.8-27B a 4 bits (18 GB) y
  contexto de 128K, y la tabla cubre desde 8-12 GB con modelos de 9B-12B hasta
  32 GB+ con ese modelo o Inkling 2 Mini de Thinking Machines Lab, 26.4B
  parámetros lanzado el 17 de noviembre. También cubre Mac con MLX y adelanta
  secciones sobre rendimiento, túneles de red y agentes locales.
---

El contexto es una guía de GPUPartner que promete un ChatGPT en casa en 10-15
minutos, con 659 puntos en Hacker News. La mayoría coincidió en que montar con
Unsloth Desktop es sencillo, que la cuantización y los modelos MoE dan modelos
serios en tarjetas modestas, y que el cuello de botella es la memoria, no los
FLOPS de la CPU, con 128 GB de memoria unificada como la mejor opción. Sin
embargo, la controversia central es el dinero: un lado sostiene que el hardware
sigue fuera de presupuesto, porque una tarjeta de $6,500 equivale a 16 años de
Claude Pro a $17/mes, y que esta es la fase de plasma de la IA local. Aun así,
el otro lado apuesta por la lección amarga: en unos 5 años el hardware de
consumo correrá esos modelos, y hoy ya sirven para programar con $10-20k. Un
choque concreto: el post afirma que Qwen3.6-35B a 4 bits necesita 32 GB de VRAM
y un comentarista responde que ese modelo MoE corre sin problemas en una RTX
3060. Como nota menor, un hilo temió que PCs caseras sirvan de botnet de agentes
en la red.
