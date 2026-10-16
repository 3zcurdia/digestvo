---
layout: post
title: "Sunsetting decomp.dev"
date: 2026-10-16 09:38:43 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://decomp.dev/"
lobsters_url: "https://lobste.rs/s/kaerns/sunsetting_decomp_dev"
share_text: "Years of reverse engineering, undone by token-burning forks chasing the progress bar"
summary: >-
  The maintainer of decomp.dev, a tracker for matching decompilations of
  classic games, is shutting down its public index. He writes that matching
  decompilation once took years of painstaking human work, but recent models
  like GPT-6-Astra can generate matching C, permute variants, and sustain long
  tasks cheaply with the right guidance. That capability unleashed hostile
  AI-finished forks, rushed half-working PC ports built on others' work, and a
  hollow leaderboard race. The site will keep serving existing project pages
  and history but accept no new projects.
---

Most commenters land in sympathy with the maintainer, because the specific
failure they recognize is drive-by AI forks that chase the progress percentage
without hand-reviewing for code the original developers could plausibly have
written. The Melee example becomes the dividing line: LLM output is acceptable
when maintainers meticulously clean up cheating matches and inlined helpers,
worthless when it just burns tokens to make the number go up. The sharpest
objection is over the closed repository and refusal to allow forks, because
critics say an all-rights-reserved tracker hurts the same open community AI
already damaged and does nothing to stop training. Defenders answer that after
watching open decompilations get scraped into models that then raced to port the
games, keeping the site code human-written and closed is self-preservation.
