---
layout: post
title: "Example.com just launched the biggest redesign in decades"
date: 2026-10-06 09:23:08 -0600
categories: digest
tags: ["Web & Platforms"]
source_url: "https://www.debugbear.com/blog/example-dot-com-redesign-history"
hn_url: "https://news.ycombinator.com/item?id=49971921"
summary: >-
  IANA's reserved documentation domain example.com got its biggest overhaul in
  decades on 28 September 2026. The static English page gained six languages —
  English, Arabic, Chinese, French, Russian and Spanish — originally rotating
  every five seconds with a per-character opacity transition, plus a
  JavaScript-inserted SVG book icon. IANA says it split the page into a bare
  HTML core and a separate JavaScript file because most of its traffic is
  automated and never fetches that file, cutting bandwidth. On 3 October the
  animation was dropped and all languages render at once, with the browser's
  preferred language bumped to the top.
---

Most commenters land on the bandwidth arithmetic as the real story, because
IANA's statement points out that most hits on example.com come from copy-pasted
config files and bots that never execute JavaScript, so shipping the
translations in s.js costs those clients nothing. The sharpest objection is that
the page should have stayed static and English-only, since a placeholder serving
a courtesy HTTP endpoint gains little from six translated paragraphs plus an
SVG, and account42 argues the zero-overhead simplicity was the entire point of
the domain. A second flank is accessibility: readers found the five-second
language rotation impossible to finish before it flipped to the next script,
which IANA conceded by removing the animation on 3 October, though a few
defenders call the SVG the only color on an otherwise bare page. A smaller side
argument broke out over whether the DebugBear article itself was AI-written,
after one commenter claimed the SVG still appeared with JavaScript disabled and
another pasted the s.js source proving it injects the markup.
