---
layout: post
title: "I got targeted: Trying to get your credentials via a git post-checkout hook"
date:   2026-10-04 00:44:46 -0600
categories: digest
tags: ["Security & Privacy"]
source_url: https://frankwiles.com/posts/i-got-targeted/
lobsters_url: https://lobste.rs/s/cd5gdk/i_got_targeted_trying_get_your
summary: >-
  Frank Wiles, founder of REVSYS, describes a targeted phishing attempt that
  delivered a fake Ed Tech project brief via a Dropbox folder containing a git
  repository. Inside .git/hooks sat a real post-checkout hook alongside the usual
  .example files; it fetched an OS-specific binary from a Vercel-hosted
  command-and-control server, made it executable, ran it, and deleted itself.
  Wiles caught it when the "client" told him to switch to an NDA branch, and
  alerted Dropbox and Vercel. The operators were also impersonating a real
  development shop.
---

Most commenters land on Git needing a direnv-style gate before hooks run,
because .git is treated as trusted local state even when a repo arrived as a
Dropbox download or a tarball rather than a clone; the post author himself
endorses the idea. The sharpest objection comes from agwa, who notes that a
plain git clone is safe by design: Git refuses to check out paths under .git/
and treats a clone that pwns you as a vulnerability, so the danger lives
entirely in installing a directory tree some other way and anyone who only ever
clones is out of reach. The thread also escalates the payload, with agwa's
core.fsmonitor variant firing on a bare git status that IDEs, go build and shell
prompts run implicitly, making a shipped .git/config nastier than any hook. A
heavily upvoted tip to disable hooks with core.hooksPath /dev/null draws fire
when oger points out a repo's own config can set it back.
