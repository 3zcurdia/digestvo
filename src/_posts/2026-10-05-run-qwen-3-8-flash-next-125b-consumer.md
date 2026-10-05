---
layout: post
title: "Run Qwen 3.8 Flash Next (125B) on consumer hardware (RTX 4090) at 100T/s"
date: 2026-10-05 09:09:57 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://github.com/Niko1221/Strata"
hn_url: "https://news.ycombinator.com/item?id=49953495"
summary: >-
  Strata is an open-source inference engine and one-click installer that runs
  Qwen3.8-Flash-Next, a 125-billion-parameter mixture-of-experts model, on
  ordinary gaming PCs. The project spreads the model's 24,576 experts across
  GPU, RAM and SSD, and uses speculative decoding to report 53-94 tokens per
  second on an RTX 5070, with an RTX 3090 estimated at 100-140. It ships
  quantizations from 2-bit up to near-4-bit, plus a Coder variant with half
  the experts removed that keeps 91% of the full model's SWE-bench Verified
  score while fitting 32GB of RAM. Setup exposes OpenAI- and
  Anthropic-compatible APIs on localhost, so nothing leaves the machine.
---

Most commenters land on the model being good enough to replace API models for
coding, because several report real speeds above the claimed 100 tokens/s on a
4090 and one says they stopped using Claude. The sharpest objection is the 2-bit
quantization: one commenter cites a paper showing 4-bit usually preserves
performance while 2-bit often causes broad degradation, and another notes that
published numbers show a 4-bit 27B beating Flash Next at 3 bits. Against that,
defenders argue the IQ3 imatrix quants cut unimportant weights surgically and
that the Coder variant's 91% of full-model SWE-bench Verified is the number that
matters. A secondary argument is over what surprisingly well means: speed is one
thing, benchmarked accuracy another, and almost nobody in the thread posts both.
