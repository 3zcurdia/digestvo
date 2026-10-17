---
layout: post
title: "Apple ML Research: Muse Spark Open with MLX on Mac Studio"
date: 2026-10-17 11:04:42 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://machinelearning.apple.com/research/mlx-distributed-inference"
hn_url: "https://news.ycombinator.com/item?id=50118320"
summary: >-
  Apple's ML research team shows how to run Muse Spark Open, Meta's new
  open-weight mixture-of-experts model with 816 billion total parameters, on
  Mac Studio hardware with the latest MLX release. A cluster of four M5 Ultra
  Mac Studios linked over RDMA Thunderbolt 5 decodes at about 37 tokens per
  second, while a single 512GB machine runs smaller models like Qwen 3.8 and
  Mistral Medium 3.5. The post benchmarks time-to-first-token and throughput
  on M3 and M5 Ultra, reporting up to 4.6x faster prefill on the new chips'
  GPU Neural Accelerators, and walks through pipeline and tensor
  parallelization with mlx.launch.
---

Most commenters land on the price arithmetic: four 512GB Mac Studios run to
roughly $40,000, and several say they would rather put that money into
OpenRouter credits, because hardware ages faster than a model market that shifts
requirements every year. The sharpest objection to the numbers themselves is the
precision choice: Apple benchmarks Muse Spark Open at 4-bit NVFP4 while leaving
Qwen 3.8 at native BF16, which reads as sandbagging Qwen, though a defender
notes Table 1 lists every quant and that showing speedups at full precision is
defensible. A second camp defends local inference on privacy and contractual
grounds, arguing API pricing is a moving target while a local model's terms are
fixed.
