---
layout: post
title: "Button Sounds, colección de clics de botones grabados profesionalmente"
date: 2026-11-25 10:51:19 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://buttons.joshwcomeau.com/"
image: "/images/digest/2026-11-25-button-sounds-collection-professionally-recorded-button-clicks-presses.jpg"
hn_url: "https://news.ycombinator.com/item?id=50638032"
share_text: "Más de 50 clics multigrabados, y una discusión sobre si los sonidos de UI deben romper el modo silencioso #WebAudio #UX"
summary: >-
  Button Sounds es una colección gratuita de más de 50 clics y toggles de
  interfaz multigrabados por el desarrollador front-end Josh Comeau, con
  formación en ingeniería de audio. Cada sonido se compone en realidad de
  varias grabaciones del mismo objeto, así que pulsar el mismo botón dos veces
  nunca suena robótico. Los archivos se distribuyen como WAV de 48kHz o MP3 de 192kbps
  bajo licencia MIT, junto con un paquete NPM con bindings de JavaScript puro y
  de React. El sitio es un laboratorio para escuchar todos los sonidos, y el
  autor recomienda reproducirlos al 25% o 50% del volumen con opción de
  silenciar.
---

La publicación llega como un proyecto secundario pulido de Josh Comeau, un
ingeniero de audio que graba decenas de tomas por sonido para que los clics
repetidos nunca suenen robóticos, y la mayoría de los comentarios responde con
entusiasmo por la calidad de la grabación, la licencia MIT gratuita y la idea
del multigrabado. Sin embargo, la tensión más viva fue la etiqueta de audio en
móvil: el autor señala que los navegadores, iOS Safari en particular, pueden
negarse a reproducir sonido, y un comentario señaló que poner
navigator.audioSession.type en "playback" lo desbloquea incluso en modo
silencioso. Otros respondieron que los sonidos de interfaz deberían respetar el
interruptor de silencio, porque son ruido de fondo no solicitado y no
multimedia que el usuario pidió. Una segunda crítica, más concreta, vino de
alguien que notó que la variante DOWN4 está casi un semitono por debajo de las
otras muestras de pulsación, y pidió variaciones afinadas con ecualización,
distorsión y reverb en lugar de pitch shifting. Nota menor: el hilo también se
desvió hacia los sonidos de puertas de autos, con varias personas describiendo
cómo los fabricantes diseñan a propósito el golpe seco de un Golf o de una
Mercedes G-wagon.
