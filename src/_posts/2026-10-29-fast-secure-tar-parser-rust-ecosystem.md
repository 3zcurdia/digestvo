---
layout: post
title: "Un parser de tar rápido y seguro para el ecosistema de Rust"
date: 2026-10-29 10:29:35 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://astral.sh/blog/tar-codec"
image: "/images/digest/2026-10-29-fast-secure-tar-parser-rust-ecosystem.jpg"
lobsters_url: "https://lobste.rs/s/q7arzy/fast_secure_tar_parser_for_rust_ecosystem"
share_text: "Astral reescribe el parser de tar de uv para que uv y pip no vean archivos distintos en el mismo tarball: 2x más rápido"
summary: >-
  El equipo de Astral presenta tar-codec, el parser de tar que desde uv 0.13
  reemplaza a astral-tokio-tar. Es aproximadamente el doble de rápido que su
  predecesor y reduce la exposición a parser differentials: la situación en la
  que uv, pip u otras herramientas ven contenidos distintos para el mismo
  tarball. El post recorre la familia de formatos tar —V7, UStar/pax y GNU— y
  explica cómo un estado de máquina estricto, que bloquea cada archivo a una
  sola familia, rechaza en lugar de adivinar las ambigüedades que otros
  parsers resuelven de forma inconsistente. También presenta archive-trait,
  una capa común de extracción anclada con cap-std.
---

Durante un año uv recibió informes de seguridad sobre astral-tokio-tar que
permitían hacer que uv, pip u otras herramientas vieran contenidos distintos
para el mismo tarball, y tar-codec es la reescritura estricta que Astral eligió
en lugar de parchear ese parser. El post se recibió con entusiasmo por sus
diagramas y su explicación del formato, y hubo consenso en que extraer a disco
es la capa más difícil, porque cada sistema operativo y filesystem aplica sus
propias semánticas. Sin embargo, la tensión principal es un argumento de andyc:
compatibilidad y evitar parser differentials son fundamentalmente opuestos,
porque soportar más features amplía el espacio de divergencias posibles; su
salida sería acotar el problema, definir el 'tar mínimo' que necesitan los
sdists de PyPI y rechazar en la subida. La escala se puso en números: bakkot
consultó el BigQuery de PyPI y contó 9,8 millones de .tar.gz, unas 12 TB de
tráfico para bajarlos todos. Como nota menor, otro intercambio discutió si
'parser differentials' es un anglicismo: un comentario la tachó de inglés de
Claude, votado negativo, y tres réplicas señalaron que es un término de arte de
2011.
