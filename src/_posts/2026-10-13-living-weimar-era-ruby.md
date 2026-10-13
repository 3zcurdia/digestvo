---
layout: post
title: "Living in the Weimar era of Ruby"
date: 2026-10-13 09:16:08 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://blog.julik.nl/2026/10/the-weimar-of-ruby"
lobsters_url: "https://lobste.rs/s/lfen2h/living_weimar_era_ruby"
share_text: "DHH left, Ruby bloomed: 8,900 new gems in a year, PDFs and Qt revived by LLMs. Weimar era? #Ruby"
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

Most commenters land on skepticism toward the article's claim that typing is the
bottleneck, because generating lines was never the scarce part of programming.
The sharpest pushback asks who these fast-brained developers are, arguing that
LOC worship contradicts everything learned about boilerplate, autocomplete, and
expressive languages reducing keystrokes for years. The counterpoint that gains
ground is narrower: LLMs earn their keep on rote chores like converting a Rust
struct from Copy to non-Copy or chewing through repetitive scaffolding, not on
design. Meanwhile the PDF-gap anecdote draws sympathy, with even Go developers
surprised Rails lacked layout tooling and others noting hexapdf and ReportLab
show the pain was never Ruby-only.
