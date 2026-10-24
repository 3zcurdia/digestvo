---
layout: post
title: "Kimi K3.1 Pro y K3.1 Pro Highspeed"
date: 2026-10-23 18:01:17 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://www.kimi.ai/blog/kimi-k3-1-pro"
hn_url: "https://news.ycombinator.com/item?id=50212065"
share_text: "Moonshot depuró los datos de ciber de Kimi K3.1 Pro: su benchmark de exploits bajó de 90.5% a 81.0%. En HN no lo creen."
summary: >-
  Moonshot AI ha lanzado Kimi K3.1 Pro, su modelo abierto de pesos más capaz de
  la clase 3T, con una ventana de contexto de 1 millón de tokens y una variante
  Highspeed que corre de 2 a 3 veces más rápido. Con postentrenamiento sobre K3,
  con mucho más cómputo y RL conjunta a cientos de dominios, alcanza 65.7% en
  Terminal-Bench 4.0, justo detrás del 66.4% de Claude Opus 5.5, y reduce su
  tasa de alucinación a nivel de afirmación del 23.4% al 8.3%. Los pesos llegan
  antes del 4 de noviembre, pero los datos de entrenamiento sobre ciberataques
  se retiraron de la versión abierta.
---

La mayoría de los comentarios señala el recorte de capacidades cibernéticas
como la verdadera historia, porque Moonshot admite abiertamente que retiró los
datos de ciber del mid-training y de la mezcla del entorno de RL: su propia
puntuación en xdev-bench-hard cae del 90.5% del checkpoint sin filtrar al
81.0% de los pesos publicados. Sus defensores sostienen que el gating mantiene
la capacidad de explotación de vanguardia fuera de los pesos abiertos por
ahora, y consideran creíble la metodología porque el blog nombra exactamente
qué tipos de tareas se recortaron. La objeción más dura es que ataque y defensa
son la misma capacidad, así que el nerf perjudica más a los defensores: varios
dicen que confían en GLM-5.3 precisamente porque los modelos de vanguardia
rehúsan hacer trabajo de seguridad sobre su propio código, y dejan el
hallazgo de vulnerabilidades reales a quien haga fine-tuning sorteando la
restricción. Un grupo más pequeño se burla del planteamiento de "seguir el
ritmo de la frontera" como un cártel con los laboratorios de EE. UU., mientras
los escépticos dudan de que la eliminación sea real o solo una historia de
marketing.
