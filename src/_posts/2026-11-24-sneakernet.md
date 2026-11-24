---
layout: post
title: "Sneakernet"
date: 2026-11-24 12:28:37 -0600
categories: digest
tags: ["Systems & Infra"]
source_url: "https://sneakernet.eu/"
image: "/images/digest/2026-11-24-sneakernet.jpg"
lobsters_url: "https://lobste.rs/s/pdecff/sneakernet"
share_text: "Sneakernet reparte mensajes cifrados con el portátil, pero admite que no hay secreto hacia adelante #Security #OpenSource"
summary: >-
  Sneakernet es un sistema en desarrollo para enviar mensajes cifrados sin
  usar Internet. Los mensajes se pasan automáticamente entre usuarios de
  Sneakernet en la misma red local y luego se transportan físicamente en el
  portátil de alguien hasta otra red, donde los nodos los reciben y los
  reenvían. Todos los mensajes van autenticados y los privados van además
  cifrados, así que quien los transporta no puede leerlos ni alterarlos. El
  proyecto prevé aplicaciones construidas sobre él, como correo, tablones de
  anuncios y compartir archivos, siempre que toleren latencia alta y mensajes
  fuera de orden.
---

El proyecto de Drew DeVault llegó a Lobsters con 40 puntos y el hilo arrancó con
la queja de que la web no explica cómo funciona, una duda que el código en
SourceHut resuelve: multicast UDP en la LAN, sin pen drives, eso sería
sneakerweb. En lo esencial hubo acuerdo: es un proyecto curioso y honesto en sus
advertencias, pero de utilidad acotada, pensado para pasar mensajes con el
portátil entre redes en hackerspaces o eventos, no para sustituir a Internet; se
propuso en vano resucitar UUCP o NNCP, que ya hacen esto. La controversia
principal fue la seguridad: la propia página admite que es trivial averiguar
quién envía mensajes a quién, que no hay secreto hacia adelante y que no es
aconsejable organizar acciones directas con ello, así que un comentarista
sostuvo que llamarlo seguro es engañoso: los metadatos se recogen y las claves
se filtran. Sin embargo, la defensa fue que la advertencia está explícita, use
sneakernet to have fun, not to get into trouble, y que exigir un modelo de
amenaza de nivel Estado descalifica cualquier herramienta. Como nota menor, el
hilo derivó hacia la política de Drew DeVault contra dependencias con código
generado por LLM.
