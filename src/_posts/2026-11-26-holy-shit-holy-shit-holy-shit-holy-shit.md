---
layout: post
title: "Caray caray caray caray: la magnitud de lo que está pasando"
date: 2026-11-26 14:13:18 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://scottaaronson.blog/?p=10379"
image: "/images/digest/2026-11-26-holy-shit-holy-shit-holy-shit-holy-shit.jpg"
hn_url: "https://news.ycombinator.com/item?id=50646108"
lobsters_url: "https://lobste.rs/s/ilit8q/scott_aaronson_on_recent_complexity"
share_text: "OpenAI afirma omega=9/4 con cota inferior acorde, y Aaronson dice que P!=NP ya está cerca #AI #Math"
summary: >-
  Scott Aaronson argumenta que los laboratorios de IA han pasado de soltar
  resultados aislados a responder de plano problemas abiertos de hace décadas.
  Durante una sola cena de Acción de Gracias vio a OpenAI reclamar una
  demostración de que el exponente de la multiplicación de matrices es
  exactamente 9/4, igualando su propia cota superior de octubre, y seguir las
  demostraciones de OpenAI y Anthropic de VP != VNP y el resultado de la
  hipótesis de Riemann de Alpoge/Anthropic. Otro artículo de OpenAI afirma que
  la transformada de Fourier necesita N(log N)^(1/2+o(1)) puertas lineales,
  superando tanto la FFT de los años 60 como su propia cota anterior. Dice que
  una demostración de P != NP ahora se siente cercana, y reporta rumores de que
  los laboratorios tienen algoritmos que rompen criptosistemas.
---

**En Hacker News.** La publicación llegó en medio de la cena mientras OpenAI y
Anthropic seguían subiendo PDFs a GitHub sin comunicados de prensa, y el punto de
Aaronson es que el ritmo ha cambiado la categoría: las preguntas antiguas se
responden de plano en lugar de socavarlas poco a poco. Dice que ahora cree que
una demostración de P != NP no está lejos, y su actualización añade que el
resultado omega = 9/4 vuelve mucho más difícil sostener la idea de que la IA
solo funciona dentro de las técnicas existentes. La mayoría de los lectores
aceptó la magnitud del logro, sobre todo una vez que los certificados de Lean
respaldaron las afirmaciones, pero la discusión más intensa gira en torno a la
afirmación de Aaronson de que los laboratorios de IA guardan algoritmos capaces
de romper criptosistemas: los escépticos señalan que el rumor no está
verificado, que un gobierno podría clasificar un hallazgo así y que el reciente
artículo de factorización subexponencial determinista no toca RSA. Aun así, una
veta de comentarios insiste en que los avances no valen nada sin beneficio
práctico, y Aaronson rechaza ese encuadre de plano. Nota menor: un debate
lateral se preguntó si omega = 9/4 resuelve de verdad la multiplicación de
matrices, dado que el exponente se define para circuitos aritméticos mientras
que la complejidad en bits sobre campos finitos podría quedar por debajo de
n^9/4.

**En Lobsters.** La publicación salió de una semana en la que OpenAI y
Anthropic empezaron a subir a GitHub pruebas verificadas por Lean sin
comunicados, desde la hipótesis de Riemann hasta VP ≠ VNP hasta ω = 9/4, y
Aaronson lee esa secuencia como evidencia de que la IA ya está escalando la
montaña hacia P ≠ NP. Los comentarios coincidieron en un punto estrecho: su
reacción vale la pena seguirse por quién es, un teórico de la complejidad que
pasó años en OpenAI, y gignico contestó a quienes la descalificaban como el
blog de cena de cualquier tipo. La pelea de fondo es si el entusiasmo está
justificado. Escépticos como cblake y gcupc dicen que la generalización va por
delante de la evidencia y que su trasfondo racionalista y de seguridad de la IA
tiñe la lectura, mientras repl respondió que los kernels de Lean verifican
mecánicamente cada paso, a diferencia de las pruebas de software, así que la
prueba de RH está genuinamente verificada. Una nota menor aparte arrastró el
hilo hacia la regulación de las empresas de IA y hacia si Twitter es donde
debería seguirse el campo.
