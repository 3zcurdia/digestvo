---
layout: post
title: "Esto no es sostenible"
date: 2026-10-29 10:29:35 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://www.netmeister.org/blog/defense-ddos.html"
image: "/images/digest/2026-10-29-sustainable.jpg"
lobsters_url: "https://lobste.rs/s/cpaibp/this_is_not_sustainable"
share_text: "Más del 50% de los parches de IA fallan: una semana con 5 CVE simultáneos. Reparar nunca fue el cuello de botella."
summary: >-
  El autor, responsable de respuesta a incidentes, sostiene que el ritmo actual
  de divulgación de vulnerabilidades se ha vuelto insostenible. Recorre cuatro
  incendios simultáneos de una sola semana de octubre de 2026 —una fuga de KVM,
  el compromiso de la CA eMudhra, la vulnerabilidad de PHP revelada fuera de
  embargo que se afirmaba afectaba a 'más del 70% de los sitios web' y una RCE
  de Brotli que alcanzó mucho más allá de Node.js— para demostrar que una
  corrección upstream lista nunca es el cuello de botella. Lo difícil es
  encontrar todos los sistemas afectados, juzgar si un bug aplica al entorno y
  desplegar la corrección con seguridad, y los defensores no dan abasto. No
  ofrece otra solución que asumir el compromiso y limitar el radio de explosión.
---

La publicación apareció la misma semana en que las empresas de IA se
apresuraron a atribuirse el mérito de la RCE de Brotli, un bug cuya corrección
upstream se había publicado realmente en febrero. La mayoría coincidió con el
diagnóstico central: la corrección upstream nunca es el cuello de botella —
enumerar cada copia vendorizada de una biblioteca en sus stacks y desplegarla
con seguridad sí lo es—, y la IA en conjunto está haciendo el triage más
difícil. Los informes generados por IA llegan con miles de palabras, a menudo
como un binario que nadie puede explicar, y un defensor que no entiende un bug
tiende a confiar en la severidad inflada. Sin embargo, el hilo se dividió sobre
qué hacer. La propuesta más ruidosa —reducir todo a stacks más pequeños, más
simples y demostrablemente correctos— recibió una réplica contundente: una
máquina de Turing de 6 estados cuyo problema de parada es desconocido demuestra
que la pequeñez es un proxy poco fiable para razonar sobre software, y lo que
la ingeniería de sistemas críticos demuestra de verdad es el sistema, no el
programa. Aun así, la mayoría se decantó por una respuesta sin glamour:
asumir el compromiso, limitar el radio de explosión y financiar a las personas
que hacen ese trabajo. Nota menor: una tangente sobre los paquetes de
confianza de CA vendorizados de NixOS se convirtió en una sesión de debugging
en vivo, con un mantenedor de nixpkgs confirmando que la corrección del
root-bundle de uv ya había llegado en 26.05-small.
