---
layout: post
title: "¿La era de la calidad del software o la era de los avestruces?"
date: 2026-10-04 08:46:00 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://blogs.gnome.org/mcatanzaro/2026/10/02/the-era-of-software-quality-or-the-era-of-ostriches/"
lobsters_url: "https://lobste.rs/s/elziso/era_software_quality_era_ostriches"
share_text: "GNOME pasó de 13 CVE a 188 proyectados, todos hallados por IA. Dejen de vetar esos reportes. #Security"
summary: >-
  Michael Catanzaro, miembro del equipo de versiones de GNOME, sostiene que el análisis
  de vulnerabilidades con IA ya es obligatorio: GNOME pasó de 13 CVE en 2023 a 188
  proyectados en 2026, en su mayoría problemas hallados por IA, y un análisis de
  GLib encargado por Red Hat reportó 118 vulnerabilidades. Dice que los reportes generados
  por IA ya son en su mayoría de alta calidad y pide a los mantenedores que dejen de
  vetarlos, señalando que el programa de recompensas de GNOME cerró tras pagar 183.900 euros
  por 71 fallas. Aun así recomienda auditorías humanas y desaconseja Rust para GNOME porque
  el riesgo de la cadena de suministro de Cargo supera las ventajas de la seguridad de memoria.
---

La mayoría de los comentarios coinciden en rechazar la afirmación de "cero esperanza sin el análisis
de vulnerabilidades con IA" por exagerada, porque ven la propia elección de GNOME de usar C, C++
y Vala, y no la ausencia de IA, como el origen de la ola de CVE. La
objeción más dura es contra el comentario final que desaconseja Rust para GNOME
por Cargo: pyfisch, wrs y ghoti señalan que cargo vendor, las versiones fijadas
y los registros personalizados le dan a GNOME control total de sus dependencias, así que el verdadero
dilema es la disciplina del vendoring, no Rust frente a crates troyanizados. Un segundo
frente es la carga de los mantenedores: schneems y agent281 dicen que los reportes de IA destruyen las
señales de esfuerzo que los mantenedores usaban para evaluar colaboradores, mientras simonw y
skyfaller discuten si 100 dólares en tokens realmente sustituyen a un
equipo de pentesting una vez que se cuenta el precio subsidiado de los tokens.
