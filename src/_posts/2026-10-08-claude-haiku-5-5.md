---
layout: post
title: "Claude Haiku 5.5"
date: 2026-10-08 10:53:43 -0600
categories: digest
tags: ["AI Release"]
source_url: "https://www.anthropic.com/claude-haiku-5-5"
hn_url: "https://news.ycombinator.com/item?id=49996437"
summary: >-
  Anthropic launched Claude Haiku 5.5, its cheapest, fastest small model,
  aimed at high-volume work like summaries, compaction, classification and
  subagent tasks running under Opus 5.5 and Sonnet 5.5. The company says it
  costs about 75% less than Haiku 4.5 to run, scoring far above its
  predecessor and above GPT-6 Luna on Terminal-Bench, OSWorld and Humanity's
  Last Exam while still trailing Sonnet 5.5. Pricing splits at 100,000 tokens:
  $0.10 per million input and $0.50 output below that line, five times more
  above it. Anthropic also halved Sonnet 5.5's cache-read price and added
  monthly API credits for Max and Team subscribers.
---

Most commenters land on the new pricing tiers rather than the benchmarks,
because the 100,000-token cutoff jumps input and output prices 5x and applies
only to Haiku. The sharpest objection is that agentic work routinely blows past
100k, so the headline discount evaporates exactly where Haiku would be used as a
subagent, at which point one commenter's reading of Artificial Analysis data
puts Haiku at roughly 3x Luna's cost per task, with GPT-6.1 Sol matching it on
cost at higher intelligence. The counter is that flat per-token pricing was
always a fiction, since neither encode nor decode scales linearly with compute,
so tiering merely approximates real serving cost; others argue token price is
the wrong yardstick and cost per completed task favors Haiku on Anthropic's own
chart. Supporters add that Haiku was noticeably smarter than Luna and finally
gives Anthropic a cheap model for summarization and triage work. A smaller
current underneath debates whether the 47% quarterly drop in cost per unit of
intelligence survives Jevons-paradox demand, which is why total AI spending
keeps climbing.
