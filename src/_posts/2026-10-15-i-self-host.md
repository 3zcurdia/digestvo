---
layout: post
title: "Lo que autoalojo"
date: 2026-10-15 09:41:50 -0600
categories: digest
tags: ["Systems & Infra"]
source_url: "https://viceconsole.fyi/blog/2026/10/10/what-i-self-host/"
lobsters_url: "https://lobste.rs/s/j4tlzg/what_i_self_host"
share_text: "Una mini PC de 180 € corre 28 servicios autoalojados, pero ¿quién vigila al vigilante autoalojado?"
summary: >-
  Harto de los servicios de streaming y sus trucos de engagement, el autor
  mudó casi todo a una sola mini PC Beelink —un Intel N100 con 16 GB de RAM
  comprado por 180 €— y ahora corre 28 servicios autoalojados: 17 binarios
  nativos y 11 contenedores Podman, todos gestionados por systemd. El
  inventario incluye Jellyfin, Immich, Frigate con 8 cámaras IP, Home
  Assistant, Caddy, Vaultwarden y respaldos con Restic, con htop mostrando
  solo 7.5 GB de memoria en uso. Sus reglas básicas: no exponer nada a la
  internet pública (su ISP está detrás de CGNAT), preferir servicios nativos
  de un solo binario sobre pilas de compose, y nada de Docker.
---

La mayoría de los comentarios coincide en el único punto ciego del
artículo: autoalojar Uptime Kuma, porque el monitor muere con la máquina que
vigila. La objeción más fuerte es la de markerz —un disco lleno o un corte
de luz tumba al monitor junto con todo lo demás, por eso él mantiene el
monitoreo en la nube. Las respuestas contestan con detalles: una diminuta
VPS always-free de Oracle usada solo para sondear, un dead-man's switch de
healthchecks.io que alerta cuando el monitor deja de reportarse, y la idea
más votada, de technomancy —que quienes autoalojan intercambien monitoreo y
respaldos entre sí como ayuda mutua en vez de comprar almacenamiento B2. Un
segundo debate gira sobre Tailscale: los lectores temen depender de él, uno
migró a WireGuard plano para un montaje de dos servidores, y los usuarios de
Headscale reportan que cada versión obliga a editar el archivo de
configuración.
