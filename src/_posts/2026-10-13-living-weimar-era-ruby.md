---
layout: post
title: "Viviendo en la era Weimar de Ruby"
date: 2026-10-13 09:16:08 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://blog.julik.nl/2026/10/the-weimar-of-ruby"
lobsters_url: "https://lobste.rs/s/lfen2h/living_weimar_era_ruby"
share_text: "DHH se fue, Ruby floreció: 8.900 gems nuevas en un año, PDF y Qt revividos por LLM. ¿Era Weimar? #Ruby"
summary: >-
  Julik Tarkhanov argumenta que Ruby vive un renacimiento creativo aun cuando la
  keynote de David Heinemeier Hansson en RailsWorld —donde anunció que reescribió
  HEY con vibe y que ya no necesita Rails— marca la salida del fundador. Con los
  LLM absorbiendo el tecleo, brechas de años se están cerrando: dos librerías de
  PDF capaces (sghtmltopdf y stationery), bindings revividos de Qt y Shoes, una
  reescritura de gRPC amable con async y una librería Parquet que él mismo
  construyó en días. Contando nombres de gems recién reclamados en rubygems.org,
  mide unas 8.900 en el último año contra 4.600 el año anterior —un salto que
  empieza en marzo de 2026—, evidencia de que la gente construye lo que falta en
  vez de invocar "nadie hace esto con Ruby de todos modos".
---

La mayoría de los comentarios se ubica en el escepticismo frente a la afirmación del artículo de que el tecleo es el cuello de botella, porque generar líneas nunca fue la parte escasa de programar. La réplica más aguda pregunta quiénes son esos desarrolladores de cerebro rápido, y argumenta que adorar las LOC contradice todo lo aprendido sobre boilerplate, autocompletado y lenguajes expresivos que reducen pulsaciones desde hace años. El contrapunto que gana terreno es más estrecho: los LLM se ganan el puesto en tareas rutinarias como convertir un struct de Rust de Copy a no Copy o masticar scaffolding repetitivo, no en diseño. Mientras tanto, la anécdota de la brecha en PDF genera simpatía, con incluso desarrolladores de Go sorprendidos de que Rails careciera de herramientas de maquetación y otros que señalan que hexapdf y ReportLab muestran que el dolor nunca fue solo de Ruby.
