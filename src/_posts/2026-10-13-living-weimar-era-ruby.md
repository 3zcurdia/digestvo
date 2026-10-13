---
layout: post
title: "Living in the Weimar era of Ruby"
date: 2026-10-13 09:16:08 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://blog.julik.nl/2026/10/the-weimar-of-ruby"
lobsters_url: "https://lobste.rs/s/lfen2h/living_weimar_era_ruby"
summary: >-
  Julik Tarkhanov argues Ruby is in a creative renaissance even as David
  Heinemeier Hanson's RailsWorld keynote — announcing he vibe-rewrote HEY and
  no longer needs Rails — marks the founder's exit. With LLMs absorbing the
  typing, long-standing gaps are closing: two capable PDF libraries
  (sghtmltopdf and stationery), revived Qt and Shoes bindings, an
  async-friendly gRPC rewrite, and a Parquet library he built himself in days.
  Counting newly claimed gem names on rubygems.org, he measures about 8,900
  over the past year against 4,600 the year before — a step change beginning
  March 2026 — evidence that people are building the missing thing instead of
  invoking "nobody does this with Ruby anyway."
---

Most commenters land on the article's core claim that LLMs let one person ship
the libraries that used to need a team: zem argues the real payoff is domain
experts producing shared libraries rather than one-shot scripts, and nertzy
backs it with a Zed contribution he could not have written in Rust himself. The
sharpest objection targets the quoted line that typing every line by hand is "no
longer sustainable" — gspr and threedaymonk ask who ever hit typing speed as the
bottleneck, noting lines-of-code was abandoned as a metric years ago, while
atilaneves answers that typing was his bottleneck and he simply does not type
code anymore. The PDF example also splits the thread: sjamaan says PDF
generation is painful in every ecosystem without a corporate backer, and
weaksauce points out hexapdf already existed. The top-scored comment, from
kristoff, sidesteps the debate to argue the healthiest thing is to stop talking
about DHH altogether.
