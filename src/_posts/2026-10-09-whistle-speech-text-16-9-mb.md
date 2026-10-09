---
layout: post
title: "Whistle: Speech to Text in 16.9 MB"
date: 2026-10-09 08:51:10 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://cactuscompute.com/blog/whistle"
hn_url: "https://news.ycombinator.com/item?id=50008427"
summary: >-
  Cactus Compute releases Whistle, an open speech recognition model packaged
  as a single 16.9 MB file that runs on the CPU with no dependencies. It
  transcribes seven languages, English, German, French, Spanish, Italian,
  Dutch and Polish, with word timestamps and speech embeddings, all on device.
  The blog post reports it beating Whisper base and Moonshine tiny v2 on
  several word error rate benchmarks while reaching its first token in 11.1 ms
  and decoding 1,319 tokens per second. Weights, a C++ engine and a Python
  package ship on Hugging Face, GitHub and PyPI.
---

Most commenters land on the benchmarks being genuinely impressive for the size,
because hands-on tests in the thread transcribed complex sentences accurately in
a footprint small enough to sit in CPU L3 cache. The sharpest objection is that
binary size was never the hard part of speech-to-text: one commenter says the
real challenge is transcribing his 84-year-old stroke-impaired father, and every
sound his mouth makes still lands on the page. That connects to a recurring
quality complaint, since small models reportedly hold up on clean
in-distribution western accents but degrade on Mexican and Venezuelan Spanish
and on conversational rhythm. A narrower argument runs over the L3 claim itself:
one reader says cache residency buys an order of magnitude in latency, another
replies it mostly shows up as throughput rather than end-to-end latency.
