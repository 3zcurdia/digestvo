---
layout: post
title: "La sudo en Rust de Ubuntu 26.04 no es compatible con la sudo estándar"
date: 2026-11-04 09:41:47 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://utcc.utoronto.ca/~cks/space/blog/linux/Ubuntu2604RustSudoNotCompatible"
image: "/images/digest/2026-11-04-ubuntu-26-04-rust-sudo-compatible-standard-sudo.jpg"
lobsters_url: "https://lobste.rs/s/e201eb/ubuntu_26_04_rust_sudo_is_not_compatible"
share_text: "Ubuntu pasó a sudo-rs: rechaza hasta '!requiretty' y eliminó -E, así que la sudo por defecto ya no entiende tu sudoers"
summary: >-
  El artículo no se pudo abrir — el sitio bloquea a los agentes de IA. El
  hilo comenta una entrada sobre Ubuntu, que sustituyó sudo por sudo-rs, una
  reescritura en Rust que no es compatible con la sudo estándar. Los
  comentaristas detallan los daños: la nueva orden rechaza ajustes válidos del
  sudoers como requiretty, incluso en su forma negada, elimina el flag -E y
  limita los comodines en los comandos. Y debaten a quién culpar: al proyecto
  por no facilitar la transición o a Canonical por cambiar una herramienta
  crítica sin avisar.
---

El detonante es que Ubuntu pasó de sudo a sudo-rs, una reescritura en Rust, y el
titular de Siebenmann asegura que la orden por defecto ya no es compatible con
la sudo estándar. El consenso es que la culpa no es del proyecto: sudo-rs
advierte en su README que aún no cubre lo que se espera de sudo, así que señalan
a Canonical, que cambió una herramienta crítica sin transición ni aviso. La
controversia principal es si el nombre obliga a no romper nada: ajustes válidos
del sudoers dejan de validar, rechaza requiretty e incluso su negación
!requiretty, desaparece -E, la vía más cómoda a lanzar una app gráfica como
root, y los comodines ya solo valen en el argumento final de un comando. Sin
embargo, se argumenta que en el escritorio sudo-rs cubre el uso típico de un
solo usuario y que el reemplazo de -E es declarar en sudoers las variables de
entorno que se permiten, algo que un usuario no técnico no debería tocar. Como
nota menor, un debate lateral pregunta si al autor no le cabía abrir un ticket
en vez de ventilar su frustración en el blog.
