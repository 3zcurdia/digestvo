---
layout: post
title: "Mistral Large 4"
date: 2026-10-06 09:23:08 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://docs.mistral.ai/models/mistral-large-4-0"
hn_url: "https://news.ycombinator.com/item?id=49977979"
summary: >-
  Mistral has released Mistral Large 4, an open-weight general-purpose
  multimodal model built on a granular mixture-of-experts architecture with 49
  billion active parameters out of 1.05 trillion total, plus a 1.6B vision
  encoder. It ships in public preview with a 1M-token context window and API
  pricing of $0.68 per million input tokens and $2.09 per million output
  tokens, roughly half list price during the preview. Mistral positions it as
  state of the art across reasoning, vision and cybersecurity benchmarks, and
  it can be deployed from the company's own API or self-hosted from the
  released weights.
---

Most commenters land on the benchmarks being genuinely better than expected,
because the numbers put an open-weight European model within reach of GLM 5.3
and DeepSeek's flash tier on coding agentic tasks while the vision and
cyber-security scores look best-in-class for the price. The sharpest objection
comes from erichocean, who argues Mistral never advances the state of the art
and is spending GPU hours retraining last-generation backbones, when
post-training an existing open model the way Cursor does would be far cheaper
and more useful than sovereign-AI pretraining. The counter is that Europe needs
a high-quality model not owned by American trillion-dollar companies or Chinese
labs, and that the open weights are what actually deliver that independence. A
third camp treats the 50%-off preview pricing as the real story, since it lands
directly against DeepSeek Flash V4.1 and turns the release into a price move
rather than a capability move. A long side argument about European economic
stagnation swamped part of the thread but did not change the split.
