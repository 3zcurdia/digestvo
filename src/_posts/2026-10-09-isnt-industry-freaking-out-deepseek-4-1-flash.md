---
layout: post
title: "Why isn't the industry freaking out about DeepSeek 4.1 Flash?"
date: 2026-10-09 08:51:10 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://www.dgt.is/blog/2026-10-07-deepseek-freek-out/"
hn_url: "https://news.ycombinator.com/item?id=50000488"
summary: >-
  The author says a month of heavy use of DeepSeek 4.1 Flash across a dozen
  projects left him unable to tell it apart from Claude Opus, at a small
  fraction of the price. He argues the frontier labs should be worried because
  distilled Chinese models now handle the same workloads a month or two behind
  Anthropic and OpenAI, even if they learned from mined Claude data. The
  enabler is a KV cache roughly 437 times smaller than V1's, which keeps
  all-day coding sessions under a dollar. He likens it to generic drug makers
  underpricing big pharma, and says self-hosting will pay off once these cache
  tricks run locally.
---

Most commenters land on the price being genuinely transformative but the quality gap real: several report cancelling Claude Max or GPT subscriptions because 4.1 Flash handles their coding and agent work at pennies per session, while others point to the pacman-bakeoff leaderboard, where Opus 5.5 scores 99/100 to Flash's. The sharpest objection is that the article's "a month or two behind" claim is wrong — open models still trail February's Fable 5 by 6 to 12 months, and casual benchmarks hide the difference on hard orchestration work. The other live argument is economics: with flat $100-a-month subscriptions there is no price
gap left for individuals, only for per-token API buyers, which is why nobody is freaking out.
