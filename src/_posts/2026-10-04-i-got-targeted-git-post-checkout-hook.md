---
layout: post
title: "Fui un objetivo: intentaron robar mis credenciales con un hook post-checkout de git"
date:   2026-10-04 00:44:46 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: https://frankwiles.com/posts/i-got-targeted/
lobsters_url: https://lobste.rs/s/cd5gdk/i_got_targeted_trying_get_your
share_text: "'Cliente' envió un repo git por Dropbox. El hook post-checkout robaba credenciales. No confíe en ningún repo. #InfoSec"
summary: >-
  Frank Wiles, fundador de REVSYS, describe un intento de phishing dirigido que
  entregó un brief falso de un proyecto de tecnología educativa mediante una carpeta de Dropbox
  con un repositorio git. Dentro de .git/hooks había un hook post-checkout real junto a los
  habituales archivos .example; descargaba un binario específico del sistema operativo desde un servidor
  de comando y control alojado en Vercel, lo hacía ejecutable, lo corría y se borraba a sí mismo.
  Wiles lo detectó cuando el "cliente" le dijo que cambiara a una rama de NDA, y
  alertó a Dropbox y a Vercel. Los atacantes también estaban suplantando a una
  empresa de desarrollo real.
---

La mayoría de los comentarios coinciden en que Git necesita una barrera estilo direnv antes de ejecutar hooks,
porque .git se trata como estado local confiable aun cuando un repo llegó como una
descarga de Dropbox o un tarball en vez de un clon; el propio autor del artículo
respalda la idea. La objeción más dura viene de agwa, quien señala que un
git clone simple es seguro por diseño: Git se niega a extraer rutas bajo .git/
y trata un clon que lo compromete como una vulnerabilidad, así que el peligro vive
por completo en instalar un árbol de directorios por otra vía y quien solo
clona está fuera de alcance. El hilo también escala el payload, con la
variante core.fsmonitor de agwa que se dispara con un simple git status que los IDE, go build y los
prompts del shell ejecutan de forma implícita, haciendo un .git/config incluido más peligroso que cualquier hook. Un
consejo muy votado de desactivar los hooks con core.hooksPath /dev/null recibe críticas
cuando oger señala que la propia configuración de un repo puede revertirlo.
