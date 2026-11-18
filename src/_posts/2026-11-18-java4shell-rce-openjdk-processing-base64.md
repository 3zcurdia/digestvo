---
layout: post
title: "Java4Shell: RCE en OpenJDK al procesar Base64"
date: 2026-11-18 10:36:09 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://calif.io/java4shell/"
image: "/images/digest/2026-11-18-java4shell-rce-openjdk-processing-base64.jpg"
hn_url: "https://news.ycombinator.com/item?id=50538240"
lobsters_url: "https://lobste.rs/s/g0bf9i/java4shell_write_once_rce_everywhere"
share_text: "62 bytes más allá de un array del heap: el fallo AVX-512 Base64 de OpenJDK da RCE pre-auth en Jenkins y Jira. #Java #Security"
summary: >-
  Java4Shell (CVE-2026-114938) es un fallo de corrupción de memoria en el
  decodificador Base64 AVX-512 escrito a mano de OpenJDK. Una entrada
  malformada de 64 caracteres A seguidos de un signo igual hace que la
  longitud de salida calculada haga underflow, de modo que una escritura
  vectorial enmascarada de 64 bytes cae 62 bytes más allá del final de un
  array del heap de 50 bytes. Calif demostró RCE pre-auth en Keycloak, Jira,
  Confluence, Jenkins y otros, además de una fuga de heap estilo Heartbleed, y
  dijo que Codex encontró el fallo en una hora por menos de $200. Los parches
  salieron el 17 de noviembre y los hosts ARM no se ven afectados.
---

**En Hacker News.** El fallo está en ensamblador x86-64 escrito a mano dentro
del intrinsic de Base64 de HotSpot, y en el hilo coincidieron ampliamente en
que este tipo de código de JIT e intrinsics es el verdadero tema: como puso un
comentario, la teoría de los muchos ojos solo funciona cuando esos ojos
entienden de verdad el código, mientras otro dudaba de que el ensamblador
ajustado a mano sea el último fallo de este tipo. La discusión práctica fue
sobre qué flag de mitigación empujar: -XX:UseAVX=2 contra
-XX:-UseBASE64Intrinsics. El flag de AVX falla en hosts sin AVX2 y se rompe en
ARM, donde OpenJDK se niega a arrancar, así que varias personas prefirieron
desactivar los intrinsics de Base64. Una tensión relacionada era si empujar un
flag del JVM en toda una flota mixta para evitar revisar cada host, o si eso
solo tapa capas de abstracción que hacen más difíciles de atacar fallos como
este. Aun así, la mayoría coincidió en que actualizar de inmediato vale más que
debatir, ya que los parches salieron el mismo día. Nota menor: una larga
divagación sobre si el fallo ya se está explotando en el mundo real y si CISA
es funcional, que se convirtió en una pelea partidista.

**En Lobsters.** Los precondiciones marcaron la agenda: el exploit necesita
hardware AVX-512 VBMI, un proxy inverso que no haga buffer de los cuerpos de
petición y un layout de heap específico para cada objetivo. La mayoría de los
comentarios coincidió en que el umbral de hardware es amplio en la práctica,
ya que AVX-512 VBMI cubre Intel desde Ice Lake en adelante y AMD desde Zen 4
en adelante, y ya que nginx es la excepción mientras Traefik, Envoy y HAProxy
dejan el buffering de peticiones desactivado por defecto. La tensión principal
es si la afirmación de RCE everywhere del título se sostiene. Los escépticos
la llamaron un nothingburger al lado de log4shell y advirtieron que inflar
afirmaciones desgastará la próxima emergencia real, mientras los defensores
argumentaban que son tres condiciones comunes y ortogonales más que una
combinación rara. Aun así, ambos bandos concedieron que no hay un payload
universal, que la cadena actual apunta solo a G1 y que ZGC sigue arriesgando
denegación de servicio. Un debate lateral menor preguntó si la historia del
SIMD seguro de Rust, con core::simd aún solo en nightly, lo habría hecho
mejor.
