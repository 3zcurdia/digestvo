---
layout: post
title: "Kolibri: A Sovereign Open-Weight Model"
date:   2026-10-04 00:44:46 -0600
categories: digest
tags: ["AI/ML"]
source_url: https://aleph-alpha.com/en/blog/kolibri-has-landed-a-sovereign-open-weight-model/
hn_url: https://news.ycombinator.com/item?id=49942706
summary: >-
  Aleph Alpha released Kolibri, a 78B-total, 3B-active mixture-of-experts
  transformer for English and German, with 1M-token context and Apache 2.0
  weights on Hugging Face. Two models shipped three months apart because the
  pipeline runs as code: every change triggers an end-to-end run, checkpoints
  land hourly, and 38 hardware faults in 21 days went unattended. Specialised
  for German and agentic work, it is trained to abstain, holding back on 44% of
  AA-Omniscience items.
---

Commenters mostly distrust the benchmark framing: the comparison set is a year
old, and spijdar and amoshebb note Qwen3.8 27B beats Kolibri on German in
Kolibri's own harness, 79.9 to 70.8. The sovereignty framing is challenged
head-on — petesergeant calls it a cover for weak performance, and others ask how
sovereign a Cohere-owned, Toronto-operated company is. The team and its defenders
answer that sovereignty is choice and control of data, not benchmark position, and
that small tool-calling models need less copyrighted data than people assume. A
long sub-thread splits on whether open weights are neo-feudalism in reverse or a
proliferation risk nobody can gate.