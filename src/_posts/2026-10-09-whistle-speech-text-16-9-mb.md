---
layout: post
title: "Whistle: voz a texto en 16.9 MB"
date: 2026-10-09 08:51:10 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://cactuscompute.com/blog/whistle"
hn_url: "https://news.ycombinator.com/item?id=50008427"
share_text: "Voz a texto en 16.9MB, en CPU, 11ms al primer token. Whisper quedó atrás. #AI #STT"
summary: >-
  Cactus Compute lanza Whistle, un modelo abierto de reconocimiento de voz
  empaquetado como un solo archivo de 16.9 MB que corre en la CPU sin
  dependencias. Transcribe siete idiomas, inglés, alemán, francés, español,
  italiano, neerlandés y polaco, con marcas de tiempo por palabra y embeddings
  de voz, todo en el dispositivo. La publicación reporta que supera a Whisper
  base y a Moonshine tiny v2 en varios benchmarks de tasa de error de
  palabras, alcanzando su primer token en 11.1 ms y decodificando 1.319 tokens
  por segundo. Los pesos, un motor en C++ y un paquete de Python llegan en
  Hugging Face, GitHub y PyPI.
---

La mayoría de los comentarios coinciden en que los benchmarks son genuinamente impresionantes para el tamaño, porque pruebas directas en el hilo transcribieron frases complejas con precisión en una huella lo bastante pequeña para caber en la caché L3 de la CPU. La objeción más aguda es que el tamaño del binario nunca fue lo difícil de la voz a texto: un comentarista dice que el verdadero reto es transcribir a su padre de 84 años con secuelas de un derrame, y cada sonido que sale de su boca igual termina en la página. Eso conecta con una queja recurrente de calidad, porque los modelos pequeños supuestamente rinden en acentos occidentales limpios dentro de la distribución pero se degradan con el español mexicano y venezolano y con el ritmo conversacional. Un argumento más estrecho corre sobre la afirmación de la L3 misma: un lector dice que residir en caché compra un orden de magnitud en latencia, otro responde que se nota sobre todo en throughput más que en latencia de punta a punta.
