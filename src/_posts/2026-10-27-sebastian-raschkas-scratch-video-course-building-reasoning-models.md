---
layout: post
title: "El curso en video de Sebastian Raschka para construir modelos de razonamiento desde cero"
date: 2026-10-27 09:56:27 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://magazine.sebastianraschka.com/p/building-reasoning-models"
hn_url: "https://news.ycombinator.com/item?id=50245138"
share_text: "Raschka arma un modelo de razonamiento en 11 horas de video, desde Qwen3 0.6B. La objeción: un video no enseña a entrenar."
summary: >-
  Sebastian Raschka publicó ocho videos gratuitos de código, más de 11 horas,
  como secuela de su curso Coding LLMs from the Ground Up y complemento de su
  libro Build a Reasoning Model (From Scratch). Partiendo de los pesos
  preentrenados de Qwen3 0.6B en PyTorch, la serie construye un verificador de
  respuestas matemáticas, evalúa en MATH-500 y luego implementa escalado en
  tiempo de inferencia mediante muestreo, autocoherencia y autorrefinamiento,
  un bucle GRPO simplificado con recorte y términos KL, y por último destilación
  a partir de las respuestas de DeepSeek R1. Los primeros capítulos corren en
  CPU; el entrenamiento pide una GPU.
---

Los comentarios reciben el curso como una ovación de pie: lectores de los dos
libros de Raschka dicen que la pedagogía es lo que por fin les hizo entender
backprop y la tokenización, y uno que se gana la vida entrenando modelos dice
que el libro de LLM le enseñó más que cualquier otra fuente. La objeción más
afilada viene de hypfer, que pregunta para quién es el curso si un tutorial en
video no puede llevarte a través de un entrenamiento real, y llama al género una
compra de identidad; CamperBob2 responde que una clase nunca tuvo que reemplazar
la tarea, y hypfer concede en gran parte el punto. Debajo hay una preocupación
más práctica: qué hace un aficionado después del último capítulo, dados los
costos de preentrenar. La respuesta consensuada es no lo hagas: mejor hacer
fine-tuning o correr post-entrenamiento con LoRA y RL sobre modelos pequeños, o
cambiar los LLM por una ResNet.
