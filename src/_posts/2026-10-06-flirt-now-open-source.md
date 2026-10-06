---
layout: post
title: "Flirt is now Open-Source"
date: 2026-10-06 09:23:08 -0600
categories: digest
tags: ["Dev Tools"]
source_url: "https://blog.buenzli.dev/flirt-is-open-source/"
lobsters_url: "https://lobste.rs/s/9iztqv/flirt_is_now_open_source"
summary: >-
  Flirt, a local-first code review tool built around the patch-series workflow
  where authors continuously amend, rebase and force-push, has been released
  as open source on Codeberg. The tool remembers what a reviewer has already
  seen and shows the difference to the current state, working across backends
  such as GitHub and email mailing lists. Its author warns that Flirt is not
  yet ready for general use, with bugs and missing features still outstanding,
  and points contributors to a Zulip instance where LLM-written messages are
  banned. A Forgejo backend, which would let the project dogfood itself, is
  next on the roadmap.
---

Most commenters land on enthusiasm for the tool itself, because sjamaan and
arcade say they had independently wanted this patch-series review workflow and
value its local-first, forge-agnostic design. The sharpest objection is the AGPL
license, because novafacing reports that legal departments at every employer
they have worked for ban AGPL software even as a locally run binary on a work
laptop, leaving them unable to try a tool they badly need; singpolyma pushes
back that reviewing patches never involves deploying or shipping the code. A
second argument concerns the LLM contribution policy: mxey notes that merely
saying contributors may use LLMs personally is enough to land a project on the
open-slopware list, while senekor replies that what people do outside the
project is none of his business and agrees to soften the wording. manfred's
practical criticism is that the launch post and README did not explain what
Flirt is or how to install it, which the author fixed within the thread.
