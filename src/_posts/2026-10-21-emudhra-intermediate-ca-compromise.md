---
layout: post
title: "Compromiso de certificados intermedios de la CA eMudhra"
date: 2026-10-21 10:09:14 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://emudhra.we-have-a-problem.com/"
hn_url: "https://news.ycombinator.com/item?id=50166579"
share_text: "Las 8 claves intermedias de eMudhra se generaron tan mal que cualquiera puede recuperarlas desde los certificados"
summary: >-
  Se han comprometido las claves privadas de ocho certificados de CA
  intermedia de eMudhra, lo que permite a cualquiera que las posea suplantar
  cualquier sitio o servicio. La causa no fue una brecha externa: la CA
  generó mal las claves, de modo que cualquiera puede recuperarlas desde los
  propios certificados. La falla ha sido explotable desde que se crearon los
  certificados en abril de 2025, aunque su ausencia en los registros de
  transparencia de certificados impedía atacar a los navegadores que exigen
  CT; los clientes que no son navegadores a menudo omiten CT. Firefox y
  Chrome bloquearon los intermedios el 17 de octubre, Apple el 19 y Microsoft
  el 20, y decenas de almacenes de confianza de distribuciones y lenguajes
  siguen publicando actualizaciones.
---

La mayoría de los comentarios concluye que esto es un argumento sobre la arquitectura de la Web PKI más que sobre una CA mala, porque el mismo titular se repite cada pocos años y la generación rota de claves de eMudhra llevaba activa dieciocho meses. La discusión converge en una propuesta concreta: DANE sobre DNSSEC, que citamstr y account42 defienden porque la confianza seguiría la jerarquía del dominio en vez de cada miembro del almacén raíz, y el daño quedaría limitado a un subárbol. La objeción más aguda es la de tptacek: DANE no ofrece un actor malicioso expulsable ni un registro de transparencia obligatorio, así que un operador de TLD comprometido sería permanente, mientras que la Web PKI puede simplemente eliminar a eMudhra del almacén raíz. Un segundo argumento, más concreto, trata de las restricciones de nombre: eqvinox dice que las sub-CA sin restricciones son el flagelo, y agwa responde que eMudhra vende al público general como proveedor preferido de InCommon para universidades de EE. UU., así que no hay nada significativo que restringir.
