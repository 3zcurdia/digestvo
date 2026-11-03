---
layout: post
title: "Astra lee y escribe pesos para mejorar Qwen"
date: 2026-11-03 09:14:45 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://rikiyat.github.io/blog/weight-space-programming/"
image: "/images/digest/2026-11-03-astra-read-write-weights-improve-qwen.jpg"
hn_url: "https://news.ycombinator.com/item?id=50341174"
share_text: "Astra editó el 0.016% de los pesos de Qwen3.5-0.8B y MATH-500 saltó de 7.9% a 48.1% — sin un solo gradiente"
summary: >-
  El equipo de MIT CSAIL publicó un experimento en el que GPT-6 Astra lee y
  escribe pesos de redes neuronales sin gradientes ni entrenamiento. Astra
  identifica qué juego entrenó una red solo con sus pesos, repara una política
  de PPO atascada editando el 3.5% de sus pesos y escribe redes desde cero que
  superan a PPO entrenado 100 millones de pasos. En el resultado más
  llamativo, editar 131,072 pesos (0.016%) de Qwen3.5-0.8B para eliminar
  bucles de razonamiento sube MATH-500 de 7.9% a 48.1% e IFEval de 21.0% a
  62.3%. Los autores publicaron los logs de todos los experimentos y el modelo
  editado.
---

El blog de MIT CSAIL publicó el 2 de noviembre Weight-Space Programming, en el
que GPT-6 Astra lee y edita pesos sin gradientes, y la historia llegó a 2,872
puntos en Hacker News. La mayoría coincidió en subrayar lo inesperado del
hallazgo: Astra nombra el juego que entrenó una red solo con sus pesos,
encuentra las induction heads que coinciden con el ground truth, y editar el
0.016% de los pesos de Qwen3.5-0.8B sube MATH-500 de 7.9% a 48.1%; varios lo
llamaron un golpe al stochastic parrot. Sin embargo, la discusión real es si
esto es una capacidad nueva o interpretability de siempre: los escépticos
apuntaron que buena parte de los experimentos es multiplicar matrices a mano, y
que el arreglo de Qwen solo elimina un bucle que la propia model card ya
advertía; el propio post admite que Astra no mejoró Gemma 3 270M, que no buclea.
Aun así, otros defendieron que el modelo lee patrones que ningún humano leería y
que el método abre auditoría sin evaluación. Como nota menor, una rama lateral
derivó hacia si esto cuenta como AGI y hacia la desigualdad social.
