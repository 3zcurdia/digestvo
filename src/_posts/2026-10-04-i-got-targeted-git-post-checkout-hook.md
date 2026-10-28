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

Frank Wiles relataba cómo un "cliente" le envió un repositorio malicioso mediante una carpeta de Dropbox. El ataque aprovechaba un hook *post-checkout* en `.git/hooks` para descargar, ejecutar y borrarse a sí mismo un binario desde un servidor de comando y control alojado en Vercel.

La mayoría de los comentarios coincidió en que Git necesita una barrera al estilo *direnv* antes de ejecutar hooks, ya que `.git` se trata como estado local confiable incluso cuando el repositorio llega como una descarga o un tarball en lugar de un clon. El propio autor apoyaba esta idea.

Sin embargo, el mayor punto de controversia fue el alcance del riesgo. Un comentario señalaba que un `git clone` simple es seguro por diseño (Git no extrae rutas bajo `.git/` y trataría un clon comprometido como una vulnerabilidad), por lo que el peligro se limita a instalar un árbol de directorios por otras vías. Además, se advirtió que variantes como `core.fsmonitor` pueden dispararse con acciones implícitas (`git status`, builds, prompts del shell), lo que hace que un `.git/config` incluido sea potencialmente más peligroso que un hook. Como nota menor, un consejo muy votado de desactivar hooks con `core.hooksPath /dev/null` recibió críticas al señalarse que la propia configuración del repositorio puede revertirlo.
