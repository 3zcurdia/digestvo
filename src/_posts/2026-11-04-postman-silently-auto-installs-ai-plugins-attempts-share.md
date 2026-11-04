---
layout: post
title: "Postman instala en silencio plugins de IA e intenta compartir todos los datos de la API"
date: 2026-11-04 09:41:47 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://github.com/postmanlabs/postman-app-support/issues/14370"
image: "/images/digest/2026-11-04-postman-silently-auto-installs-ai-plugins-attempts-share.jpg"
hn_url: "https://news.ycombinator.com/item?id=50354960"
share_text: "Postman instaló plugins de Codex y Claude al arrancar y luego escribió el hash que aprueba su propio hook de inicio."
summary: >-
  Un usuario de macOS detalla en un issue de GitHub que abrir Postman 12.33.4
  desencadenó una "auto-existing-upgrade" que instaló en silencio plugins para
  Codex y Claude Code, añadió un endpoint MCP remoto y un Postman CLI, y
  registró un hook de inicio que le ordena al agente cargar la skill de
  Postman en cualquier tarea de API que no sea trivial. El propio registro de
  Postman consigna las instalaciones, y el código fuente fijado del instalador
  muestra cómo escribe un hash de confianza que preaprueba el hook que acaba
  de plantar. El reportero se detiene antes de afirmar que haya exfiltración
  de datos, y Postman no ha respondido públicamente. El issue acumula 337
  votos y 452 comentarios en Hacker News.
---

El contexto es un issue de GitHub, minucioso, de un usuario de macOS del 25
de octubre: el propio registro de Postman 12.33.4 consigna una
"auto-existing-upgrade" que instaló los plugins de Codex y Claude Code, y el
código fuente fijado del instalador muestra cómo la aplicación escribe el
hash de confianza que aprueba su propio hook de arranque. La mayoría
coincide en la ofensa: reescribir la configuración global de otra
herramienta y pre-confiar tu propia instrucción es una violación del
consentimiento, y el tono del hilo va de las desinstalaciones a las
comparaciones con malware. Sin embargo, la disputa más filuda es hasta dónde
alcanza la evidencia: el reportero se detiene explícitamente antes de afirmar
que haya exfiltración de datos, mientras que el titular de Hacker News dice
que Postman "attempts to share all API data", y un comentarista que no pudo
reproducir el disparo del hook recibió diez downvotes por decirlo. Una segunda discusión son las alternativas — Bruno, Insomnia, Yaak y
Sannr —, pero Insomnia ahora exige una cuenta en la nube y Bruno y Yaak
tienen páginas de precios, así que varios concluyen que todo cliente
comercial sigue el camino de Postman. Nota menor: si 400 millones de dólares
en capital de riesgo corrompen inevitablemente un producto, con un ingeniero
objetando que cobrar un precio justo no debería tratarse como un pecado.
