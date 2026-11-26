---
layout: post
title: "Los lentos tiempos de respuesta de seguridad de Ubuntu"
date: 2026-11-26 14:13:18 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://www.openwall.com/lists/oss-security/2026/11/25/9"
image: "/images/digest/2026-11-26-slow-ubuntu-security-response-times.jpg"
lobsters_url: "https://lobste.rs/s/wzlzlh/slow_ubuntu_security_response_times"
share_text: "9 días sin fix: Ubuntu seguía vulnerable al NoisyTCP mientras otras distros parchean el día uno #Security #Ubuntu"
summary: >-
  El investigador de seguridad Hanno Böck denuncia en oss-security que Ubuntu
  tarda demasiado en responder a fallos graves. Nueve días después de
  publicarse los detalles de NoisyTCP, una corrupción remota de memoria en la
  pila TCP del kernel (CVE-2026-99288), Canonical aún no ofrecía parche,
  mientras otras distribuciones ya lo tenían listo el día de la divulgación.
  La misma demora afecta a una fuga de KVM en virtualización AMD
  (CVE-2026-99312). Böck sostiene que este tipo de vulnerabilidades debería
  resolverse en horas, no en días o semanas.
---

El detonante fue el post de Hanno Böck en oss-security: NoisyTCP
(CVE-2026-99288) se publicó el 16 de noviembre y nueve días después Ubuntu
seguía sin fix, mientras otras distribuciones parchearon al momento de la
divulgación. La lista suma la fuga de KVM de AMD (CVE-2026-99312) sin arreglo y
otra corrupción TCP remota (CVE-2026-98432) que tardó semanas, con indicios de
explotación activa según GreyNoise. En los comentarios el acuerdo es amplio:
la calidad del soporte de Canonical no mejora, y hay quien ya plantea migrar su
infraestructura a Debian. La tensión de fondo es la estrategia de kernel: Böck
señala que Ubuntu mantiene un 7.0.0-44 propio con backports en lugar de
apoyarse en los kernels longterm de kernel.org, y llama a esa práctica apenas
viable, frente al 6.12.118+deb13 de Debian stable. Aun así, una defensa
puntual recordó que Ubuntu sigue ofreciendo un escritorio que funciona sin
tantos ajustes. Nota menor: la comunidad también discutió si el hilo violaba las
reglas de Lobsters sobre autoedición, y un moderador explicó por qué lo dejó
pasar.
