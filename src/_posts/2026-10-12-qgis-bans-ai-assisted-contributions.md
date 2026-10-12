---
layout: post
title: "QGIS bans AI assisted contributions"
date: 2026-10-12 10:54:29 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://github.com/qgis/QGIS-Enhancement-Proposals/pull/387"
hn_url: "https://news.ycombinator.com/item?id=50054751"
summary: >-
  QGIS has adopted QEP 428, a strict policy banning AI-assisted contributions
  to the project and replacing the earlier "human in the loop" rule, under
  which any tool was fine as long as the contributor understood the code and
  could answer questions about it. Maintainers say the volume of AI-assisted
  pull requests outruns what human review can absorb, piling unbearable
  pressure on reviewers and risking unreviewed code reaching the project.
  Opened September 24 by Nyall Dawson and merged October 7 after a vote, the
  proposal is explicitly a stopgap: start with the door shut, then open
  specific exceptions case by case later.
---

Most commenters grant the maintainers' motive, because the deluge of AI PRs
lands on reviewers who already had too little time — one reply to the claim that
agent factories could rewrite QGIS in hours is "you are the reason for this
policy change." The sharpest objection is the wording: the policy bans anything
"AI assisted" without defining it, so nobody knows whether LLM autocomplete,
brainstorming with ChatGPT, or Google Translate counts, and timlinux's
compliance test — "did you in good conscience write the code yourself" — is
exactly the vagueness critics mean when the penalty is rejection. A second
flashpoint is the companion QEP 429 to exempt trusted contributors from the ban,
which reads to some as LLMs allowed for maintainers but not for outsiders, while
defenders note the ban is unenforceable by detection anyway and exists to
justify quick rejections of obvious slop.
