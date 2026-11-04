---
layout: post
title: "Jailbreak al navegador de mi coche solo para poder cambiar la hora"
date: 2026-11-03 09:14:45 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://blog.nns.ee/2026/11/02/renault-hack/"
hn_url: "https://news.ycombinator.com/item?id=50339288"
image: "/images/digest/2026-11-03-jailbreaking-my-cars-navigation-system-i-change-time.jpg"
lobsters_url: "https://lobste.rs/s/qvdatp/jailbreaking_my_car_s_navigation_system"
share_text: "Sin SD con DRM no hay menú de hora: 60 EUR o core pattern para obtener root en el coche"
summary: >-
  El autor de un Renault Latitude de 2014 consiguió cambiar la hora de su
  navegador TomTom Carminat LIVE, que oculta el menú de ajuste de reloj si no
  detecta una tarjeta SD de mapas original con DRM por CID. Antes de pagar 60
  EUR por un recambio, revirtió el firmware, montó un emulador en QEMU para
  probar ataques y encadenó un path traversal en el intérprete de
  master.script con el core pattern de Linux para ejecutar su script como
  root. Con acceso total editó el desfase horario guardado en settings.dat, de
  180 a 120 minutos.
---

**En Hacker News.** El autor compró un Renault Latitude 2014 y, tras el cambio
de horario en Estonia, se encontró el reloj desfasado una hora: la opción de
ajustar la hora vivía detrás de una tarjeta SD de mapas con DRM que el dueño
anterior había tirado, y una réplica legítima costaba unos 60 EUR. El consenso
del hilo es que el diseño es hostil: aplauden el artículo por documentar el
exploit antes de que haga falta otra vez y comparten sus propios relojes
imposibles, desde un CR-V 2014 sin botón de pausa hasta un Toyota 2025 con dos
relojes que solo actualiza vendiendo datos de conducción a aseguradoras. Aun
así, la tensión gira en torno a si merecía la pena: varios sostienen que habría
bastado con comprar la tarjeta de 60 EUR o un equipo de navegación
aftermarket, mientras otros defienden que un ajuste de hora no debería depender
de un accesorio con DRM ligado al CID de la tarjeta. Como nota menor, parte del
hilo especuló con que algunas unidades no recibirán las nuevas reglas DST de
provincias canadienses que dejaron de cambiar los relojes este otoño, y
rememoró los relojes de VCR parpadeando en 12:00.

**En Lobsters.** Un artículo sobre cómo obtener root en la unidad TomTom de un
Renault de 2014, escrito sin otra razón mayor que la imposibilidad de mover el
reloj por el cambio de horario, encendió el debate. La mayoría de los
comentarios coincidió en la acusación más amplia: la navegación de fábrica
envejece mal, con la unidad de un Seat Ibiza abandonada unos dos años después
de fabricarse el coche, mientras que autos tan básicos como el Slate se ganan
elogios porque cada quien lleva su propio teléfono. La pelea de fondo es sobre
el diseño que hizo posible ese bloqueo. Algunos leyeron las protecciones — DRM
por ID de la tarjeta, actualizaciones firmadas aplicadas por un módulo de
kernel dedicado y montajes de solo lectura o noexec — como
impresionantemente sólidas para un dispositivo Linux 2.6 de 2011; un dueño
señaló que TomTom todavía vende mapas para su Megane de 2013, así que la
antipiratería puede haber valido la pena. Aun así, el consenso en contra de
TomTom y Renault se mantiene: esa misma protección escondía la definición del
menú en una tarjeta SD propietaria que costaba unos 60 EUR, convirtiendo un
ajuste de reloj en un jailbreak de firmware. Nota menor: un par de
comentaristas contaron sus propias quejas de relojes, desde un Mazda 3 ajeno
al horario de verano hasta un tablero de motocicleta dejado permanentemente
mal.
