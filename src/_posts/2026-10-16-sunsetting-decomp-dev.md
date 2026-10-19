---
layout: post
title: "El cierre de decomp.dev"
date: 2026-10-16 09:38:43 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://decomp.dev/"
lobsters_url: "https://lobste.rs/s/kaerns/sunsetting_decomp_dev"
share_text: "Años de ingeniería inversa, deshechos por forks que queman tokens tras la barra de progreso"
summary: >-
  El mantenedor de decomp.dev, un índice de decompilaciones equivalentes de
  juegos clásicos, está cerrando su índice público. Escribe que la
  decompilación equivalente antes tomaba años de minucioso trabajo humano,
  pero modelos recientes como GPT-6-Astra pueden generar C equivalente,
  permutar variantes y sostener tareas largas a bajo costo con la guía
  adecuada. Esa capacidad desató forks hostiles terminados con IA, ports a PC
  apresurados y a medio funcionar construidos sobre trabajo ajeno, y una
  hueca carrera por el leaderboard. El sitio seguirá sirviendo las páginas e
  historiales de proyectos existentes, pero no aceptará proyectos nuevos.
---

La mayoría de los comentarios coincide en la simpatía con el mantenedor,
porque la falla concreta que reconocen son los forks de IA oportunistas que
persiguen el porcentaje de progreso sin revisar a mano si hay código que los
desarrolladores originales plausiblemente habrían escrito. El ejemplo de
Melee se vuelve la línea divisoria: la salida de un LLM es aceptable cuando
los mantenedores limpian con rigor los matches con trampa y los helpers
inlined, y no vale nada cuando solo quema tokens para subir el número. La
objeción más fuerte es por el repositorio cerrado y la negativa a permitir
forks, porque los críticos dicen que un índice con todos los derechos
reservados daña a la misma comunidad abierta que la IA ya dañó y nada hace
para frenar el entrenamiento. Los defensores responden que, tras ver cómo
decompilaciones abiertas se scrapeaban hacia modelos que luego corrían a
portear los juegos, mantener el código del sitio escrito por humanos y
cerrado es autopreservación.
