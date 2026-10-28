---
layout: post
title: "Four Months of Zig"
date: 2026-10-28 10:57:10 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://gracefulliberty.com/articles/four-months-of-zig/"
lobsters_url: "https://lobste.rs/s/qr59sa/four_months_zig"
share_text: "Zig: 1-2 deps, cero indirectas; los más pequeños de Rust, docenas. Su stdlib es solo lo que su compilador necesitaba."
summary: >-
  Cuatro meses después de volver a Zig desde Rust, la autora relata la
  escritura de snurl, una biblioteca cliente de smallnet (Gemini, Finger,
  Gopher), y su asistencia a Zig Day Seattle, donde apareció Andrew Kelley.
  Lo que le gusta: los parámetros explícitos de asignador y E/S que hacen
  visibles la asignación y los efectos secundarios, comptime, el sistema de
  compilación, árboles de dependencias casi nulos, el manejo de errores
  basado en try y un compilador incremental de menos de un segundo. Lo que
  pide: estabilidad de la stdlib antes de la 1.0, ayuda del compilador con
  lifetimes, documentación, asignadores en tiempo de compilación para JSON y
  una ruta de arranque que no dependa de un blob WASM incluido en el
  repositorio, que bloquea el empaquetado en Debian. Está portando ReTangled
  de Rust a Zig y mantendrá Zig como su lenguaje predeterminado.
---

La mayoría de los comentarios coincide en el argumento de la cultura de
dependencias, porque encaja con su propia experiencia: wofo, un usuario
intensivo de Rust, llama a los árboles de dependencias transitivas de Cargo
su mayor molestia con el ecosistema, y la lista de baterías de la stdlib de
Zig de kprotty (JSON, base64, PRNG, TLS, compresión) se ganó las gracias de
un fan sorprendido de Rust. La objeción más fuerte apunta a la afirmación
del artículo de que Rust lleva a los programadores a insertar panics:
zmitchell, el comentario con más votos del hilo, responde que usar unwrap por
defecto no es la norma y que el operador ? es más rápido que unwrap en
cualquier caso, y ghoti señala los lints de Clippy que prohíben unwrap y
expect en CI. Liberty responde que los panics de prototipo sobreviven
rutinariamente a producción, algo que Clippy no puede corregir en todo un
ecosistema, y ghoti contraataca diciendo que acertar a la primera no es un
consejo accionable; subir el rigor gradualmente en CI sí lo es. Una objeción
más discreta, de intelfx, es que la stdlib de Zig son solo cosas extraídas
del compilador, de modo que sus baterías reflejan lo que el compilador
necesitaba más que una biblioteca estándar bien redondeada.
