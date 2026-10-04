---
layout: post
title: "We're going to need default hard budget caps on pretty much everything"
date:   2026-10-04 00:44:46 -0600
categories: digest
tags: ["Systems & Infra"]
source_url: https://simonwillison.net/2026/Oct/3/default-hard-budget-caps/
hn_url: https://news.ycombinator.com/item?id=49949235
summary: >-
  Simon Willison argues pay-by-usage services should ship hard budget caps by
  default — after $X a month, cut the service off and return errors — with
  removing the cap an explicit opt-in checkbox. The trigger is coding agents,
  which make it easy to spin up code that spends money while you sleep. The timing
  is that AWS shipped per-project monthly spend limits on 16 September, pausing a
  project for the rest of the month, and Google Cloud launched per-service Spend
  Caps in July.
---

Almost everyone agrees the feature should exist and that AWS and GCP arrived
absurdly late; the argument is about defaults. Enterprise operators lead the
pushback: 'never spend more than $X' also means shutting down a business-critical
app at 2am because someone forgot to plan a report run, and kasey_junk says the
best customers would rather take the overage. Willison's answer is that a hospital
ticks a box saying no limit, and today's hobbyist is tomorrow's procurement
decision-maker. The sharpest technical objection is that billing is asynchronous,
so you only learn a query cost $100 after running it; the proposed fix is
traffic-light thresholds and per-service rather than per-account caps.