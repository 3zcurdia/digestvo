---
layout: post
title: "Desactive Apple Intelligence en macOS 27 y recupere su espacio en disco"
date: 2026-10-05 09:09:57 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://github.com/omlahore/RemoveMacAI"
hn_url: "https://news.ycombinator.com/item?id=49957116"
share_text: "macOS 27 no suelta Apple Intelligence. Este pequeño CLI lo elimina y recupera su disco. #macOS"
summary: >-
  macOS 27 ya no incluye un solo interruptor para Apple Intelligence, y sus
  modelos descargados permanecen en disco aun después de desactivar las
  funciones. RemoveMacAI es un pequeño CLI para Apple silicon que aplica las
  propias claves de restricción de Apple mediante un perfil de configuración,
  elimina los modelos de foundation, generación de imágenes, Spatial Photos y
  Clean Up a través del servicio de assets, y redirige sus descargas a un
  puerto local cerrado para que macOS nunca vuelva a descargarlos. Todo es
  reversible con removemacai revert. Se instala con un script canalizado por
  curl o un tap de Homebrew, y cada versión se compila en GitHub Actions con
  una atestación verificable de procedencia de la compilación.
---

La mayoría de los comentarios se concentra en el método de instalación más que
en la herramienta: el one-liner del README que canaliza curl a bash provocó la
respuesta más ruidosa y abrió un largo debate sobre si canalizar el script de
un desconocido hacia la terminal es en realidad peor que npm install o pip
install. La objeción más aguda corre en ambas direcciones. Los defensores
señalan que el script solo descarga un binario verificado por SHA-256 y
atestación desde el mismo repositorio, y que los gestores de paquetes ya
ejecutan setup.py arbitrarios y código postinstall de todos modos, así que la
indignación es teatro. Los críticos responden que un script mutable del lado
del servidor destruye la propiedad de artefacto compartido que hace auditable
una vez para todos un zip de una versión fija, y que el público al que apunta
son desarrolladores con credenciales empresariales en su entorno. Una segunda
división es si el premio justifica la molestia: quienes tienen portátiles de
256 GB llaman a 14 GB de modelos entre el 10 y el 20% de su disco, mientras
otros dicen que Apple Intelligence simplemente funciona ahora y que solo a
quienes no les sobra almacenamiento les importa.
