---
layout: post
title: "Un investigador siembra 2 millones de canarios en la cadena de suministro de IA y destapa un desastre de privacidad"
date: 2026-11-23 11:02:24 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://arstechnica.com/security/2026/11/a-leaky-ai-supply-chain-is-exposing-secret-user-data-at-an-alarming-rate/"
image: "/images/digest/2026-11-23-researcher-plants-2m-canaries-ai-supply-chain-privacy.jpg"
lobsters_url: "https://lobste.rs/s/32rhzb/researcher_plants_2m_canaries_into_ai"
share_text: "Secretos plantados destapan routers de IA leyendo prompts marcados con retención cero. #AI #Security"
summary: >-
  El investigador de Dragos HD Moore sembró casi dos millones de prompts, cada
  uno con un secreto único como una clave AWS, una contraseña o una URL
  privada, en routers de IA y revendedores de inferencia, y observó dónde
  reaparecieron esos secretos. Ars Technica informa que al menos tres
  proveedores de hosting fueron vulnerados por atacantes que copiaron los
  prompts en la puerta de entrada, que varios revendedores registraron prompts
  para sí mismos, y que un laboratorio chino obtuvo URLs secretas de más de la
  mitad de los prompts enviados a sus modelos, incluidos la mayoría marcados
  con retención cero de datos. OpenRouter ha enviado desde entonces correos a
  sus clientes sobre una posible exposición y eliminó la etiqueta de retención
  cero de los endpoints de MiniMax.
---

El experimento que encendió la discusión viene del investigador de Dragos HD
Moore, quien sembró dos millones de secretos canario únicos, claves AWS,
contraseñas y URLs privadas, uno por prompt, y observó cuáles se usaron días
después. El acuerdo es tajante: enviar prompts por brokers que enrutan al
postor más bajo no puede ser compatible con la privacidad, porque cada salto
descifra el texto plano y lo registra. La discusión real fue si eso es
inherente o corregible. Un lado sostiene que la premisa solo funciona con
cifrado de extremo a extremo y que cuando hay dinero en la mesa los
operadores del postor más bajo ofrecen poca confiabilidad; el otro responde
que el brokering funciona bien en otros lados, Signal hace proxy de las
peticiones GIF a GIPHY, así que falta cifrado hasta el modelo más integridad
del operador. Una objeción más fuerte es que los proveedores nombrados no
eran de oferta: Novita AI tiene clientes reales y opera sus propios modelos,
lo que hace las filtraciones sorprendentes incluso para quienes asumen que
los revendedores baratos raspan los prompts. Como nota menor, los comentarios
preguntaron si Private Cloud Compute de Apple sobreviviría el mismo test de
canarios, y uno señaló que los TEE aún descifran dentro del enclave.
