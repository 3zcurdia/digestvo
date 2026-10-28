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

La autora relataba cuatro meses usando Zig tras volver desde Rust para escribir *snurl* (un cliente de smallnet) y su asistencia a Zig Day Seattle. Destacaba los parámetros explícitos de asignador y E/S, *comptime*, el sistema de compilación, los árboles de dependencias casi nulos, el manejo de errores con *try* y un compilador rápido. También pedía estabilidad en la *stdlib* antes de la 1.0, mejor ayuda con *lifetimes*, documentación y una ruta de arranque independiente de un blob WASM incluido en el repo.

La mayoría de los comentarios coincidió en que la cultura de dependencias era el punto fuerte de Zig. Varios señalaron las quejas habituales con los árboles transitivos de Cargo y elogiaron la *stdlib* de Zig por cubrir utilidades como JSON, base64, PRNG, TLS o compresión sin depender de paquetes externos.

Sin embargo, el mayor debate fue sobre si Rust lleva inevitablemente a usar *panics*. Algunos argumentaron que *unwrap* por defecto no es la norma, que el operador `?` es eficiente y que *Clippy* prohíbe *unwrap/expect* en CI. Otros replicaron que los *panics* de prototipo sobreviven a producción y que los linters no corrigen ese hábito en todo el ecosistema, lo que llevó a un intercambio sobre cómo subir el rigor gradualmente.

Como nota menor, se señaló que la *stdlib* de Zig son esencialmente utilidades extraídas del compilador, por lo que su cobertura refleja lo que este necesitaba, no necesariamente una biblioteca estándar bien redondeada.
