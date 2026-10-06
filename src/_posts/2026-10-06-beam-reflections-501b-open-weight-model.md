---
layout: post
title: "Beam: Reflection's 501B open-weight model"
date: 2026-10-06 09:23:08 -0600
categories: digest
tags: ["AI Release"]
source_url: "https://reflection.ai/blog/introducing-beam"
hn_url: "https://news.ycombinator.com/item?id=49969183"
summary: >-
  Reflection AI introduces Beam, a 501-billion-parameter sparse
  mixture-of-experts model with 23 billion active parameters, pretrained on
  23.8 trillion tokens and post-trained with a four-week reinforcement
  learning run on 10,500 GB300 GPUs producing over 100 million rollouts. The
  company claims coding and agentic performance competitive with larger open
  models like GLM 5.2 while using 3-4x less inference compute, plus a
  1-million-token context window from midtraining. The weights, technical
  report and model card are promised under Apache 2.0 later this month, with a
  waitlist open for early access. The model is text-only.
---

Most commenters land on the announcement being premature, because Reflection is
marketing open weights it has not shipped: the weights, technical report and
model card are promised "later this month," and release promises from labs have
gone unfulfilled before. The sharpest objection is to the land/water
generalization demo, which argues the viral grid puzzle "is a few days old, so
could not appear in the training data" to justify Beam's 95.5% score, when
commenters note the original puzzle is far older, making the freshness claim
sloppy at best. Others attack the benchmark chart for cutting stronger open
models off at the fold, so Beam appears to beat the DeepSeek V4.1 Flash and Kimi
K3 rows it actually trails. A minority current defends the proprietary training
data as ordinary practice, since licensed corpora and RL trajectories are trade
secrets, while the surrounding data-sourcing subthread turns into a grim joke
about distilling Claude.
