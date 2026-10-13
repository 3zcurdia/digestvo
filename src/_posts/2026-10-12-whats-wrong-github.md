---
layout: post
title: "What's Wrong with GitHub"
date: 2026-10-12 10:54:29 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://www.gnu.org/philosophy/whats-wrong-with-github.html"
lobsters_url: "https://lobste.rs/s/u9ue6c/what_s_wrong_with_github"
share_text: "GNU says quit GitHub: nonfree JS, Copilot lock-in, fake-distributed git. Self-host or submit. #GitHub #FOSS"
summary: >-
  The GNU Project urges developers to stop hosting repositories on GitHub,
  faulting its vague licensing guidance (Choose a License treats a copied
  license file as sufficient), its demand that visitors run nonfree
  JavaScript, and Copilot as SaaSS subject to forced upgrades and the 2026
  move to token-based billing. It also argues that GitHub re-centralizes a
  distributed system: pull requests can only reference GitHub-hosted forks,
  Actions runners auto-update behind a dispatch service, email addresses are
  hidden behind account links, and achievements badges gamify dependency on
  the site. As an interim measure, the essay suggests publishing a contact
  email in your README and hosting documentation on a site readable without
  nonfree software.
---

Most commenters land on the article discrediting itself, because the
nonfree-JavaScript objection and the snide asides overshadow its better material
on Copilot's token-based billing and GitHub's capture of the fork/pull-request
workflow. The sharpest objection is pyfisch's: GNU's own ethical repository
criteria rate Codeberg an F, identical to GitHub's, recommending only Sourcehut
beside Savannah, so the critique rings hollow from a project whose own Savannah
is dated and bypassed by Guix and GIMP. Alongside that, thombles argues the
JavaScript complaint is moot since even unminified GPL-licensed GitHub
JavaScript would improve nobody's life, while cadey reports being called malware
after labeling correctly. A minority concedes the substance: toastal wants to
delete his account but network effect and free Actions CI keep him, and
eliasebner has quietly moved personal projects to Codeberg.
