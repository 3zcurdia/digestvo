---
layout: post
title: "JPEG XL frente a AVIF para casos de uso web"
date: 2026-10-16 09:38:43 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://jakearchibald.com/2026/jpeg-xl-vs-avif/"
lobsters_url: "https://lobste.rs/s/uejdwj/jpeg_xl_vs_avif_for_web_use_cases"
share_text: "AVIF supera a JPEG XL 15–25% en fotos, salvo que la métrica le mienta"
summary: >-
  Jake Archibald comparó AVIF contra JPEG XL (encoders libjxl y jixel) en
  fotos, capturas, ilustraciones, transparencia, HDR y lossless, después de
  que JPEG XL llegara a todos los navegadores principales. AVIF produjo
  archivos con pérdida más livianos en casi todos los casos web, típicamente
  15–25% más chicos que JPEG XL en fotos y muy por debajo en capturas y
  transparencia. JPEG XL ganó en compresión sin pérdida y en achicar JPEG
  existentes sin pérdida entre 9 y 20%. El veredicto: usar AVIF 4:4:4 por
  defecto para imágenes web, y probar JPEG XL con jixel solo cuando AVIF dé
  un archivo inusualmente grande.
---

La mayoría de los comentarios coincide en un reparto claro —AVIF para las
imágenes que se publican, JPEG XL para masters y archivos sin pérdida—,
porque los números de Archibald muestran AVIF 15–25% más chico en fotos y
muy adelante en capturas y alfa, mientras JPEG XL domina el lossless. La
objeción más fuerte apunta a que la métrica SSIMULACRA2 sesga los resultados
hacia AVIF, porque un comentarista repitió la comparación con Butteraugli y
encontró a JPEG XL ganando en alta calidad y recortando la brecha en calidad
media, con el autor admitiendo que el encoder jixel más nuevo muestra
artefactos visibles que la métrica no capta. Un segundo debate metodológico
cuestiona servir imágenes de 1598px escaladas por CSS, ya que el escalado
oculta artefactos que la vista en pantalla completa revela. La corrección más
útil es que un elemento picture no deja al navegador elegir el mejor
formato, así que publicar todos los formatos es esfuerzo desperdiciado
frente a afinar uno solo.
