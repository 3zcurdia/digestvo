---
layout: post
title: "Saltarse el límite de 60 FPS de iOS Safari para crear aplicaciones web que se sienten nativas"
date: 2026-11-25 10:51:19 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://rida.dev/blog/bypassing-ios-safari-60-fps-limit"
image: "/images/digest/2026-11-25-bypassing-ios-safaris-60-fps-limit-build-web.jpg"
hn_url: "https://news.ycombinator.com/item?id=50637890"
share_text: "Sin flags, 118 FPS: un controlador de scroll invisible más OffscreenCanvas saca a iOS Safari del tope de 60 Hz #WebKit #iOS"
summary: >-
  Rida F'kih explica cómo saltarse el tope de 60 FPS que WebKit impone en iOS
  Safari a menos que actives un ajuste de desarrollador llamado Prefer
  Rendering Updates near 60fps. Su truco trata áreas desplazables invisibles
  como controladores, leyendo su posición de scroll fuera del renderer con un
  bucle MessageChannel sincronizado con vsync, mientras un pequeño scroller
  acelerado por GPU mantiene la pantalla en sus 120 Hz completos. Para la
  salida, mover un canvas a un OffscreenCanvas hace que WebKit se salte la
  espera al siguiente paso de render, lo que entrega dibujo real a 120 FPS. Un
  benchmark de tres segundos de arrastre marca 118 FPS frente a 60 fijos en
  eventos de puntero.
---

El video de Jordan Walker con una interacción móvil que se siente nativa,
construida solo con DOM y CSS, puso en marcha la investigación, y la mayoría
de los lectores coincidió en que la queja es real: WebKit limita
requestAnimationFrame a 60 Hz en una pantalla de 120 Hz y mantiene la entrada
táctil en la misma tasa salvo que se active un flag de desarrollador enterrado.
La división más viva fue perceptual: un bando llamó engañoso al artículo
porque la demo muestra como mucho 60 cuadros con tirones visibles, mientras el
otro sostuvo que la diferencia entre 60 y 120 Hz se nota de inmediato al mover
una caja, y que limitar una app a la mitad de la tasa de refresco del panel le
hace un flaco favor al usuario. Un punto medio útil vino de los lectores
cuyos dispositivos estaban limitados por el Modo de bajo consumo o por el
ajuste de tasa de refresco de Accesibilidad, lo que explica por qué varios no
vieron diferencia alguna. La tensión sin resolver es de costo y permiso:
incluso los aficionados preguntaron qué compran el desgaste de batería y la
complejidad adicional frente a una app nativa, y el autor admite que Apple
podría cerrar mañana la puerta de OffscreenCanvas. Como nota menor, el widget
de scroll con efecto de vidrio líquido de la demo recibió quejas de
accesibilidad por migrañas y sensibilidad al movimiento.
