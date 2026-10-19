---
layout: post
title: "Example.com acaba de lanzar el mayor rediseño en décadas"
date: 2026-10-06 09:23:08 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://www.debugbear.com/blog/example-dot-com-redesign-history"
hn_url: "https://news.ycombinator.com/item?id=49971921"
share_text: "example.com tuvo su mayor rediseño en décadas. Seis idiomas, un libro en SVG. #Web"
summary: >-
  El dominio reservado para documentación de IANA, example.com, recibió su
  mayor renovación en décadas el 28 de septiembre de 2026. La página estática
  en inglés sumó seis idiomas —inglés, árabe, chino, francés, ruso y
  español— que al inicio rotaban cada cinco segundos con una transición de
  opacidad por carácter, además de un ícono de libro en SVG insertado con
  JavaScript. IANA dice que dividió la página en un núcleo de HTML puro y un
  archivo JavaScript separado porque la mayor parte de su tráfico es
  automatizado y nunca descarga ese archivo, lo que reduce el ancho de banda.
  El 3 de octubre se eliminó la animación y todos los idiomas se muestran a la
  vez, con el idioma preferido del navegador al inicio.
---

La mayoría de los comentarios coincide en que la aritmética del ancho de banda
es la verdadera historia, porque la declaración de IANA señala que la mayoría
de las visitas a example.com viene de archivos de configuración copiados y
pegados y bots que nunca ejecutan JavaScript, así que servir las traducciones
en s.js no les cuesta nada a esos clientes. La objeción más aguda es que la
página debió seguir estática y solo en inglés, pues un marcador que sirve un
endpoint HTTP de cortesía gana poco con seis párrafos traducidos más un SVG, y
account42 argumenta que la simplicidad sin costo era todo el sentido del
dominio. Un segundo flanco es la accesibilidad: los lectores encontraron
imposible terminar la rotación de idiomas de cinco segundos antes de que
saltara al siguiente alfabeto, lo que IANA concedió al eliminar la animación
el 3 de octubre, aunque algunos defensores llaman al SVG el único color en una
página por lo demás desnuda. Un debate lateral menor estalló sobre si el
artículo de DebugBear fue escrito con IA, después de que un comentarista
afirmara que el SVG seguía apareciendo con JavaScript desactivado y otro
pegara el código de s.js que prueba que inyecta el marcado.
