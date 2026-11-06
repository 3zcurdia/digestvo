---
layout: post
title: "Claude Code envía tu dirección de correo a los sitios web"
date: 2026-11-06 10:01:08 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://github.com/anthropics/claude-code/issues/107757"
image: "/images/digest/2026-11-06-claude-code-sends-email-address-websites.jpg"
hn_url: "https://news.ycombinator.com/item?id=50385272"
share_text: "Claude Code enviaba tu correo en cabeceras User-Agent: decenas de estafas al día y un fix que solo bloquea esa dirección"
summary: >-
  Una issue de GitHub contra Claude Code afirma que la herramienta puso el correo
  de la cuenta del usuario en la cabecera User-Agent de las peticiones web de
  salida, de modo que todo sitio que visita el agente lo ve; quien la reporta
  dice que por esto recibe decenas de correos de estafa al día y que está
  cambiando su empresa de Anthropic. El reporte lleva 589 reacciones de pulgar
  hacia arriba y las etiquetas de area:security. Anthropic respondió que un mod
  integrado, cc-plugin-privacy, se distribuye activado por defecto en la v2.1.317
  y bloquea el comportamiento de forma determinista. Varios comentaristas señalan
  que la SEC y Wikimedia sí piden una dirección de contacto a los clientes
  automatizados.
---

El punto de partida es un cliente que despierta lleno de correo de estafa:
quien reporta el caso dice que Claude Code puso el correo de su cuenta en el
User-Agent de las peticiones web de salida y que está sacando a su empresa de
Anthropic, y la mayoría de los comentaristas coincidió en que exponer la
dirección de un cliente que paga es indefendible sin importar la intención. La
polémica central es dónde vive realmente la filtración. Un bando la trata como
código determinista del andamiaje que adjunta la dirección; otro argumenta que
el correo simplemente vive en el contexto del modelo y que el modelo improvisa
comandos curl -A, de modo que no hay una línea que borrar. Aun así, ambos
bandos coinciden en que la solución que envió Anthropic, el mod cc-plugin-privacy
de la v2.1.317 que rechaza las llamadas a shell que nombran la dirección de la
cuenta, es demasiado estrecho: solo coincide con el correo, así que una cabecera
personalizada, un script escrito con Edit o un token derivado de la sesión como
my-project-site-build/1.0 sigue pasando. Como nota menor: algunos defendieron
la práctica, porque la SEC y Wikimedia sí piden una dirección de contacto a los
clientes automatizados.
