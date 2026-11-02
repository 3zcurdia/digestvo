---
layout: post
title: "¿WTF, Ubuntu?"
date: 2026-11-02 10:45:04 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://chalmovsky.com/posts/wtf-ubuntu"
image: "/images/digest/2026-11-02-wtf-ubuntu.jpg"
hn_url: "https://news.ycombinator.com/item?id=50337608"
share_text: "Debian parcheó el fallo TCP 9.8 del kernel el 16/10; dos semanas después Ubuntu sigue sin nada — y vende 'parches oportunos'"
summary: >-
  Una falla crítica CVSS 9.8 en la pila TCP del kernel, presente desde 2016 y
  explotable de forma remota para obtener root, fue parchada por Debian el 16 de
  octubre, pero más de dos semanas después Ubuntu aún lista todas las versiones
  soportadas como vulnerables — incluidas las LTS. Anthropic dice que construyó
  un exploit funcional. El autor, que apagó sus servidores Ubuntu antes que
  correrlos sin parche, protesta porque el marketing de Canonical promete
  'parches oportunos para vulnerabilidades críticas' mientras distros
  mantenidas por voluntarios salieron primero.
---

CVE-2026-98432 es una falla calificada 9.8 en la pila TCP del kernel, presente
desde 2016, explotable de forma remota hasta root, con un exploit funcional que
Anthropic dice haber construido. Debian la parchó el 16 de octubre; dos semanas
después Ubuntu aún lista todas las versiones soportadas como vulnerables mientras
promociona 'parches oportunos para vulnerabilidades críticas.' La mayoría de los
comentaristas coincidió en que el retraso es indefendible — Debian, Arch, Alpine
y hasta el Amazon Linux de AWS salieron primero, y Canonical es el que vende
suscripciones de seguridad. La discusión de fondo fue qué sigue ofreciendo
Ubuntu: los defensores citaron los cinco años garantizados de actualizaciones
LTS (quince con un contrato de pago) que satisfacen a los auditores, además de un
kernel más amigable con el hardware moderno que el 6.12 de Debian stable. Aun
así, otros señalaron que la cadencia de LTS de Ubuntu también es cada dos años y
que sus paquetes vienen de Debian, dejando la inercia y los valores por defecto
de los proveedores de VPS como la razón real para quedarse. Nota menor: un
debate lateral ponderó Debian o Fedora para escritorios.
