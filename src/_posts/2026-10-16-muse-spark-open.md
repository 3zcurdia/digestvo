---
layout: post
title: "Muse Spark Open"
date: 2026-10-16 09:38:43 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://research.meta.ai/blog/muse-spark-open"
hn_url: "https://news.ycombinator.com/item?id=50107379"
share_text: "Meta's 816B open-weight giant runs on two Mac Studios, if you have $25K lying around"
summary: >-
  Meta released the weights for Muse Spark Open, billed as the most capable US
  open-weight model to date. It is a natively multimodal mixture-of-experts
  model with 816B total parameters, 42B active, and a 1M-token context window
  aimed at coding and agentic work. Meta says it runs on a desktop pair of M5
  Ultra Mac Studios via MLX, and ships day-one support for SGLang, vLLM,
  llama.cpp and other runtimes plus hosted APIs. Weights are available on
  Hugging Face and major clouds under the Muse Model License with limited
  commercial terms.
---

Most praise centers on Meta doing the unglamorous deployment work, with day-one
support for MLX, vLLM, SGLang and llama.cpp raising the bar beyond just dumping
weights. That enthusiasm collides with the hardware math, since the headline
desktop setup needs two M5 Ultra Mac Studios with up to 512GB of unified memory
each, a 20 to 30 thousand dollar proposition that makes local ownership a
specialty purchase. The sharpest objection is that none of that buys Meta a
consumer moat, because critics call the Muse assistant a reskinned agent harness
with no network effects and argue Apple, Google and Microsoft still own the OS
layer. Defenders answer that commoditizing the model is the moat, since
standardizing on Meta weights and optimizing the surrounding infra steadily
lowers Meta's own serving costs.
