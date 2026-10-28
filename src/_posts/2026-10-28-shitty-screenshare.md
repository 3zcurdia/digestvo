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

La mayoría de los comentarios coinciden en que WHIP es la solución
equivocada, porque los incumbentes ya manejan esto: calvin señala que Zoom
usa por defecto un codificador orientado a texto y Discord envía perfiles
separados para juegos frente a fidelidad de texto, de modo que poco le queda
por resolver a un nuevo estándar de ingesta. La objeción más fuerte es la de
k0nserv: un proveedor debe dictar la configuración del codificador y las
escalas de ancho de banda para cada espectador, de modo que un ingreso WHIP
arbitrario es estructuralmente incompatible con el funcionamiento de esos
servicios —y valpackett añade que ninguno de los puntos WHIP listados es una
aplicación de llamadas para el usuario final, mientras que Jitsi lo
rechazó. Muchos lectores tampoco llegaron a ver la evidencia, ya que los
videos de comparación no cargaban en móvil. Chisnall redirige la queja al
reescalado del lado del cliente, que desdibuja el texto con antialiasing sea
cual sea el bitrate, proponiendo el truco de Teams de ejecutar Office en
cada cliente en su lugar —una solución que bityard responde que nadie pidió.
