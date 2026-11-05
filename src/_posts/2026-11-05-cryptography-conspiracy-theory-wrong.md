---
layout: post
title: "Tu teoría conspirativa sobre criptografía está equivocada"
date: 2026-11-05 09:27:29 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://soatok.blog/2026/10/29/your-cryptography-conspiracy-theory-is-wrong/"
image: "/images/digest/2026-11-05-cryptography-conspiracy-theory-wrong.jpg"
lobsters_url: "https://lobste.rs/s/bqllfe/your_cryptography_conspiracy_theory_is"
share_text: "Si ML-KEM fuera un backdoor de la NSA, ¿por qué movería sus sistemas TOP SECRET a ese algoritmo?"
summary: >-
  Soatok repasa la historia de la injerencia de la NSA y NIST en la
  criptografía estándar, de las S-box de DES al Clipper Chip, Dual EC DRBG,
  Snowden y las semillas de las curvas P resueltas este mes, para demostrar
  que las teorías conspirativas actuales no se sostienen. Su tesis es que la
  NSA tiene recursos e incentivos finitos, definidos por sus misiones COMSEC y
  SIGINT, en lugar de poderes mágicos. Concluye que es muy improbable que
  ML-KEM sea un backdoor: el Gobierno estadounidense no migraría sus sistemas
  clasificados a un algoritmo roto. No pide confiar en ningún gobierno, solo
  descartar los argumentos más flojos.
---

La publicación responde a la ola de sospechas sobre criptografía que acompañó el plan
final de NIST para la transición poscuántica (IR 8547) y la recomendación de la
NSA de adoptar ML-KEM-1024 sin modo híbrido, con las declaraciones de Bernstein
citadas como respaldo. Sobre el fondo hay acuerdo en que el historial avala al
autor: las S-box de DES reforzaron el cifrado, Dual EC DRBG sí era un backdoor
denunciado a tiempo y los archivos de Snowden no revelan ataques criptanalíticos
secretos. Sin embargo, la tensión está en si tachar de conspiración estas dudas
cierra el debate: raven recuerda que los backdoors NOBUS son hechos documentados
y que el punto no es que la NSA vaya a atacar a una persona concreta, sino la
vigilancia masiva a escala, ejemplificada con ICE y Palantir. Aun así, fanf
objetó que Bernstein combate algo que no ocurre: nadie está forzando
criptografía poscuántica exclusiva, porque el modo híbrido sigue siendo la
opción principal y la no poscuántica sigue disponible. Nota menor: parte del
hilo discute el estilo de Bernstein y su desconocimiento del rough consensus del
IETF, sin decidir si su escepticismo técnico se sostiene.
