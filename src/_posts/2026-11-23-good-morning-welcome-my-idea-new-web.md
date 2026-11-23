---
layout: post
title: "Buenos días y bienvenidos a mi idea de una web nueva"
date: 2026-11-23 11:02:24 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://dave.writersweb.org/index.md"
image: "/images/digest/2026-11-23-good-morning-welcome-my-idea-new-web.jpg"
lobsters_url: "https://lobste.rs/s/l8u1tj/good_morning_welcome_my_idea_new_web"
share_text: "La web de Winer deja CSS y JavaScript, pero los dialectos de Markdown harían sitios incompatibles. #Web #Markdown"
summary: >-
  Dave Winer propone una web donde Markdown reemplaza a HTML como el formato
  en que se sirven las páginas. Su navegador de prueba, con el nombre en
  código BonBon, toma la URL de cualquier archivo Markdown de la web y lo
  renderiza como una página legible. Los sitios no pueden enviar CSS ni
  JavaScript: los estilos y los scripts pertenecen al software del lector,
  que aplica sus propias plantillas y hojas de estilo. La demo también
  ofrece un conmutador para ver el código, un selector de hoja de estilo y
  enlaces a páginas de ejemplo y tablas de contenido OPML.
---

La propuesta viene de Dave Winer, el inventor de RSS, y llega con una demo
en vivo que renderiza cualquier URL de Markdown como una página cuyo CSS y
scripts pertenecen a la app del lector, no al sitio. Hubo acuerdo en la meta:
los navegadores podrían renderizar Markdown de forma nativa sin complementos,
y las páginas ya se leen bien con curl y pandoc o un navegador de texto como
w3m. El debate principal fue la elección de formato. Markdown se parte en un
millón de dialectos, muchos permiten HTML incrustado, y el post nunca nombra
a cuál apuntar, así que los sitios quedarían incompatibles entre navegadores;
el front matter de YAML es un apaño que oculta que Markdown no tiene
metadatos, y otros propusieron en su lugar Djot, reStructuredText, AsciiDoc,
Org Mode o Typst. Sin embargo, FRIGN argumentó que el error más profundo es
dejar HTML a un lado para todos, produciendo otro Gopher segregado: la
negociación de contenido de HTTP con las cabeceras Accept y Vary permitiría
que cada cliente pida text/markdown y mantenga las puertas abiertas. Como
nota menor, los lectores se quejaron de que el texto crudo es ilegible en un
teléfono, con líneas del tamaño de dos pantallas, y la demo se había enviado
cuatro días antes como markdownweb.
