---
layout: post
title: "Jailbreak al navegador de mi coche solo para poder cambiar la hora"
date: 2026-11-03 09:14:45 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://blog.nns.ee/2026/11/02/renault-hack/"
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

El detonante fue el cambio a horario de invierno en Estonia: el reloj del
Renault quedó una hora desfasado y el menú para ajustarlo no existía sin la
tarjeta SD, porque la definición del propio menú se lee de la tarjeta y la DRM
exige su CID único. Sin embargo, el hilo no discute el hack sino su motivo: el
comentario más votado lamenta un Seat Ibiza cuyo TomTom quedó abandonado dos
años después de salir de fábrica, mientras el autor solo quería cambiar la hora.
El consenso es doble: el writeup destaca por ser ingeniería inversa hecha a
mano, sin lanzar un LLM al problema, y la seguridad del aparato de 2011 resulta
sorprendente, con montajes de solo lectura y noexec y actualizaciones firmadas
por un módulo de kernel propio. Aun así, la tensión real es si esa seguridad
protege al usuario o lo encierra: sin la tarjeta de 60 EUR no había menú, y la
alternativa fue escribir en core pattern con el comando LOG para lanzar
payload.sh como root. Como nota menor, otros lectores comparten relojes
imposibles, de un Mazda 2010 que ignora el horario de verano a una moto que se
reinicia cada invierno.
