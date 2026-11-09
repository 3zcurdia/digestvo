---
layout: post
title: "KetchUp – Alternativa de código abierto a SketchUp, hecha con Rust y WebGPU"
date: 2026-11-09 09:41:49 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://ketchup3d.github.io/app/"
image: "/images/digest/2026-11-09-ketchup-open-source-sketchup-alternative-built-rust-webgpu.jpg"
hn_url: "https://news.ycombinator.com/item?id=50418176"
share_text: "629 upvotes en HN, pero los testers dicen que hay que nombrar cada rectángulo — y KetchUp ya es BenchUp"
summary: >-
  BenchUp, lanzada como KetchUp, es una aplicación gratuita de modelado 3D de
  código abierto que funciona en el navegador o como descarga de escritorio
  para Windows, macOS y Linux. Construida con Rust y WebGPU, se dirige a
  carpinteros y fabricantes de muebles: dibujar líneas, rectángulos y
  círculos, convertir caras en formas con Push/Pull, ajustar a la geometría,
  escribir longitudes exactas y organizar piezas con grupos, componentes y
  etiquetas. El trabajo se guarda automáticamente en archivos .ketchup
  portables, y la aplicación puede importar geometría de SketchUp u exportar
  OBJ para otros flujos de trabajo. El proyecto ha sido renombrado
  posteriormente por problemas con la marca.
---

El lanzamiento obtuvo 629 upvotes y elogios inmediatos por la tecnología:
quienes lo probaron en el navegador dijeron que la interfaz y el renderizado de
texto en Rust se sienten realmente nativos. Sin embargo, los testers coincidieron
en el problema central: toda la promesa de SketchUp era la intuitividad de usarlo
sin aprendizaje, y KetchUp se queda corto — exige un nombre para cada
rectángulo, push/pull requiere antes seleccionar la cara con la herramienta de
flecha, el ajuste a la cuadrícula viene desactivado por defecto y la barra de
menús no se comporta como se espera. El debate principal es más amplio: un
comentarista argumentó que entramos en una era en la que se construye una
herramienta a medida con Claude en lugar de aprender Blender, y otros
compartieron modeladores en VR que agentes habían armado en horas. Aun así, los
opositores replicaron que las herramientas personales heredan la carga de
mantenimiento de la Maldición de Lisp, pierden interoperabilidad y funciones
probadas en batalla, y un mantenedor calificó a estos clones como callejones sin
salida a largo plazo que se consolidarán alrededor de aplicaciones completas.
Nota menor: varios comentaristas advierten que el nombre KetchUp invita a una
demanda de marca por parte de SketchUp; el proyecto se ha renombrado como
BenchUp.
