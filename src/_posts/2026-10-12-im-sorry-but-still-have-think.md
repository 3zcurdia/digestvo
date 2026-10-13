---
layout: post
title: "I'm sorry, but you still have to think"
date: 2026-10-12 10:54:29 -0600
categories: digest
tags: ["AI/ML"]
source_url: "https://itsallaboutthebit.com/i-am-sorry-but-you-still-have-to-think/"
lobsters_url: "https://lobste.rs/s/k2natg/i_m_sorry_you_still_have_think"
share_text: "DHH's agent rewrites prove nothing — the Rust port drops messages under load. You still have to think. #Rust"
summary: >-
  Piotr Sarnacki dissects DHH's AI-agent rewrites of Campfire from Rails into
  Rust, Elixir and Go, done without reading the resulting code. Non-functional
  choices such as backwards compatibility, dropping the CSRF token or
  replacing Redis with in-process queues get silently answered by the prompt
  rather than the language, making the cross-language comparison meaningless.
  The Rust version runs blocking database queries and sync locks inside
  cooperative async tasks, and its broadcast channel capacity of 256 drops
  most notifications under load; the Elixir version trades that for HTTP
  timeouts and 1.8GB of memory. His conclusion: you still have to think about
  failure modes and trade-offs.
---

Most commenters land on the article's thesis — delegating to AI does not remove
the need for judgment — because reliability comes from keeping the system simple
and reasoning about it constantly, not from automated checks passing. The
sharpest objection is that AI can still be aimed at the right job: alandekok
argues DHH's mistake was asking for a rewrite instead of first having the model
write a full test suite to use as the requirements, and wpld reports doing
exactly that on an Angular-to-Vue migration with one browser input-type bug.
tinthedev pushes further, treating LLMs as virtual colleagues let loose inside
areas of limited blast radius wherever he can test what good looks like. The
number carrying the argument is Zach Daniels' 1% notification delivery rate for
the Rust rewrite under load, which facundoolano reads as proof that champions of
heavy AI delegation either do not care about reliability or assume passing
checks means a working system. The top-scored comment, at 38, is wry rather than
angry: the analysis probably took more human effort than the AI rewrite it
dissects.
