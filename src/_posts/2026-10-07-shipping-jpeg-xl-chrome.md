---
layout: post
title: "JPEG XL llega a Chrome"
date: 2026-10-07 09:11:08 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://developer.chrome.com/blog/jpeg-xl-in-chrome"
hn_url: "https://news.ycombinator.com/item?id=49991227"
share_text: "JPEG XL vuelve a Chrome, decodificado con una reescritura en Rust puro. Por fin. #WebPerf"
summary: >-
  Chrome incorpora la decodificación de JPEG XL desde Chrome 155, revirtiendo
  la eliminación que hizo en Chrome 110. La publicación explica que el
  decodificador es jxl-rs, una reescritura en Rust puro del decodificador
  libjxl, elegido porque los decodificadores de imágenes analizan bytes no
  confiables dentro del renderizador y la regla de dos de Chromium impulsa el
  código memory-safe. Igualar la velocidad de C exigió estabilizar una función
  SIMD de Rust y construir una capa de abstracción SIMD inspirada en Highway
  de Google, con cifras de rendimiento seguidas en un panel público. Chrome
  atribuye la decisión a los comentarios de desarrolladores de Interop 2026 y
  recomienda probar tanto AVIF como JPEG XL.
---

La mayoría de los comentarios coincide en que la reversión viene forzada desde
fuera de Google: la PDF Association eligió JXL como el próximo formato de
imagen para PDF, así que los navegadores que quieran mostrar PDF necesitan un
decodificador de todos modos, y exponer ese decodificador también a las
etiquetas img sale gratis. La objeción más aguda es contra la historia cínica
de política interna —que JXL se abandonó para proteger AVIF/WebP y se revive
para que alguien reclame un ascenso— porque empleados de Google escribieron la
especificación, el decodificador de referencia y jxl-rs, y el aviso original
de deprecación de Chrome nunca citó seguridad ni AVIF como motivo. La
teoría contraria, impulsada sobre todo por un par de comentaristas, es que
otro códec gigante en C era simplemente un pasivo que valía la pena asumir
hasta que la reescritura en Rust lo abarató, pues libjxl tenía un largo
historial de errores y Project Zero había advertido contra decodificadores
inseguros. Una pelea menor estalla sobre la calidad de los códecs: un
comentarista insiste en que AVIF sigue ganando por debajo de un bit por
píxel, otro reporta lo contrario para miniaturas pequeñas.
