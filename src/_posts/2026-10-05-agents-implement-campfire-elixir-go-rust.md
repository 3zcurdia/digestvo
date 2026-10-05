---
layout: post
title: "Agents Implement Campfire in Elixir, Go, and Rust"
date: 2026-10-05 09:42:17 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://x.com/dhh/status/2106810173683851564"
summary: >-
  DHH says he had coding agents implement and optimize the Campfire web app in Elixir, Go, and Rust, with Ruby slowest. He long accepted that cost for productivity and developer joy. He asks whether that trade still holds if agents write and validate code humans no longer read. In a follow-up he adds Rust has costs like slow compiles, but insists agent-written code demands a new view of language choice.
---

Most repliers land on the benchmark being uneven rather than on DHH's question about unread code, because the Rust port got hundreds of commits over days while Elixir and Go got one or two from an initial rewrite. The sharpest objection is Jose Valim's process point, backed by Zach Daniel's code details: vague prompts let agents make architectural choices like funneling all SQL through a single GenServer.call, keeping Redis in Elixir, and dropping CSRF for cacheable HTML in Rust. DHH answers that out-of-the-box agent output is the point, with Laravel and Django ports showing the same exercise, but that concedes the ranking measures agent defaults, not language ceilings. The constructive reply is Jakub Skalecki's clean-room idiomatic Elixir redo, aimed at testing whether equal effort closes the gap.
