---
layout: post
title: "Windows 11 recopila datos sobre qué agentes de código y herramientas de desarrollo usas"
date: 2026-11-19 09:49:06 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://xusheng.dev/posts/windows-coding-agent-telemetry/"
image: "/images/digest/2026-11-19-windows-11-collects-data-which-coding-agents-dev.jpg"
lobsters_url: "https://lobste.rs/s/cwxmdw/windows_11_collects_data_on_which_coding"
share_text: "Renombrar cmd.exe a codex.exe basta para que Windows 11 lo detecte y lo suba a Microsoft por defecto. #Security #Windows"
summary: >-
  Un ingeniero inverso encontró que MissionControlAggregator.dll, un
  componente de Windows 11, contiene una lista fija de agentes de código como
  codex.exe, claude.exe, cursor.exe y copilot.exe, junto a herramientas como
  python.exe, gcc.exe y code.exe. El componente escucha eventos de procesos
  existentes, compara los ejecutables en marcha con esa lista y guarda solo un
  bitmap de qué herramientas han aparecido. El autor lo verificó en una
  instalación limpia de Windows 11 al copiar cmd.exe a codex.exe y gcc.exe, y
  encontró los bits resultantes en la cola de subida de DiagTrack. Con los
  datos diagnósticos opcionales activados, valor por defecto en la
  configuración estadounidense probada, el informe se sube a Microsoft.
---

Un análisis asistido por IA de los binarios de Windows encontró en
MissionControlAggregator.dll una lista fija de agentes, copilot.exe, claude.exe,
codex.exe y cursor.exe, bajo la función CLICodingAgentUsage (ID 62580080); el
autor verificó en una instalación limpia que su bitmap de uso se sube a
Microsoft si están activados los datos opcionales, el valor por defecto en su
configuración estadounidense. El acuerdo en los comentarios fue amplio: el
mensaje más votado llama a Windows un spyware y varios dijeron que el hallazgo
refuerza su paso a Debian, aunque en Estados Unidos no haya ley de privacidad
que lo impida. La disputa principal no fue sobre la telemetría sino sobre si
vale la pena seguir en Windows: los defensores listaron PowerShell y Active
Directory para administración de flotas, RDP, WSL2 y 33 años de compatibilidad
de binarios, mientras los críticos respondieron que nada de eso compensa la
vigilancia, y añadieron que las empresas solo se libran pagando. Aun así, un
comentarista sostuvo que saber que un agente corre salvaje en la máquina ayuda a
leer un informe de fallo. Como nota menor, la rama más larga acabó en impresión
y compatibilidad de software en Linux.
