---
layout: post
title: "Perdón, pero todavía hay que pensar"
date: 2026-10-12 10:54:29 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://itsallaboutthebit.com/i-am-sorry-but-you-still-have-to-think/"
lobsters_url: "https://lobste.rs/s/k2natg/i_m_sorry_you_still_have_think"
share_text: "Las reescrituras con agentes de DHH no prueban nada: la versión en Rust pierde mensajes bajo carga. Hay que pensar. #Rust"
summary: >-
  Piotr Sarnacki desarma las reescrituras de Campfire hechas por DHH con agentes
  de IA, de Rails a Rust, Elixir y Go, sin leer el código resultante. Decisiones
  no funcionales como la compatibilidad hacia atrás, eliminar el token CSRF o
  reemplazar Redis con colas en proceso quedan respondidas en silencio por el
  prompt y no por el lenguaje, lo que vuelve la comparación entre lenguajes un
  sinsentido. La versión en Rust ejecuta consultas bloqueantes a la base de datos
  y locks sincrónicos dentro de tareas asíncronas cooperativas, y su canal de
  broadcast con capacidad de 256 pierde la mayoría de las notificaciones bajo
  carga; la versión en Elixir lo cambia por timeouts HTTP y 1,8 GB de memoria.
  Su conclusión: igual hay que pensar en los modos de fallo y los trade-offs.
---

La mayoría de los comentarios coincide con la tesis del artículo —delegar a la IA no elimina la necesidad de criterio— porque la confiabilidad viene de mantener el sistema simple y razonar sobre él sin pausa, no de que pasen los chequeos automatizados. La objeción más aguda es que la IA igual puede apuntarse al trabajo correcto: alandekok argumenta que el error de DHH fue pedir una reescritura en vez de primero pedirle al modelo una suite completa de pruebas para usarla como requisitos, y wpld cuenta que hizo exactamente eso en una migración de Angular a Vue con un solo bug de un input en el navegador. tinthedev va más lejos y trata a los LLM como colegas virtuales sueltos dentro de áreas de radio de impacto limitado, dondequiera que pueda probar cómo se ve un buen resultado. La cifra que sostiene el argumento es la tasa de entrega de notificaciones del 1 % de la reescritura en Rust bajo carga, según Zach Daniels, que facundoolano lee como prueba de que quienes defienden delegar tanto en la IA o no se preocupan por la confiabilidad o suponen que pasar los chequeos significa un sistema que funciona. El comentario más votado, con 38, es irónico más que furioso: el análisis probablemente tomó más esfuerzo humano que la reescritura con IA que desarma.
