---
layout: post
title: "Postgres 19 va tarde porque ahora se encuentran muchos más bugs"
date: 2026-11-02 10:45:04 -0600
categories: digest
tags: ["Systems & Infra"]
source_url: "http://rhaas.blogspot.com/2026/10/postgres-19-is-late-and-its-ais-fault.html"
image: "/images/digest/2026-11-02-postgres-19-late-because-many-bugs-being-found.jpg"
hn_url: "https://news.ycombinator.com/item?id=50312408"
lobsters_url: "https://lobste.rs/s/0yxkvs/postgres_19_is_late_it_s_ai_s_fault"
share_text: "40 años de bugs que los humanos no hallaban: PostgreSQL 19 se retrasa porque los LLM sí los encuentran"
summary: >-
  Robert Haas explica que PostgreSQL 19 saldrá tarde, probablemente en
  noviembre en lugar de entre mediados de septiembre y octubre, porque los LLM
  encuentran bugs que antes se escapaban. Entre el 27 de agosto y el 15 de
  septiembre se retiraron tres funciones grandes del release, algo inusual tan
  tarde. Desde la congelación de funciones hasta el 25 de septiembre, los
  commits parcheados a la rama estable subieron más del 60% en un año y los de
  ramas anteriores más del 74%, mientras los commits al master bajaron. Las
  correcciones siguen necesitando revisión humana, y esa revisión se desvió
  hacia errores de seguridad en ramas viejas.
---

**En Hacker News.** Robert Haas atribuye el retraso de PostgreSQL 19, que
saltará de octubre a noviembre, a que los LLM encuentran muchísimos más bugs de
los que los humanos veían: tres funciones grandes se revertieron entre el 27 de
agosto y el 15 de septiembre y los commits parcheados a la rama estable subieron
más del 60% en un año. La mayoría coincide en que el cuello de botella ya no es
descubrir errores sino verificarlos: los informes se multiplican, pero los
revisores humanos no se han vuelto más rápidos y las correcciones que redactan
los LLM siguen exigiendo revisión. El debate central es qué hacer con ese flujo:
unos sostienen que no todo bug merece arreglo, que tocar casos extremísimos
puede costar rendimiento o romper comportamientos de los que otros dependen, y
que hasta una confusión de mayúsculas en un mensaje de error se ignora sin
perder nada. Sin embargo, otros responden que en software crítico no se puede
saber de antemano qué parte es prescindible, con ejemplos como Swissair 111 o
Heartbleed, y que dejar bugs sin resolver solo encarece el trabajo siguiente.
Como nota menor, también se discutió si la IA es mejor buscando errores que
escribiendo código.

**En Lobsters.** Durante una década PostgreSQL llegó puntuales en septiembre y
octubre, y Robert Haas confirma que la 19 se retrasará hasta noviembre, con tres
funciones grandes revertidas entre el 27 de agosto y el 15 de septiembre. En
Lobste.rs el acuerdo fue que ese retraso es el precio justo: entre el 8 de abril
y el 25 de septiembre los back-patches a la rama estable de la 19 crecieron más
de 60% en un año mientras los commits de nuevas funciones apenas se movían, así
que el proyecto eligió estabilización sobre velocidad. Sin embargo, el debate de
fondo fue si un bug cuenta cuando nadie lo reportó jamás: frente a la duda de si
un defecto sin impacto justifica bloquear funciones, se respondió que las bases
de datos fallan de forma no determinista y solo en condiciones raras, y que la
ley de Hyrum convierte un comportamiento no intencionado en algo en lo que la
gente confía. Aun así, la sombra que queda viene del propio artículo: cuarenta
años de bugs que los humanos no encontraban y los LLM sí, con revisores que no
se han vuelto más listos. Como nota menor, se señaló que el título es clicbait.
