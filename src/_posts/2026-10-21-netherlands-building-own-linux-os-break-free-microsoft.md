---
layout: post
title: "Países Bajos construye su propio Linux para romper con Microsoft"
date: 2026-10-21 10:09:14 -0600
categories: digest
tags: ["Systems & Infra"]
source_url: "https://www.techspot.com/news/114018-netherlands-building-own-linux-os-break-free-microsoft.html"
lobsters_url: "https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os"
share_text: "Las sanciones a la CPI bloquearon nuevas licencias de Windows, así que el gobierno neerlandés construye una distro NixOS — que aún depende de GitHub"
summary: >-
  El gobierno neerlandés está construyendo un sistema operativo soberano basado
  en NixOS para sustituir Windows y Office en las instituciones públicas. El
  proyecto DAWO — Digitaal Autonome Werkomgeving Overheid — combina un SO
  propio, aplicaciones ofimáticas, servicios en la nube y herramientas de
  gestión sobre el gestor de paquetes Nix, creado por desarrolladores
  neerlandeses. El trabajo serio empezó hace unos meses y los primeros pilotos
  ya corren en entornos locales y privados, con el plan de cubrir todas las
  instituciones del país. El detonante fueron las sanciones de Washington
  contra la CPI, con sede en La Haya, tras las cuales Microsoft habría cortado
  el correo y los servicios de TI de los fiscales.
---

La mayoría de los comentarios lo ve como algo tardío y genuinamente bueno, porque las sanciones de EE. UU. contra la CPI no dejaron vía para renovar las licencias de Windows: las exenciones cubren comunicaciones y software de nómina, pero no sistemas operativos, así que el cambio fue forzado en la práctica y La Haya nunca lo habría elegido por su cuenta. Las respuestas más votadas lo llaman una bendición disfrazada, pues nada más había roto una cultura de TI neerlandesa donde, como dice un comentarista, todo el mundo usa Microsoft porque todo el mundo lo usa, y hasta los registros de correo de ASML apuntan a la protección de Outlook. La objeción más aguda es que la soberanía NixOS sigue pasando por Microsoft: Nixpkgs y la infraestructura del proyecto Nix dependen de GitHub, y la mayoría de las expresiones de paquetes descargan sus tarballs desde GitHub. El hilo converge en que eso es corregible y no descalifica, pues las salidas de fetchFromGitHub quedan cacheadas en cache.nixos.org y nixpkgs se puede replicar, y sacar NixOS de GitHub es mucho más fácil que sacar a un gobierno de Windows.
