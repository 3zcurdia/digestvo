---
layout: post
title: "DeepSeek libera su motor de inferencia"
date: 2026-10-20 09:10:22 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://github.com/deepseek-ai/DeepInfer"
hn_url: "https://news.ycombinator.com/item?id=50163277"
share_text: "DeepSeek libera su motor de inferencia: $38/GPU-hora hoy, ¿márgenes mínimos mañana?"
summary: >-
  DeepSeek publicó DeepInfer, el framework de inferencia de alto rendimiento
  que sostiene sus servicios de producción a gran escala, bajo Apache 2.0. La
  versión ofrece inferencia local para DeepSeek-V4.1-Flash con kernels
  optimizados, paralelismo de expertos MoE con balanceo de carga,
  planificación asíncrona, muestreo determinista y salidas estructuradas.
  Soporta GPU NVIDIA SM100 y NPU Huawei Ascend 950. Los gráficos comparan el
  rendimiento de prefill y decode, y el proyecto reconoce a vLLM, SGLang y
  TensorRT-LLM como base.
---

La mayoría de los comentarios coincide en la cifra de $38 por GPU-hora citada del anuncio en chino de DeepSeek, junto con los 155 billones de tokens diarios de un solo clúster V4.1 Flash, como prueba de que la inferencia ya es sólidamente rentable. Apuntan al estimador de ganancias de SemiAnalysis y a la energía barata en China para sostener que la narrativa de pérdidas quedó atrás, con una cifra filtrada que afirma que meses de inferencia pueden recuperar el costo de entrenamiento. La objeción más dura es que se trata de márgenes actuales sobre hardware rentado o subsidiado, porque servir modelos es un commodity indiferenciado que se comprimirá hacia márgenes de supermercado de 3-5% cuando la oferta alcance a la demanda. Eso abre una segunda disputa sobre si el código abierto destruye el foso por completo, con escépticos que preguntan quién financiará el entrenamiento de frontera si versiones como las de DeepSeek pueden destilarlo gratis.
