---
layout: post
title: "Agentes implementan Campfire en Elixir, Go y Rust"
date: 2026-10-05 09:42:17 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://x.com/dhh/status/2106810173683851564"
share_text: "DHH dejó que agentes reescribieran Campfire en 3 lenguajes. Ruby perdió. ¿Aún importa el lenguaje? #Ruby #Rust"
summary: >-
  DHH cuenta que puso a agentes de programación a implementar y optimizar la app web Campfire en Elixir, Go y Rust, con Ruby como el más lento. Dice que hace tiempo aceptó ese costo a cambio de productividad y alegría del desarrollador. Pregunta si ese intercambio aún vale si los agentes escriben y validan código que los humanos ya no leen. En un seguimiento añade que Rust tiene costos como compilaciones lentas, pero insiste en que el código escrito por agentes exige una nueva visión de la elección del lenguaje.
---

La mayoría de las respuestas apuntan a que la comparación fue desigual más que a la pregunta de DHH sobre el código que nadie lee, porque el port a Rust recibió cientos de commits durante días mientras Elixir y Go recibieron uno o dos desde una reescritura inicial. La objeción más dura es el punto de proceso de Jose Valim, respaldado por los detalles de código de Zach Daniel: los prompts vagos dejaron que los agentes tomaran decisiones arquitectónicas como canalizar todo el SQL por un solo GenServer.call, mantener Redis en Elixir y eliminar CSRF por HTML cacheable en Rust. DHH responde que la salida de los agentes sin ajustes es justamente el punto, con ports a Laravel y Django que muestran el mismo ejercicio, pero eso concede que el ranking mide los valores por defecto de los agentes, no los techos de los lenguajes. La respuesta constructiva es la rehechura idiomática de Elixir desde cero de Jakub Skalecki, orientada a probar si igual esfuerzo cierra la brecha.
