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

The thread's landing point is that Git itself is not vulnerable here: cloning
refuses to check out anything under .git/, which z3bra confirmed by getting
"error: invalid path '.git/hooks/post-checkout'" on a test clone. The danger is
any other way of installing a directory tree — zip, tarball, Dropbox — and vifon
pointed back to the 2014 case-insensitive-filesystem Git vulnerability that did let
writes land in .git on clone. The sharpest objection is to the reflex to harden
globally: arialdo's `git config --global core.hooksPath /dev/null` was shot down by
oger, since a malicious repo can re-enable hooksPath in its own config. The
most-liked fix is direnv-style explicit consent, with agwa noting core.fsmonitor
is an even better vector because plain `git status` triggers it.