---
layout: post
title: "Qwenputer: una CPU RISC-V funcional y determinista dentro de Qwen3.5"
date: 2026-10-29 10:29:35 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://divagr.com/blog/qwenputer"
image: "/images/digest/2026-10-29-qwenputer-functioning-deterministic-risc-v-cpu-inside-qwen3.jpg"
hn_url: "https://news.ycombinator.com/item?id=50282838"
share_text: "18M instrucciones RISC-V sin errores en los pesos de Qwen: ¿refutación del determinismo o máquina de Rube Goldberg?"
summary: >-
  Qwenputer es un modelo Qwen3.5 4B de fábrica con una CPU RISC-V de 32 bits
  funcional compilada directamente en sus pesos: sin entrenamiento, sin
  herramientas, sin runtime externo. Al fijar el gate de Gated DeltaNet y la
  fuerza de escritura en 1 con claves one-hot, las capas de atención
  recurrente del modelo se convierten en RAM exacta y direccionable, y 11
  capas añadidas ejecutan instrucciones mientras Qwen decodifica. El autor
  afirma que el núcleo pasa las oficiales riscv-tests, coincide con qemu y
  ejecutó 18 millones de instrucciones sin errores. En los benchmarks
  aritméticos eleva a Qwen base del 48,6% al 100% en enteros largos de
  NUPA, igualando a una herramienta en Python, y una variante experimental
  añade un filesystem de 512 archivos que persiste entre chats.
---

Un núcleo RISC-V que pasa las riscv-tests, coincide con qemu y ejecutó 18
millones de instrucciones en régimen libre dentro de un Qwen3.5 de fábrica fue lo
que captó los votos positivos, y la mayoría de los comentarios coincidió en
que el truco es legible: una CPU no es más que una función del estado de un
ciclo al siguiente, materializada aquí en pesos, con el estado de Gated
DeltaNet fijado como RAM exacta y direccionable. La disputa principal, sin
embargo, gira en torno a lo que eso demuestra sobre el determinismo: un
lector lo llamó una contundente refutación de la idea de que los LLM son
inherentemente no deterministas, mientras que otros respondieron que una CPU
codificada a mano en la arquitectura no dice nada sobre la inferencia en
producción, donde ni siquiera temp=0 garantiza reproducibilidad. Un segundo
frente es el propósito mismo: la demo fue puesta al lado de DOOM corriendo
dentro del sistema de tipos de TypeScript y llamada máquina de Rube Goldberg,
interesante pero enteramente superflua. Nota menor: una larga tangente se
dedicó al steering de un evil-Qwen a nivel de neurona individual, y otra más
breve preguntó si congelar los pesos de la CPU podría mantenerla en
funcionamiento durante el entrenamiento continuado.
