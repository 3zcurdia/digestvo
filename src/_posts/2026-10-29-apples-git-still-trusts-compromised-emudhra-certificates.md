---
layout: post
title: "El git de Apple aún confía en los certificados comprometidos de eMudhra"
date: 2026-10-29 10:29:35 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://emudhra.we-have-a-problem.com/apple.html"
image: "/images/digest/2026-10-29-apples-git-still-trusts-compromised-emudhra-certificates.jpg"
lobsters_url: "https://lobste.rs/s/xybmsj/apple_s_git_still_trusts_compromised"
share_text: "11 días después del aviso, Apple sigue sin arreglar git en macOS y la actualización del 26 borró el parche manual"
summary: >-
  Once días después de ser notificada del incidente eMudhra, Apple sigue
  distribuyendo con macOS herramientas como git, curl y python3 que confían en
  los certificados de la autoridad comprometida. El artículo explica que
  cualquier atacante en la ruta de red puede así interceptar clonados y pushes
  por HTTPS, alterar código en tránsito y robar credenciales como tokens de
  GitHub. Peor aún, macOS 27.2, publicado el 26 de octubre, no corrigió el
  problema y revirtió el arreglo manual que los usuarios ya habían aplicado.
  Mientras tanto, docenas de proyectos, muchos mantenidos por voluntarios,
  publicaron sus correcciones hace días.
---

Apple fue notificada del incidente eMudhra el 17 de octubre y, once días
después, las herramientas de línea de comandos que empaqueta con macOS siguen
confiando en los certificados comprometidos; el lanzamiento del 26 de octubre no
solo no arregló nada, sino que deshizo el parche manual de los usuarios. El
acuerdo en los comentarios es doble: los desarrolladores son un objetivo de alto
valor, porque un clon comprometido se convierte en un incidente de cadena de
suministro que afecta a mucha más gente, y la lentitud de Apple se debe a
burocracia, a los trámites que exige cualquier actualización que toca archivos
de sistema. Sin embargo, el desacuerdo está en si esa explicación resulta
suficiente: afecta a una fracción pequeña de usuarios, pero los certificados
comprometidos permiten interceptar cualquier conexión HTTPS, y proyectos
voluntarios llevaron sus parches hace días. Como nota menor, la conversación
derivó hacia Homebrew y MacPorts, que ya compilan sus propias copias de git, y
hacia el precio de la acción de eMudhra, que salió del negocio del PKI público
sin sufrir ninguna sanción financiera.
