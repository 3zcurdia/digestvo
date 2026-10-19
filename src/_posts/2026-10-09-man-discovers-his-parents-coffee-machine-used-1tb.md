---
layout: post
title: "Descubre que la cafetera de sus padres consumió 1TB de datos en 10 días"
date: 2026-10-09 08:51:10 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://www.dexerto.com/entertainment/man-discovers-his-parents-coffee-machine-used-1tb-of-data-in-10-days-3416399/"
hn_url: "https://news.ycombinator.com/item?id=49995495"
share_text: "La cafetera de sus padres devoró 1TB en 10 días. La desconectó y compró una tonta. #IoT"
summary: >-
  Un hombre que auditaba la red doméstica de sus padres descubrió que su
  cafetera inteligente Keurig había generado un terabyte completo de tráfico
  en apenas diez días, y compartió el hallazgo en una publicación viral en X.
  Dice que lleva más de diez años trabajando en TI y que ayuda a sus padres a
  gestionar su conexión a internet en remoto. Después de que la publicación
  ganó atención, aclaró que la mayor parte del tráfico se quedó dentro de la
  casa en vez de cruzar su enlace de internet, y lo llamó «probablemente un
  bug de esta unidad» que saturó su punto de acceso. En vez de investigar más,
  desconectó la máquina y va a comprarles una cafetera nueva.
---

La mayoría de los comentarios toman el episodio como prueba de que el IoT de consumo no pertenece a una red doméstica normal, y varios responden con salidas prácticas: una VLAN separada para IoT, un dongle con ESPhome o una Moccamaster tonta de hace quince años. La pelea sustantiva es sobre qué fue realmente ese terabyte. Grombobulous sostiene que no puede ser deliberado, porque ningún fabricante pagaría por ingerir un terabyte cada dos semanas de millones de máquinas, y mindslight hace las cuentas —1.1MB/seg son unas 17.000 sondas de sesenta y cuatro bytes por segundo, más de lo que un chip clase ESP32 siquiera puede enviar— antes de conceder que igual huele a bug. La objeción más aguda viene de altairprime, remitiendo al hilo original en X: el volumen se quedó mayormente en local, así que el escándalo no es el ancho de banda sino que la máquina escanea tu hogar para construir datos que Keurig vende a anunciantes. Ese reencuadre divide al hilo sobre el consentimiento: darle a un aparato tu contraseña de Wi-Fi es consentimiento implícito, dicen varios, frente a la postura de que no se puede esperar que un comprador común sepa que su cafetera está mapeando la casa.
