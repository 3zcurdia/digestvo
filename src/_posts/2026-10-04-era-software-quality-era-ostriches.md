---
layout: post
title: "The Era of Software Quality, or the Era of Ostriches?"
date: 2026-10-04 08:46:00 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: "https://blogs.gnome.org/mcatanzaro/2026/10/02/the-era-of-software-quality-or-the-era-of-ostriches/"
lobsters_url: "https://lobste.rs/s/elziso/era_software_quality_era_ostriches"
summary: >-
  GNOME release team member Michael Catanzaro argues that AI vulnerability
  scanning is now mandatory: GNOME went from 13 CVEs in 2023 to a projected
  188 in 2026, mostly from AI-found issues, and a Red Hat-commissioned scan of
  GLib reported 118 vulnerabilities. He says AI-generated reports are now
  mostly high quality and asks maintainers to stop banning them, noting
  GNOME's bug bounty closed after paying 183,900 euros for 71 flaws. He still
  recommends human audits, and advises against Rust for GNOME because Cargo's
  supply-chain risk outweighs the memory-safety gains.
---

Most commenters land on rejecting the "zero hope without AI vulnerability
scanning" claim as overstated, because they read GNOME's own choice of C, C++
and Vala rather than the absence of AI as the source of the CVE wave. The
sharpest objection is to the closing aside recommending against Rust for GNOME
over Cargo: pyfisch, wrs and ghoti point out that cargo vendor, pinned versions
and custom registries give GNOME full control of dependencies, so the real
trade-off is vendoring discipline, not Rust versus trojanized crates. A second
front is maintainer load: schneems and agent281 say AI reports destroy the
effort signals maintainers used to triage contributors, while simonw and
skyfaller argue over whether 100 dollars of tokens actually substitutes for a
pentest team once subsidized token pricing is counted.
