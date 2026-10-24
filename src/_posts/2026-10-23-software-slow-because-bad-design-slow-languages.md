---
layout: post
title: "El software es lento por el mal diseño, no por los lenguajes lentos"
date: 2026-10-23 18:01:17 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://www.seangoedecke.com/software-is-slow-because-of-bad-design-not-slow-languages/"
lobsters_url: "https://lobste.rs/s/hd72yt/software_is_slow_because_bad_design_not"
share_text: "Las consultas a la BD tardan 5ms, pero las respuestas 500ms: Lobsters rebate que 'el software es lento por el mal diseño'."
summary: >-
  Sean Goedecke sostiene que la tendencia actual de pedir a los agentes de IA
  que reescriban el software en Rust, C o ensamblador pasa por alto el punto,
  porque la mayoría de los programas no se puede acelerar de forma significativa
  con un cambio de lenguaje. Los programas reales, escribe, suelen estar
  limitados por E/S, esperando a bases de datos, redes o APIs de terceros, de
  modo que la ley de Amdahl limita cualquier reescritura a una ganancia de
  aproximadamente 2x. Donde queda trabajo limitado por CPU, los lenguajes
  lentos ya delegan en C rápido o bibliotecas nativas. Las aceleraciones
  significativas que realmente ha visto vinieron de rediseños: caché, pasar a
  asíncrono, paralelizar y arreglar consultas N+1.
---

La mayoría de los comentarios rechaza la premisa central de la publicación, que
la mayoría de los programas reales están limitados por E/S, porque no coincide
con su perfilado: una consulta a la base de datos tarda ~5ms pero una respuesta
promedio tarda ~500ms, de modo que la mayor parte del tiempo es sobrecarga
limitada por CPU dentro de la propia aplicación, no en el cable. La objeción
más dura, del comentario mejor puntuado, es que "los programas reales en su
mayoría" significa en silencio servidores CRUD: los motores de disposición del
navegador, los renderizadores 3D, los procesadores de texto y las redes
neuronales son todos limitados por CPU, y el planteamiento del artículo los
excluye por construcción. Un segundo flanco ataca el argumento de que "los
lenguajes lentos ya delegan en bibliotecas rápidas": untitaker y weberc2
informan de que el marshaling de datos a través de la frontera de la FFI ha
hecho retroceder el rendimiento en proyectos que reescribieron puntos calientes
en C o Rust. Un hilo más pequeño debate si la semántica del lenguaje marca un
suelo del que ninguna implementación puede escapar, con nrposner argumentando
que el dispatch dinámico sin monomorfización es un overhead inevitable, y fanf
contraargumentando que un JIT al estilo Self podría monomorfizar cualquier
cosa.
