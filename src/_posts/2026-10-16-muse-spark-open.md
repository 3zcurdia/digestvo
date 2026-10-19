---
layout: post
title: "Muse Spark Open"
date: 2026-10-16 09:38:43 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://research.meta.ai/blog/muse-spark-open"
hn_url: "https://news.ycombinator.com/item?id=50107379"
share_text: "El gigante open-weight de 816B de Meta corre en dos Mac Studio, si le sobran $25K"
summary: >-
  Meta liberó los pesos de Muse Spark Open, presentado como el modelo
  estadounidense de pesos abiertos más capaz hasta la fecha. Es un modelo
  mixture-of-experts nativamente multimodal con 816B de parámetros totales,
  42B activos y una ventana de contexto de 1M de tokens, orientado a
  programación y trabajo agéntico. Meta dice que corre en un par de Mac
  Studio M5 Ultra de escritorio vía MLX, y llega con soporte desde el primer
  día para SGLang, vLLM, llama.cpp y otros runtimes, además de APIs
  hospedadas. Los pesos están disponibles en Hugging Face y las principales
  nubes bajo la Muse Model License, con términos comerciales limitados.
---

La mayoría de los elogios se centra en que Meta hizo el trabajo poco
glamoroso del despliegue, con soporte desde el primer día para MLX, vLLM,
SGLang y llama.cpp que sube la vara más allá de solo soltar los pesos. Ese
entusiasmo choca con las cuentas del hardware, pues el montaje estrella de
escritorio requiere dos Mac Studio M5 Ultra con hasta 512GB de memoria
unificada cada uno, una propuesta de 20 a 30 mil dólares que vuelve la
propiedad local una compra especializada. La objeción más fuerte es que nada
de eso le compra a Meta un foso de consumo, porque los críticos califican al
asistente Muse de harness de agentes con otra piel, sin efectos de red, y
sostienen que Apple, Google y Microsoft siguen dueñas de la capa del sistema
operativo. Los defensores responden que comoditizar el modelo es el foso, ya
que estandarizar sus pesos y optimizar la infra alrededor baja sin pausa los
propios costos de servicio de Meta.
