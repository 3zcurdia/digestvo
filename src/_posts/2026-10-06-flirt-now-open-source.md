---
layout: post
title: "Flirt ahora es de código abierto"
date: 2026-10-06 09:23:08 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://blog.buenzli.dev/flirt-is-open-source/"
lobsters_url: "https://lobste.rs/s/9iztqv/flirt_is_now_open_source"
share_text: "¿Ahogado en force-pushes al revisar? Flirt muestra solo lo no visto. Ya es open source. #DevTools"
summary: >-
  Flirt, una herramienta de revisión de código local-first construida alrededor
  del flujo de series de parches donde los autores enmiendan, hacen rebase y
  force-push continuamente, se publicó como código abierto en Codeberg. La
  herramienta recuerda lo que el revisor ya vio y muestra la diferencia con el
  estado actual, funcionando con backends como GitHub y listas de correo. Su
  autor advierte que Flirt aún no está listo para uso general, con errores y
  funciones faltantes todavía pendientes, y dirige a los colaboradores a una
  instancia de Zulip donde los mensajes escritos por LLM están prohibidos. Un
  backend de Forgejo, que permitiría al proyecto probarse a sí mismo, es lo
  siguiente en la hoja de ruta.
---

La mayoría de los comentarios coincide en el entusiasmo por la herramienta en
sí, porque sjamaan y arcade dicen que habían querido de forma independiente
este flujo de revisión de series de parches y valoran su diseño local-first y
agnóstico al forge. La objeción más aguda es la licencia AGPL, porque
novafacing reporta que los departamentos legales de cada empleador para el
que ha trabajado prohíben el software AGPL incluso como binario local en una
portátil de trabajo, lo que le impide probar una herramienta que necesita
mucho; singpolyma responde que revisar parches nunca implica desplegar ni
distribuir el código. Un segundo debate concierne la política de
contribuciones con LLM: mxey señala que con solo decir que los colaboradores
pueden usar LLM en lo personal basta para que un proyecto caiga en la lista de
open-slopware, mientras senekor responde que lo que la gente hace fuera del
proyecto no es su asunto y acepta suavizar la redacción. La crítica práctica
de manfred es que la publicación de lanzamiento y el README no explicaban qué
es Flirt ni cómo instalarlo, lo que el autor corrigió dentro del hilo.
