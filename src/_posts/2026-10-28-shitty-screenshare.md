---
layout: post
title: "Shitty Screenshare"
date: 2026-10-28 10:57:10 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "http://shittyscreenshare.com"
lobsters_url: "https://lobste.rs/s/cxxcik/shitty_screenshare"
share_text: "OBS puede enviar un screenshare perfecto a cualquier llamada — si los proveedores adoptan WHIP. Zoom, Teams y Jitsi, no."
summary: >-
  shittyscreenshare.com abre con dos videos en bucle de la misma hoja de
  cálculo: uno compartido desde el navegador, borroso, y otro enrutado por
  OBS, nítido. El sitio sostiene que la diferencia está en el control —tu
  navegador elige el bitrate, el códec y la resolución por ti— y promueve
  WHIP (RFC 9725), un estándar abierto que permite que OBS o FFmpeg envíen
  video en vivo directamente a una videollamada con los ajustes que se
  elijan. Muestra la configuración de transmisión WHIP de OBS con capas de
  simulcast, lista los servicios que aceptan WHIP hoy y concluye instando a
  los lectores a escribir a su proveedor pidiendo estándares abiertos en
  lugar de un cliente propietario.
---

El sitio *shittyscreenshare.com* compara dos formas de compartir pantalla: una nítida a través de OBS con control total, y otra borrosa desde el navegador. Propone WHIP (RFC 9725) como estándar abierto para permitir a herramientas como OBS o FFmpeg enviar video en vivo directamente a las videollamadas.

La mayoría de los comentarios coincidió en que los proveedores ya resuelven este problema. Se señaló que Zoom usa por defecto un codificador orientado a texto y que Discord envía perfiles separados para juegos frente a fidelidad de texto, por lo que hay poco que un nuevo estándar de ingesta pueda aportar.

Sin embargo, la principal objeción fue estructural. Para que funcione bien con múltiples espectadores, el proveedor debe dictar la configuración del codificador y las escalas de ancho de banda, lo que hace que un ingreso WHIP arbitrario sea estructuralmente incompatible con esos servicios. Además, se apuntó que los ejemplos de adopción de WHIP no eran aplicaciones de videollamadas para el usuario final y que Jitsi lo había rechazado.

Como nota menor, algunos lectores no pudieron ver la evidencia porque los videos de comparación no cargaban en móvil. También surgió un debate lateral sobre el reescalado del lado del cliente: se propuso que Teams ejecutara Office en cada cliente para evitar el antialiasing, una idea que otros consideraron poco práctica.
